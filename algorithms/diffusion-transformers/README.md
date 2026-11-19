# 扩散 Transformer：从输入表示到预算

状态：初步学习说明。主要来源：[DiT](../../papers/2022/dit.md)、[Seaweed-7B](../../papers/2025/seaweed-7b.md)、[视频尺度定律](../../papers/2024/video-dit-scaling-laws.md)、[Seedance 1.0](../../papers/2025/seedance-1.0.md)。

常见路径是将图像或视频压缩为潜表示，再将潜表示分块为 token；扩散或流模型学习从噪声恢复条件内容，Transformer 负责处理 token 与条件之间的关系。具体噪声参数化、注意力结构、位置编码和训练任务依论文而定。

增加帧数、分辨率和上下文会改变 token 数与注意力成本；增加模型参数则改变每次网络求值的成本。推理还包含文本编码、VAE 解码、上采样、通信和调度，因此只计算 Transformer 前向不能等同端到端延迟。

## 待逐项推导

1. 确认论文使用的时间/空间压缩比例与 patch 大小，推导 token 数。
2. 明确使用全注意力、分解注意力还是稀疏注意力，估算哪些项随序列长度增长。
3. 区分网络求值次数 NFE、采样步数和 classifier-free guidance 的额外前向。
4. 阅读尺度定律中的计算预算、训练 token、学习率和 batch size 假设；只在其实验范围内解释拟合。
5. 用实际模型配置与设备测量验证理论估算；当前仓库没有执行这一步。

相关效率材料：[AdaSpa](../../papers/2025/adaspa.md)、[RayFlow](../../papers/2025/rayflow.md)、[Seaweed-APT](../../papers/2025/seaweed-apt.md)。方法可用性与某一闭源产品是否采用该方法需要分别说明。
