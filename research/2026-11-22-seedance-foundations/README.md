# 2026-11-22：Seedance 基础梳理与落地方案

状态：模型辅助定点核查与工程方案草稿，待用户逐块审阅。承接用户提供的 [talk2deepseek.md](../../talk2deepseek.md)，原文件未改写。

用户目标：先理解 Seedance 2.5 依赖的基础，再依据外部信息提炼可行架构，进一步落到数据制作、训练、推理优化和业务问题。不能只补一个论文清单或将模型摘录换个排版。

## 本轮产出

- [15 块学习入口](../../topics/video-generation/seedance-2.5/README.md)：M00–M14。
- [证据与能力](../../topics/video-generation/seedance-2.5/evidence.md)：官方能力与未知实现。
- [候选架构](../../topics/video-generation/seedance-2.5/architecture.md)、[训练计划](../../topics/video-generation/seedance-2.5/training.md)：开放基座的分阶段增量路线。
- [数据制作](../../datasets/recipes/audio-video-production/README.md)、[业务映射](../../applications/video-production/solutions.md)：格式、检查、失败分流与 pilot。
- [模块探针](../../experiments/2026-11-22-foundation-probes/README.md)：可重跑解析演示，不是模型实验。
- [纠错](corrections.md)、[来源核查](source-checks.json)、[过程/验证日志](journal.md)。

所有新知识块仍为 draft；未取得源码/checkpoint 准入、真实训练数据、GPU 训练/推理结果或业务试验结果。后续按 [逐块检查表](../../topics/video-generation/seedance-2.5/review.md) 继续，不以篇幅代替完成度。

随后按用户要求重写为 15 篇独立文章：正文只保留来源 ID，公式使用美元定界符，加入论文裁图并提供 [离线阅读环境](../../docs/article-reading.md)。细粒度定位与本轮纠错保留为研究材料，不要求先读这些材料才能理解文章。
