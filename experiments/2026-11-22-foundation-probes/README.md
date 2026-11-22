# 基础模块探针

状态：可运行的解析演示；执行记录见本轮 [研究日志](../../research/2026-11-22-seedance-foundations/journal.md)。输入为手工数字和索引，没有真实视频、权重、随机采样或外部服务。

```bash
python experiments/2026-11-22-foundation-probes/run.py
python experiments/2026-11-22-foundation-probes/run.py --check
```

Python 3.10+ 标准库即可，输出 [results.json](results.json)。结果为以下明确命题提供小例子：

| 探针 | 可检查的命题 | 不验证什么 |
|---|---|---|
| latent shape | 首帧公式、元素比、两种 patch 网格 | VAE 重建和 checkpoint 兼容性 |
| causal convolution | 含 stride/dilation 的前缀无未来依赖 | 真实 VAE 全网因果/归一化/chunk |
| RoPE | 固定内容向量同移坐标的点积不变 | 模型长上下文质量和 kernel 布局 |
| attention | 逐位置与窗口连接不同，复杂度乘数 | 真实 attention 权重、FLOPs/延迟 |
| flow | 固定时间约定下速度符号与 Euler 方向 | 实际 sampler 稳定性、低步数质量 |
| cache | prompt/timestep 变化可令因果缓存失效 | 真实缓存层输出等价与加速 |

脚本以断言检查预期关系，失败退出非零；可精确重复生成 JSON。输出不包含虚构训练、GPU 性能、生成效果或业务数据。
