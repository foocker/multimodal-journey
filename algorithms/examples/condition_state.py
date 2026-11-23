"""每token干净条件/带噪目标的教学构造；省略codec边界与采样器。

clean/noise: [B,N,C]；active: [B,N] bool；sigma/sigma_next: [B]。
训练时确保每条参与该模态loss的样本至少有一个活动位置。
"""
import torch


def prepare_target(clean, noise, active, sigma):
    token_sigma = sigma[:, None] * active.to(clean.dtype)
    s = token_sigma[..., None]
    state = (1 - s) * clean + s * noise
    velocity_target = noise - clean
    return state, token_sigma, velocity_target, active


def euler_active(state, velocity, active, sigma, sigma_next, clean):
    step = (sigma_next - sigma)[:, None, None]
    updated = state + step * velocity
    return torch.where(active[..., None], updated, clean)


# 这只定义latent更新。是否处理隐藏状态、是否存在音频，是另外两个开关。
