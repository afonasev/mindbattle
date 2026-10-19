"""Technical completion must not masquerade as deployed software."""
from pathlib import Path
import tempfile
import unittest

from tools.flow import Flow


class PendingDeploy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'openspec/changes').mkdir(parents=True)
        self.flow = Flow(self.root)
        self.new('software')
        path, record = self.flow.get('software')
        record.update(stage='merged', owner='worker')
        record['evidence'].update(commit='implementation', merge={'commit': 'integrated'})
        self.flow.save(path, record, 'fixture')

    def new(self, cid):
        path = self.root / 'openspec/changes' / cid
        path.mkdir()
        (path / '.openspec.yaml').write_text('schema: flow-quick\n')
        self.flow.init(cid, route='quick')

    def pending(self):
        return {'status': 'pending', 'commit': 'integrated', 'environment': 'production',
                'reason': 'Publication not authorized', 'authorization_source': 'user policy decision',
                'next_step': 'Human authorizes deployment of integrated to production'}

    def finalize(self):
        path, _ = self.flow.get('software')
        (path.parent / 'acceptance.md').write_text('Review source revision; deployment pending.')
        self.flow.evidence('software', 'acceptance_guide', 'acceptance.md')
        for key in ['spec_sync', 'cleanup']:
            self.flow.evidence('software', key, {'result': 'verified'})
        return self.flow.finalize('software', 'worker')

    def start(self):
        self.flow.evidence('software', 'pending_deploy', self.pending())
        self.flow.transition('software', 'finalizing', 'worker')

    def test_pending_is_bound_to_merge_and_requires_explicit_record(self):
        with self.assertRaisesRegex(ValueError, 'must be an object'):
            self.flow.evidence('software', 'pending_deploy', 'pending')
        for key, value in [('commit', 'stale'), ('status', 'deployed'), ('reason', ''),
                           ('authorization_source', ''), ('environment', ''), ('next_step', '')]:
            with self.subTest(key=key):
                pending = self.pending()
                pending[key] = value
                self.flow.evidence('software', 'pending_deploy', pending)
                with self.assertRaisesRegex(ValueError, 'pending_deploy'):
                    self.flow.transition('software', 'finalizing', 'worker')

    def test_finalize_accept_and_restart_keep_deploy_visible_and_dependencies_blocked(self):
        self.start()
        self.assertEqual(self.finalize()['stage'], 'awaiting-acceptance')
        self.flow.accept('software', 'Accepted source work', 'user message', 'implementation', 'Source only')
        self.flow.finalize('software')
        self.flow = Flow(self.root)
        row = next(row for row in self.flow.inbox() if row['id'] == 'software')
        self.assertEqual(row['stage'], 'accepted')
        self.assertEqual(row['pending_deploy'], self.pending())
        self.assertFalse(row['acceptance'])
        self.assertNotIn('release', self.flow.get('software')[1]['evidence'])
        for threshold in ['delivered', 'accepted']:
            self.new(threshold)
            self.flow.dependency(threshold, 'software', threshold)
            self.flow.evidence(threshold, 'scope', 'approved')
            with self.assertRaisesRegex(ValueError, 'dependency:software'):
                self.flow.transition(threshold, 'ready')
        self.flow.evidence('software', 'archive', {'commit': 'archive-commit'})
        path, _ = self.flow.get('software')
        dest = path.parent.parent / 'archive/2026-10-19-software'
        dest.parent.mkdir()
        path.parent.rename(dest)
        with self.assertRaisesRegex(ValueError, 'Pending deployment'):
            self.flow.transition('software', 'archived')

    def test_stale_pending_record_and_cleanup_still_block_finalization(self):
        self.start()
        self.flow.evidence('software', 'cleanup_pending', {'completed': False})
        with self.assertRaisesRegex(ValueError, 'cleanup-pending'):
            self.finalize()
        self.flow.evidence('software', 'cleanup_pending', {'completed': True})
        self.flow.evidence('software', 'merge', {'commit': 'new-integration'})
        with self.assertRaisesRegex(ValueError, 'invalid-pending-deploy'):
            self.finalize()

    def test_resuming_deploy_requires_new_human_authorization_release_and_smoke(self):
        self.start()
        self.finalize()
        with self.assertRaisesRegex(ValueError, 'Missing evidence: release'):
            self.flow.transition('software', 'deployed')
        self.flow.evidence('software', 'release', {'identity': 'release-1', 'commit': 'integrated'})
        with self.assertRaisesRegex(ValueError, 'Missing evidence: smoke'):
            self.flow.transition('software', 'deployed')
        self.flow.evidence('software', 'smoke', {'result': 'pass', 'release': 'release-1'})
        for authorization in [{}, {'source': ' ', 'commit': 'integrated', 'environment': 'production'},
                              {'source': 'user', 'commit': 'other', 'environment': 'production'},
                              {'source': 'user', 'commit': 'integrated', 'environment': 'test'}]:
            if authorization:
                self.flow.evidence('software', 'deploy_authorization', authorization)
            with self.assertRaisesRegex(ValueError, 'Separate human deploy_authorization'):
                self.flow.transition('software', 'deployed')
        self.flow.evidence('software', 'deploy_authorization',
                           {'source': 'new explicit human command', 'commit': 'integrated', 'environment': 'production'})
        result = self.flow.transition('software', 'deployed')
        self.assertEqual(result['stage'], 'deployed')
        self.assertEqual(result['evidence']['pending_deploy']['status'], 'deployed')
        self.assertIsNone(self.flow.inbox()[0]['pending_deploy'])


if __name__ == '__main__':
    unittest.main()
