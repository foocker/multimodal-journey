from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from training_data import ROOT, validate_records


class TrainingDataChecks(unittest.TestCase):
    def setUp(self):
        self.rows = [json.loads(s) for s in (ROOT / 'datasets/recipes/audio-video-production/example-records.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]

    def test_format_examples_pass_but_production_rejects(self):
        self.assertEqual(validate_records(self.rows), [])
        self.assertTrue(any('production' in e for e in validate_records(self.rows, production=True)))

    def test_target_and_reference_sources_cannot_cross_splits(self):
        a = copy.deepcopy(self.rows[0])
        b = copy.deepcopy(a)
        for row in [a, b]:
            row.update(kind='licensed_source', split='train')
            row['rights']['status'] = 'approved'
        b.update(record_id='different-target', source_group='different-source', dedupe_group='different-dup', split='test')
        # Only the reference source is shared: this still contaminates held-out inputs.
        errors = validate_records([a, b])
        self.assertTrue(any('split leakage' in e and 'fictional-reference-a' in e for e in errors))

    def test_future_history_is_rejected(self):
        row = copy.deepcopy(self.rows[2])
        row['references'][0]['end_ms'] = 3100
        self.assertTrue(any('future' in e for e in validate_records([row])))

    def test_bad_time_and_unknown_binding_are_rejected(self):
        self.rows[1]['edit']['end_ms'] = 8000
        self.rows[0]['references'][0]['subject_ids'] = ['missing']
        errors = validate_records(self.rows)
        self.assertTrue(any('time interval' in e for e in errors))
        self.assertTrue(any('unknown subject' in e for e in errors))

    def test_identity_policy_is_distinct_from_source_policy(self):
        a, b = copy.deepcopy(self.rows[0]), copy.deepcopy(self.rows[0])
        for row in [a, b]:
            row.update(kind='licensed_source', split='train')
            row['rights']['status'] = 'approved'
            row['references'] = []
            row['task'] = 't2v'
        b.update(record_id='new', source_group='new-source', dedupe_group='new-dup', split='test')
        self.assertEqual(validate_records([a, b]), [])
        self.assertTrue(any('identity=' in e for e in validate_records([a, b], split_policy='identity-disjoint')))

    def test_nan_and_missing_audio_metadata_fail(self):
        self.rows[0]['media']['fps'] = float('nan')
        self.rows[1]['media']['audio_sample_rate'] = None
        errors = validate_records(self.rows)
        self.assertTrue(any('non-finite' in e for e in errors))
        self.assertTrue(any('audio presence' in e for e in errors))

    def test_reference_rights_and_source_hashes_are_checked(self):
        row = copy.deepcopy(self.rows[0])
        row.update(kind='licensed_source', split='train')
        row['rights']['status'] = 'approved'
        row['media']['uri'] = 'object://target'
        row['provenance']['media_sha256'] = 'a' * 64
        ref = row['references'][0]
        ref.update(uri='object://reference', sha256='b' * 64)
        ref['rights']['status'] = 'pending'
        errors = validate_records([row], production=True)
        self.assertTrue(any('production reference' in e for e in errors))
        ref['rights']['status'] = 'approved'
        self.assertEqual(validate_records([row], production=True), [])

    def test_content_hash_catches_relabelled_duplicate(self):
        a, b = copy.deepcopy(self.rows[0]), copy.deepcopy(self.rows[0])
        for row in [a, b]:
            row.update(kind='licensed_source', task='t2v', split='train', references=[])
            row['rights']['status'] = 'approved'
            row['provenance']['media_sha256'] = 'c' * 64
        b.update(record_id='duplicate-content', split='test', source_group='other', dedupe_group='other')
        self.assertTrue(any('content=' in e for e in validate_records([a, b])))


if __name__ == '__main__':
    unittest.main()
