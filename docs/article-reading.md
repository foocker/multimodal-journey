# 独立文章的编写与阅读

文章目录由 [articles.json](../articles.json) 登记，Markdown 为唯一正文。M00–M20 是目录编号，不写入单篇标题；每篇自行定义术语、符号、例子和适用条件，不依赖上一节才能读懂。

## 公式和来源

行内公式用 `$...$`，独立公式用单独两行 `$$`。反引号保留给代码、字段名和实际接口形状。正文不出现 PDF 页码、章节号、Figure 编号、摘录纠正过程或“原文这里指出”的碎片化引用；只保留 `source_ids` 元数据。

论文版本、证据定位和纠错继续在 `sources/`、`papers/`、`research/` 维护。精简文章引用不会把候选架构变成官方事实；必要的适用条件仍用自然叙述表达。

## 插图

论文裁图保存在 [assets/paper-figures](../assets/paper-figures/manifest.json)，manifest 记录来源 ID、固定 PDF 哈希、页序、裁剪坐标和输出路径。只裁需要的图，完整保留图中结构和语义，不夹带半行图注，也不以整页截图代替插图。

固定 PDF 下载到 `.cache/papers/` 后，可重做裁图：

```bash
python scripts/crop_paper_figures.py
```

当前插图用于用户要求的学习文章，不代表获得论文全文、代码、权重或全部素材的再分发许可。

## 离线阅读环境

```bash
npm ci --ignore-scripts
npm run articles:build
```

打开 `.cache/reading/index.html`。每篇输出独立 HTML，已经渲染数学公式，并内嵌所用图片、KaTeX 字体与样式；无需启动服务、联网或依赖旁边的资源目录。可以单独复制任意 `m00.html` 至 `m20.html` 阅读。文章中的本地 Python/JSON 链接内嵌为下载，源码可随文章取得；跨文章导航在同一输出目录使用，真实仓库链接需联网。

默认输出为本地缓存，不进入 Git；在新机器上用相同命令重建。需要指定输出目录：

```bash
node scripts/build_articles.mjs --out .cache/reading-export
```

生成器会拒绝错误公式、遗留的非美元数学定界符、缺失图片和未内嵌字体。`build-report.json` 记录每篇公式与插图数量，但不代表内容经过科学复现。

渲染依赖固定为 markdown-it 14.1.0、markdown-it-texmath 1.0.0、KaTeX 0.16.22，均为 MIT；固定依赖树见 `package-lock.json`。依赖由 npm 安装，不把第三方实现复制进源码目录；生成 HTML 中保留相应许可证文本。
