"""Check failures that could otherwise turn an error page into a cached paper."""
import hashlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('paper_tools', Path(__file__).resolve().parents[1] / 'papers.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
PDF = b'%PDF-1.7\nminimal downloader test fixture\n%%EOF\n'


class Response(io.BytesIO):
    def __init__(self, data, length=None):
        super().__init__(data)
        self.headers = {'Content-Length': str(len(data) if length is None else length)}


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.paper = {'id': 'example', 'arxiv_version': 'v1', 'pdf_url': 'https://example.org/paper.pdf', 'file_check': {'sha256': hashlib.sha256(PDF).hexdigest()}}

    def tearDown(self):
        self.directory.cleanup()

    def test_valid_download_and_cache_reuse(self):
        path = MODULE.download(self.paper, self.root, lambda *a, **kw: Response(PDF))
        self.assertEqual(path.read_bytes(), PDF)
        MODULE.download(self.paper, self.root, lambda *a, **kw: self.fail('Cached PDF should be reused'))

    def test_html_and_truncated_responses_leave_no_cache(self):
        for payload, length in [(b'<html>Error</html>', None), (PDF, len(PDF) + 100), (PDF[:-7], None)]:
            with self.subTest(payload=payload, length=length):
                with self.assertRaises(ValueError):
                    MODULE.download(self.paper, self.root, lambda *a, **kw: Response(payload, length))
                self.assertFalse(list(self.root.iterdir()))

    def test_different_edition_is_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            MODULE.download(self.paper, self.root, lambda *a, **kw: Response(PDF.replace(b'1.7', b'1.6')))
        self.assertFalse(list(self.root.iterdir()))

    def test_corrupt_cache_is_not_silently_reused(self):
        MODULE.cache_path(self.paper, self.root).write_bytes(b'not a pdf')
        with self.assertRaises(ValueError):
            MODULE.download(self.paper, self.root, lambda *a, **kw: self.fail('Inspect corrupt cache before replacing it'))


if __name__ == '__main__':
    unittest.main()
