# 2026-11-22：依据现有论文补齐关键设计

用户指出 `downloads/曾妍_Seedance_论文与报道` 中还有论文，并授权缺少材料时自行检索下载。本轮承接其独立文章、美元公式、论文裁图、极简代码/真实仓库且不运行代码的要求。

## 本地材料与新增来源

先按内容hash盘点整个目录，见 [paper-inventory.json](paper-inventory.json)。发现当前知识库尚未纳入的 AlcheMinT、Geometry-as-Context、VideoCoF；重新读取已登记的 VINCIE-NExT、LCT、Phantom 和 LongLive，补查其它本地阅读包中的 LTX-2。

新下载 VACE v2，并按出版方URL取得三篇新纳入论文的CVPR版、按固定版本取得LTX-2 v1。选定阅读版保存在用户目录的 `design-supplement-20261122/`，含URL/hash清单；仓库内PDF仍只进缓存。来源共增五篇，当前28篇。

## 当前产出

- [多参考与时间控制](../../topics/video-generation/seedance-2.5/reference-timeline.md)：资产/主体/角色/时间绑定、token预算、区间门与数据监督。
- [统一编辑条件](../../topics/video-generation/seedance-2.5/editing-conditions.md)：reactive/inactive、源条件、区域中间表示、图像编辑示例传播。
- [几何控制](../../topics/video-generation/seedance-2.5/geometry-control.md)：已知白模、Plücker相机、带置信度记忆与重访测试。
- [完整候选架构](../../topics/video-generation/seedance-2.5/integrated-design.md)：选定LTX-2原系列共同基座，逐项分清保留和新增，联合/因果版本分开。
- [完整训练配方](../../topics/video-generation/seedance-2.5/integrated-training.md)：数据池、有效loss、候选混合比例、阶段出口与资源量级。
- [设计规格](../../topics/video-generation/seedance-2.5/design-spec.json)：便于逐项审核，非实际训练配置或实测结果。

三份新增教学代码只展示时间门、统一条件与相机射线。原系列LTX、VACE和VideoCoF源码入口分别固定commit，未导入上游实现、未执行。

## 关键证据定位

| 来源 | 实际阅读范围 | 用于什么、不支持什么 |
|---|---|---|
| AlcheMinT CVPR版 | PDF pp.4–5，binding/data与WeRoPE | 支持主体/描述绑定和区间监督；equation5数学歧义单列，不照抄 |
| Geometry-as-Context CVPR版 | pp.3–6，公式/变体/CGA/训练 | 支持几何交错与相机条件思路；基座为Bagel，不是LTX插件 |
| VideoCoF CVPR版 | pp.3–5，concat/噪声/位置/loss/data | 支持区域中间表示；原算法联合reason/target去噪，不是本文显式两阶段 |
| VACE v2 | pp.3–5，VCU/拆分/embedder/adapter | 提供明确的视觉条件接口；不自动解决音频参考和LTX迁移 |
| LTX-2 v1 | pp.4–8，AV块/文本/codec/CFG | 支持已披露联合主干，不能套后来型号 |
| VINCIE-NExT v1 | pp.4–6，分解/联合任务/位置/推理 | 支持V→I→I→V与异构数据；不是同一个VideoCoF算法 |
| LTX原系列代码 | types.py、video_vae.py、configurator、AV/IC-LoRA配置 | 核对/8、/32、128通道、音频8×16和默认block配置，实例以checkpoint配置为准 |

详细固定版本、hash、来源URL在来源登记和代码登记中。正文不含这类碎片定位。

## 已作出的设计选择

Wan保留为轻量机制/单能力验证路线，LTX原系列用于完整候选设计。共同表示解决“随意拼Wan与音频模型”的缺口；参考、编辑与结构adapter仍是新增工作。论文证据支持局部机制，跨方法组合的有效性尚待实际研究，不写成已复现。

因果续写从联合模型另派生，所有AV边也遵守块间因果；没有完成训练前不声称支持精确KV缓存。首版时间控制保留主干RoPE，使用单独reference支路soft bias；白模先走已知结构条件，预测几何另设任务。

## 验证边界

本轮未运行教学代码、模型、训练或GPU基准，未下载权重。仅做来源核对、公式/设计审读、论文图裁剪与阅读版构建、仓库结构检查。

实际完成的检查：

- `python scripts/check_repo.py`：28篇论文、18项其它来源，JSON、source_ids、本地链接和文件边界通过。
- `npm run articles:build`：21篇独立离线HTML，189处行内/块级公式、16处插图使用。
- Chrome无头文档检查：21篇分别在1280px、390px宽度断网读取，公式数、字体、图片、横向页面溢出、外部资源请求与浏览器错误均通过。新增M16–M20截图与修正后的几何裁图已目视检查。
- 五篇PDF的缓存与用户目录副本均核对SHA-256，与来源登记及裁图manifest一致。
- `git diff --check`通过；暂存区为空，未提交或推送。

渲染/截图结果在本地 `.cache/reading/`，布局检查脚本在 `.cache/qa_key_design.cjs`；它只读取HTML，不导入机制片段或模型。源码/文档的结构与渲染通过不改变各篇draft状态，也不构成组合方案效果验证。
