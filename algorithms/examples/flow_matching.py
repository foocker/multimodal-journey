"""极简流匹配：统一 t=0 数据、t=1 噪声；不直接适配任何基座 scheduler。"""
import torch


def training_pair(clean, time):
    # clean: [B,C,T,H,W]；time: [B]。
    noise = torch.randn_like(clean)
    t = time.reshape(-1, 1, 1, 1, 1)
    noisy = (1 - t) * clean + t * noise
    return noisy, noise - clean


def velocity_loss(prediction, target, valid):
    # valid 可为 [B,1,T,H,W]；只对有效元素平均，不能把 padding 计进去。
    weights = valid.to(prediction).expand_as(prediction)
    assert weights.sum() > 0
    return ((prediction - target).square() * weights).sum() / weights.sum()


@torch.no_grad()
def euler_sample(model, noise, condition, steps=20):
    assert steps > 0
    x = noise
    times = torch.linspace(1, 0, steps + 1, device=x.device)
    for t, next_t in zip(times[:-1], times[1:]):
        velocity = model(x, t.expand(x.shape[0]), condition)
        x = x + (next_t - t) * velocity
    return x
