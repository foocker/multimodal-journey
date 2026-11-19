# 历史模型初稿：2026-11-19

本文保留当时下载资料包的说明与模型输出，尚非人工审核稿。“本地 PDF / 新增文件”等文字描述当时工作目录；本仓库只提交 URL。链接已转换为公开来源。摘录可能按字符截断，引用前应回到原文。当前结论以 [专题综述](../../../topics/video-generation/evolution.md) 和 [结论登记](../../../topics/video-generation/claims.json) 为准。

---

# 技术演进与业务落地：补充论文及证据指南

整理日期：2026-11-19。新增 **14 篇论文 PDF**，加上上层目录原有的 4 篇，共 18 篇。页码均指本次保存 PDF 的页序，包含首页、目录和附录。论文年份以首次公开或列明的会议年份为准；下载版本另见完整目录。

这份材料围绕“视频底座与数据 → 多镜头 → 原生音视频 → 后训练与效率 → 参考和编辑”建立技术主线。组织调整、产品上线和具体商业收入，需要与对应的官方发布、组织公告或可核实的采访结合。

## 1. 先读这 8 篇

**Seaweed-7B → Seedance 1.0 → Long Context Tuning → Phantom → Seedance 1.5 Pro → 视频 DiT 尺度定律 → DanceGRPO → RewardDance。**

再回到原有的 [Seedance 2.0 报告](https://arxiv.org/pdf/2604.14148v1) 和 [VINCIE-NExT](https://arxiv.org/pdf/2610.12104v1)，就能把产品能力与前面的工程问题对应起来。深入推理成本时再读 RayFlow、AdaSpa、Seaweed-APT；讲定制与编辑时补 LoRA、VINCIE。

## 2. 底座、训练成本与产品化

| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |
|---|---|---|
| **[Seaweed-7B](https://arxiv.org/pdf/2504.08685v2)**<br>2025；26 页 | 补上 Seaweed 这一条研究路线。7B、665,000 H100 GPU 小时、VAE/DiT、数据管线和下游适配均有公开说明；第 17 页还有端到端推理比较。 | 第 1–2、5、14–19 页 |
| **[Seedance 1.0](https://arxiv.org/pdf/2506.09113v2)**<br>2025；26 页 | 把多镜头能力、数据处理、训练、RLHF、蒸馏与系统优化连起来看。第 4 页明确写位置编码设计 following Seaweed and LCT；第 12 页写量化、稀疏和 RayFlow。 | 第 4–8、11–13 页 |
| **[Seedance 1.5 Pro](https://arxiv.org/pdf/2512.13507v3)**<br>2025；11 页 | 音视频联合生成的直接官方材料：双分支 DiT、跨模态交互、音画数据管线、SFT/RLHF 与超过 10 倍的推理加速概述；首页也说明火山引擎可访问。 | 第 1–2 页；其余按评测需要查阅 |

Seaweed-7B 的价值在于展示“有限预算下怎样安排模型、数据、训练和部署”。其报告称 7B 为中等规模，并披露 665,000 H100 GPU 小时的训练成本；这与只沿参数量扩张讲故事的视角不同。

Seedance 1.0 第 4 页明确承接 Seaweed 和 LCT 的 MM-RoPE 设计；第 6–8 页讲数据处理和基础设施，第 11–13 页讲 RLHF 与推理优化。这些是公开可核对的技术联系。

## 3. 从单镜头到参考可控、多镜头叙事

| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |
|---|---|---|
| **[Long Context Tuning](https://arxiv.org/pdf/2503.10589v1)**<br>2025；11 页 | 把单镜头模型扩展到场景级：场景与分镜数据、交错位置编码、异步加噪，以及 KV-cache 支持的自回归镜头续写。直接回答多镜头故事为何需要训练设计。 | 第 1、4–8 页 |
| **[Phantom](https://arxiv.org/pdf/2502.11079v2)**<br>2025；16 页 | Subject-consistent video generation via cross-modal alignment：参考图中的人物、服装、物品如何进入生成过程，怎样减少图像内容泄漏和多主体混淆。Seaweed 报告将其列为主体一致性下游研究。 | 第 1、3–7 页 |
| **[VINCIE](https://arxiv.org/pdf/2506.10941v2)**<br>2025 / ICLR 2026；46 页 | 从视频天然变化中构造交错图文编辑序列，学习多轮图像编辑。与已下载的 VINCIE-NExT 对照，可以讲清图像与视频编辑能力如何相互迁移。 | 第 1–7 页 |

LCT 处理镜头间的上下文；Phantom 处理主体参考与文本指令的对齐；VINCIE 和 VINCIE-NExT 则处理编辑数据如何构造、如何跨图像与视频迁移。这几类任务相互关联，但各自有不同的训练目标和数据要求。

## 4. 从反馈到可用率：策略优化与奖励模型

| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |
|---|---|---|
| **[DanceGRPO](https://arxiv.org/pdf/2505.07818v4)**<br>2025；30 页 | 解释生成模型如何用组内相对奖励做后训练，结合运动、审美和文本对齐等多种奖励；Seedance 1.0、1.5 Pro 和 2.0 报告均列有该研究的引用。 | 第 1、3–6 页 |
| **[RewardDance](https://arxiv.org/pdf/2509.08826v1)**<br>2025；19 页 | 解释反馈闭环中的“谁来判好坏”：生成式奖励建模、奖励模型扩展与 reward hacking。论文直接报告 Seedance-1.0 上的实验，并讨论奖励模型扩展到 26B。 | 第 1、3–9 页 |

Seedance 1.0 第 11 页写得较明确：从训练集和线上用户收集提示词，筛选、平衡后生成视频对，再进行人工偏好标注。这能支撑“线上需求参与反馈训练”的表述。点赞、重绘、导出等事件是否直接作为某一代模型的训练信号，公开报告没有在这里给出对应证据。

## 5. 推理成本：少步采样、稀疏注意力与并行

| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |
|---|---|---|
| **[RayFlow](https://arxiv.org/pdf/2503.07699v2)**<br>2025 / CVPR 2025；23 页 | Instance-Aware Diffusion Acceleration via Adaptive Flow Trajectories：解释低步数生成时的轨迹与蒸馏。Seedance 1.0 第 12 页明确写采用 RayFlow 的 Score Distillation；1.5 Pro 也引用它。 | 第 1、3–7 页 |
| **[AdaSpa](https://arxiv.org/pdf/2502.21079v1)**<br>2025；14 页 | 正式标题 Training-free and Adaptive Sparse Attention for Efficient Long Video Generation。拆解长视频 attention 的成本，以及分块稀疏、动态搜索和跨去噪步复用。Seedance 1.0 的第 12–13 页引用该研究。 | 第 1、3–9 页 |
| **[Seaweed-APT](https://arxiv.org/pdf/2501.08316v3)**<br>2025 / ICML 2025；16 页 | 正式标题 Diffusion Adversarial Post-Training for One-Step Video Generation。看对抗后训练怎样让视频生成走向单步，理解降低去噪步数与保真之间的取舍。 | 第 1–4 页及第 15 页附录 E |

Seedance 1.0 第 12 页明确提到借鉴 RayFlow 的 Score Distillation，并分别讨论量化和稀疏；同页到下一页的系统优化引用 AdaSpa。Seaweed-APT 则提供另一条少步视频生成研究路线。讲商业落地时，应把模型效果、单位生成成本和交付延迟共同考虑，并保留硬件、时长、分辨率等实验条件。

## 6. 规模与客户定制：基础材料

| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |
|---|---|---|
| **[视频 DiT 尺度定律](https://arxiv.org/pdf/2411.17470v2)**<br>2024 / CVPR 2025；16 页 | Towards Precise Scaling Laws for Video Diffusion Transformers：同时考虑参数量、训练 token、计算预算、学习率和 batch size，而不是只谈“模型越大越好”。 | 第 1–8 页，尤其第 5、7 页 |
| **[DiT](https://arxiv.org/pdf/2212.09748v2)**<br>2022 / ICCV 2023；25 页 | Scalable Diffusion Models with Transformers：理解从 U-Net 到 Transformer，以及模型深度、宽度、token 数和计算量怎样影响效果。 | 第 1–5 页 |
| **[LoRA](https://arxiv.org/pdf/2106.09685v2)**<br>2021 / ICLR 2022；26 页 | Low-Rank Adaptation of Large Language Models：理解冻结大模型、只训练低秩更新，为什么能减少客户定制的训练与存储开销。可搭配 Seaweed 第 17–19 页看视频适配。 | 第 1、3–5 页 |

尺度定律论文最适合支撑的问题是：在固定训练预算下，模型容量、数据量和超参数怎样搭配；部署时是否值得用更小模型换取更低推理成本。它不能证明一家公司的未公开参数配置。

## 7. 对现有叙事的事实核对

| 现有表述 | 论文能够支持到哪里 | 建议写法 |
|---|---|---|
| 2024 年 PixelDance 与 Seaweed 内部双线赛马 | 两条研究路线各有公开材料；本次论文不直接记录 2024 年发布会安排与内部决策 | 讲研究路线并行；具体产品发布与内部赛马另引官方发布记录或可靠采访 |
| 2025 年 4 月组织合并，随后两套架构“大合并” | Seedance 1.0 第 4 页明确引用 Seaweed 与 LCT 的位置编码设计 | 写“可确认存在技术设计承接”；组织合并、完整架构融合与权重合并分别需要证据 |
| Seedance 1.0 约 5 秒生成完成 | 第 1 页是用 41.4 秒生成 **5 秒时长**、1080p 视频，硬件为 NVIDIA L20 | 区分成片时长与推理耗时 |
| 到 Seedance 2.0 才采用双分支 DiT | 1.5 Pro 的摘要已明确写 dual-branch Diffusion Transformer | 将原生音视频和双分支结构的公开证据放在 1.5 Pro 阶段；2.0 的具体内部结构按其披露范围表述 |
| Seedance 2.0 已公开证实为 200B | 本次核查的官方 26 页报告没有披露 200B 参数配置 | 将 200B 保留为待核实说法；尺度定律论文用来解释决策问题，不能充当参数量证据 |
| 四模态输入代表已公开全部四模态联合训练细节 | 2.0 第 1–2 页直接支持文本、图像、音频、视频参考输入和音视频输出能力 | 讲可确认的输入、输出和控制能力；不据此补写未披露的训练分布与结构 |
| 海量点赞、重绘、导出直接用于 RLHF/DPO | 1.0 第 11 页支持线上提示词及人工偏好标注；未在此披露这些具体事件的用法 | 讲“线上提示需求 + 偏好标注 + 奖励优化”的公开流程 |
| 火山引擎已提供 Seedance 视频 LoRA 微调 | Seaweed 报告讨论 LoRA 适配；1.0 提示改写模型也使用 LoRA；1.5 Pro 报告确认火山引擎访问 | “LoRA 技术可用于低成本适配”和“具体商业训练接口已开放”分别核实 |
| Seaweed-7B 论文公开等于模型权重开源 | 本次确认的是报告与项目展示；没有据此确认权重发布状态 | 写“公开报告的 Seaweed-7B”，不要直接写“开源 Seaweed-7B” |
| VINCIE-NExT 的论文证明 Seedance 2.0 内部使用该方法 | 两者都讨论编辑与参考能力；本次没有找到直接实现对应的证据 | 将其作为相关编辑研究与数据迁移方法来介绍 |

## 8. 适合科普视频的可核对主线

**一段视频的可用性，需要同时解决五件事：算得起、镜头连得上、声音对得齐、参考改得准、反馈能改善结果。**

1. 用 PixelDance 与 Seaweed 展开不同的技术探索；Seaweed 给出训练预算、部署成本和多类下游适配的公开讨论。
2. 用 Seedance 1.0、LCT 解释多镜头、数据管线、奖励训练和系统效率怎样一起推动可用性。
3. 用 Seedance 1.5 Pro 解释原生音视频联合建模；用 2.0 报告说明控制输入、参考编辑与生产工作流的扩展。
4. 用视频 DiT 尺度定律讨论预算分配，再用 RewardDance 说明需要扩展的也包括奖励模型能力。
5. 用 Phantom、VINCIE 系列和推理工程解释可控性与成本为何影响专业工作流的采用。

这条顺序用于组织讲述；不同研究实际存在时间重叠，不能据此假定每篇论文都按顺序进入同一产品实现。

## 9. 完整下载目录与版本

| 编号 | 正式标题 / PDF | 固定 arXiv 版本 | 页数 |
|---|---|---|---:|
| 05 | [Seaweed-7B: Cost-Effective Training of Video Generation Foundation Model](https://arxiv.org/pdf/2504.08685v2) | [2504.08685v2](https://arxiv.org/abs/2504.08685v2) | 26 |
| 06 | [Seedance 1.0: Exploring the Boundaries of Video Generation Models](https://arxiv.org/pdf/2506.09113v2) | [2506.09113v2](https://arxiv.org/abs/2506.09113v2) | 26 |
| 07 | [Seedance 1.5 pro: A Native Audio-Visual Joint Generation Foundation Model](https://arxiv.org/pdf/2512.13507v3) | [2512.13507v3](https://arxiv.org/abs/2512.13507v3) | 11 |
| 08 | [Scalable Diffusion Models with Transformers](https://arxiv.org/pdf/2212.09748v2) | [2212.09748v2](https://arxiv.org/abs/2212.09748v2) | 25 |
| 09 | [DanceGRPO: Unleashing GRPO on Visual Generation](https://arxiv.org/pdf/2505.07818v4) | [2505.07818v4](https://arxiv.org/abs/2505.07818v4) | 30 |
| 10 | [RewardDance: Reward Scaling in Visual Generation](https://arxiv.org/pdf/2509.08826v1) | [2509.08826v1](https://arxiv.org/abs/2509.08826v1) | 19 |
| 11 | [Diffusion Adversarial Post-Training for One-Step Video Generation](https://arxiv.org/pdf/2501.08316v3) | [2501.08316v3](https://arxiv.org/abs/2501.08316v3) | 16 |
| 12 | [Training-free and Adaptive Sparse Attention for Efficient Long Video Generation](https://arxiv.org/pdf/2502.21079v1) | [2502.21079v1](https://arxiv.org/abs/2502.21079v1) | 14 |
| 13 | [VINCIE: Unlocking In-context Image Editing from Video](https://arxiv.org/pdf/2506.10941v2) | [2506.10941v2](https://arxiv.org/abs/2506.10941v2) | 46 |
| 14 | [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/pdf/2106.09685v2) | [2106.09685v2](https://arxiv.org/abs/2106.09685v2) | 26 |
| 15 | [Long Context Tuning for Video Generation](https://arxiv.org/pdf/2503.10589v1) | [2503.10589v1](https://arxiv.org/abs/2503.10589v1) | 11 |
| 16 | [Phantom: Subject-consistent video generation via cross-modal alignment](https://arxiv.org/pdf/2502.11079v2) | [2502.11079v2](https://arxiv.org/abs/2502.11079v2) | 16 |
| 17 | [Towards Precise Scaling Laws for Video Diffusion Transformers](https://arxiv.org/pdf/2411.17470v2) | [2411.17470v2](https://arxiv.org/abs/2411.17470v2) | 16 |
| 18 | [RayFlow: Instance-Aware Diffusion Acceleration via Adaptive Flow Trajectories](https://arxiv.org/pdf/2503.07699v2) | [2503.07699v2](https://arxiv.org/abs/2503.07699v2) | 23 |

所有 PDF 已检查文件格式、首页正式标题和逐页文本可读性。原始来源、摘要、页数、文件大小与 SHA-256 保存在 [当前来源登记](../../../sources/papers.json)。重点原文可查 [同轮摘录初稿](evidence-excerpts-v0.md)。
