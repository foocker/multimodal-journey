---
status: draft
updated: 2026-11-22
source_ids: ["geometry-as-context"]
topic_ids: ["video-generation"]
---

# Geometry-as-Context：显式几何作为生成上下文

阅读版：CVPR 2026 出版方11页版本；arXiv编号2602.21929。重点读PDF pp.3–6，未复现。

## 方法与边界

传统重建—投影—修复链会把几何错误反馈到后续生成。该方法将RGB、几何和新视角生成组织为可学习的交错序列；选用 `{Ii, Geometry, Gi, Image, Ii+1}` 一类格式，任务提示区分生成几何还是图像。

PDF p.6 的camera gated attention让相机射线影响query残差与输出gate；geometry dropout减少上下文长度，也兼容无几何路径。训练基础为Bagel-7B、FLUX-VAE、RealEstate10K，而不是Wan/LTX。

这些支持“显式几何任务和相机条件能帮助场景一致性”的方法研究，不证明任意白模输入已经精确遵循，也不能将论文批评的某类不可微重建泛化成所有渲染器都不可微。

候选方案先用已知clay/depth/normal/pose/camera做条件，预测几何另设阶段。相机绕行再返回、物体出视野后恢复是关键测试，静态背景和动态主体分开记忆。正文见 [几何控制](../../topics/video-generation/seedance-2.5/geometry-control.md)。
