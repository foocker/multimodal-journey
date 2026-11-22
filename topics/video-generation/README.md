# 视频生成：技术演进与业务落地

本专题从 PixelDance / Seaweed 的研究线索出发，关注数据、架构、音视频联合建模、可控编辑、推理效率与交付可用率。组织关系与未公开参数仍有证据缺口。

## 阅读入口

- [Seedance 2.5：M00–M20](seedance-2.5/README.md)：从依赖基础到候选架构、数据/训练/推理、业务与代码，逐块阅读和修订。
- [完整候选架构](seedance-2.5/integrated-design.md) 与 [联合训练配方](seedance-2.5/integrated-training.md)：以同一音视频主干组织多参考、编辑、空间控制与长叙事。
- [演进综述](evolution.md)：当前理解与证据边界。
- [时间线](timeline.md)：论文公开时间和技术问题，不把发布时间自动视为产品继承关系。
- [结论与证据](claims.json)：稳定结论 ID、支持材料、原文定位与待核实项。
- [研究过程](../../research/2026-11-19-seedance/README.md)：最初输入、检索、初稿和纠错。
- [应用研究](../../applications/video-production/README.md)：可控性、质量、成本与业务验证。

## 推荐顺序

| 顺序 | 论文 | 要回答的问题 |
|---|---|---|
| 1 | [Seaweed-7B](../../papers/2025/seaweed-7b.md) | 训练和部署预算怎样反过来影响底座设计？ |
| 2 | [Seedance 1.0](../../papers/2025/seedance-1.0.md) | 数据、模型、后训练和系统优化怎样组成一个可用系统？ |
| 3 | [Long Context Tuning](../../papers/2025/long-context-tuning.md) | 从单镜头走向场景级上下文需要改什么？ |
| 4 | [Phantom](../../papers/2025/phantom.md) | 如何同时遵循参考主体和文本要求？ |
| 5 | [Seedance 1.5 Pro](../../papers/2025/seedance-1.5-pro.md) | 原生音画联合生成怎样改变任务与数据要求？ |
| 6 | [视频 DiT 尺度定律](../../papers/2024/video-dit-scaling-laws.md) | 参数、数据、计算预算和超参数如何共同选择？ |
| 7 | [DanceGRPO](../../papers/2025/dancegrpo.md)、[RewardDance](../../papers/2025/rewarddance.md) | 怎样学偏好，怎样判断“更好”？ |
| 8 | [Seedance 2.0](../../papers/2026/seedance-2.0.md) | 多模态参考、编辑与音视频能力公开到了哪一步？ |

进一步读 [RayFlow](../../papers/2025/rayflow.md)、[AdaSpa](../../papers/2025/adaspa.md)、[Seaweed-APT](../../papers/2025/seaweed-apt.md) 理解效率；读 [VINCIE](../../papers/2025/vincie.md) 与 [VINCIE-NExT](../../papers/2026/vincie-next.md) 理解编辑能力迁移。

## 当前还缺什么

需要继续核对 2024 年发布会与两款产品的对应关系、2025 年组织调整的原始报道、Seedance 2.0 参数规模、具体 LoRA 商业接口和用户交互进入训练的细节。缺乏公开证据的事项保留为问题，不用相邻论文替代证明。
