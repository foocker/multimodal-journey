"""Deterministic illustration; inputs are assumptions, not model measurements."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location('budget', ROOT / 'algorithms/compute-budget/budget.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare recomputed results with the curated output')
    parser.add_argument('--config', type=Path, default=HERE / 'config.json')
    parser.add_argument('--output', type=Path, default=HERE / 'results.json')
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding='utf-8'))
    rows = []
    for scenario in config['scenarios']:
        assumptions = {key: value for key, value in scenario.items() if key != 'id'}
        values = MODULE.expected_cost(deliveries=config['deliveries'], **assumptions)
        rows.append({'id': scenario['id'], **{key: round(value, 6) for key, value in values.items()}})
    result = {'kind': config['kind'], 'currency': config['currency'], 'deliveries': config['deliveries'], 'results': rows}
    if args.check:
        if json.loads(args.output.read_text(encoding='utf-8')) != result:
            raise SystemExit('Curated output differs from current calculation; inspect the change and rerun')
        print('OK: illustrative result reproduced exactly')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
