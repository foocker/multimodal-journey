"""参考时间门教学代码；每行参考一个合法区间，只展示 soft bias。

query_times: [N]秒；intervals: [R,2]秒且start<end；softness>0。
多区间归并、主体/镜头mask、null token由调用者处理，不是完整adapter。
"""
import torch


def interval_gate(query_times, intervals, softness=0.25):
    tau = query_times[:, None]
    start, end = intervals[None, :, 0], intervals[None, :, 1]
    return torch.sigmoid((tau - start) / softness) * torch.sigmoid((end - tau) / softness)


def attention_bias(query_times, intervals, eps=1e-4):
    gate = interval_gate(query_times, intervals)
    return (eps + (1 - eps) * gate).log()


# 显式时间门，不是 WeRoPE 的原实现；仍需要区间外缺席的训练数据。
