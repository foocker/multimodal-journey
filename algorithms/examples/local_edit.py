"""时间区间、已知 latent 覆盖与最终像素合成；三者不是同一个 mask。"""


def frames_in_interval(frame_pts, start, end):
    # frame_pts 为真实秒数 [F]；可变帧率也按 PTS 选择，区间为 [start,end)。
    return (frame_pts >= start) & (frame_pts < end)


def clamp_known_latent(current, clean_source, fixed_noise, time, generate_mask):
    # t=0 数据、t=1 噪声；generate_mask=1 的地方允许生成。
    # fixed_noise 在同一采样链中复用；time 可为标量或可广播张量。
    known_at_t = (1 - time) * clean_source + time * fixed_noise
    return generate_mask * current + (1 - generate_mask) * known_at_t


def composite_pixels(generated, source, edit_alpha):
    # 输入布局相同；alpha 可广播到颜色通道，范围 [0,1]。
    # alpha=0 的像素直接取源图，而不是要求 VAE 无损重建源图。
    return edit_alpha * generated + (1 - edit_alpha) * source


# latent mask 需考虑 VAE/patch 感受野，不能将像素 mask 随意缩放后冒充精确边界。
