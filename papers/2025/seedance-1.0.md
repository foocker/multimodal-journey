---
status: draft
updated: 2026-11-22
source_ids: ["seedance-1.0"]
topic_ids: ["video-generation"]
---

# Seedance 1.0

**正式标题：** Seedance 1.0: Exploring the Boundaries of Video Generation Models

| 项目 | 记录 |
|---|---|
| 来源 ID | `seedance-1.0` |
| 首次公开 / 阅读版本 | 2025 / `2506.09113v2` |
| 实际保存版本 | arXiv 2506.09113v2 |
| 链接 | [来源页](https://arxiv.org/abs/2506.09113v2) · [PDF URL](https://arxiv.org/pdf/2506.09113v2) · [arXiv 固定版本](https://arxiv.org/abs/2506.09113v2) |
| 页数 / 阅读位置 | 26 页；第 4–8、11–13 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

把多镜头能力、数据处理、训练、RLHF、蒸馏与系统优化连起来看。第 4 页明确写位置编码设计 following Seaweed and LCT；第 12 页写量化、稀疏和 RayFlow。

## 放在技术演进中怎样理解

主线必读。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

第 1 页的速度是 NVIDIA L20 上用 41.4 秒生成一段 5 秒、1080p 视频，不能写成 5 秒完成生成。技术引用支持设计承接，不能据此断言两套模型做过权重合并。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 2026-11-22 定点精读：结构与配方

| 定位（PDF页序） | 核查结果与支持范围 |
|---|---|
| p.4 §2.1 | Causal VAE，(4,16,16)，C=48；连续 latent，移除 DiT patchification |
| pp.4–5 §2.2 / Figure 2 | spatial MMDiT 双模态独立权重；temporal 仅视觉、窗口时空交互；未给精确窗口参数 |
| pp.5–6 §2.4 | Qwen2.5-14B PE，全参 SFT、LoRA DPO；不是视频生成器 LoRA 证据 |
| p.7 §3.2 | 基于 Tarsier2 的 caption 适配，冻结视觉、全参微调语言部分 |
| pp.8–9 §4 | pretrain→CT→SFT→反馈；flow matching velocity/logit-normal/分辨率shift；I2V比例20%→40% |
| p.9 Model Merging | SFT 子集模型合并，不是两条历史产品线权重合并的证据 |
| p.12 §4.4.3 | 直接最大化复合奖励，并与 DPO/PPO/GRPO 比较；不能写成直接采用 DanceGRPO |
| pp.12–13 §5 | TSCD、RayFlow score distillation、APT扩展、thin decoder、量化/稀疏/并行/offload |

本轮核查 Figure 2 的渲染图，空间层输出含 Vision/Text MLP，时间层标 spatial-temporal attention。未运行模型。原理与实现问题见 [基础入口](../../topics/video-generation/seedance-2.5/README.md)，重要修正见 [本轮纠错](../../research/2026-11-22-seedance-foundations/corrections.md)。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
