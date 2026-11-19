---
status: draft
updated: 2026-11-19
source_ids: ["pixeldance"]
topic_ids: ["video-generation"]
---

# PixelDance

**正式标题：** Make Pixels Dance: High-Dynamic Video Generation

| 项目 | 记录 |
|---|---|
| 来源 ID | `pixeldance` |
| 首次公开 / 阅读版本 | 2023 / `2311.10982v1` |
| 实际保存版本 | CVPR 2024, pp. 8850–8860 |
| 链接 | [来源页](https://openaccess.thecvf.com/content/CVPR2024/html/Zeng_Make_Pixels_Dance_High-Dynamic_Video_Generation_CVPR_2024_paper.html) · [PDF URL](https://openaccess.thecvf.com/content/CVPR2024/papers/Zeng_Make_Pixels_Dance_High-Dynamic_Video_Generation_CVPR_2024_paper.pdf) · [arXiv 固定版本](https://arxiv.org/abs/2311.10982v1) |
| 页数 / 阅读位置 | 11 页；第 1–5 页及实验部分 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

用文本和首尾帧图像指令控制扩散式视频生成，面向复杂场景与较大幅度运动。将动作生成与条件控制联系起来，是观察早期视频模型路线的材料。

## 放在技术演进中怎样理解

主线材料。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

研究模型、2024 年商业模型选项和后续 Seedance 产品不是自动等同的对象；不能从作者重合直接推断完整架构继承。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
