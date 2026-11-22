---
status: draft
updated: 2026-11-22
source_ids: ["alchemint"]
topic_ids: ["video-generation"]
---

# AlcheMinT：参考主体的时间区间控制

阅读版：CVPR 2026 出版方11页版本；首次arXiv公开为2025年。PDF身份与URL见来源登记，本轮重点读取PDF pp.4–5方法/绑定/数据管线，未复现。

## 方法与作用

参考图由原视频VAE编码，参考实体词经文本编码与MLP后加入视觉序列；同一索引embedding绑定图像与词。joint self-attention处理视频/参考，caption仍通过文本cross-attention进入。WeRoPE试图组合区间中点与边缘的时间轮廓，使参考对一个区间持续有效，而不只表示中点。

数据使用实体提取、Grounding DINO、多时间检测、SAM2双向跟踪，获取主体可见性与区间。训练中从与目标片段较远的位置抽参考，配合裁剪和增强减少复制。

## 不能直接转抄的地方

PDF p.5 equation 5 将相位加权后的旋转写成加权旋转结果的和，并称为RoPE线性。一般的旋转角度不满足这种线性等式；需要结合作者实现或补充材料确认“frequency/rotation”的准确对象。本轮未取得作者对应实现，不能把该等式直接编成生产代码。

因此候选方案借鉴“主体—词绑定＋区间监督”的任务设计，首版用独立reference attention上的显式时间bias，不改主干原RoPE；这属于自行设计，未声称复现WeRoPE。首次/末次可见边界也不能表达中途缺席，数据接口用多区间列表和可见性置信度扩展。

当前独立文章：[多参考与时间控制](../../topics/video-generation/seedance-2.5/reference-timeline.md)。作者项目页当前提供论文与展示，不把其页面模板仓库误认为模型代码。尚缺时间控制误差、多人串用、压缩参考容量的真实验证。
