"""因果三维卷积的教学实现；不包含完整 VAE、归一化或分块缓存。"""
import torch.nn.functional as F
from torch import nn


class CausalConv3d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel=(3, 3, 3),
                 temporal_stride=1, temporal_dilation=1):
        super().__init__()
        kt, kh, kw = kernel
        assert kh % 2 == kw % 2 == 1  # 空间保持尺寸，示例只讨论奇数核。
        self.pad = (kw // 2, kw // 2, kh // 2, kh // 2,
                    temporal_dilation * (kt - 1), 0)
        self.conv = nn.Conv3d(in_channels, out_channels, kernel,
                              stride=(temporal_stride, 1, 1),
                              dilation=(temporal_dilation, 1, 1), padding=0)

    def forward(self, x):
        # x: [B,C,T,H,W]；时间只左补，因此输出 j 最远读取 j*stride。
        return self.conv(F.pad(x, self.pad))


# 例：CausalConv3d(3, 48, temporal_stride=4)
# 输入 [B,3,121,H,W] → 输出 [B,48,31,H,W]。
# 这里只压缩时间；完整 VAE 还需要空间下采样和编码/解码结构。
