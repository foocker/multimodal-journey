# 研究与验证日志

## 输入与查找

2026-11-22 读取仓库约定、首轮研究、来源/结论、用户摘录全部模块及重复尾段。先从已下载的固定版 PDF 抽取文本，核对 16 份现有 PDF 的 SHA-256 与登记一致；按问题定点阅读，不将“抽取全文”记为“精读全文”。

直接访问 Seed 官方产品页与 sitemap，找到 2.5 正式发布正文。最初猜测的 `/en/blog/seedance-2-5` 虽 HTTP 200，但只有空壳标题，未用作证据；sitemap 给出的完整正式 URL 才用于登记。Tarsier2 编号以 Seedance 1.0 参考文献 [32] 和作者仓库交叉定位，不使用题目不符的候选 arXiv 页面。

新增下载 MAGVIT-v2 v3、RoPE v1、Tarsier2 v1、LongLive v2；Wan v2 从已有本地阅读包核对。版本/页数/bytes/hash/阅读范围见 [source-checks.json](source-checks.json)。论文与网页全文均只进 `.cache/`，未加入 Git。

视觉核查 Seedance 1.0 v2 PDF p.5 Figure 2，确认 Spatial Attention 的双模态输出与 Temporal 的 spatial-temporal 标注；核查 1.5 Pro v3 p.2 Figure 2，确认它是训练/推理总流程，不能从图里补出 joint module 的层级公式。其余重点文本定位记录在当前论文笔记与模块内。

## 方案决定

将输入拆成 M00–M14。基础说明只维护在 algorithms，2.5 专题连接证据、候选架构、训练与审核；数据/业务各归原目录。所有块仍为 draft，未由模型自授 reviewed。

候选研究基座是 Wan-2.1 T2V-1.3B，保留 VAE/patch/text 接口；不把多篇不同模型的模块直接宣称为兼容实现。API 接入与自训分轨，原生长上下文、联合音频、RL/蒸馏分阶段准入。

## 实际执行的验证

已运行：

```bash
python scripts/papers.py index
python experiments/2026-11-22-foundation-probes/run.py
python scripts/training_data.py datasets/recipes/audio-video-production/example-records.jsonl
python -m unittest discover -s scripts/tests -v
```

结果：23 篇论文索引生成；6 组解析探针通过并保存结果；3 条格式样例通过 metadata 校验；首轮工具＋新增数据完整性测试共 14 项通过。生产模式拒绝格式样例、检查参考权利，以及内容 hash 捕获重新标记的重复等路径均由测试覆盖。

CI 增加 schema 校验依赖、格式样例检查、探针 `--check`。首次运行该检查模式发现 Python tuple 与 JSON array 的类型差异导致错误比较，已将运行结果先标准化为 JSON 数据结构；RoPE 浮点值允许跨平台 libm 的 1e-12 绝对容差，其余结构/整数精确比较。

最终 `python scripts/check_repo.py` 通过：23 篇论文、8 项其他来源、JSON/引用/本地链接/文件范围；`git diff --check` 通过，暂存区为空，PDF/全文/网页快照都未进入版本控制。原始摘录 hash 与入轮记录一致。结构检查只验证结构，单元测试只验证工具行为；它们不是科学正确性或训练效果证明。

## 未执行与下一次工作

没有下载 checkpoint、运行真实生成、制作真实训练数据、训练模型、测 GPU/API 延迟、做客户试验或提交/推送远端。当前机器的 Python 环境没有 torch；本轮解析工具用标准库，PDF 用 PyMuPDF，数据 schema 用 jsonschema，无需为文档工作安装训练框架。

先按 M00/M01 的验收题逐块修订，再进入 T0 的 checkpoint/许可/硬件准入。尚缺物料和资源的部分在各块明确标为计划，不能将格式演示当作落地验证。

## 按独立文章要求改写

用户进一步明确：文章应直接吸收资料，每篇独立讲清一个问题；公式使用 `$`/`$$`，正文只需 `source_ids`，不需要 PDF 页码、章节、Figure 编号与摘录修正过程；需要图时从原论文裁切。

据此重写 M00–M14 正文，去掉模块前置、跨篇依赖、逐条定位和研究自述。概念、符号、例子、适用条件与验证方法保留在正文；事实定位、纠错、审核问题继续在研究层维护。原始用户摘录保持不变。

新增论文插图与裁剪 manifest，记录固定 PDF hash、页序、坐标，使用 PyMuPDF 重做并视觉检查。新增固定版本 Markdown/KaTeX 渲染器，将 15 篇文章生成为单文件离线 HTML，图片与公式字体均内嵌；渲染 146 处公式、11 处插图。

用本机 Chrome headless 在断网环境检查全部 15 篇、1280px 与 390px 两种宽度：无公式错误、断图、页面横向溢出、外部网络请求或控制台异常。检查中发现字体 CSS 的空白导致初版未内嵌，已修复并加入构建拒绝条件；重跑通过。实际查看 VAE 公式、DiT 插图与移动页面截图，确认显示正常。生成结果与视觉记录在 `.cache/reading/`，从源码可重做；未进行真实模型训练或推理测试。
