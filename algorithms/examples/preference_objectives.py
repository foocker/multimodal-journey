"""只展示两个目标的计算；不包含策略采样、答案 logp 或奖励模型。"""
import torch.nn.functional as F


def dpo_loss(chosen_logp, rejected_logp, ref_chosen_logp, ref_rejected_logp, beta=0.1):
    # 四个输入均为 [B] 的有效答案 token logp 总和；ref 模型冻结。
    margin = (chosen_logp - rejected_logp) - (ref_chosen_logp - ref_rejected_logp).detach()
    return -F.logsigmoid(beta * margin).mean()


def group_advantage(rewards, eps=1e-6):
    # rewards: [B,G]；按同一 prompt 的 G 个候选计算，不跨 prompt 混合。
    centered = rewards - rewards.mean(dim=-1, keepdim=True)
    return centered / (rewards.std(dim=-1, keepdim=True, correction=0) + eps)


def clipped_policy_loss(new_logp, old_logp, advantages, clip=0.2):
    # 仅显示单步 surrogate；真实视觉 GRPO 还需要定义 SDE 转移密度与时间采样。
    ratio = (new_logp - old_logp.detach()).exp()
    objective = (ratio * advantages.detach()).minimum(
        ratio.clamp(1 - clip, 1 + clip) * advantages.detach())
    return -objective.mean()
