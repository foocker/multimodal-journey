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
import pymupdf
import requests

ROOT = Path(__file__).resolve().parents[3] / '.cache' / 'legacy-seedance'
BASE = ROOT / 'downloads' / '曾妍_Seedance_论文与报道'
OUT = BASE / '补充论文_技术演进与业务落地'
WORK = ROOT / 'tmp' / 'seedance_supplement_research_20261119'
WORK.mkdir(parents=True, exist_ok=True)
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; research-reference-archive/1.0)'}


def get(url, params=None):
    response = requests.get(url, params=params, headers=HEADERS, timeout=(15, 45))
    response.raise_for_status()
    return response


def discover():
    jobs = [
        ('scaling_video', 'https://arxiv.org/search/', {'query': '"scaling" "video generation"', 'searchtype': 'title', 'size': 50}),
        ('scaling_dit', 'https://arxiv.org/search/', {'query': '"scaling laws" "diffusion"', 'searchtype': 'title', 'size': 50}),
        ('vincie', 'https://raw.githubusercontent.com/ByteDance-Seed/VINCIE/main/README.md', None),
        ('seaweed_project', 'https://seaweed.video/', None),
    ]

    def one(job):
        name, url, params = job
        try:
            response = get(url, params)
            (WORK / (name + '.html')).write_text(response.text, encoding='utf-8')
            if 'README' in url:
                return {'name': name, 'text': response.text[:6000]}
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            if '/search/' in url:
                rows = []
                for element in soup.select('li.arxiv-result'):
                    a = element.select_one('p.list-title a')
                    t = element.select_one('p.title')
                    abstract = element.select_one('span.abstract-full')
                    rows.append({'title': t.get_text(' ', strip=True) if t else '', 'url': a.get('href') if a else '', 'abstract': abstract.get_text(' ', strip=True)[:700] if abstract else ''})
                (WORK / (name + '.json')).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
                return {'name': name, 'rows': rows[:12]}
            for tag in soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()
            return {'name': name, 'text': soup.get_text(' ', strip=True)[:6500], 'links': [(a.get_text(' ', strip=True), a.get('href')) for a in soup.select('a[href]') if any(term in a.get('href', '').lower() for term in ['arxiv', 'github', 'huggingface', 'model'])][:20]}
        except Exception as exc:
            return {'name': name, 'error': str(exc)}

    for result in ThreadPoolExecutor(max_workers=4).map(one, jobs):
        print(json.dumps(result, ensure_ascii=False), flush=True)


PAPERS = [
    {'key': '05', 'short': 'Seaweed-7B', 'arxiv_id': '2504.08685', 'category': '底座、训练预算与扩展', 'expected': ['Seaweed-7B', 'Cost-Effective Training']},
    {'key': '06', 'short': 'Seedance_1.0', 'arxiv_id': '2506.09113v2', 'category': '多镜头与产品化', 'expected': ['Seedance 1.0', 'Exploring the Boundaries'], 'local': str(ROOT / 'downloads/Seedream5.5_Seedance2.5_ReadingPack/V03_Seedance_1.0_2506.09113v2.pdf')},
    {'key': '07', 'short': 'Seedance_1.5_Pro', 'arxiv_id': '2512.13507v3', 'category': '原生音视频', 'expected': ['Seedance 1.5 pro', 'Audio-Visual Joint'], 'local': str(ROOT / 'downloads/Seedream5.5_Seedance2.5_ReadingPack/V02_Seedance_1.5_Pro_2512.13507v3.pdf')},
    {'key': '08', 'short': 'DiT', 'arxiv_id': '2212.09748', 'category': '扩展规律基础', 'expected': ['Scalable Diffusion Models with Transformers']},
    {'key': '09', 'short': 'DanceGRPO', 'arxiv_id': '2505.07818', 'category': '后训练与反馈', 'expected': ['DanceGRPO', 'Unleashing GRPO']},
    {'key': '10', 'short': 'RewardDance', 'arxiv_id': '2509.08826', 'category': '后训练与反馈', 'expected': ['RewardDance', 'Reward Scaling']},
    {'key': '11', 'short': 'Seaweed_APT', 'arxiv_id': '2501.08316', 'category': '少步生成与推理成本', 'expected': ['Adversarial Post-Training', 'One-Step Video Generation']},
    {'key': '12', 'short': 'Adaptive_Sparse_Attention', 'arxiv_id': '2502.21079', 'category': '稀疏注意力与推理成本', 'expected': ['Training-free and Adaptive Sparse Attention', 'Efficient Long Video Generation']},
    {'key': '13', 'short': 'VINCIE', 'arxiv_id': '2506.10941', 'category': '视频数据到图像编辑', 'expected': ['VINCIE', 'Unlocking In-context Image Editing from Video']},
    {'key': '14', 'short': 'LoRA', 'arxiv_id': '2106.09685', 'category': '低成本定制基础', 'expected': ['LoRA', 'Low-Rank Adaptation']},
    {'key': '15', 'short': 'Long_Context_Tuning', 'arxiv_id': '2503.10589', 'category': '长视频与跨镜头一致性', 'expected': ['Long-Context', 'Video Generation']},
    {'key': '16', 'short': 'Phantom', 'arxiv_id': '2502.11079', 'category': '多图参考与主体一致性', 'expected': ['Phantom', 'Video Generation']},
    {'key': '17', 'short': 'Video_DiT_Scaling_Laws', 'arxiv_id': '2411.17470', 'category': '视频模型的尺度定律', 'expected': ['Towards Precise Scaling Laws', 'Video Diffusion Transformers']},
    {'key': '18', 'short': 'RayFlow', 'arxiv_id': '2503.07699', 'category': 'Seedance 报告引用的蒸馏加速', 'expected': ['RayFlow', 'Instance-Aware Diffusion Acceleration']},
]


def metadata_one(paper):
    result = dict(paper)
    try:
        response = get('https://arxiv.org/abs/' + paper['arxiv_id'])
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        def meta(name):
            element = soup.select_one('meta[name="' + name + '"]')
            return element.get('content') if element else None
        heading = soup.select_one('h1.title')
        abstract = soup.select_one('blockquote.abstract')
        version_match = re.search(r'\[v(\d+)\]', soup.get_text(' ', strip=True))
        versioned_pdf = soup.select_one('a[href^="/pdf/"]')
        pdf_id = versioned_pdf['href'].split('/')[-1] if versioned_pdf else paper['arxiv_id']
        if not re.search(r'v\d+$', pdf_id):
            history_versions = [int(v) for v in re.findall(r'\[v(\d+)\]', soup.get_text(' ', strip=True))]
            pdf_id += 'v' + str(max(history_versions) if history_versions else 1)
        if re.search(r'v\d+$', paper['arxiv_id']):
            pdf_id = paper['arxiv_id']
        result.update({
            'title': meta('citation_title') or (heading.get_text(' ', strip=True).removeprefix('Title:') if heading else ''),
            'authors': [m.get('content') for m in soup.select('meta[name=citation_author]')],
            'published': meta('citation_date'),
            'pdf_id': pdf_id,
            'landing_url': 'https://arxiv.org/abs/' + pdf_id,
            'pdf_url': 'https://arxiv.org/pdf/' + pdf_id,
            'filename': paper['key'] + '_' + paper['short'] + '_' + pdf_id + '.pdf',
            'abstract': abstract.get_text(' ', strip=True).removeprefix('Abstract:') if abstract else '',
            'comments': [td.get_text(' ', strip=True) for td in soup.select('td.tablecell.comments')],
            'external_links': [(a.get_text(' ', strip=True), a.get('href')) for a in soup.select('a[href]') if any(term in a.get('href', '').lower() for term in ['github.io', 'github.com', 'huggingface.co'])],
        })
        (WORK / (paper['short'] + '_abstract.html')).write_text(response.text, encoding='utf-8')
        print(json.dumps({k: result.get(k) for k in ['key', 'title', 'pdf_id', 'published', 'abstract', 'comments']}, ensure_ascii=False), flush=True)
    except Exception as exc:
        result['error'] = str(exc)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def metadata():
    results = list(ThreadPoolExecutor(max_workers=5).map(metadata_one, PAPERS))
    (WORK / 'metadata.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')


def compact(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())


def verify(path, paper):
    with path.open('rb') as stream:
        if not stream.read(1024).lstrip().startswith(b'%PDF-'):
            raise ValueError('Not a PDF')
    with pymupdf.open(path) as doc:
        pages = [page.get_text() for page in doc]
        first = compact(' '.join(pages[:2]))
        for expected in paper['expected']:
            if compact(expected) not in first:
                raise ValueError('PDF title mismatch: ' + expected)
        return {'page_count': len(doc), 'empty_text_pages': [i+1 for i, t in enumerate(pages) if not t.strip()], 'page_texts': pages}


def download_one(paper):
    result = dict(paper)
    path = OUT / paper['filename']
    try:
        if path.exists():
            result['retrieval'] = 'validated existing file'
        elif paper.get('local') and Path(paper['local']).exists():
            verify(Path(paper['local']), paper)
            shutil.copy2(paper['local'], path)
            result['retrieval'] = 'copied local PDF of the same pinned arXiv version'
        else:
            response = get(paper['pdf_url'])
            part = path.with_suffix('.pdf.part')
            part.write_bytes(response.content)
            verify(part, paper)
            part.replace(path)
            result['retrieval'] = 'downloaded from arXiv'
        verification = verify(path, paper)
        (WORK / (paper['short'] + '_pages.json')).write_text(json.dumps(verification.pop('page_texts'), ensure_ascii=False, indent=2), encoding='utf-8')
        result.update(verification)
        result['bytes'] = path.stat().st_size
        result['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        result['status'] = 'saved_and_verified'
        print(json.dumps({k: result[k] for k in ['key', 'filename', 'page_count', 'bytes', 'status']}, ensure_ascii=False), flush=True)
    except Exception as exc:
        result.update({'status': 'error', 'error': str(exc)})
        print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def download():
    OUT.mkdir(parents=True, exist_ok=True)
    papers = json.loads((WORK / 'metadata.json').read_text(encoding='utf-8'))
    if any(paper.get('error') for paper in papers):
        raise SystemExit('Metadata has errors')
    results = list(ThreadPoolExecutor(max_workers=4).map(download_one, papers))
    (OUT / '论文来源与校验.json').write_text(json.dumps({'date': '2026-11-19', 'papers': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    if any(paper['status'] == 'error' for paper in results):
        raise SystemExit(1)


if __name__ == '__main__':
    {'discover': discover, 'metadata': metadata, 'download': download}[sys.argv[1]]()
