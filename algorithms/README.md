# 算法与方法

本目录按可复用的技术问题组织，避免为每个模型复制一套算法说明。

[极简代码目录](examples/README.md) 将机制落到张量操作；[真实工程路线](../docs/code-paths.md) 提供官方仓库、固定版本和具体源码入口。示例仅用于说明，未执行运行验证。

| 方法 | 当前内容 | 实现 / 实验 |
|---|---|---|
| [M01 因果视频 VAE](causal-video-vae/README.md) | 首帧、压缩率、因果卷积、解码与损失 | 解析索引探针；未跑真实 VAE |
| [M02 流匹配](flow-matching/README.md) | 时间方向、速度目标、条件/mask、CFG | 标量更新探针；未训练 |
| [M03 扩散 Transformer](diffusion-transformers/README.md) | MMDiT/reshape/复杂度、规模预算 | 连接/成本探针；未训练 |
| [M04 多模态位置](multimodal-position/README.md) | RoPE、坐标/归属/mask、布局风险 | 二维旋转探针 |
| [M05 联合音视频](audio-video-joint/README.md) | 候选双分支、物理时间、缺音轨 | 方案，未测同步 |
| [M06 长视频](long-video/README.md) | LCT/LongLive、异步噪声、cache依赖 | 依赖反例；未测真实缓存 |
| [M07 参考控制](reference-conditioning/README.md) | 素材绑定、Phantom与候选adapter、token预算 | 关联数据配方，未跑生成模型 |
| [M08 局部编辑](video-editing/README.md) | 区间/区域、感受野、保持/合成、白模/绿幕 | 候选接口与验收 |
| [M09 后训练](post-training/README.md) | Caption/PE/生成器/奖励，SFT/DPO/GRPO | 公式与停止条件，未训练 |
| [M10 推理优化](inference-optimization/README.md) | 计时、蒸馏/量化/缓存、质量预算 | 基准协议，未测延迟 |
| [交付成本演算](compute-budget/README.md) | 生成、审片、返工与交付成本的假设模型 | 有标准库实现与可复现演示 |

方法说明应指向原论文和具体实验。第三方实现采用外链；后续引入代码需记录 commit、许可证和实际改动。
