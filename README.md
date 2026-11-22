# multimodal-journey

记录多模态技术从论文、算法、数据和实验走向产品与商业化的学习过程。以视频生成为第一个专题，后续扩展到图像、音频、视觉语言模型及其交叉方向。

这里保存持续修订的研究记录。模型输出可以作为初稿；结论需要标明来源、适用条件和未解决的问题。

## 从这里开始

- [Seedance 2.5：基础到落地，M00–M20](topics/video-generation/seedance-2.5/README.md)：基础、数据、训练、推理、业务、代码与完整候选方案。
- [代码路线与仓库选择](docs/code-paths.md)：12 份极简机制代码，10 个上游仓库的 11 份固定版本记录、44 个源码/配置入口。
- [视频生成专题](topics/video-generation/README.md)：技术演进、论文路线、证据与待核实问题。
- [论文索引](papers/README.md)：28 篇论文的 URL、版本、阅读笔记与证据定位。
- [第一轮研究日志](research/2026-11-19-seedance/README.md)：问题如何提出、查找过程、历史代码、初稿和纠错。
- [目录设计](docs/organization.md)：为什么这样组织，以及新内容应放在哪里。
- [工作流程](docs/workflow.md)：查资料 → 读论文 → 验证 → 实验 → 综述 → 修订。
- [应用与商业化](applications/video-production/README.md)：工作流、评测与成本问题。

## 目录

```text
sources/       来源登记：论文、项目页、产品文档、媒体线索
papers/        一篇论文一份笔记，按首次公开年份归档
topics/        跨论文的演进综述、时间线、结论与证据
algorithms/    按技术问题解释算法，链接论文和可执行实验
experiments/   每次实验的配置、代码、结果与复现说明
datasets/      数据定义、制作配方、样例、质量与权利记录
applications/  行业工作流、落地评测、成本与商业化分析
research/      按研究轮次保存过程：问题、输入、查找、初稿、纠错
templates/     新论文、研究轮次、实验、数据集和纠错模板
scripts/       可复用的下载、抽取、索引和仓库检查工具
docs/          仓库约定、目录取舍与后续计划
.cache/        本地 PDF、全文抽取、生成索引等，不进入 Git
```

**专题是阅读入口，论文是稳定对象，研究轮次记录过程。** 同一篇论文只维护一份当前笔记，各专题通过 ID 和链接引用；旧初稿保留在研究日志中。

论文 PDF、模型权重、原始数据和视频通过 URL 引用。论文登记记录固定版本、来源和校验信息；少量自有文本样例和可复现的小结果可以入库。

## 本地使用

文章离线阅读（包含公式渲染与内嵌插图）：

```bash
npm ci --ignore-scripts
npm run articles:build
```

打开 `.cache/reading/index.html`；每篇 HTML 可单独复制阅读，无需联网。[阅读与写作约定](docs/article-reading.md) 说明公式、插图和来源的维护方式。

核心检查和实验只依赖 Python 3.10+ 标准库。

```bash
python scripts/check_repo.py
python scripts/papers.py list
python scripts/papers.py download seedance-2.0
python experiments/2026-11-19-compute-budget/run.py
python experiments/2026-11-22-foundation-probes/run.py
```

如需抽取本地 PDF 全文或校验新的训练数据格式：

```bash
python -m pip install -r requirements.txt
python scripts/papers.py extract seedance-2.0
python scripts/training_data.py datasets/recipes/audio-video-production/example-records.jsonl
```

PDF 默认保存在 `.cache/papers/`；目录可通过 `--cache-dir` 指定。下载不改变笔记的阅读或审核状态。

## 怎样持续积累

1. 把新论文登记到 [sources/papers.json](sources/papers.json)，按 [论文模板](templates/paper.md) 建立笔记。
2. 为具体问题开一个 `research/YYYY-MM-DD-slug/` 研究轮次，记录检索词、取舍和失败路径。
3. 把跨论文结论汇总到 `topics/`；重要结论记录来源版本、页码和证据强度。
4. 将代码、数据配方、实际运行记录分别放进 `algorithms/`、`experiments/`、`datasets/`。
5. 发现错误时修改当前文档，在研究轮次的纠错记录中说明依据，再由 Git 保存历史。

文档默认为 `draft`。`reviewed` 需要明确的审核人、审核范围和日期；工具校验通过只表示结构或文件检查通过。

## 当前进度

28 篇论文已登记。21 篇独立文章使用 `$`/`$$` 公式、论文裁图和离线阅读环境，覆盖基础、代码选型与完整候选方案；研究定位与纠错留在独立记录。代码层补充 12 份极简机制片段，并为 10 个上游仓库登记 11 份固定版本、44 个源码/配置入口；按用户要求未运行这些教学片段。

各块仍为 draft，待 [逐块审核](topics/video-generation/seedance-2.5/review.md)。完整联合方案已选定共同主干、参考/编辑/几何接口及训练课程，见 [候选架构](topics/video-generation/seedance-2.5/integrated-design.md) 与 [训练配方](topics/video-generation/seedance-2.5/integrated-training.md)。尚无真实模型训练、推理性能实测或业务试验结果；本次补充见 [关键设计研究](research/2026-11-22-key-design/README.md)。

后续优先任务见 [路线图](docs/roadmap.md)。
