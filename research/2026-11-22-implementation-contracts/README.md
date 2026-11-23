# 从候选设计到实现契约与最终推测方案

开始于2026-11-22，2026-11-23续作。状态draft，未进行真实训练、模型生成或GPU测试。

## 本轮目标与用户补充

承接上一轮独立文章、论文插图、极简代码与固定版本真实实现的要求，补齐新增模块、参考绑定、编辑、长视频、数据训练和推理交付六类规格。用户已明确不要求运行教学片段，不据此扩建训练框架或新增运行测试。

2026-11-23用户进一步指定：最终需要针对Seedance 2.5的完全推测且合理的完整方案，覆盖架构、基础模块、数据、训练、优化、成本与应用；该部分可以有引用。投入方向必须明确，例如技术架构保持相对稳定，重点做应用适配、插件或数据。新增 [最终方案](../../topics/video-generation/seedance-2.5/speculative-plan.md) 将这些要求统一为“稳定联合主干、任务数据优先、缺接口才加有限条件插件、行业工作流驱动交付”，并允许可点击引用。

## 产出入口

| 文章 | 目的 | 完成边界 |
|---|---|---|
| [M21 模块契约](../../topics/video-generation/seedance-2.5/adapter-contract.md) | 固定主干、插入层位、宽度、门控、参数收集与保存 | 纸面接口，不是现成插件 |
| [M22 参考绑定](../../topics/video-generation/seedance-2.5/reference-binding-spec.md) | 主体槽、属性、时间、冲突、预算与声音归属 | 摘要与细节效果未验证 |
| [M23 AV编辑](../../topics/video-generation/seedance-2.5/av-editing-spec.md) | 四类mask、音轨任务、工作区与合成保证 | 无真实编辑对训练或交付测量 |
| [M24 长视频](../../topics/video-generation/seedance-2.5/long-video-spec.md) | 四类因果边、干净重算缓存、历史重标与decoder前瞻 | 独立可选派生路线，未实现 |
| [M25 数据训练](../../topics/video-generation/seedance-2.5/data-training-spec.md) | 数据生产、噪声课程、loss、参数组与恢复 | 候选数值，不是收敛配方 |
| [M26 推理交付](../../topics/video-generation/seedance-2.5/inference-delivery-spec.md) | 资源项、求值次数、质量档位、pilot与返工 | 算术口径，无GPU/业务实测 |
| [M27 最终方案](../../topics/video-generation/seedance-2.5/speculative-plan.md) | 面向2.5完整推测，明确每方向目的与投入 | 公开事实、假设、替代选型与成本示例分开 |

新增四份 [机制片段](../../algorithms/examples/README.md)：零门控读取、逐token条件状态、四类AV块mask、逐样本有效损失；合计16份，均未调用。真实代码登记扩展到10个仓库、11份固定版本记录、57个源码/配置入口。

## 来源身份与实际阅读

### 公开产品依据

沿用 [基础轮次网页快照记录](../2026-11-22-seedance-foundations/source-checks.json)：2.5发布页2026-07-31正文明确“延续了Seedance 2.0统一的多模态音视频联合生成架构”。它支持总体方向连续，不证明层数、权重、条件路径不变，也不证明改进主要由某个数据集或插件贡献。未刷新当前API可用性、价格和套餐。

Phantom、AlcheMinT、VACE、VideoCoF、Geometry-as-Context、LCT与LongLive用于候选机制论证；论文定位沿用 [关键设计轮次](../2026-11-22-key-design/README.md)。晚于发布的VINCIE-NExT只能作当前设计类比，不能作为历史采用证据。

### 原系列源码

固定commit `bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638`。13个本轮补查文件的URL与SHA-256见 [source-checks.json](source-checks.json)；已有transformer.py、video_vae.py等仍由 [sources/code.json](../../sources/code.json) 记录。检查的是文本、配置和依赖关系，没有导入上游代码。

| 路径/符号 | 定点发现 | 影响 |
|---|---|---|
| `transformer/model.py`，块循环与前后处理 | 原生投影和联合块，未包含本文新增支路 | 12处插入是候选改动 |
| `transformer/transformer.py:137`，`BasicAVTransformerBlock.forward` | `run_ax`控制音频隐藏计算；双向AV读取交换前norm状态 | latent固定不等于隐藏状态禁用或静态缓存 |
| 同文件self/AV Attention调用 | 文本mask已有，本文四类块因果mask未完整透传 | 因果派生需修改数据结构与调用 |
| `transformer/transformer_args.py`，噪声与AV调制 | 可处理逐token噪声状态，倍率来自实例配置 | 干净历史/音轨须显式传0 |
| `components/patchifiers.py`，坐标转换与音频时间 | 位置网格、帧率/采样率与首帧偏移 | 位置边界不是完整codec感受野 |
| `training_strategies/text_to_video.py` | 可联合AV，两流共同sigma起步 | 可作基础AV策略入口 |
| `training_strategies/video_to_video.py` | 干净参考拼目标，输出`audio=None` | 不是候选联合音频编辑策略 |
| `timestep_samplers.py`，`_get_shift_for_sequence_length` | 0.95至2.05为插值锚点，不是自动截断范围 | 长阶段候选限制shift，保留原生对照 |
| `trainer.py`，参数收集与`_save_checkpoint:856` | 基于Transformer收集参数，LoRA经PEFT筛选；当前保存主要为权重 | 新模块与训练恢复包需要显式实现 |

### 模型配置与文件头

固定模型revision `64f65d09e0b76c96202b5bc09997673184cf9b5d`、文件 `ltx-2-19b-dev.safetensors`。上一段工作已通过小文件和远端Range读取JSON文件头，缓存中有603120字节头数据；本次续作核对其哈希和配置，没有下载张量载荷。记录在 [model-config-check.json](model-config-check.json)。

- 原生头配置：48层、视频4096/音频2048宽度、32头、两流128维输入输出、文本3840、split RoPE、float64频率、1000倍时间/AV调制。
- 配套VAE配置及原生头：因果编码与非因果解码需分开，`vae.causal_decoder=false`不支持无前瞻流式交付假设。
- 远端声明全文件43285058242字节及SHA-256；不是本地完整文件校验。`local_full_weight_hash`保持null，`tensor_payload_downloaded_bytes=0`。
- 头中`model.diffusion_model.*`约19585115392标量元素、39176743424存储字节，只是序列化统计，不直接写成精确可训练参数量。

以上仅约束公开替代基座，不能转写为Seedance2.5的层宽、参数或训练预算。

## 修订与继续工作

同步修订M19/M20、代码路线、论文笔记、目录、路线图与 `candidate-av-v2`。逐项变化见 [corrections.md](corrections.md)。下一步是审阅最终方案的能力取舍与任务假设；模型实施、真实数据生产与成本测量仍是后续工作，不因本文完成而自动获得结论。

## 实际检查

已完成：13个定点源文件、7个小型模型配置和JSON头的缓存SHA-256与登记比对；只使用标准库读取文本。确认注意力矩阵99.0647GiB、参考K/V 50.331648MB、源条件缓存500.957184MB的算术，非显存实测。

本轮最终仓库与阅读构建结果另记在 [verification.json](verification.json)。不导入机制片段、不运行模型/训练/旧实验；格式、引用和渲染检查不构成科学复现。
