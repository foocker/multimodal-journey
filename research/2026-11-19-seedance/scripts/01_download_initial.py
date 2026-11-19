# Historical session script; see this directory README before running.
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import bs4
import pymupdf as fitz
import requests

ROOT = Path(__file__).resolve().parents[3] / '.cache' / 'legacy-seedance'
OUT = ROOT / 'downloads' / '曾妍_Seedance_论文与报道'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; reference-archive/1.0)'}


def report_search():
    jobs = [
        ('bing_title', 'https://www.bing.com/search', {'q': '"29岁掌舵字节视频大模型"'}),
        ('bing_name', 'https://www.bing.com/search', {'q': '"曾妍与Seedance"'}),
        ('baidu_title', 'https://www.baidu.com/s', {'wd': '29岁掌舵字节视频大模型 曾妍 技术豪赌'}),
        ('sogou_title', 'https://www.sogou.com/web', {'query': '"曾妍" "技术豪赌"'}),
        ('seedance_metadata', 'https://arxiv.org/abs/2604.14148', None),
    ]

    def one(job):
        name, url, params = job
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=25)
            response.encoding = response.apparent_encoding if 'arxiv' not in url else 'utf-8'
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            if 'arxiv' in url:
                return {
                    'name': name, 'status': response.status_code, 'url': response.url,
                    'title': [m.get('content') for m in soup.select('meta[name=citation_title]')],
                    'author_count': len(soup.select('meta[name=citation_author]')),
                    'authors': [m.get('content') for m in soup.select('meta[name=citation_author]')],
                    'text': soup.get_text(' ', strip=True)[:6500],
                }
            links = []
            selectors = ['li.b_algo', 'div.result', 'div.vrwrap', 'div.rb']
            elements = soup.select(','.join(selectors))
            for item in elements[:12]:
                links.append({'text': item.get_text(' ', strip=True)[:1600], 'links': [(a.get_text(' ', strip=True), a.get('href')) for a in item.select('h2 a[href], h3 a[href]')]})
            return {'name': name, 'status': response.status_code, 'url': response.url, 'results': links, 'text': soup.get_text(' ', strip=True)[:6500] if not links else ''}
        except Exception as exc:
            return {'name': name, 'error': str(exc)}

    results = list(ThreadPoolExecutor(max_workers=5).map(one, jobs))
    for item in results:
        print(json.dumps(item, ensure_ascii=False), flush=True)
    return results


PAPERS = [
    {
        'id': '01', 'short_name': 'X-VLM', 'venue': 'ICML 2022 / PMLR 162:25994–26009',
        'title': 'Multi-Grained Vision Language Pre-Training: Aligning Texts with Visual Concepts',
        'authors': ['Yan Zeng', 'Xinsong Zhang', 'Hang Li'],
        'landing_url': 'https://proceedings.mlr.press/v162/zeng22c.html',
        'arxiv_url': 'https://arxiv.org/abs/2111.08276',
        'pdf_url': 'https://proceedings.mlr.press/v162/zeng22c/zeng22c.pdf',
        'filename': '01_X-VLM_ICML2022.pdf',
        'expected': ['Multi-Grained Vision Language Pre-Training', 'Aligning Texts with Visual Concepts'],
    },
    {
        'id': '02', 'short_name': 'PixelDance', 'venue': 'CVPR 2024, pp. 8850–8860',
        'title': 'Make Pixels Dance: High-Dynamic Video Generation',
        'authors': ['Yan Zeng', 'Guoqiang Wei', 'Jiani Zheng', 'Jiaxin Zou', 'Yang Wei', 'Yuchen Zhang', 'Hang Li'],
        'landing_url': 'https://openaccess.thecvf.com/content/CVPR2024/html/Zeng_Make_Pixels_Dance_High-Dynamic_Video_Generation_CVPR_2024_paper.html',
        'arxiv_url': 'https://arxiv.org/abs/2311.10982',
        'pdf_url': 'https://openaccess.thecvf.com/content/CVPR2024/papers/Zeng_Make_Pixels_Dance_High-Dynamic_Video_Generation_CVPR_2024_paper.pdf',
        'filename': '02_PixelDance_CVPR2024.pdf',
        'expected': ['Make Pixels Dance', 'High-Dynamic Video Generation'],
    },
    {
        'id': '03', 'short_name': 'Seedance 2.0', 'venue': 'arXiv, 2026-04-15; model card / technical report',
        'title': 'Seedance 2.0: Advancing Video Generation for World Complexity',
        'landing_url': 'https://arxiv.org/abs/2604.14148v1',
        'arxiv_url': 'https://arxiv.org/abs/2604.14148v1',
        'pdf_url': 'https://arxiv.org/pdf/2604.14148v1',
        'filename': '03_Seedance_2.0_2604.14148v1.pdf',
        'expected': ['Seedance 2.0', 'Advancing Video Generation for World Complexity'],
        'existing_copy': str(ROOT / 'downloads' / 'Seedream5.5_Seedance2.5_ReadingPack' / 'V01_Seedance_2.0_2604.14148v1.pdf'),
    },
    {
        'id': '04', 'short_name': 'VINCIE-NExT', 'venue': "NeurIPS 2026 (according to the arXiv authors' comment)",
        'title': 'VINCIE-NExT: Unlocking Video Editing from Images via In-Context Modeling',
        'authors': ['Leigang Qu', 'Feng Cheng', 'Ziyan Yang', 'Bangbang Yang', 'Zhaoyang Huang', 'Wei Chow', 'Yicong Li', 'Wenjie Wang', 'Tat-Seng Chua', 'Yan Zeng'],
        'landing_url': 'https://arxiv.org/abs/2610.12104v1',
        'arxiv_url': 'https://arxiv.org/abs/2610.12104v1',
        'project_url': 'https://vincie-next.github.io/',
        'code_url': 'https://github.com/LgQu/VINCIE-NExT',
        'pdf_url': 'https://arxiv.org/pdf/2610.12104v1',
        'filename': '04_VINCIE-NExT_NeurIPS2026_2610.12104v1.pdf',
        'expected': ['VINCIE-NExT', 'Unlocking Video Editing from Images'],
    },
]


def verify_pdf(path, expected):
    if not path.read_bytes()[:1024].lstrip().startswith(b'%PDF-'):
        raise ValueError('Downloaded response is not a PDF')
    with fitz.open(path) as doc:
        first_text = ' '.join(doc[i].get_text() for i in range(min(2, len(doc)))).replace('\xad', '')
        normalized = ' '.join(first_text.split()).lower()
        missing = [text for text in expected if text.lower() not in normalized]
        if missing:
            raise ValueError(f'Title verification failed: {missing}')
        empty = [i + 1 for i in range(len(doc)) if not doc[i].get_text().strip()]
        return {'page_count': len(doc), 'empty_text_pages': empty, 'first_page_text': first_text[:2200]}


def download_one(paper):
    record = dict(paper)
    target = OUT / paper['filename']
    try:
        if target.exists():
            record['retrieval_method'] = 'existing validated copy in output directory'
        elif paper.get('existing_copy') and Path(paper['existing_copy']).exists():
            verify_pdf(Path(paper['existing_copy']), paper['expected'])
            shutil.copy2(paper['existing_copy'], target)
            record['retrieval_method'] = 'copied existing local copy of the same arXiv version'
        else:
            response = requests.get(paper['pdf_url'], headers=HEADERS, timeout=(20, 90))
            response.raise_for_status()
            if not response.content[:1024].lstrip().startswith(b'%PDF-'):
                raise ValueError(f"Not a PDF: {response.headers.get('Content-Type')}")
            partial = target.with_suffix('.pdf.part')
            partial.write_bytes(response.content)
            verify_pdf(partial, paper['expected'])
            partial.replace(target)
            record['retrieval_method'] = 'downloaded from publisher or arXiv'
            record['final_download_url'] = response.url
        verification = verify_pdf(target, paper['expected'])
        record.update({k: v for k, v in verification.items() if k != 'first_page_text'})
        record['bytes'] = target.stat().st_size
        record['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        record['status'] = 'saved_and_verified'
        print(json.dumps({'file': target.name, 'status': record['status'], **verification, 'bytes': record['bytes']}, ensure_ascii=False), flush=True)
    except Exception as exc:
        record['status'] = 'error'
        record['error'] = str(exc)
        print(json.dumps(record, ensure_ascii=False), flush=True)
    return record


def download_papers():
    OUT.mkdir(parents=True, exist_ok=True)
    results = list(ThreadPoolExecutor(max_workers=4).map(download_one, PAPERS))
    (OUT / '论文来源与校验.json').write_text(json.dumps({'saved_date': '2026-11-19', 'papers': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    if any(item['status'] == 'error' for item in results):
        raise SystemExit(1)


REPORT_TITLE = '29岁掌舵字节视频大模型：曾妍与Seedance的“技术豪赌”'
REPORT_PARAGRAPHS = [
    '字节跳动AI团队中，一位29岁的研究员正走向核心。曾妍，1997年出生，2021年以校招生身份加入字节AI Lab，短短五年便成长为Seedance视频大模型预训练负责人，并在一年内连升两级至4-2职级，对应高级总监层级，年薪总包据估算可达500万元以上。',
    '曾妍的“早慧”在入职两个月时便已显现。她以第一作者身份发表X-VLM论文，提出多粒度视觉语言对齐方法，让AI既能把握整体场景，又能精准定位文本对应的物体与动作。这篇论文被ICML 2022接收，其中的“从粗到细”建模思路，为她日后主导视频生成的预训练埋下了伏笔。此后，PixelDance论文被CVPR 2024接收，尝试解决复杂运动中人物失真、主体不一致的难题，成为Seedance的重要技术积累。',
    '真正让曾妍进入舞台中央的，是2025年底的一次关键决策。面对团队内部对训练规模的分歧，她坚持将Seedance 2.0做到至少2000亿参数，并争取到管理层支持。2026年2月，Seedance 2.0发布，采用双分支扩散变换器架构，支持文本、图像、音频、视频四种模态输入，能在60秒内生成带有原生音轨的多镜头序列视频。其多镜头叙事功能可自动保持角色与风格的一致性，被业内人士评价为“或将彻底改变电影制作的未来”。同年4月，团队在arXiv发布26页论文，171人署名中曾妍在列，体现了罕见的学术透明。10月，她团队主导的VINCIE-NExT被NeurIPS 2026接收，将图像编辑能力迁移至视频编辑，减少了对大规模配对视频数据的依赖。',
    '曾妍的崛起并非孤例。2026年的中国AI圈，一批90后甚至95后研究员正集体进入大厂核心研发岗位。字节Seed核心负责人周旸的管理范围在下半年有所收缩，部分工作逐渐由曾妍承担，她近期还在扩招语言模型方向的研发人员。从校招生到视频大模型预训练一号位，曾妍的五年路径，折射出AI竞赛对年轻技术判断力的空前押注——在模型能力上限由预训练决定的世界里，资历正在让位于对“塑造模型世界观”的敏锐直觉。',
]
REPORT_NOTE = '根据本次对话中用户提供的截图转录，保存日期：2026-11-19。未定位到可确认的原始网页，作者、发布日期及原始链接不明。正文保留截图中的表述。'
REPORT_BASENAME = '报道_29岁掌舵字节视频大模型_截图转录'


def write_report_pdf(path):
    document = fitz.open()
    font_file = Path('C:/Windows/Fonts/msyh.ttc')
    font = fitz.Font(fontfile=str(font_file))
    page = None
    y = 0
    margin = 48
    page_width, page_height = 595.28, 841.89
    line_width = page_width - margin * 2

    def new_page():
        nonlocal page, y
        page = document.new_page(width=page_width, height=page_height)
        page.insert_font(fontname='ReportCJK', fontfile=str(font_file))
        y = 55

    def lines_for(text, size):
        line = ''
        for char in text:
            if line and font.text_length(line + char, fontsize=size) > line_width and char not in '，。；：！？、）》”’':
                yield line
                line = char
            else:
                line += char
        if line:
            yield line

    def paragraph(text, size, leading, color=(0.08, 0.10, 0.13)):
        nonlocal y
        for line in lines_for(text, size):
            if y + leading > page_height - 55:
                new_page()
            page.insert_text((margin, y), line, fontsize=size, fontname='ReportCJK', color=color)
            y += leading
        y += leading * 0.6

    new_page()
    paragraph(REPORT_TITLE, 17, 25)
    paragraph(REPORT_NOTE, 9, 15, (0.40, 0.43, 0.47))
    for text in REPORT_PARAGRAPHS:
        paragraph(text, 11, 20)
    for index, current in enumerate(document):
        current.insert_text((margin, page_height - 30), f'{index + 1} / {len(document)}', fontsize=9, fontname='helv', color=(0.45, 0.45, 0.45))
    document.set_metadata({'title': REPORT_TITLE, 'subject': '用户提供截图的文字转录', 'creator': 'Screenshot transcription archive'})
    document.subset_fonts()
    document.save(path, garbage=4, deflate=True)
    document.close()
    with fitz.open(path) as check:
        text = re.sub(r'\s+', '', ''.join(page.get_text() for page in check))
        for paragraph_text in [REPORT_TITLE, *REPORT_PARAGRAPHS]:
            if re.sub(r'\s+', '', paragraph_text) not in text:
                raise ValueError('Report PDF text verification failed')
        check[0].get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(ROOT / 'tmp' / 'seedance_report_preview_20261119.png')
        print(json.dumps({'report_pdf': str(path), 'pages': len(check), 'text_verified': True}, ensure_ascii=False), flush=True)


def archive_report():
    OUT.mkdir(parents=True, exist_ok=True)
    markdown = '# ' + REPORT_TITLE + '\n\n> ' + REPORT_NOTE + '\n\n' + '\n\n'.join(REPORT_PARAGRAPHS) + '\n'
    (OUT / (REPORT_BASENAME + '.md')).write_text(markdown, encoding='utf-8')
    css = 'body{max-width:760px;margin:48px auto;padding:0 24px;color:#19212c;background:#fff;font-family:"Microsoft YaHei","PingFang SC",sans-serif;line-height:1.9}h1{font-size:27px;line-height:1.5}p{font-size:17px;margin:1.4em 0}.note{color:#68717d;font-size:13px;border-left:3px solid #c5ccd6;padding-left:14px}a{color:#175da8}li{margin:16px 0}@media print{body{margin:0;max-width:none}p{font-size:12pt}h1{font-size:19pt}}'
    body = '<h1>' + html.escape(REPORT_TITLE) + '</h1><p class="note">' + html.escape(REPORT_NOTE) + '</p>' + ''.join('<p>' + html.escape(p) + '</p>' for p in REPORT_PARAGRAPHS)
    report_html = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(REPORT_TITLE) + '</title><style>' + css + '</style></head><body><article>' + body + '</article></body></html>'
    (OUT / (REPORT_BASENAME + '.html')).write_text(report_html, encoding='utf-8')
    write_report_pdf(OUT / (REPORT_BASENAME + '.pdf'))

    manifest_path = OUT / '论文来源与校验.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['report'] = {'title': REPORT_TITLE, 'source_type': 'user-provided screenshot', 'original_url': None, 'note': REPORT_NOTE, 'files': [REPORT_BASENAME + ext for ext in ['.md', '.html', '.pdf']]}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    rows = []
    for paper in manifest['papers']:
        rows.append(f"| [{paper['short_name']}]({paper['filename']}) | {paper['title']} | {paper['page_count']} | [来源]({paper['landing_url']}) |")
    readme = '# 曾妍与 Seedance：截图涉及论文及报道\n\n保存日期：2026-11-19。\n\n已保存 4 篇论文 PDF 和 1 篇中文报道；论文均已检查 PDF 格式、正式标题及全部页面的可读性。\n\n| 论文 | 正式标题 | 页数 | 公开来源 |\n| --- | --- | ---: | --- |\n' + '\n'.join(rows) + '\n\nSeedance 2.0 对应截图中“2026 年 4 月、26 页、171 个署名条目”的报告；arXiv 条目为 2604.14148，署名列表包含 Yan Zeng。此 PDF 复用了本地已有的同一 arXiv v1 版本，其余三篇从 PMLR、CVF 或 arXiv 下载。X-VLM 和 PixelDance 采用会议公开版本；VINCIE-NExT 采用 arXiv v1 版本，其 arXiv 页面注明获 NeurIPS 2026 接收。\n\n## 中文报道\n\n- [PDF](' + REPORT_BASENAME + '.pdf)\n- [离线网页](' + REPORT_BASENAME + '.html)\n- [Markdown](' + REPORT_BASENAME + '.md)\n\n' + REPORT_NOTE + '\n\n论文的公开链接、文件大小、页数及 SHA-256 校验值保存在 [论文来源与校验.json](论文来源与校验.json)。\n'
    (OUT / 'README.md').write_text(readme, encoding='utf-8')

    items = '<h1>曾妍与 Seedance：论文与报道</h1><p>保存日期：2026-11-19</p><ul>'
    for paper in manifest['papers']:
        items += '<li><a href="' + html.escape(paper['filename'], quote=True) + '">' + html.escape(paper['short_name']) + '</a>（' + str(paper['page_count']) + ' 页）<br>' + html.escape(paper['title']) + '</li>'
    items += '</ul><h2>中文报道</h2><p><a href="' + REPORT_BASENAME + '.pdf">PDF</a> · <a href="' + REPORT_BASENAME + '.html">离线网页</a> · <a href="' + REPORT_BASENAME + '.md">Markdown</a></p><p class="note">' + html.escape(REPORT_NOTE) + '</p>'
    (OUT / 'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>曾妍与 Seedance：论文与报道</title><style>' + css + '</style></head><body>' + items + '</body></html>', encoding='utf-8')

    zip_path = OUT.with_suffix('.zip')
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(OUT.iterdir()):
            if path.is_file():
                archive.write(path, arcname=OUT.name + '/' + path.name)
    with zipfile.ZipFile(zip_path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP verification failed')
        print(json.dumps({'archive': str(zip_path), 'bytes': zip_path.stat().st_size, 'files': archive.namelist()}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['search']:
        report_search()
    elif sys.argv[1:] == ['download']:
        download_papers()
    elif sys.argv[1:] == ['archive']:
        archive_report()
    else:
        raise SystemExit('Use search, download, or archive')
