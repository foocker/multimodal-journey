# 目录设计与维护边界

## 按对象分工，以专题连接

本仓库同时回答两个问题：“现在理解到哪里了”和“这些理解是怎样形成的”。当前结论放专题与论文笔记；过程放研究轮次。代码和数据也有自己的复现边界。

| 目录 | 保存什么 | 典型文件 | 更新方式 |
|---|---|---|---|
| `sources/` | 来源身份与固定版本；论文和非论文资料 | `papers.json`、`web.json` | 同一来源更新条目，保留实际读过的版本 |
| `papers/` | 单篇论文的当前理解、证据、局限 | `2025/seaweed-7b.md` | 原地修订，用 Git 和纠错记录追踪变化 |
| `topics/` | 跨论文综述、时间线、结论与开放问题 | `video-generation/evolution.md` | 新论文可能改变既有关系，需同步修订 |
| `algorithms/` | 方法原理、伪代码、实现入口 | `diffusion-transformers/README.md` | 以方法为单位，引用来源与实验 |
| `experiments/` | 可复现的代码、参数、小结果与解释 | `YYYY-MM-DD-slug/` | 新实验新目录；同一实验记录不同配置或 run ID |
| `datasets/` | 数据规格、制作步骤、样例、质量规则 | `recipes/multishot-reference/` | 修改规格时记录版本，原始数据外置 |
| `applications/` | 客户问题、工作流、评测、单位经济模型 | `video-production/` | 产品能力、技术事实、商业假设分别标明 |
| `research/` | 一轮探索的原始输入、日志、初稿、纠错 | `2026-11-19-seedance/` | 过程只补充必要记录，避免每天复制整个知识库 |
| `templates/` | 新条目模板 | `paper.md`、`experiment.md` | 模板不代表任务已完成 |
| `scripts/` | 多轮研究都能使用的工具 | `papers.py`、`check_repo.py` | 保持便携，用实际数据验证行为 |
| `docs/` | 仓库约定与演进决策 | 本文、`workflow.md` | 结构改变时说明迁移原因 |

顶层按对象类型固定，专题数量增长时扩展 `topics/`；模型品牌变多时无需在顶层新增厂商目录。论文按首次公开年份放置，会议年份在元数据另记。

## 一个具体问题如何流转

以“多镜头一致性怎样进入可用产品”为例：

```text
sources/papers.json                       来源与版本
       ↓
papers/2025/long-context-tuning.md          论文笔记
       ↓
topics/video-generation/claims.json        带证据范围的结论
       ↓
topics/video-generation/evolution.md       跨论文解释
       ↓
datasets/recipes/multishot-reference/       数据制作规格
       ↓
experiments/<date>-<question>/             可验证的运行
       ↓
applications/video-production/             工作流、可用率与成本
```

`research/<round>/` 记录这条路径中的疑问、输入、查找和纠错。任何环节都可以返回上游；缺少实验时就标记缺少，不补造结果。

## 稳定 ID、链接与单一维护位置

- 论文 ID：`seedance-1.0`、`seaweed-7b`。模型版本本身有意义，ID 可以包含版本号。
- 论文版本：`arxiv_version` 固定实际阅读版本，`pdf_url` 使用固定版本 URL；会议版另记 `edition` 与出版方 URL。
- 研究轮次：`YYYY-MM-DD-question-slug`，通常围绕一个问题而不是一天的全部工作。
- 结论 ID：专题内使用 `VG-001` 等稳定编号。文章、纠错和实验可引用同一个编号。
- 论文和非论文来源 ID 都在 `sources/` 登记；代码仓库链接属于资料入口，若要引入代码还需记录 commit 与许可证。
- 每篇论文只保留一份当前笔记。专题不复制整篇解析，而是引用它并解释关系。

## 草稿、确认与撤回

文档状态使用 `draft`、`reviewed`、`superseded`。这是文档的审核状态，与结论证据状态不同。

结论状态使用：

| 状态 | 含义 |
|---|---|
| `supported` | 已定位到直接支持该表述的材料；实验结果仍受作者设置限制 |
| `partially_supported` | 部分成立，当前文字需缩小范围或补充证据 |
| `unverified` | 当前材料不足，待查；不能解读为“已证伪” |
| `contradicted` | 有明确相反证据，并记录冲突的具体范围 |
| `withdrawn` | 因错误或不再适用撤回，保留理由与替代结论 |

首批笔记均为模型辅助整理的 `draft`。`supported` 只表示原文能支持特定命题，不等于人工审核、独立复现或对整篇论文的担保。

## PDF、数据与中间文件

独立文章只显示 `source_ids`，不显示细粒度页码/章节/图号；定位继续保留在研究层。文章由 [目录](../articles.json) 连接，遵循 [独立文章约定](article-reading.md)，避免把研究札记直接作为成文输出。

用户要求的必要论文裁图可保存在 `assets/paper-figures/`，由 manifest 记录来源和可重做的裁剪参数；PDF 和整篇全文仍放缓存。离线文章 HTML 由源码生成到 `.cache/reading/`，不形成第二份需要手工维护的正文。

PDF 在 `sources/papers.json` 中保留 URL、版本、SHA-256、页数和检查日期；可通过脚本下载到 `.cache/`。不提交 PDF、模型权重、大型数据集或视频。

小型 JSON 配置、手工构造的教学数据、标注规范、清洗脚本和汇总结果可以提交。原始数据、全文抽取、临时搜索页面、批量输出通过 manifest 或研究日志记录来源和处理步骤。

第一轮历史脚本保留在研究轮次，其输出隔离到 `.cache/legacy-seedance/`。后续维护以 `scripts/` 的通用工具为入口。这样既保留研究过程，也避免历史脚本成为主流程依赖。

## 暂时采用的约定

2026-11-22 增加 `topics/video-generation/seedance-2.5/` 作为 M00–M20 的学习/设计/审核入口。通用基础仍只放 `algorithms/`，数据配方/业务方案沿用各自目录，避免按品牌复制全部知识。Wan 轻量路线与 LTX 原系列联合候选方案各自保留表示和训练边界；新的 training record schema 面向单任务样本，与旧的多镜头 scene schema 并存，互不静默升级。

来源目录以 JSON 为准，Markdown 索引由工具生成。当前不引入数据库、专用知识库服务或自动论文打分；等实际检索、协作规模产生需要时再调整。结构变更写进本文件，并保持旧链接可追溯。

代码说明采用两层：`algorithms/examples/` 放独立编写的机制片段，`sources/code.json` 记录上游工程固定 commit、许可证和入口。代码路线文章连接两者；第三方源码只在缓存中阅读，不为了配套文章复制一套训练框架。默认不为教学片段进行运行验证，按用户当前要求维护。
