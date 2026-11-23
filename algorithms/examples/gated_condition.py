"""单头候选参考残差；不执行训练，不是上游LTX模块。

h: [B,N,width], memory: [B,R,512], bias: [B,1,N,R]。
调用者必须提供有效null位置，保证每行至少一个有限logit。
"""
import torch
from torch import nn
from torch.nn import functional as F


class GatedReference(nn.Module):
    def __init__(self, width, memory_width=512, inner=512):
        super().__init__()
        self.q = nn.Linear(width, inner, bias=False)
        self.k = nn.Linear(memory_width, inner, bias=False)
        self.v = nn.Linear(memory_width, inner, bias=False)
        self.out = nn.Linear(inner, width, bias=False)
        self.gate = nn.Parameter(torch.zeros(()))

    def forward(self, h, memory, bias):
        norm = F.rms_norm(h, (h.shape[-1],))
        q = self.q(norm)[:, None]
        k, v = self.k(memory)[:, None], self.v(memory)[:, None]
        delta = F.scaled_dot_product_attention(q, k, v, attn_mask=bias)
        return h + self.gate.tanh() * self.out(delta[:, 0])


# gate=0，投影正常初始化；首步可学gate，后续才更新读取支路。
