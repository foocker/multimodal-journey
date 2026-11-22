"""用单头 SDPA 展示连接范围；省略 QKV 投影、位置编码、残差和 FFN。"""
import torch
import torch.nn.functional as F


def attend(sequence):
    # sequence: [groups,N,d]；Q=K=V 仅用于突出序列组织。
    x = sequence.unsqueeze(1)
    return F.scaled_dot_product_attention(x, x, x).squeeze(1)


def spatial_attention(x):
    b, t, h, w, d = x.shape
    return attend(x.reshape(b * t, h * w, d)).reshape(b, t, h, w, d)


def temporal_attention(x):
    b, t, h, w, d = x.shape
    seq = x.permute(0, 2, 3, 1, 4).reshape(b * h * w, t, d)
    return attend(seq).reshape(b, h, w, t, d).permute(0, 3, 1, 2, 4)


def window_temporal_attention(x, window=(2, 2)):
    b, t, h, w, d = x.shape
    wh, ww = window
    assert h % wh == w % ww == 0  # 为便于阅读，省略余数 padding。
    nh, nw = h // wh, w // ww
    seq = x.reshape(b, t, nh, wh, nw, ww, d)
    seq = seq.permute(0, 2, 4, 1, 3, 5, 6).reshape(b * nh * nw, t * wh * ww, d)
    out = attend(seq).reshape(b, nh, nw, t, wh, ww, d)
    return out.permute(0, 3, 1, 4, 2, 5, 6).reshape(b, t, h, w, d)


def multimodal_attention(qv, kv, vv, qt, kt, vt):
    # 各模态先独立投影为 [B,heads,N,d_head]，再在 token 轴拼接。
    n_visual = qv.shape[-2]
    out = F.scaled_dot_product_attention(torch.cat((qv, qt), dim=-2),
                                        torch.cat((kv, kt), dim=-2),
                                        torch.cat((vv, vt), dim=-2))
    return out[..., :n_visual, :], out[..., n_visual:, :]
