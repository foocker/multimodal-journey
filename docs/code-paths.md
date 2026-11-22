---
status: draft
updated: 2026-11-22
source_ids: ["wan21-code", "diffsynth-code", "phantom-code", "longlive-code", "vincie-code", "ltx-code", "dancegrpo-code", "tarsier-code", "ltx-original-code", "vace-code", "videocof-code"]
---

# 从机制示例到真实工程：视频生成的代码路线

理解一个视频模块时，几十行代码往往比完整训练框架更清楚；真正制作数据、训练和生成时，则应使用已经组织好模型加载、调度、分布式和输出流程的工程。这两种代码各有用途，不需要把教学片段扩写成另一个大型框架。

这里把十二份本地机制示例与十个上游仓库对应起来，其中 LTX 原系列与当前版本分别固定。仓库版本、源码入口和许可证已经查阅，未运行模型或训练，也不据此承诺它们满足某个具体业务的效果与硬件条件。

## 用极简代码理解一件事

| 机制 | 本地示例 | 阅读重点 | 真实实现入口 |
|---|---|---|---|
| 因果时空卷积 | [causal_conv.py](../algorithms/examples/causal_conv.py) | 时间左 padding 与 stride/dilation | Wan VAE |
| 流匹配 | [flow_matching.py](../algorithms/examples/flow_matching.py) | noisy、速度目标、有效区损失、Euler | Wan 采样与 DiffSynth 训练 |
| 三维 RoPE | [rope.py](../algorithms/examples/rope.py) | 按通道分轴旋转 Q/K | Wan / VINCIE / LTX RoPE |
| 空间与时间注意力 | [attention_layout.py](../algorithms/examples/attention_layout.py) | 哪些维合成 batch，哪些合成序列 | Wan block / VINCIE MM attention |
| 参考条件 | [reference_adapter.py](../algorithms/examples/reference_adapter.py) | query、reference K/V、绑定 mask、门控 | Phantom-Wan |
| 区间与区域编辑 | [local_edit.py](../algorithms/examples/local_edit.py) | 时间选择、已知区重噪、最终像素保留 | VINCIE 图像编辑 / LTX 条件流水线 |
| 联合音视频 | [audio_video_exchange.py](../algorithms/examples/audio_video_exchange.py) | 双向读取更新前状态 | LTX AV Transformer |
| 偏好优化 | [preference_objectives.py](../algorithms/examples/preference_objectives.py) | DPO、组内优势、clipped objective | DanceGRPO |
| 缓存失效 | [cache_context.py](../algorithms/examples/cache_context.py) | 历史与条件不变才能复用 | LongLive 因果推理 |
| 参考时间门 | [reference_timing.py](../algorithms/examples/reference_timing.py) | 物理时间、软区间偏置；归属mask与null token另接 | 候选支路；不是WeRoPE复现 |
| 统一视觉条件 | [condition_unit.py](../algorithms/examples/condition_unit.py) | 待变/保留拆分、时间与空间编辑范围 | VACE条件与mask预处理 |
| 相机射线 | [camera_rays.py](../algorithms/examples/camera_rays.py) | camera-to-world、方向与矩、单位一致 | 结构条件投影由候选工程新增 |

示例的约束写在各文件开头：有的省略多头，有的要求每个 query 至少有一个有效参考，有的只支持整除的空间窗口。它们解释依赖关系，不负责补齐生产环境中的所有分支，也不能直接加载这些仓库的 checkpoint。

## 从 Wan 建立基础生成链路

[Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1) 适合阅读和使用基础文生视频、图生视频、VAE 与 DiT。固定版本为 `9737cba9c1c3c4d04b33fcad41c111989865d315`。

- [生成入口 generate.py](https://github.com/Wan-Video/Wan2.1/blob/9737cba9c1c3c4d04b33fcad41c111989865d315/generate.py)：参数、任务选择和结果输出。
- [text2video.py](https://github.com/Wan-Video/Wan2.1/blob/9737cba9c1c3c4d04b33fcad41c111989865d315/wan/text2video.py)：文本、噪声、scheduler 和解码怎样衔接。
- [vae.py](https://github.com/Wan-Video/Wan2.1/blob/9737cba9c1c3c4d04b33fcad41c111989865d315/wan/modules/vae.py)：`CausalConv3d`、上下采样、encoder/decoder 和缓存。
- [model.py](https://github.com/Wan-Video/Wan2.1/blob/9737cba9c1c3c4d04b33fcad41c111989865d315/wan/modules/model.py)：`WanAttentionBlock`、`rope_apply` 与主干。

阅读顺序可先从 `generate.py` 跟进 `text2video.py`，再进入模块。只看 VAE 中的一个卷积类，无法推导完整视频采样流程。

## 用 DiffSynth-Studio 接入真实训练

[modelscope/DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio) 提供 Wan 的推理、LoRA 和全参训练。固定版本为 `d32f72424cd22bc0ea8100cc57559149b4eac933`。

- [训练入口 train.py](https://github.com/modelscope/DiffSynth-Studio/blob/d32f72424cd22bc0ea8100cc57559149b4eac933/examples/wanvideo/model_training/train.py)：`WanTrainingModule`、数据参数和训练组件。
- [1.3B LoRA 配方](https://github.com/modelscope/DiffSynth-Studio/blob/d32f72424cd22bc0ea8100cc57559149b4eac933/examples/wanvideo/model_training/lora/Wan2.1-T2V-1.3B.sh)：数据路径、模型组件、学习率、rank 与 target modules。
- [1.3B 全参配方](https://github.com/modelscope/DiffSynth-Studio/blob/d32f72424cd22bc0ea8100cc57559149b4eac933/examples/wanvideo/model_training/full/Wan2.1-T2V-1.3B.sh)：与 LoRA 比较哪些参数进入训练。
- [1.3B 推理样例](https://github.com/modelscope/DiffSynth-Studio/blob/d32f72424cd22bc0ea8100cc57559149b4eac933/examples/wanvideo/model_inference/Wan2.1-T2V-1.3B.py)：模型加载与 pipeline 调用。

真实实施可先沿用这个训练框架，再增加业务数据和所需条件路径。现成 LoRA 能调整模型行为，但不会自动获得角色绑定、任意参考数量或时间戳编辑；这些能力还依赖对应模型接口与数据任务。

## 用 Phantom-Wan 研究主体参考

[Phantom-video/Phantom](https://github.com/Phantom-video/Phantom) 的公开实现建立在 Wan 上，固定版本为 `bd84b602dcc949e23c89cbbf266b6f5975f2f025`。

- [generate.py](https://github.com/Phantom-video/Phantom/blob/bd84b602dcc949e23c89cbbf266b6f5975f2f025/generate.py)：参考图片列表与主体生成参数。
- [subject2video.py](https://github.com/Phantom-video/Phantom/blob/bd84b602dcc949e23c89cbbf266b6f5975f2f025/phantom_wan/subject2video.py)：参考编码与采样编排。
- [model.py](https://github.com/Phantom-video/Phantom/blob/bd84b602dcc949e23c89cbbf266b6f5975f2f025/phantom_wan/modules/model.py)：参考条件怎样进入主干。

该版本提供参考推理，README 的训练代码项目仍未勾选。因此它适合作为参考生成和结构阅读入口，不能直接称为可用的完整训练仓库。公开的 Phantom-Wan 与论文内部基座也需要区分。

## 从 LongLive1.0 阅读长视频训练与缓存

[NVlabs/LongLive](https://github.com/NVlabs/LongLive) 固定版本为 `31c70d9071cd7851d82939806dc9fac645fcabe5`。仓库已同时包含多个后续项目，研究原始长视频框架应进入 `LongLive1.0/`。

- [inference.py](https://github.com/NVlabs/LongLive/blob/31c70d9071cd7851d82939806dc9fac645fcabe5/LongLive1.0/inference.py) 与 [train.py](https://github.com/NVlabs/LongLive/blob/31c70d9071cd7851d82939806dc9fac645fcabe5/LongLive1.0/train.py)：整体入口。
- [causal_inference.py](https://github.com/NVlabs/LongLive/blob/31c70d9071cd7851d82939806dc9fac645fcabe5/LongLive1.0/pipeline/causal_inference.py)：当前块去噪、历史缓存及窗口组织。
- [streaming_training.py](https://github.com/NVlabs/LongLive/blob/31c70d9071cd7851d82939806dc9fac645fcabe5/LongLive1.0/pipeline/streaming_training.py)：流式训练如何使用历史。
- [causal_model.py](https://github.com/NVlabs/LongLive/blob/31c70d9071cd7851d82939806dc9fac645fcabe5/LongLive1.0/wan/modules/causal_model.py)：`CausalWanSelfAttention` 和缓存数据路径。

这里的价值是读取“模型、训练分布、缓存”怎样配套，而不是把缓存类单独移植到任意双向扩散模型。它也不是 Seedance 已确认的内部实现。

## 从 VINCIE 阅读多轮编辑与交错序列

[ByteDance-Seed/VINCIE](https://github.com/ByteDance-Seed/VINCIE) 固定版本为 `97cd2c5701e694dabcfea320c0cf59893d427fab`。

- [generate.py](https://github.com/ByteDance-Seed/VINCIE/blob/97cd2c5701e694dabcfea320c0cf59893d427fab/generate.py)：`VINCIEGenerator` 多轮图像编辑入口。
- [生成配置](https://github.com/ByteDance-Seed/VINCIE/blob/97cd2c5701e694dabcfea320c0cf59893d427fab/configs/generate.yaml)：模型与采样配置。
- [mmattn.py](https://github.com/ByteDance-Seed/VINCIE/blob/97cd2c5701e694dabcfea320c0cf59893d427fab/models/dit/blocks/attention/mmattn.py)：联合多模态与窗口注意力。
- [rope.py](https://github.com/ByteDance-Seed/VINCIE/blob/97cd2c5701e694dabcfea320c0cf59893d427fab/models/dit/rope.py)：多模态位置编码。

它直接处理的是多轮图像编辑，不能把这个生成入口当成通用视频时间戳编辑。图像上下文方法怎样传播到时间连续的视频，是另一层任务和实现。

## 用 LTX 阅读可实现的联合音视频

[Lightricks/LTX-2](https://github.com/Lightricks/LTX-2) 固定版本为 `daa6b16fc7f0f1628f2c9e36a303e3312b333cc6`。

- [transformer.py](https://github.com/Lightricks/LTX-2/blob/daa6b16fc7f0f1628f2c9e36a303e3312b333cc6/packages/ltx-core/src/ltx_core/model/transformer/transformer.py)：`BasicAVTransformerBlock` 的视频/音频交互。
- [rope.py](https://github.com/Lightricks/LTX-2/blob/daa6b16fc7f0f1628f2c9e36a303e3312b333cc6/packages/ltx-core/src/ltx_core/model/transformer/rope.py)：位置与频率实现。
- [推理说明](https://github.com/Lightricks/LTX-2/blob/daa6b16fc7f0f1628f2c9e36a303e3312b333cc6/packages/ltx-pipelines/README.md)：选择模型对应的 pipeline。
- [训练说明](https://github.com/Lightricks/LTX-2/blob/daa6b16fc7f0f1628f2c9e36a303e3312b333cc6/packages/ltx-trainer/README.md) 与 [音视频条件配置](https://github.com/Lightricks/LTX-2/blob/daa6b16fc7f0f1628f2c9e36a303e3312b333cc6/packages/ltx-trainer/configs/av2av_ic_lora.yaml)：真实训练路线。

当前版本覆盖多个 LTX 型号，模型、codec、文本组件与 LoRA 要按对应说明匹配。代码是 Apache-2.0，模型使用单独的 Community License；这两类许可不能混为一项。LTX 可作为联合音视频工程的独立选择，不能直接成为 Wan 的兼容音频插件。

## 将 LTX 原系列固定为共同主干

完整候选设计选择初始公开系列，另固定 `bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638`，避免后续型号的文本、codec与训练配置混入。阅读顺序是表示、主干、训练策略：

- [types.py](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/packages/ltx-core/src/ltx_core/types.py)：视频/音频latent布局及尺寸约定。
- [transformer.py](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/packages/ltx-core/src/ltx_core/model/transformer/transformer.py)：原生AV交互、调制和门控。
- [video_vae.py](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/packages/ltx-core/src/ltx_core/model/video_vae/video_vae.py)：视频编码、解码与原生归一化。
- [音视频LoRA配置](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/packages/ltx-trainer/configs/ltx2_av_lora.yaml) 与 [视频条件IC-LoRA配置](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/packages/ltx-trainer/configs/ltx2_v2v_ic_lora.yaml)：已有策略、组件和参数组的落地起点。

这些配置没有自动包含候选方案的多参考池化、角色时间绑定、VACE式支路或因果续写；新增接口与任务仍需实现。该历史commit的 [根许可证](https://github.com/Lightricks/LTX-2/blob/bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638/LICENSE) 是 LTX-2 Community License，应按历史版本记录，不能回填当前版本的Apache代码许可结论。

## 从 VACE 阅读统一视觉条件

[ali-vilab/VACE](https://github.com/ali-vilab/VACE) 固定 `48eb44f1c4be87cc65a98bff985a26976841e9f3`，代码Apache-2.0。它把不同视觉条件组织为帧与mask，再接入相应基座。

- [vace_preproccess.py](https://github.com/ali-vilab/VACE/blob/48eb44f1c4be87cc65a98bff985a26976841e9f3/vace/vace_preproccess.py)：条件预处理入口，文件名沿用上游拼写。
- [mask.py](https://github.com/ali-vilab/VACE/blob/48eb44f1c4be87cc65a98bff985a26976841e9f3/vace/annotators/mask.py)：编辑区域和mask组织。
- [vace_wan_inference.py](https://github.com/ali-vilab/VACE/blob/48eb44f1c4be87cc65a98bff985a26976841e9f3/vace/vace_wan_inference.py)：条件、checkpoint与Wan采样链路怎样配合。

这是可用视觉控制工程的入口，但不同基座分支有各自权重和条件层。即使目录中出现LTX分支，也不代表能直接加载到这里固定的LTX-2原系列。

## 从 VideoCoF 阅读区域中间表示

[knightyxp/VideoCoF](https://github.com/knightyxp/VideoCoF) 固定 `f45b8009616b3ef8e2024a7da585249b4c74fc2b`，代码Apache-2.0，包含Wan/VideoX-Fun的推理与训练入口。

- [predict_v2v_cot_json.py](https://github.com/knightyxp/VideoCoF/blob/f45b8009616b3ef8e2024a7da585249b4c74fc2b/examples/wan2.1/predict_v2v_cot_json.py)：源视频、指令与区域式编辑的推理组织。
- [train_joint_img_video_lora.py](https://github.com/knightyxp/VideoCoF/blob/f45b8009616b3ef8e2024a7da585249b4c74fc2b/scripts/wan2.1/train_joint_img_video_lora.py)：图像/视频联合训练与LoRA入口。
- [pipeline_wan.py](https://github.com/knightyxp/VideoCoF/blob/f45b8009616b3ef8e2024a7da585249b4c74fc2b/videox_fun/pipeline/pipeline_wan.py)：条件与去噪执行路径。

区域与目标联合去噪是一种具体建模选择。候选设计为了可检查性先定位再编辑，执行图和训练数据组织都要相应修改；不能只把这个采样入口改名就视为完成迁移。

## 从 DanceGRPO 看完整视觉策略优化

[XueZeyue/DanceGRPO](https://github.com/XueZeyue/DanceGRPO) 固定版本为 `15cc71d53cc2e6e18a68ee607d5fb6ba9a99e344`。

- [Hunyuan 视频训练](https://github.com/XueZeyue/DanceGRPO/blob/15cc71d53cc2e6e18a68ee607d5fb6ba9a99e344/fastvideo/train_grpo_hunyuan.py)：采样、奖励、优势和策略更新。
- [启动配方](https://github.com/XueZeyue/DanceGRPO/blob/15cc71d53cc2e6e18a68ee607d5fb6ba9a99e344/scripts/finetune/finetune_hunyuan_grpo.sh)：数据、模型和分布式设置。
- [Wan 分支](https://github.com/XueZeyue/DanceGRPO/blob/15cc71d53cc2e6e18a68ee607d5fb6ba9a99e344/fastvideo/train_grpo_wan_2_1.py)：比较基座差异。

固定版 README 将 Wan 分支当作图像生成并使用 HPS 奖励，所以不能据其文件名就认定已经提供完整视频任务的可靠奖励配方。阅读重点是 SDE 转移概率、组内比较和更新流程；奖励是否代表业务质量仍需另行定义。

## 用 Tarsier 进入描述数据生产

[bytedance/tarsier](https://github.com/bytedance/tarsier) 固定版本为 `63de87a760c2aec6b31470a08046969a13787126`。

- [inference_caption.py](https://github.com/bytedance/tarsier/blob/63de87a760c2aec6b31470a08046969a13787126/tasks/inference_caption.py)：批量描述入口。
- [启动脚本](https://github.com/bytedance/tarsier/blob/63de87a760c2aec6b31470a08046969a13787126/scripts/run_inference_caption.sh)：输入、模型和输出组织。
- [模型封装](https://github.com/bytedance/tarsier/blob/63de87a760c2aec6b31470a08046969a13787126/models/modeling_tarsier.py) 与 [评价入口](https://github.com/bytedance/tarsier/blob/63de87a760c2aec6b31470a08046969a13787126/evaluation/evaluate.py)：描述模型怎样被调用与评价。

选 checkpoint 时同时匹配 Tarsier/Tarsier2 的 processor 和配置。描述生成完成后，仍应抽检动作遗漏、时序和事实；自动生成文本不等于获得无误差监督。

## 实际选型时怎样组合

基础推理可从 Wan 开始，业务微调可用 DiffSynth；已有主体参考需求可先看 Phantom-Wan 的推理结构，长视频单独研究 LongLive；多轮图像编辑看 VINCIE，统一视频条件看 VACE，区域中间表示看 VideoCoF，联合音视频另选配套的 LTX 路线；数据生产由描述工具支持，策略优化放在基础数据和目标稳定之后。

它们可以共享任务规格、素材和评价方法，但训练入口、权重、scheduler 和条件接口并不自动兼容。只有明确需要修改的接口时，才把某个机制迁入另一个基座。

10个仓库的11份固定版本记录与44个代码/配置入口登记在 [sources/code.json](../sources/code.json)。需要阅读固定版本时，可以使用以下形式获取源码；安装、权重与启动参数以相应版本的说明为准：

```bash
git clone https://github.com/Wan-Video/Wan2.1.git
git -C Wan2.1 checkout 9737cba9c1c3c4d04b33fcad41c111989865d315
```
