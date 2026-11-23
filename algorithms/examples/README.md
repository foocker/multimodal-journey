# 机制的极简代码

这些文件用于配合文章理解张量和依赖关系，每个只说明一件事。它们是独立编写的教学片段，不是 Seedance 实现，也不构成训练/生成框架。本轮未运行代码、训练或效果测试。

| 文件 | 说明的问题 | 刻意省略的部分 |
|---|---|---|
| [causal_conv.py](causal_conv.py) | 左 padding、dilation、stride 怎样保证时间因果 | 完整 VAE、decoder、归一化、chunk 缓存 |
| [flow_matching.py](flow_matching.py) | noisy/velocity、有效位置损失、Euler 更新 | 各基座 scheduler、CFG、分布 shift |
| [rope.py](rope.py) | 三轴如何切分并旋转 Q/K | checkpoint 特定频率、布局与跨镜头 offset |
| [attention_layout.py](attention_layout.py) | 空间/逐位置时间/窗口时空 reshape、MMDiT 拼接 | 完整 block、学习型投影、位置和任务 mask |
| [reference_adapter.py](reference_adapter.py) | query 如何按绑定读取参考，零门控的作用 | 编码器、token预算、无参考分支、训练 |
| [reference_timing.py](reference_timing.py) | 主体出场区间如何变成soft bias | 完整WeRoPE、缺席监督 |
| [local_edit.py](local_edit.py) | PTS 区间、latent 已知区覆盖、最终像素合成 | mask 生成、感受野扩张、遮挡/光照处理 |
| [condition_unit.py](condition_unit.py) | 源帧/参考/控制图与mask统一条件 | 完整adapter与任务训练 |
| [camera_rays.py](camera_rays.py) | 相机内外参与像素的Plücker射线 | 3D重建、标定、几何缓存 |
| [audio_video_exchange.py](audio_video_exchange.py) | 两分支双向读取更新前状态 | 音频 codec、时间对齐、门控和联合训练 |
| [preference_objectives.py](preference_objectives.py) | DPO、组内优势、截断目标的核心计算 | 策略采样、SDE logp、奖励和分布式训练 |
| [cache_context.py](cache_context.py) | 条件版本改变时缓存为何必须失效 | 完整 AR 注意力、缓存追加、滑动窗口 |
| [gated_condition.py](gated_condition.py) | 零门控如何把512维参考残差接入不同宽度的流 | 多头、原生调制、区域kernel、训练 |
| [condition_state.py](condition_state.py) | 逐token噪声状态、活动区Euler与干净条件保持 | codec边界、模态存在位、隐藏状态开关 |
| [block_causal_mask.py](block_causal_mask.py) | 两流self与双向AV的四种块因果关系 | block ID分配、padding、空模态与块稀疏kernel |
| [masked_sample_loss.py](masked_sample_loss.py) | FP32逐样本有效元素平均与缺失监督排除 | 分布式全局归约、梯度累积和任务采样 |

张量片段使用 PyTorch；没有为阅读示例引入训练环境要求。`cache_context.py` 只使用标准库。若要真实训练或推理，应从 [代码路线与仓库选择](../../docs/code-paths.md) 进入已核对的上游工程，按其环境、权重和参数说明操作。
