# 算法与方法

本目录按可复用的技术问题组织，避免为每个模型复制一套算法说明。

| 方法 | 当前内容 | 实现 / 实验 |
|---|---|---|
| [扩散 Transformer 与尺度问题](diffusion-transformers/README.md) | 表示、条件、计算成本和阅读问题 | 尚未实现模型训练 |
| [参考控制与上下文](reference-conditioning/README.md) | LCT、Phantom、VINCIE 系列的任务边界 | 关联数据配方，尚未跑生成模型 |
| [交付成本演算](compute-budget/README.md) | 生成、审片、返工与交付成本的假设模型 | 有标准库实现与可复现演示 |

方法说明应指向原论文和具体实验。第三方实现采用外链；后续引入代码需记录 commit、许可证和实际改动。
