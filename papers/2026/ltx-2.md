---
status: draft
updated: 2026-11-23
source_ids: ["ltx-2", "ltx-original-code", "ltx-original-model"]
topic_ids: ["video-generation"]
---

# LTX-2：明确的联合音视频主干与时间表示

阅读版：arXiv2601.03233v1，14页；重点PDF pp.4–8。与原系列源码commit `bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638` 定点对照，不与当前仓库包含的2.5型号混用。未运行、未下载权重。

补充检查：原系列 `ltx-2-19b-dev.safetensors` 已读取603120字节JSON文件头及配套小型配置，没有下载张量载荷；未完成完整权重本地哈希校验，模型运行状态仍为空。

## 结构与数值

14B视频流与5B音频流，每块依次为流内self-attention、text cross-attention、AV cross-attention、FFN；跨模态使用共同时间RoPE与调制/gate。论文文本为Gemma3系，早期多层投影训练后冻结，connector继续训练。

音频使用16kHz立体声mel、causal VAE，约25时间位置/秒、128维；经vocoder解码为24kHz立体声。原实现可保留8通道×16频带的内部latent，再整理为每时间位置128维。

视频源码types.py与video_vae.py给默认时间/8、空间/32、128通道，F=1+8k。transformer configurator给出48层与4096/2048宽度的默认值，但checkpoint配置仍是实例配置依据，不将默认值宣称全部型号固定规格。

## 固定开发权重的实例配置

模型来源revision为 `64f65d09e0b76c96202b5bc09997673184cf9b5d`，文件头 `__metadata__.config.transformer` 确认48层、视频32头×128维、音频32头×64维、两流输入输出128维、文本宽3840、split RoPE、float64频率与1000倍噪声/AV调制。文件头投影shape分别为 `[4096,128]` 与 `[2048,128]`。原生VAE元数据 `causal_decoder=false`，配套转换配置另标 `encoder_causal=true`；因果encoder不能推出无前瞻decoder。

固定源码 `transformer.py:137` 后可见 `run_ax` 与latent采样更新是不同机制；视频/音频self和AV调用也未透传本文候选四类块因果mask。trainer的 `text_to_video.py` 支持共同sigma的AV目标，`video_to_video.py` 返回 `audio=None`；`trainer.py:_save_checkpoint` 保存模型/LoRA权重，不是完整训练恢复包。文件身份、哈希及详细支持范围见 [模型检查](../../research/2026-11-22-implementation-contracts/model-config-check.json) 与 [定点定位](../../research/2026-11-22-implementation-contracts/README.md)。这些事实只约束该公开替代基座，不是Seedance内部配置。

## 选择意义

可作为完整候选方案的共同基座，已有AV表示/交互，不再要求把Wan与一个随意音频模型硬接。多参考binding、编辑条件、长因果训练仍需新增；原系列源码有AV LoRA与video-only IC-LoRA配方，也不证明这些配方已经覆盖本方案的全部条件。

正文见 [完整候选架构](../../topics/video-generation/seedance-2.5/integrated-design.md)、[联合训练](../../topics/video-generation/seedance-2.5/integrated-training.md)。代码与模型许可分别记录；不得用后来型号的文本编码器替换原系列，再声称仍在复现这篇报告。
