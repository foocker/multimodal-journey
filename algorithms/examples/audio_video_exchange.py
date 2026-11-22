"""说明双向交换的数据依赖；省略 codec、多头、时间 mask 和噪声调制。"""
from torch import nn


class AudioVideoExchange(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.video_reads_audio = nn.MultiheadAttention(dim, num_heads=1, batch_first=True)
        self.audio_reads_video = nn.MultiheadAttention(dim, num_heads=1, batch_first=True)

    def forward(self, video, audio):
        # video: [B,Nv,d]，audio: [B,Na,d]；两边都读更新前的输入。
        dv, _ = self.video_reads_audio(video, audio, audio, need_weights=False)
        da, _ = self.audio_reads_video(audio, video, video, need_weights=False)
        return video + dv, audio + da


# 同步不能靠 token index 一一对应，实际实现还需映射到同一物理时间轴。
# 缺失音轨应跳过音频目标；真实静音仍是有效目标。
