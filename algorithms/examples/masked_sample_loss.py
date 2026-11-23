"""FP32逐样本有效元素MSE；pred/target [B,N,C], token_mask [B,N]。

返回每样本loss与有效样本标记；调用者只平均有效样本。
分布式与梯度累积的全局有效计数由trainer处理。
"""
import torch


def masked_sample_mse(pred, target, token_mask):
    error = (pred.float() - target.float()).square().mean(dim=-1)
    weights = token_mask.float()
    counts = weights.sum(dim=1)
    valid = counts > 0
    per_sample = (error * weights).sum(dim=1) / counts.clamp_min(1)
    return per_sample, valid


def mean_valid(per_sample, valid):
    if not bool(valid.any()):
        return None  # 此模态没有监督，调用者跳过，不添加伪造的零loss样本。
    return per_sample[valid].mean()
