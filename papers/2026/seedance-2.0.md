---
status: draft
updated: 2026-11-19
source_ids: ["seedance-2.0"]
topic_ids: ["video-generation"]
---

# Seedance 2.0

**正式标题：** Seedance 2.0: Advancing Video Generation for World Complexity

| 项目 | 记录 |
|---|---|
| 来源 ID | `seedance-2.0` |
| 首次公开 / 阅读版本 | 2026 / `2604.14148v1` |
| 实际保存版本 | arXiv, 2026-04-15; model card / technical report |
| 链接 | [来源页](https://arxiv.org/abs/2604.14148v1) · [PDF URL](https://arxiv.org/pdf/2604.14148v1) · [arXiv 固定版本](https://arxiv.org/abs/2604.14148v1) |
| 页数 / 阅读位置 | 26 页；第 1–3、20–23 页 |
| 阅读进度 | 初步阅读；已核对部分原文，尚未完成全文精读和独立复现 |

## 要解决的问题与主要方法

官方模型卡说明四模态参考输入、原生音视频、镜头叙事、编辑与续写，并以多任务评测讨论可用性。适合研究产品能力、评价维度和生产工作流。

## 放在技术演进中怎样理解

主线材料。与其他工作的关系见 [视频生成专题](../../topics/video-generation/README.md)；涉及产品或组织的说法需同时查看 [结论与证据](../../topics/video-generation/claims.json)。

## 能支持的说明与局限

主要内容是能力与评测，未披露完整训练配方、200B 参数量或具体双分支结构。第 22 页也报告续写等任务上的不足，不应把整体优势扩写成每个子项都领先。

实验数据来自论文作者的设置，本仓库本轮没有重新训练或复测。对于闭源产品，没有披露的实现不能用相邻论文补齐为既定事实。

## 下一次阅读

- 精读上面标出的章节，补充方法输入/输出、训练数据、损失函数、基线和消融条件。
- 如需实现，先确定可获得的代码、权重、数据权限与计算资源，再建立独立实验目录。
- 新证据改变当前理解时，更新本页，并在 [研究纠错记录](../../research/2026-11-19-seedance/corrections.md) 说明影响。
