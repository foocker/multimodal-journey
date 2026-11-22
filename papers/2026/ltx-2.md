---
status: draft
updated: 2026-11-22
source_ids: ["ltx-2", "ltx-original-code"]
topic_ids: ["video-generation"]
---

# LTX-2：明确的联合音视频主干与时间表示

阅读版：arXiv2601.03233v1，14页；重点PDF pp.4–8。与原系列源码commit `bd92a5f408eb8c99f8c05e9fe2fcaaec8b56b638` 定点对照，不与当前仓库包含的2.5型号混用。未运行、未下载权重。

## 结构与数值

14B视频流与5B音频流，每块依次为流内self-attention、text cross-attention、AV cross-attention、FFN；跨模态使用共同时间RoPE与调制/gate。论文文本为Gemma3系，早期多层投影训练后冻结，connector继续训练。

音频使用16kHz立体声mel、causal VAE，约25时间位置/秒、128维；经vocoder解码为24kHz立体声。原实现可保留8通道×16频带的内部latent，再整理为每时间位置128维。

视频源码types.py与video_vae.py给默认时间/8、空间/32、128通道，F=1+8k。transformer configurator给出48层与4096/2048宽度的默认值，但checkpoint配置仍是实例配置依据，不将默认值宣称全部型号固定规格。

## 选择意义

可作为完整候选方案的共同基座，已有AV表示/交互，不再要求把Wan与一个随意音频模型硬接。多参考binding、编辑条件、长因果训练仍需新增；原系列源码有AV LoRA与video-only IC-LoRA配方，也不证明这些配方已经覆盖本方案的全部条件。

正文见 [完整候选架构](../../topics/video-generation/seedance-2.5/integrated-design.md)、[联合训练](../../topics/video-generation/seedance-2.5/integrated-training.md)。代码与模型许可分别记录；不得用后来型号的文本编码器替换原系列，再声称仍在复现这篇报告。
