"""Manage paper links and local caches; do not store PDFs in Git."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def load_papers(root=ROOT):
    data = json.loads((root / 'sources/papers.json').read_text(encoding='utf-8'))
    return data['papers']


def cache_path(paper, cache_dir):
    version = paper.get('arxiv_version') or paper.get('edition_id', 'publisher')
    return Path(cache_dir) / f"{paper['id']}-{version}.pdf"


def validate_pdf(path, expected_hash=None):
    path = Path(path)
    with path.open('rb') as stream:
        head = stream.read(1024)
        stream.seek(max(0, path.stat().st_size - 2048))
        tail = stream.read()
    if not head.lstrip().startswith(b'%PDF-') or b'%%EOF' not in tail:
        raise ValueError('Response is not a complete PDF')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected_hash and digest != expected_hash:
        raise ValueError('SHA-256 differs from the archived edition; inspect the source/version before updating its record')
    return digest


def download(paper, cache_dir, opener=urlopen):
    target = cache_path(paper, cache_dir)
    expected = paper.get('file_check', {}).get('sha256')
    if target.exists():
        validate_pdf(target, expected)
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix('.pdf.part')
    request = Request(paper['pdf_url'], headers={'User-Agent': 'multimodal-journey/0.1 (paper reference downloader)'})
    try:
        with opener(request, timeout=60) as response, partial.open('wb') as output:
            expected_length = response.headers.get('Content-Length')
            total = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                output.write(chunk)
        if expected_length and total != int(expected_length):
            raise ValueError('Downloaded length does not match Content-Length')
        validate_pdf(partial, expected)
        partial.replace(target)
    finally:
        partial.unlink(missing_ok=True)
    return target


def extract(paper, cache_dir):
    try:
        import pymupdf
    except ImportError as exc:
        raise ValueError('Install optional extraction dependency: python -m pip install -r requirements.txt') from exc
    target = cache_path(paper, cache_dir)
    if not target.is_file():
        raise ValueError('Download this paper first')
    validate_pdf(target, paper.get('file_check', {}).get('sha256'))
    with pymupdf.open(target) as doc:
        pages = [{'pdf_page': i + 1, 'text': page.get_text()} for i, page in enumerate(doc)]
    result = {'paper_id': paper['id'], 'pdf_url': paper['pdf_url'], 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'pages': pages}
    output = target.with_suffix('.pages.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return output


def index_text(papers):
    lines = ['# 论文索引', '', '由 `python scripts/papers.py index` 从来源登记生成。每篇笔记是当前的初步理解，完整版本、页数和校验信息见 [来源登记](../sources/papers.json)。', '', '| 首次公开 | 论文 / 阅读笔记 | 固定版本 / PDF | 阅读状态 |', '|---|---|---|---|']
    for paper in sorted(papers, key=lambda p: (p['year'], p['id'])):
        path = Path(paper['note_path']).relative_to('papers').as_posix()
        version = paper.get('edition') or paper.get('arxiv_version', '')
        lines.append(f"| {paper['year']} | [{paper['title']}]({path}) | [{version}]({paper['pdf_url']}) | {paper['reading_status']} |")
    lines += ['', '阅读状态 `partial` 表示已核对摘要或部分章节，并非逐篇全文精读或复现。', '', '## 常用入口', '', '- [视频生成阅读路线](../topics/video-generation/README.md)', '- [论文笔记模板](../templates/paper.md)', '- [修订流程](../docs/workflow.md)', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['list', 'download', 'extract', 'index'])
    parser.add_argument('paper_id', nargs='?')
    parser.add_argument('--cache-dir', type=Path, default=ROOT / '.cache/papers')
    args = parser.parse_args(argv)
    papers = load_papers()
    if args.command == 'list':
        for paper in papers:
            print(f"{paper['id']:28} {paper['title']}")
    elif args.command == 'index':
        (ROOT / 'papers/README.md').write_text(index_text(papers), encoding='utf-8')
        print('Updated papers/README.md')
    else:
        paper = next((p for p in papers if p['id'] == args.paper_id), None)
        if paper is None:
            parser.error('Specify a registered paper ID; use list to inspect IDs')
        if args.command == 'download':
            print(download(paper, args.cache_dir))
        else:
            print(extract(paper, args.cache_dir))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        raise SystemExit(1)
