# Seedance 2.5：从基础到可验证方案

本专题由 21 篇可独立阅读的文章组成：先理解基础机制，再形成候选架构，最后落实到数据、训练、推理、业务和代码选型。每篇自行解释概念、公式和例子；来源只保留 `source_ids`，正文不夹带论文页码与研究过程。代码使用极简片段配合真实仓库和源码链接。

直接看整体方案可从 [完整候选架构](integrated-design.md) 与 [联合训练配方](integrated-training.md) 开始。参考时间绑定、编辑条件与几何控制分别展开为 M16–M18；Wan 的轻量增量路线保留在 M12–M13。候选方案已形成接口与训练设计，组合效果尚待验证。

公式采用 `$...$` 和 `$$...$$`，必要结构图从固定版本论文裁出并嵌入。执行 `npm ci --ignore-scripts`、`npm run articles:build`，再打开 `.cache/reading/index.html`，即可阅读包含公式与图片的离线版；每篇 HTML 都可单独复制。详见 [阅读环境](../../../docs/article-reading.md)。

文章仍为 draft，待逐篇审核；独立文章、研究笔记和代码验证记录分别维护。

## 按这个顺序读

| 块 | 要解决的问题 | 正文 |
|---|---|---|
| M00 | 2.5 公开了什么、哪些依赖未确认？ | [证据与能力](evidence.md) |
| M01 | 视频怎样压缩，因果性如何证明？ | [Causal VAE](../../../algorithms/causal-video-vae/README.md) |
| M02 | noisy latent、速度目标和采样方向是什么？ | [流匹配](../../../algorithms/flow-matching/README.md) |
| M03 | Spatial/Temporal/MMDiT 怎样算？ | [张量与复杂度](../../../algorithms/diffusion-transformers/README.md) |
| M04 | 文本/视频/镜头坐标怎样对应？ | [MM-RoPE](../../../algorithms/multimodal-position/README.md) |
| M05 | 视频和音频怎样联合又怎样对齐？ | [联合音视频](../../../algorithms/audio-video-joint/README.md) |
| M06 | 长视频怎样训练，什么条件下能缓存？ | [长上下文](../../../algorithms/long-video/README.md) |
| M07 | 参考图/视频/白模怎样绑定并进入模型？ | [参考控制](../../../algorithms/reference-conditioning/README.md) |
| M08 | 只改指定区域/区间怎样定义和验收？ | [编辑](../../../algorithms/video-editing/README.md) |
| M09 | Caption、PE、生成器、奖励分别训练谁？ | [后训练](../../../algorithms/post-training/README.md) |
| M10 | 怎么测瓶颈并选择加速？ | [推理优化](../../../algorithms/inference-optimization/README.md) |
| M11 | 真实素材怎样变成不泄漏的训练数据？ | [数据配方/格式/检查](../../../datasets/recipes/audio-video-production/README.md) |
| M12 | 哪些部件兼容，增量方案怎么拼？ | [候选架构](architecture.md) |
| M13 | 每阶段训练什么、怎样复现和停止？ | [训练计划](training.md) |
| M14 | 哪类业务问题用哪条路线？ | [业务映射与 pilot](../../../applications/video-production/solutions.md) |
| M15 | 极简代码怎样对应真实工程？ | [代码路线与仓库选择](../../../docs/code-paths.md) |
| M16 | 多参考如何绑定主体与时间区间？ | [参考与时间控制](reference-timeline.md) |
| M17 | 源视频、区域与目标编辑如何统一？ | [编辑条件](editing-conditions.md) |
| M18 | 白模、相机与场景记忆如何进入模型？ | [几何控制](geometry-control.md) |
| M19 | 多参考、长叙事、编辑与音视频如何组成一套主干？ | [完整候选架构](integrated-design.md) |
| M20 | 这套候选架构如何训练？ | [完整训练配方](integrated-training.md) |

基础概念在 `algorithms/` 维护，来源在 `sources/`、单篇笔记在 `papers/`，本页只作学习入口，避免下一轮出现多份互相矛盾的基础笔记。

## 怎样逐块迭代

从 M00 或 M01 开始，用 [检查表](review.md) 留下具体问题、需修改的公式/接口、来源或反例。检查题、证据定位和纠错记录留在研究侧，不作为文章的前置阅读条件。真实网络、训练和业务验证仍是独立状态。

原始 [talk2deepseek.md](../../../talk2deepseek.md) 完整保留；与本轮当前理解不同的说法集中记录在 [纠错表](../../../research/2026-11-22-seedance-foundations/corrections.md)。
