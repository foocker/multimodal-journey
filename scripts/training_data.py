"""Validate training metadata and split boundaries; does not inspect actual media."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def finite_tree(value):
    if isinstance(value, float) and not math.isfinite(value):
        return False
    if isinstance(value, dict):
        return all(finite_tree(v) for v in value.values())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def validate_records(records, *, production=False, split_policy='source-disjoint'):
    from jsonschema import Draft202012Validator

    if split_policy not in {'source-disjoint', 'identity-disjoint'}:
        raise ValueError('Unknown split policy')
    schema = json.loads((ROOT / 'datasets/schemas/training-record.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors, seen_ids, owners = [], set(), {}
    if not records:
        return ['No records supplied']
    for line_no, record in enumerate(records, 1):
        prefix = f'record {line_no}'
        if not finite_tree(record):
            errors.append(f'{prefix}: non-finite numeric value')
            continue
        structural = sorted(validator.iter_errors(record), key=lambda e: str(list(e.path)))
        if structural:
            errors.extend(f'{prefix} {list(e.path)}: {e.message}' for e in structural)
            continue
        rid = record['record_id']
        prefix = rid
        if rid in seen_ids:
            errors.append(f'{prefix}: duplicate record ID')
        seen_ids.add(rid)
        synthetic = record['kind'] == 'synthetic_example'
        if synthetic and (record['split'] != 'example' or record['rights']['status'] != 'synthetic_example'):
            errors.append(f'{prefix}: synthetic examples must remain in example split with example rights')
        if not synthetic and record['split'] == 'example':
            errors.append(f'{prefix}: actual media must have an explicit train/validation/test split')
        if production:
            if synthetic or record['split'] == 'example' or record['rights']['status'] != 'approved':
                errors.append(f'{prefix}: production requires actual media, approved rights and a production split')
            if not record['provenance']['media_sha256']:
                errors.append(f'{prefix}: production requires a target media content hash')
            if record['media']['uri'].startswith('example:'):
                errors.append(f'{prefix}: production cannot use example media URIs')
        media = record['media']
        duration = 1000 * media['frames'] / media['fps']
        if media['audio_present'] != (media['audio_sample_rate'] is not None):
            errors.append(f'{prefix}: audio presence and sample rate disagree')

        def interval(start, end, *, limit=None, point=False):
            if end < start or (not point and end == start) or (limit is not None and end > limit + 1e-6):
                errors.append(f'{prefix}: invalid time interval [{start},{end})')

        for event in record['caption']['events']:
            interval(event['start_ms'], event['end_ms'], limit=duration)
        if record['task'] == 'edit':
            edit = record['edit']
            interval(edit['start_ms'], edit['end_ms'], limit=duration)
            if production and (edit['rights']['status'] != 'approved' or not edit['source_sha256'] or not edit['mask_sha256']):
                errors.append(f'{prefix}: production edit requires approved source rights and source/mask hashes')
            if production and any(edit[k].startswith('example:') for k in ['source_uri', 'mask_uri']):
                errors.append(f'{prefix}: production edit cannot use example URIs')
        refs = record['references']
        if record['task'] == 'reference' and not refs:
            errors.append(f'{prefix}: reference task requires a reference')
        if len({r['asset_id'] for r in refs}) != len(refs):
            errors.append(f'{prefix}: duplicate reference asset ID')
        history = []
        for ref in refs:
            if production and (ref['rights']['status'] != 'approved' or not ref['sha256'] or ref['uri'].startswith('example:')):
                errors.append(f'{prefix}: production reference requires approved rights, content hash and actual URI')
            if not set(ref['subject_ids']).issubset(record['subjects']) or not set(ref['shot_ids']).issubset(record['shot_ids']):
                errors.append(f'{prefix}: reference binding names an unknown subject/shot')
            if ref['role'] in {'identity', 'appearance', 'voice'} and not ref['subject_ids']:
                errors.append(f'{prefix}: subject reference needs a subject binding')
            interval(ref['start_ms'], ref['end_ms'], point=ref['modality'] == 'image')
            if ref['role'] == 'history':
                history.append(ref)
                if record['task'] != 'continuation':
                    errors.append(f'{prefix}: history reference is reserved for continuation')
                elif ref['source_group'] != record['source_group'] or ref['end_ms'] > record['history_cutoff_ms']:
                    errors.append(f'{prefix}: history contains future frames or a different source timeline')
        if record['task'] == 'continuation':
            if not history or record['history_cutoff_ms'] > media['source_start_ms']:
                errors.append(f'{prefix}: continuation requires past-only history before target start')
        groups = [('source', record['source_group']), ('dedupe', record['dedupe_group'])]
        if record['provenance']['media_sha256']:
            groups.append(('content', record['provenance']['media_sha256']))
        for ref in refs:
            groups.extend([('source', ref['source_group']), ('dedupe', ref['dedupe_group'])])
            if ref['sha256']:
                groups.append(('content', ref['sha256']))
        if record['task'] == 'edit':
            edit = record['edit']
            groups.extend([('source', edit['source_group']), ('dedupe', edit['dedupe_group'])])
            if edit['source_sha256']:
                groups.append(('content', edit['source_sha256']))
        if split_policy == 'identity-disjoint':
            if not record['identity_groups']:
                errors.append(f'{prefix}: identity-disjoint evaluation requires identity groups')
            groups.extend(('identity', g) for g in record['identity_groups'])
            groups.extend(('identity', g) for r in refs for g in r['identity_groups'])
        for group in groups:
            old = owners.setdefault(group, (record['split'], rid))
            if old[0] != record['split']:
                errors.append(f'{prefix}: split leakage via {group[0]}={group[1]} shared with {old[1]}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--split-policy', choices=['source-disjoint', 'identity-disjoint'], default='source-disjoint')
    args = parser.parse_args()
    try:
        records = [json.loads(line) for line in args.records.read_text(encoding='utf-8').splitlines() if line.strip()]
        errors = validate_records(records, production=args.production, split_policy=args.split_policy)
    except (OSError, ValueError, ImportError) as exc:
        print(f'ERROR: {exc}')
        return 1
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        return 1
    print(f'OK: {len(records)} metadata records; {args.split_policy}; production={args.production}. Media and annotation truth were not checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
