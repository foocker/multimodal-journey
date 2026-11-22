"""Small deterministic mathematical probes; no model training or GPU benchmark."""
from __future__ import annotations

import json
import math
import argparse
from pathlib import Path


def latent_shape(frames, height, width, *, temporal=4, spatial=16, channels=48, patch=1):
    values = [frames, height, width, temporal, spatial, channels, patch]
    if any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in values):
        raise ValueError('Shape values must be positive integers')
    if (frames - 1) % temporal or height % (spatial * patch) or width % (spatial * patch):
        raise ValueError('This probe requires exact divisibility, without padding')
    t, h, w = 1 + (frames - 1) // temporal, height // spatial, width // spatial
    return {'latent': [channels, t, h, w], 'tokens': t * (h // patch) * (w // patch),
            'element_ratio': channels * t * h * w / (3 * frames * height * width)}


def causal_conv(values, weights, *, stride=1, dilation=1):
    left = dilation * (len(weights) - 1)
    padded = [0.0] * left + list(values)
    return [sum(w * padded[j * stride + i * dilation] for i, w in enumerate(weights))
            for j in range((len(values) - 1) // stride + 1)]


def rotate(pair, position, omega=0.2):
    a = position * omega
    x, y = pair
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def run():
    reports = {}
    seedance = latent_shape(121, 480, 832)
    wan = latent_shape(121, 480, 832, spatial=8, channels=16, patch=2)
    assert seedance['latent'] == [48, 31, 30, 52]
    assert seedance['tokens'] == wan['tokens'] == 48360
    assert latent_shape(1, 480, 832)['element_ratio'] == 1 / 16
    assert seedance['element_ratio'] != 1 / 64
    try:
        latent_shape(120, 480, 832)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid temporal shape silently accepted')
    reports['shapes'] = {'seedance_1_example': seedance, 'wan_example': wan,
                         'note': 'Same token grid does not imply compatible latent channels or weights.'}

    x = list(range(13))
    altered = x[:8] + [1000] * 5
    checked = 0
    for stride in [1, 2, 4]:
        for dilation in [1, 2]:
            y = causal_conv(x, [1, 2, 3], stride=stride, dilation=dilation)
            future = causal_conv(altered, [1, 2, 3], stride=stride, dilation=dilation)
            for j in range(len(y)):
                if j * stride < 8:
                    assert y[j] == future[j]
                    checked += 1
    reports['causality'] = {'unchanged_prefix_outputs_checked': checked,
                            'scope': '1D temporal indexing only, not a real VAE'}

    q, k = (0.8, -0.3), (0.1, 1.1)
    a = dot(rotate(q, 2), rotate(k, 5))
    b = dot(rotate(q, 9), rotate(k, 12))
    assert math.isclose(a, b, abs_tol=1e-12)
    reports['rope'] = {'dot_original': a, 'dot_shifted': b, 'absolute_error': abs(a - b)}

    # All frames, same 2-position spatial window. Position-only attention cannot cross p.
    tokens = [(t, p) for t in range(4) for p in range(4)]
    query = (2, 0)
    pointwise = [v for v in tokens if v[1] == query[1]]
    windowed = [v for v in tokens if v[1] // 2 == query[1] // 2]
    assert (1, 1) in windowed and (1, 1) not in pointwise
    assert len(pointwise) == 4 and len(windowed) == 8
    t, p, m = 16, 1024, 4
    counts = {'full': (t*p)**2, 'spatial': t*p*p,
              'pointwise_temporal': p*t*t, 'window_temporal': p*t*t*m}
    assert counts == {'full': 268435456, 'spatial': 16777216,
                      'pointwise_temporal': 262144, 'window_temporal': 1048576}
    reports['attention'] = {'example_connections': counts, 'pointwise_keys': pointwise, 'window_keys': windowed}

    clean, noise, time = 2.0, 10.0, 0.75
    z = (1-time)*clean + time*noise
    velocity = noise-clean
    recovered = z + (0-time)*velocity
    assert recovered == clean
    reports['flow'] = {'z_t': z, 'target_velocity': velocity, 'euler_to_zero': recovered}

    # A changed hidden-state dependency makes even causal cached K/V stale.
    def kv(history, prompt, timestep):
        return [v + prompt + timestep for v in history]
    old = kv([1, 2], 3, 0.1)
    assert old == kv([1, 2], 3, 0.1)
    assert old != kv([1, 2], 4, 0.1)
    assert old != kv([1, 2], 3, 0.2)
    reports['cache'] = {'same_dependencies_reusable': True, 'prompt_change_invalidates': True,
                        'timestep_change_invalidates': True,
                        'scope': 'Toy dependency counterexample; not an attention implementation'}
    return {'kind': 'analytic_demonstration', 'seed': None, 'stochastic': False,
            'model_training': False, 'gpu_benchmark': False, 'probes': reports}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare with committed analytic results without writing')
    args = parser.parse_args()
    output = Path(__file__).with_name('results.json')
    result = json.loads(json.dumps(run()))
    if args.check:
        expected = json.loads(output.read_text(encoding='utf-8'))
        # libm rounding can differ slightly between Python platforms.
        for key in ['dot_original', 'dot_shifted', 'absolute_error']:
            assert math.isclose(result['probes']['rope'][key], expected['probes']['rope'][key], abs_tol=1e-12)
        result['probes']['rope'] = expected['probes']['rope']
        assert result == expected, 'Analytic results changed; inspect before refreshing results.json'
        print('OK: six mathematical probe groups match saved results. No model benchmark.')
    else:
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'OK: six mathematical probe groups; wrote {output.name}. No model quality or speed was measured.')
