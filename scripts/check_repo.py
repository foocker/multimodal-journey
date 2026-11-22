"""Offline structural checks; this does not validate scientific conclusions."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from papers import ROOT, index_text, load_papers

EXCLUDED = {'.git', '.cache', '.venv', '.venv-code', '__pycache__', 'runs', 'node_modules'}
FORBIDDEN = {'.pdf', '.zip', '.mp4', '.mov', '.mkv', '.mp3', '.wav', '.pt', '.pth', '.ckpt', '.safetensors', '.parquet'}
CLAIM_STATES = {'supported', 'partially_supported', 'unverified', 'contradicted', 'withdrawn'}


def files(root):
    return [p for p in root.rglob('*') if p.is_file() and not (set(p.relative_to(root).parts) & EXCLUDED)]


def main():
    errors = []
    all_files = files(ROOT)
    for path in all_files:
        if path.suffix.lower() == '.json':
            try:
                json.loads(path.read_text(encoding='utf-8'))
            except (ValueError, UnicodeError) as exc:
                errors.append(f'{path.relative_to(ROOT)}: invalid JSON: {exc}')
    try:
        papers = load_papers()
        web = json.loads((ROOT / 'sources/web.json').read_text(encoding='utf-8'))['sources']
    except (ValueError, OSError) as exc:
        print(f'Source registry error: {exc}')
        return 1
    ids = [p.get('id') for p in papers] + [p.get('id') for p in web]
    if len(ids) != len(set(ids)) or None in ids:
        errors.append('Source IDs must be present and unique')
    source_ids = set(ids)
    for source in web:
        if source.get('url'):
            parsed = urlsplit(source['url'])
            if parsed.scheme != 'https' or not parsed.netloc:
                errors.append(f"{source['id']}: invalid web source URL")
        elif not source.get('local_path'):
            errors.append(f"{source['id']}: a source needs a URL or local record")
        if source.get('local_path') and not (ROOT / source['local_path']).is_file():
            errors.append(f"{source['id']}: missing local source record")
    for paper in papers:
        required = {'id', 'title', 'year', 'pdf_url', 'url', 'note_path', 'reading_status'}
        if not required.issubset(paper):
            errors.append(f"{paper.get('id')}: missing required source fields")
            continue
        for key in ['url', 'pdf_url']:
            parsed = urlsplit(paper[key])
            if parsed.scheme != 'https' or not parsed.netloc:
                errors.append(f"{paper['id']}: invalid {key}")
        note = ROOT / paper['note_path']
        if not note.is_file():
            errors.append(f"{paper['id']}: missing note {paper['note_path']}")
        if paper.get('arxiv_version') and 'arxiv.org/pdf/' in paper['pdf_url'] and not paper['pdf_url'].endswith(paper['arxiv_version']):
            errors.append(f"{paper['id']}: arXiv PDF must pin the recorded version")
    expected_index = index_text(papers)
    if (ROOT / 'papers/README.md').read_text(encoding='utf-8') != expected_index:
        errors.append('Paper index is stale: run python scripts/papers.py index')
    for path in (ROOT / 'topics').glob('*/claims.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        claim_ids = []
        for claim in data['claims']:
            claim_ids.append(claim['id'])
            if claim['status'] not in CLAIM_STATES:
                errors.append(f"{path.name}: invalid claim status {claim['id']}")
            if claim['status'] == 'supported' and not claim.get('evidence'):
                errors.append(f"{claim['id']}: supported claims need evidence")
            for evidence in claim.get('evidence', []):
                if evidence['source_id'] not in source_ids or not evidence.get('locator'):
                    errors.append(f"{claim['id']}: evidence needs a registered source and locator")
        if len(claim_ids) != len(set(claim_ids)):
            errors.append(f'{path}: duplicate claim ID')
    for path in all_files:
        if path.suffix != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r'^status: reviewed$', text, re.M):
            if not re.search(r'^reviewed_by: \S', text, re.M) or not re.search(r'^reviewed_on: \d{4}-\d{2}-\d{2}$', text, re.M):
                errors.append(f'{path.relative_to(ROOT)}: reviewed status needs reviewed_by and reviewed_on')
        # Source lists in the deliberately small front matter use JSON array syntax.
        match = re.search(r'^source_ids: (\[.*\])$', text, re.M)
        if match:
            for source_id in json.loads(match.group(1)):
                if source_id not in source_ids:
                    errors.append(f'{path.relative_to(ROOT)}: unknown source {source_id}')
        # Code samples and their placeholder paths are not live navigation links.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', text):
            target = unquote(target.strip('<>').split('#', 1)[0])
            if not target or urlsplit(target).scheme or target.startswith('//'):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f'{path.relative_to(ROOT)}: broken local link {target}')
    for path in (ROOT / 'datasets/examples').glob('*.jsonl'):
        scene_ids = set()
        try:
            for line in path.read_text(encoding='utf-8').splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                if record['scene_id'] in scene_ids:
                    errors.append(f'{path.name}: duplicate scene ID')
                scene_ids.add(record['scene_id'])
                subject_ids = [subject['id'] for subject in record['subjects']]
                shot_ids = [shot['id'] for shot in record['shots']]
                if len(subject_ids) != len(set(subject_ids)) or len(shot_ids) != len(set(shot_ids)):
                    errors.append(f'{path.name}: duplicate subject or shot ID')
                if len(shot_ids) < 2 or not record['rights'] or not record['source_group']:
                    errors.append(f'{path.name}: multishot example needs two shots, rights and source_group')
                for shot in record['shots']:
                    if not set(shot['subject_ids']).issubset(subject_ids):
                        errors.append(f'{path.name}: shot references an unknown subject')
                if record['kind'] == 'synthetic_example' and record['split'] != 'example':
                    errors.append(f'{path.name}: demonstration records must remain in the example split')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{path.name}: invalid scene record: {exc}')
    # Inspect tracked/staged paths, so .gitignore cannot conceal an accidentally force-added PDF.
    tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8').split('\0')
    candidates = set(tracked) | {p.relative_to(ROOT).as_posix() for p in all_files}
    for name in filter(None, candidates):
        path = ROOT / name
        if path.suffix.lower() in FORBIDDEN or '.cache' in Path(name).parts:
            errors.append(f'External artifact/cache must not be committed: {name}')
        if path.is_file() and path.stat().st_size > 2_000_000:
            errors.append(f'Large file needs external storage or an explicit policy change: {name}')
    if errors:
        print('\n'.join(f'ERROR: {error}' for error in errors))
        return 1
    print(f'OK: {len(papers)} paper records, {len(web)} other sources, JSON, citations, local links and file boundaries. Scientific review is separate.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
