# 第一轮研究中间代码

这里保留 2026-11-19 查找、下载、校验与制作阅读目录时的三份脚本。只将原先个人工作目录替换成仓库内被忽略的 `.cache/legacy-seedance/`，未重构历史流程。

当前可维护的论文工具位于 [scripts/papers.py](../../../scripts/papers.py)。这些历史脚本保留的是探索过程，包含当时的固定日期、查询和文件布局，不作为主流程。

| 文件 | 当时用途 | 当前运行条件 |
|---|---|---|
| `01_download_initial.py` | 搜索截图报道、下载首批论文、转录与生成报告 | 依赖 requests、beautifulsoup4、PyMuPDF；报告 PDF 渲染使用 Windows 微软雅黑字体 |
| `02_download_supplement.py` | 发现补充论文、提取元数据、下载与逐页检查 | 先执行 discover / metadata，再 download；依赖同上 |
| `03_build_legacy_catalog.py` | 合并论文说明、生成历史网页与 ZIP | 需要前两份脚本输出及指定目录布局；额外依赖 Markdown |

下载、抽取和 ZIP 均输出本地缓存，无法直接生成当前仓库的规范目录。历史代码没有在新仓库完整重跑；当前首批内容从已完成的研究材料导入，并经过来源与链接检查。后续脚本逐步提炼到通用工具，不复制更多一次性路径假设。
