"""四类音视频注意力的块间因果关系；仅用于解释，未运行。

block IDs已由codec覆盖区间与共同时间边界生成。每行至少有当前块key。
返回True表示可读；真实长序列应使用块稀疏kernel而非稠密矩阵。
"""


def block_allowed(query_blocks, key_blocks):
    return key_blocks[None, :] <= query_blocks[:, None]


def audiovisual_masks(video_blocks, audio_blocks):
    return {
        "video_self": block_allowed(video_blocks, video_blocks),
        "audio_self": block_allowed(audio_blocks, audio_blocks),
        "video_reads_audio": block_allowed(video_blocks, audio_blocks),
        "audio_reads_video": block_allowed(audio_blocks, video_blocks),
    }
