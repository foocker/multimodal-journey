# Historical session script; see this directory README before running.
from __future__ import annotations

import hashlib
import html
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote

import bs4
import markdown
import pymupdf

ROOT = Path(__file__).resolve().parents[3] / '.cache' / 'legacy-seedance'
BASE = ROOT / 'downloads' / '曾妍_Seedance_论文与报道'
OUT = BASE / '补充论文_技术演进与业务落地'
WORK = ROOT / 'tmp' / 'seedance_supplement_research_20261119'
manifest = json.loads((OUT / '论文来源与校验.json').read_text(encoding='utf-8'))
papers = {paper['key']: paper for paper in manifest['papers']}


DETAILS = {
    '05': ('Seaweed-7B', '主线必读', '2025', '第 1–2、5、14–19 页', '补上 Seaweed 这一条研究路线。7B、665,000 H100 GPU 小时、VAE/DiT、数据管线和下游适配均有公开说明；第 17 页还有端到端推理比较。', '论文明确把 7B 定位为中等规模、兼顾部署成本的研究模型。它不能单独证明 2024 年内部赛马安排、后续组织合并或模型权重开源。'),
    '06': ('Seedance 1.0', '主线必读', '2025', '第 4–8、11–13 页', '把多镜头能力、数据处理、训练、RLHF、蒸馏与系统优化连起来看。第 4 页明确写位置编码设计 following Seaweed and LCT；第 12 页写量化、稀疏和 RayFlow。', '第 1 页的速度是 NVIDIA L20 上用 41.4 秒生成一段 5 秒、1080p 视频，不能写成 5 秒完成生成。技术引用支持设计承接，不能据此断言两套模型做过权重合并。'),
    '07': ('Seedance 1.5 Pro', '主线必读', '2025', '第 1–2 页；其余按评测需要查阅', '音视频联合生成的直接官方材料：双分支 DiT、跨模态交互、音画数据管线、SFT/RLHF 与超过 10 倍的推理加速概述；首页也说明火山引擎可访问。', '双分支 DiT 在这一代已经公开。报告对部分训练细节着墨较少，不宜补写成完整的内部训练配方。'),
    '08': ('DiT', '基础选读', '2022 / ICCV 2023', '第 1–5 页', 'Scalable Diffusion Models with Transformers：理解从 U-Net 到 Transformer，以及模型深度、宽度、token 数和计算量怎样影响效果。', '原始实验是图像生成；这篇提供扩展性的基础，不能用来证明 Seedance 2.0 的具体参数规模。'),
    '09': ('DanceGRPO', '主线必读', '2025', '第 1、3–6 页', '解释生成模型如何用组内相对奖励做后训练，结合运动、审美和文本对齐等多种奖励；Seedance 1.0、1.5 Pro 和 2.0 报告均列有该研究的引用。', '有研究联系和方法依据；论文没有证明某一产品的点赞、重绘、导出事件具体如何进入训练。'),
    '10': ('RewardDance', '主线必读', '2025', '第 1、3–9 页', '解释反馈闭环中的“谁来判好坏”：生成式奖励建模、奖励模型扩展与 reward hacking。论文直接报告 Seedance-1.0 上的实验，并讨论奖励模型扩展到 26B。', '这里的 26B 是奖励模型规模，不是 Seedance 生成器的参数量。实验中的效果和奖励鲁棒性应保留论文条件。'),
    '11': ('Seaweed-APT', '工程选读', '2025 / ICML 2025', '第 1–4 页及第 15 页附录 E', '正式标题 Diffusion Adversarial Post-Training for One-Step Video Generation。看对抗后训练怎样让视频生成走向单步，理解降低去噪步数与保真之间的取舍。', '“实时”必须带硬件条件：第 15 页报告 1 张 H100 的完整流程为 6.03 秒；8 张 H100 并行才实现该配置下的端到端实时。不能当作 Seedance 线上实际配方。'),
    '12': ('AdaSpa', '工程选读', '2025', '第 1、3–9 页', '正式标题 Training-free and Adaptive Sparse Attention for Efficient Long Video Generation。拆解长视频 attention 的成本，以及分块稀疏、动态搜索和跨去噪步复用。Seedance 1.0 的第 12–13 页引用该研究。', '提供稀疏注意力的具体方法和相关技术出处；其公开实验不能直接替代 Seedance 生产环境的测量。'),
    '13': ('VINCIE', '可控编辑选读', '2025 / ICLR 2026', '第 1–7 页', '从视频天然变化中构造交错图文编辑序列，学习多轮图像编辑。与已下载的 VINCIE-NExT 对照，可以讲清图像与视频编辑能力如何相互迁移。', '方向需要分清：VINCIE 主要是“视频数据 → 图像编辑”；VINCIE-NExT 主要是“图像编辑 → 视频编辑”。两者都不能单独证明 Seedance 内部直接采用同一实现。'),
    '14': ('LoRA', '基础选读', '2021 / ICLR 2022', '第 1、3–5 页', 'Low-Rank Adaptation of Large Language Models：理解冻结大模型、只训练低秩更新，为什么能减少客户定制的训练与存储开销。可搭配 Seaweed 第 17–19 页看视频适配。', '原论文研究语言模型。Seaweed 报告有 LoRA 适配的讨论，Seedance 1.0 第 6 页则是提示改写模型使用 LoRA；这些都不能证明火山引擎已开放某个 Seedance 视频 LoRA 训练服务。'),
    '15': ('Long Context Tuning', '主线必读', '2025', '第 1、4–8 页', '把单镜头模型扩展到场景级：场景与分镜数据、交错位置编码、异步加噪，以及 KV-cache 支持的自回归镜头续写。直接回答多镜头故事为何需要训练设计。', '这是 Seaweed 相关研究，且被 Seedance 1.0 的模型设计部分明确引用；不等于独立证明组织合并。'),
    '16': ('Phantom', '主线必读', '2025', '第 1、3–7 页', 'Subject-consistent video generation via cross-modal alignment：参考图中的人物、服装、物品如何进入生成过程，怎样减少图像内容泄漏和多主体混淆。Seaweed 报告将其列为主体一致性下游研究。', '支持参考图控制与主体保持的技术逻辑；不能直接写成 Seedance 2.0 的具体控制模块。'),
    '17': ('视频 DiT 尺度定律', '主线必读', '2024 / CVPR 2025', '第 1–8 页，尤其第 5、7 页', 'Towards Precise Scaling Laws for Video Diffusion Transformers：同时考虑参数量、训练 token、计算预算、学习率和 batch size，而不是只谈“模型越大越好”。', '来自快手等机构，是跨团队的对照研究。文中尺度实验和外推主要到约 1B 级；它不能验证 Seedance 的 200B 传闻。'),
    '18': ('RayFlow', '工程选读', '2025 / CVPR 2025', '第 1、3–7 页', 'Instance-Aware Diffusion Acceleration via Adaptive Flow Trajectories：解释低步数生成时的轨迹与蒸馏。Seedance 1.0 第 12 页明确写采用 RayFlow 的 Score Distillation；1.5 Pro 也引用它。', '原论文主要做图像实验。和 Seedance 官方报告一起读，才能区分原方法的实验与视频系统对它的使用。'),
}


def paper_link(key):
    paper = papers[key]
    return f"[{DETAILS[key][0]}]({paper['filename']})"


def group_table(keys):
    rows = ['| 论文 / 公开时间 | 要解决的工程问题 | 建议阅读 |', '|---|---|---|']
    for key in keys:
        short, priority, year, pages, why, limit = DETAILS[key]
        rows.append(f"| **{paper_link(key)}**<br>{year}；{papers[key]['page_count']} 页 | {why} | {pages} |")
    return '\n'.join(rows)


guide = '''# 技术演进与业务落地：补充论文及证据指南

整理日期：2026-11-19。新增 **14 篇论文 PDF**，加上上层目录原有的 4 篇，共 18 篇。页码均指本次保存 PDF 的页序，包含首页、目录和附录。论文年份以首次公开或列明的会议年份为准；下载版本另见完整目录。

这份材料围绕“视频底座与数据 → 多镜头 → 原生音视频 → 后训练与效率 → 参考和编辑”建立技术主线。组织调整、产品上线和具体商业收入，需要与对应的官方发布、组织公告或可核实的采访结合。

## 1. 先读这 8 篇

**Seaweed-7B → Seedance 1.0 → Long Context Tuning → Phantom → Seedance 1.5 Pro → 视频 DiT 尺度定律 → DanceGRPO → RewardDance。**

再回到原有的 [Seedance 2.0 报告](../03_Seedance_2.0_2604.14148v1.pdf) 和 [VINCIE-NExT](../04_VINCIE-NExT_NeurIPS2026_2610.12104v1.pdf)，就能把产品能力与前面的工程问题对应起来。深入推理成本时再读 RayFlow、AdaSpa、Seaweed-APT；讲定制与编辑时补 LoRA、VINCIE。

## 2. 底座、训练成本与产品化

''' + group_table(['05', '06', '07']) + '''

Seaweed-7B 的价值在于展示“有限预算下怎样安排模型、数据、训练和部署”。其报告称 7B 为中等规模，并披露 665,000 H100 GPU 小时的训练成本；这与只沿参数量扩张讲故事的视角不同。

Seedance 1.0 第 4 页明确承接 Seaweed 和 LCT 的 MM-RoPE 设计；第 6–8 页讲数据处理和基础设施，第 11–13 页讲 RLHF 与推理优化。这些是公开可核对的技术联系。

## 3. 从单镜头到参考可控、多镜头叙事

''' + group_table(['15', '16', '13']) + '''

LCT 处理镜头间的上下文；Phantom 处理主体参考与文本指令的对齐；VINCIE 和 VINCIE-NExT 则处理编辑数据如何构造、如何跨图像与视频迁移。这几类任务相互关联，但各自有不同的训练目标和数据要求。

## 4. 从反馈到可用率：策略优化与奖励模型

''' + group_table(['09', '10']) + '''

Seedance 1.0 第 11 页写得较明确：从训练集和线上用户收集提示词，筛选、平衡后生成视频对，再进行人工偏好标注。这能支撑“线上需求参与反馈训练”的表述。点赞、重绘、导出等事件是否直接作为某一代模型的训练信号，公开报告没有在这里给出对应证据。

## 5. 推理成本：少步采样、稀疏注意力与并行

''' + group_table(['18', '12', '11']) + '''

Seedance 1.0 第 12 页明确提到借鉴 RayFlow 的 Score Distillation，并分别讨论量化和稀疏；同页到下一页的系统优化引用 AdaSpa。Seaweed-APT 则提供另一条少步视频生成研究路线。讲商业落地时，应把模型效果、单位生成成本和交付延迟共同考虑，并保留硬件、时长、分辨率等实验条件。

## 6. 规模与客户定制：基础材料

''' + group_table(['17', '08', '14']) + '''

尺度定律论文最适合支撑的问题是：在固定训练预算下，模型容量、数据量和超参数怎样搭配；部署时是否值得用更小模型换取更低推理成本。它不能证明一家公司的未公开参数配置。

## 7. 对现有叙事的事实核对

| 现有表述 | 论文能够支持到哪里 | 建议写法 |
|---|---|---|
| 2024 年 PixelDance 与 Seaweed 内部双线赛马 | 两条研究路线各有公开材料；本次论文不直接记录 2024 年发布会安排与内部决策 | 讲研究路线并行；具体产品发布与内部赛马另引官方发布记录或可靠采访 |
| 2025 年 4 月组织合并，随后两套架构“大合并” | Seedance 1.0 第 4 页明确引用 Seaweed 与 LCT 的位置编码设计 | 写“可确认存在技术设计承接”；组织合并、完整架构融合与权重合并分别需要证据 |
| Seedance 1.0 约 5 秒生成完成 | 第 1 页是用 41.4 秒生成 **5 秒时长**、1080p 视频，硬件为 NVIDIA L20 | 区分成片时长与推理耗时 |
| 到 Seedance 2.0 才采用双分支 DiT | 1.5 Pro 的摘要已明确写 dual-branch Diffusion Transformer | 将原生音视频和双分支结构的公开证据放在 1.5 Pro 阶段；2.0 的具体内部结构按其披露范围表述 |
| Seedance 2.0 已公开证实为 200B | 本次核查的官方 26 页报告没有披露 200B 参数配置 | 将 200B 保留为待核实说法；尺度定律论文用来解释决策问题，不能充当参数量证据 |
| 四模态输入代表已公开全部四模态联合训练细节 | 2.0 第 1–2 页直接支持文本、图像、音频、视频参考输入和音视频输出能力 | 讲可确认的输入、输出和控制能力；不据此补写未披露的训练分布与结构 |
| 海量点赞、重绘、导出直接用于 RLHF/DPO | 1.0 第 11 页支持线上提示词及人工偏好标注；未在此披露这些具体事件的用法 | 讲“线上提示需求 + 偏好标注 + 奖励优化”的公开流程 |
| 火山引擎已提供 Seedance 视频 LoRA 微调 | Seaweed 报告讨论 LoRA 适配；1.0 提示改写模型也使用 LoRA；1.5 Pro 报告确认火山引擎访问 | “LoRA 技术可用于低成本适配”和“具体商业训练接口已开放”分别核实 |
| Seaweed-7B 论文公开等于模型权重开源 | 本次确认的是报告与项目展示；没有据此确认权重发布状态 | 写“公开报告的 Seaweed-7B”，不要直接写“开源 Seaweed-7B” |
| VINCIE-NExT 的论文证明 Seedance 2.0 内部使用该方法 | 两者都讨论编辑与参考能力；本次没有找到直接实现对应的证据 | 将其作为相关编辑研究与数据迁移方法来介绍 |

## 8. 适合科普视频的可核对主线

**一段视频的可用性，需要同时解决五件事：算得起、镜头连得上、声音对得齐、参考改得准、反馈能改善结果。**

1. 用 PixelDance 与 Seaweed 展开不同的技术探索；Seaweed 给出训练预算、部署成本和多类下游适配的公开讨论。
2. 用 Seedance 1.0、LCT 解释多镜头、数据管线、奖励训练和系统效率怎样一起推动可用性。
3. 用 Seedance 1.5 Pro 解释原生音视频联合建模；用 2.0 报告说明控制输入、参考编辑与生产工作流的扩展。
4. 用视频 DiT 尺度定律讨论预算分配，再用 RewardDance 说明需要扩展的也包括奖励模型能力。
5. 用 Phantom、VINCIE 系列和推理工程解释可控性与成本为何影响专业工作流的采用。

这条顺序用于组织讲述；不同研究实际存在时间重叠，不能据此假定每篇论文都按顺序进入同一产品实现。

## 9. 完整下载目录与版本

| 编号 | 正式标题 / PDF | 固定 arXiv 版本 | 页数 |
|---|---|---|---:|
'''

for key, paper in papers.items():
    guide += f"| {key} | [{paper['title']}]({paper['filename']}) | [{paper['pdf_id']}]({paper['landing_url']}) | {paper['page_count']} |\n"
guide += '\n所有 PDF 已检查文件格式、首页正式标题和逐页文本可读性。原始来源、摘要、页数、文件大小与 SHA-256 保存在 [论文来源与校验.json](论文来源与校验.json)。重点原文可查 [01_关键证据摘录.md](01_关键证据摘录.md)。\n'


def pdf_pages(filename):
    with pymupdf.open(filename) as doc:
        return [' '.join(page.get_text().split()) for page in doc]


def quote(key, page, phrase, after=470):
    pages = json.loads((WORK / (papers[key]['short'] + '_pages.json')).read_text(encoding='utf-8'))
    text = ' '.join(pages[page-1].split())
    pos = text.lower().find(phrase.lower())
    if pos < 0:
        raise ValueError(f'Quote not found: {key}, p{page}, {phrase}')
    excerpt = text[pos:pos+after]
    return f"**{DETAILS[key][0]}，PDF 第 {page} 页**（[PDF]({papers[key]['filename']}#page={page})）\n\n> {excerpt}\n\n"


evidence = '# 关键原文与证据边界\n\n核对日期：2026-11-19。以下为本地 PDF 的短段摘录；段末按长度截取，完整上下文见对应页。\n\n'
evidence += '## 1. Seaweed 明确讨论中等规模与训练成本\n\n'
evidence += quote('05', 2, 'We choose to train', 490)
evidence += '## 2. Seedance 对 Seaweed 与 LCT 的技术引用\n\n'
evidence += quote('06', 4, 'following Seaweed', 380)
evidence += '这段直接支持位置编码设计的承接，不能单独证明组织合并或权重合并。\n\n'
evidence += '## 3. 视频时长与生成耗时\n\n'
evidence += quote('06', 1, '41.4 seconds', 180)
evidence += '同段完整句说明被生成的视频为 5 秒、1080p；41.4 秒为 NVIDIA L20 上的推理时间。\n\n'
evidence += '## 4. 1.5 Pro 已公开双分支结构\n\n'
evidence += quote('07', 1, 'dual-branch Diffusion Transformer', 330)
evidence += '## 5. 反馈数据来源披露到什么程度\n\n'
evidence += quote('06', 11, 'We collect prompts', 550)
evidence += '## 6. Seedance 1.0 明确提到 RayFlow\n\n'
evidence += quote('06', 12, 'we incorporate Score Distillation', 430)
evidence += '**同报告第 13 页对 AdaSpa 的承接**：\n\n'
evidence += quote('06', 13, 'Expanding on the methodology established by AdaSpa', 440)
evidence += '## 7. 奖励模型也有扩展问题\n\n'
evidence += quote('10', 1, '26 billion parameters', 320)
evidence += '该参数量属于奖励模型，不属于视频生成器。\n\n'
evidence += '## 8. Seaweed-APT 的实时条件\n\n'
evidence += quote('11', 15, '6.03s', 360)
evidence += '## 9. 视频尺度定律的实验范围\n\n'
evidence += quote('17', 7, '1.07B model', 350)
evidence += '这是预算与模型规模的研究依据，不是 Seedance 200B 的实测或发布证明。\n\n'
evidence += '## 10. Seaweed 与 LoRA 适配\n\n'
evidence += quote('05', 17, 'LoRA', 260)
evidence += '## 11. Seedance 2.0 的能力披露与参数量\n\n'
base_2 = BASE / '03_Seedance_2.0_2604.14148v1.pdf'
base_pages = pdf_pages(base_2)
phrase = 'Seedance 2.0 supports direct generation'
start = base_pages[0].find(phrase)
if start < 0:
    raise ValueError('Seedance 2.0 quote not found')
evidence += '**Seedance 2.0，PDF 第 1 页**（[PDF](../03_Seedance_2.0_2604.14148v1.pdf#page=1)）\n\n> ' + base_pages[0][start:start+640] + '\n\n'
patterns = [r'\b200\s*[Bb]\b', r'\b200\s+billion\b', r'\bdual[-\s]branch\b']
hits = {pattern: [i+1 for i, page in enumerate(base_pages) if re.search(pattern, page, re.I)] for pattern in patterns}
evidence += '对该 PDF 全文检索 `200B` / `200 billion` / `dual-branch`，未得到对应命中。结合正文内容，本次未找到其对 200B 参数量和具体双分支结构的披露。文字检索本身不是对模型实际参数量的判定。\n\n'
evidence += '## 12. 可继续查阅的官方研究入口\n\n- [Seaweed 项目页](https://seaweed.video/)：展示 LCT、Phantom、Seaweed-APT 等相关工作。\n- [VINCIE 官方仓库](https://github.com/ByteDance-Seed/VINCIE)：包含论文、代码、数据和权重入口。\n- [VINCIE-NExT 项目页](https://vincie-next.github.io/)：与上层目录已下载论文对应。\n'

(OUT / '00_阅读指南与事实核对.md').write_text(guide, encoding='utf-8')
(OUT / '01_关键证据摘录.md').write_text(evidence, encoding='utf-8')

css = '''body{max-width:1160px;margin:40px auto;padding:0 24px 60px;font:16px/1.85 "Microsoft YaHei","PingFang SC",sans-serif;color:#1b2635;background:#fff}h1{font-size:30px;line-height:1.45}h2{font-size:23px;margin-top:42px}a{color:#175eb4;text-decoration:none}a:hover{text-decoration:underline}table{border-collapse:collapse;width:100%;margin:22px 0;font-size:14px}td,th{border:1px solid #d9e1eb;padding:12px 14px;vertical-align:top}th{background:#eef3f9;text-align:left}tr:nth-child(even){background:#f8fafc}blockquote{margin:16px 0;border-left:4px solid #b8cbe2;padding:8px 18px;background:#f5f8fb;overflow-wrap:anywhere}code{background:#eef2f6;padding:2px 5px}strong{font-weight:650}li{margin:8px 0}@media(max-width:700px){body{margin:24px auto;padding:0 16px}table{display:block;overflow-x:auto}h1{font-size:25px}}'''


def render(text, title):
    text = text.replace('.md)', '.html)')
    content = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><style>' + css + '</style></head><body>' + content + '</body></html>'


(OUT / '00_阅读指南与事实核对.html').write_text(render(guide, 'Seedance 技术演进：补充论文与事实核对'), encoding='utf-8')
(OUT / '01_关键证据摘录.html').write_text(render(evidence, 'Seedance 相关研究：关键证据摘录'), encoding='utf-8')
(OUT / 'index.html').write_text(render(guide, 'Seedance 补充论文 14 篇'), encoding='utf-8')

manifest['fact_checks'] = {
    'seedance_2_report_pages': len(base_pages),
    'seedance_2_text_search': hits,
    'interpretation': 'No public confirmation of 200B or dual-branch architecture was found in this particular official report; this is not a measurement of the actual model.',
}
manifest['reading_guide'] = '00_阅读指南与事实核对.md'
manifest['reading_notes'] = {key: dict(zip(['short', 'priority', 'year', 'pages', 'purpose', 'limits'], values)) for key, values in DETAILS.items()}
(OUT / '论文来源与校验.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

# Link the new research pack from the existing collection without changing its report transcription.
marker = '<!-- seedance-supplement-20261119 -->'
section = marker + '<section><h2>技术演进与业务落地：补充论文 14 篇</h2><p><a href="补充论文_技术演进与业务落地/index.html">阅读指南、完整论文目录与事实核对</a></p><p>覆盖 Seaweed、多镜头、原生音视频、尺度定律、奖励训练、推理加速与参考编辑。</p></section>' + marker
index_path = BASE / 'index.html'
base_html = index_path.read_text(encoding='utf-8')
if marker in base_html:
    base_html = re.sub(re.escape(marker) + '.*?' + re.escape(marker), lambda _: section, base_html, flags=re.S)
else:
    base_html = base_html.replace('</body>', section + '</body>')
index_path.write_text(base_html, encoding='utf-8')
readme_path = BASE / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
heading = '\n## 技术演进与业务落地补充（2026-11-19）\n'
if heading in readme:
    readme = readme.split(heading)[0]
readme += heading + '\n新增 14 篇论文，目录内现有论文 PDF 共 18 篇。详见 [阅读指南与事实核对](补充论文_技术演进与业务落地/00_阅读指南与事实核对.md)。补充材料另有独立 ZIP；原先 4 篇论文与报道的 ZIP 保留为首次保存的版本。\n'
readme_path.write_text(readme, encoding='utf-8')

# Verify every local link in the offline HTML and every archived file hash.
for html_path in OUT.glob('*.html'):
    soup = bs4.BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
    for link in soup.select('a[href]'):
        href = link['href']
        if re.match(r'^[a-z]+:', href) or href.startswith('#'):
            continue
        relative = unquote(href.split('#')[0])
        if not (html_path.parent / relative).is_file():
            raise ValueError(f'Broken local link: {html_path.name}: {href}')
for key, paper in papers.items():
    path = OUT / paper['filename']
    if hashlib.sha256(path.read_bytes()).hexdigest() != paper['sha256']:
        raise ValueError('PDF checksum mismatch: ' + path.name)

zip_path = ROOT / 'downloads' / 'Seedance_技术演进与业务落地_补充论文14篇.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
    for path in sorted(OUT.iterdir()):
        if path.is_file():
            archive.write(path, arcname=OUT.name + '/' + path.name)
    # Include the two previously downloaded papers referenced by the guide so its links work offline.
    for filename in ['03_Seedance_2.0_2604.14148v1.pdf', '04_VINCIE-NExT_NeurIPS2026_2610.12104v1.pdf']:
        archive.write(BASE / filename, arcname=filename)
with zipfile.ZipFile(zip_path) as archive:
    if archive.testzip() is not None:
        raise ValueError('ZIP integrity check failed')
    names = archive.namelist()
print(json.dumps({'new_papers': len(papers), 'new_paper_pages': sum(p['page_count'] for p in papers.values()), 'zip': str(zip_path), 'zip_bytes': zip_path.stat().st_size, 'zip_pdfs': sum(name.endswith('.pdf') for name in names), 'guide': str(OUT / '00_阅读指南与事实核对.md'), 'local_links_verified': True, 'sha256_verified': True}, ensure_ascii=False))
