"""Recreate curated paper illustrations from the exact registered PDFs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import pymupdf

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf-dir', type=Path, default=ROOT / '.cache/papers')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'assets/paper-figures/manifest.json').read_text(encoding='utf-8'))
    for figure in manifest['figures']:
        path = args.pdf_dir / figure['pdf_name']
        if hashlib.sha256(path.read_bytes()).hexdigest() != figure['pdf_sha256']:
            raise ValueError(f"Unexpected PDF edition: {figure['source_id']}")
        with pymupdf.open(path) as doc:
            page = doc[figure['pdf_page'] - 1]
            rect = pymupdf.Rect(figure['crop_points'])
            if not page.rect.contains(rect) or rect.is_empty:
                raise ValueError(f"Invalid crop: {figure['id']}")
            target = ROOT / figure['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(matrix=pymupdf.Matrix(figure['scale'], figure['scale']), clip=rect, alpha=False).save(target)
        print(figure['path'])


if __name__ == '__main__':
    main()
