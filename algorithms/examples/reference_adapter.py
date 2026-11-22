"""极简参考支路：单头、全 query 均有有效参考；不是 Phantom/Wan 的原实现。"""
import torch
import torch.nn.functional as F
from torch import nn


class ReferenceAdapter(nn.Module):
    def __init__(self, video_dim, reference_dim):
        super().__init__()
        self.q = nn.Linear(video_dim, video_dim)
        self.k = nn.Linear(reference_dim, video_dim)
        self.v = nn.Linear(reference_dim, video_dim)
        self.out = nn.Linear(video_dim, video_dim)
        self.gate = nn.Parameter(torch.zeros(()))

    def forward(self, video, reference, allowed):
        # video: [B,N,d]；reference: [B,R,d_ref]。
        # allowed: [B,N,R]，布尔 True 表示该 query 可读该参考。
        assert allowed.dtype == torch.bool and allowed.any(dim=-1).all()
        q = self.q(video).unsqueeze(1)
        k = self.k(reference).unsqueeze(1)
        v = self.v(reference).unsqueeze(1)
        delta = F.scaled_dot_product_attention(q, k, v,
                                              attn_mask=allowed.unsqueeze(1))
        return video + self.gate.tanh() * self.out(delta.squeeze(1))


# gate=0 时支路不改变原输出；首步先学习 gate，后续梯度再进入支路。
# 投影保持正常初始化。无参考/空绑定应由调用者走纯基座路径。
