---
status: draft
updated: 2026-11-22
source_ids: ["videocof"]
topic_ids: ["video-generation"]
---

# VideoCoF：可监督的区域中间表示与视频编辑

阅读版：CVPR 2026 出版方10页版本；arXiv首次编号2512.07469。重点读PDF pp.3–5，未复现。

## 核心机制

分别编码source、reasoning和target，再沿时间拼接。source保持干净，reasoning/target在同一采样链加噪去噪，损失只作用于后两者。灰度高亮区域作为可监督reasoning表示，不是不可见语言思维链。

source和target重置到相同局部时间1..F，reasoning用0，避免三类内容都挤在时间0的特定冲突。该位置设计不是任意视频编辑的通用公式。

数据用多实例识别、检测分割、删除/添加反转、局部替换/风格变换等专家产生，再过滤。作者报告50K数据、Wan-14B、33帧训练等条件，不代表本仓库拥有同一数据或效果。

## 实现区分

论文尽管称reason-then-edit，原文算法仍是reasoning与target在联合序列里一起去噪，并非严格先完整生成mask、再另起一条目标采样链。本候选工程为便于检查，选择显式两阶段定位/编辑，属于有额外计算与误差传播的新设计。

正文见 [统一编辑条件](../../topics/video-generation/seedance-2.5/editing-conditions.md)。需要分别评价区域准确性、编辑成功、外区保持、长视频漂移；不能把作者的长序列展示直接作为LTX迁移保证。
