---
status: draft
updated: 2026-11-22
source_ids: ["vace"]
topic_ids: ["video-generation"]
---

# VACE：统一视频条件与编辑接口

阅读版：arXiv2503.07598v2，17页，本轮新下载；重点PDF pp.3–5条件/adapter/数据，未运行代码。

## 能直接落实的设计

VCU由text、frame sequence、mask sequence组成。mask=1为待变化，0为保留；reactive与inactive分别为F*M、F*(1-M)。两路经VAE编码，mask重排/插值对齐，再channel concat进入context embedder。

reference images独立编码，再放回条件序列，防止素材边界的非预期混合。支持T2V、reference、整体V2V、maskedV2V与组合任务，但每项能力仍依赖对应训练。

full fine-tuning和context adapter tuning是两条路线；后者冻结DiT，复制若干原block形成context支路，并将输出加回主干。它为不改旧noisy输入头的增量适配提供具体参考。

## 迁移范围

从Wan/VACE移到LTX联合主干需要匹配latent通道、特征维、调制、时间和loss，不是直接加载插件。本文用其条件分解与残差路径作为候选设计；源条件latent和目标已知区重噪覆盖也必须区分。

独立正文：[统一编辑接口](../../topics/video-generation/seedance-2.5/editing-conditions.md)。VACE官方仓库可作真实条件实现入口，新增联合音频任务不由原视频VCU自动解决。
