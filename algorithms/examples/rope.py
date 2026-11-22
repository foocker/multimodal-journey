"""三轴 RoPE 的教学构造：相邻维配对，每轴独立频率；不兼容任意 checkpoint。"""
import torch


def rotate_axis(x, positions, base=10000):
    # x: [B,heads,N,d_axis]，positions: [N]；d_axis 必须为偶数。
    dim = x.shape[-1]
    assert dim > 0 and dim % 2 == 0
    omega = base ** (-torch.arange(0, dim, 2, device=x.device).float() / dim)
    angles = positions.to(x.device).float()[:, None] * omega[None, :]
    cos, sin = angles.cos().to(x.dtype), angles.sin().to(x.dtype)
    even, odd = x[..., 0::2], x[..., 1::2]
    pairs = torch.stack((even * cos - odd * sin,
                         even * sin + odd * cos), dim=-1)
    return pairs.flatten(-2)


def rope_3d(q, k, coordinates, sections=(4, 4, 4)):
    # q/k: [B,heads,N,d_head]；coordinates: [N,3]，依次为 t,y,x。
    # sections 的单位是通道数，剩余通道保持不变。
    assert sum(sections) <= q.shape[-1]
    def apply(x):
        parts, start = [], 0
        for axis, width in enumerate(sections):
            parts.append(rotate_axis(x[..., start:start + width],
                                     coordinates[:, axis]))
            start += width
        return torch.cat(parts + [x[..., start:]], dim=-1)
    return apply(q), apply(k)
