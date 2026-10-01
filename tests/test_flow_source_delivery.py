"""Source QA tooling can finalize without inventing a production deployment."""
from pathlib import Path
import tempfile
import unittest
from tools.flow import Flow

class SourceDeliveryGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        change = root / 'openspec/changes/tooling'
        change.mkdir(parents=True)
        (change / '.openspec.yaml').write_text('schema: flow-standard\n')
        self.flow = Flow(root)
        self.flow.init('tooling')
        self.path, self.record = self.flow.get('tooling')
        self.record['stage'] = 'merged'
        self.record['evidence']['merge'] = {'commit': 'reviewed-commit'}
        self.flow.save(self.path, self.record, 'fixture')

    def exemption(self):
        return {'scope': 'qa-tooling', 'runtime_changed': False, 'reason': 'No game artifact changes', 'authorization_source': 'user tooling instruction', 'commit': 'reviewed-commit'}

    def test_runtime_or_missing_exemption_cannot_skip_deploy(self):
        for changes in [None, {'scope': 'ui'}, {'runtime_changed': True}, {'runtime_changed': None}, {'reason': ''}, {'authorization_source': ''}, {'commit': 'stale'}]:
            with self.subTest(changes=changes):
                value = self.exemption() if changes is not None else {'scope': 'unapproved'}
                value.update(changes or {})
                self.flow.evidence('tooling', 'source_only_delivery', value)
                with self.assertRaisesRegex(ValueError, 'Source-only QA tooling'):
                    self.flow.transition('tooling', 'finalizing')

    def test_explicit_source_delivery_retains_pending_human_acceptance(self):
        self.flow.evidence('tooling', 'source_only_delivery', self.exemption())
        self.assertEqual(self.flow.transition('tooling', 'finalizing')['stage'], 'finalizing')
        (self.path.parent / 'acceptance.md').write_text('Review tooling commit')
        self.flow.evidence('tooling', 'commit', 'reviewed-commit')
        self.flow.evidence('tooling', 'acceptance_guide', 'acceptance.md')
        for key in ['spec_sync', 'cleanup']:
            self.flow.evidence('tooling', key, {'path': 'durable/evidence'})
        result = self.flow.finalize('tooling')
        self.assertEqual(result['stage'], 'awaiting-acceptance')
        self.assertEqual(self.flow.acceptance_status(result), 'pending')

if __name__ == '__main__':
    unittest.main()
