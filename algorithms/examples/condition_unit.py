"""统一视频条件的最小表示；省略编码器和 context adapter。"""
from dataclasses import dataclass
import torch


@dataclass
class VideoConditionUnit:
    frames: torch.Tensor  # [B,C,F,H,W]
    mask: torch.Tensor    # [B,1,F,H,W]，1=允许重生成，0=保留条件内容
    kind: str              # source / reference / depth / pose / layout

    def split_concepts(self):
        return self.frames * self.mask, self.frames * (1 - self.mask)


def edit_mask(frame_pts, spatial_mask, start, end):
    time = ((frame_pts >= start) & (frame_pts < end)).to(spatial_mask)
    return time[None, None, :, None, None] * spatial_mask
