"""Read-only, exact and bounded coordinator manifest projections."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/manifest_view.py'
SPEC = importlib.util.spec_from_file_location('manifest_view', SCRIPT)
VIEW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VIEW)


class ManifestViewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'manifest.json'
        self.raw = json.dumps({
            'CURRENT': 1148, 'owner': None, 'leaseHeld': False,
            'fences': ['HOLD remains', 'Independent FINAL required'],
            'actors': [{'id': 'reviewer', 'cursor': 'v1'}],
            'a/b': {'~key': 'Сохранено'},
            'history': ['immutable evidence'] * 10000,
        }, ensure_ascii=False).encode('utf-8')
        self.path.write_bytes(self.raw)

    def test_exact_fields_keep_null_false_fences_and_source_identity(self):
        result = json.loads(VIEW.project(self.path, ['/CURRENT', '/owner', '/leaseHeld', '/fences']))
        self.assertEqual(result['fields'], {
            '/CURRENT': 1148, '/owner': None, '/leaseHeld': False,
            '/fences': ['HOLD remains', 'Independent FINAL required'],
        })
        self.assertEqual(result['source'], {'path': str(self.path.resolve()), 'sha256': hashlib.sha256(self.raw).hexdigest()})
        self.assertTrue(result['projectionOnly'])
        self.assertEqual(self.path.read_bytes(), self.raw)
        self.assertLess(len(json.dumps(result)), 1000)

    def test_nested_arrays_and_escaped_pointer_names(self):
        result = json.loads(VIEW.project(self.path, ['/actors/0/cursor', '/a~1b/~0key']))
        self.assertEqual(result['fields'], {'/actors/0/cursor': 'v1', '/a~1b/~0key': 'Сохранено'})

    def test_missing_or_invalid_pointer_never_silently_omits_a_constraint(self):
        for pointer in ['/missing', '/actors/9', '/actors/-1', '/actors/00', '/actors/0/id/x', '/bad~2', 'CURRENT', '']:
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                VIEW.project(self.path, [pointer])
        self.assertEqual(self.path.read_bytes(), self.raw)

    def test_oversized_projection_fails_without_partial_stdout_or_source_mutation(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(self.path), '/history'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('Nothing was truncated', result.stderr)
        self.assertEqual(self.path.read_bytes(), self.raw)

    def test_limit_counts_utf8_output_bytes_and_accepts_exact_boundary(self):
        output = VIEW.project(self.path, ['/a~1b/~0key'])
        self.assertEqual(VIEW.project(self.path, ['/a~1b/~0key'], len(output.encode('utf-8'))), output)
        with self.assertRaises(ValueError):
            VIEW.project(self.path, ['/a~1b/~0key'], len(output.encode('utf-8')) - 1)
        for pointers, limit in [([], 1000), (['/CURRENT'], 0)]:
            with self.assertRaises(ValueError):
                VIEW.project(self.path, pointers, limit)


if __name__ == '__main__':
    unittest.main()
