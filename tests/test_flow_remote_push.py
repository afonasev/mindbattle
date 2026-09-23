"""The delivery gate must check a real remote feature ref, not a local assertion."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.flow import Flow


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


class RemotePushGate(unittest.TestCase):
    def test_merge_requires_matching_pushed_feature_tip(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            remote = base / 'remote.git'
            repo = base / 'code'
            remote.mkdir()
            repo.mkdir()
            git(remote, 'init', '--bare')
            git(repo, 'init', '-b', 'main')
            git(repo, 'config', 'user.email', 'test@example.com')
            git(repo, 'config', 'user.name', 'Test')
            git(repo, 'remote', 'add', 'origin', str(remote))
            (repo / 'README.md').write_text('test\n')
            git(repo, 'add', 'README.md')
            git(repo, 'commit', '-m', 'initial')
            commit = git(repo, 'rev-parse', 'HEAD')
            change = repo / 'openspec' / 'changes' / 'demo'
            change.mkdir(parents=True)
            (change / '.openspec.yaml').write_text('schema: flow-standard\n')
            flow = Flow(repo)
            flow.init('demo')
            path, record = flow.get('demo')
            record['stage'] = 'verified'
            record['evidence']['merge'] = {'repo': str(repo), 'commit': commit, 'main_ref': 'main'}
            flow.save(path, record, 'test-fixture')
            with self.assertRaisesRegex(ValueError, 'Missing evidence: remote_push'):
                flow.transition('demo', 'merged')
            record['evidence']['remote_push'] = {'repo': str(repo), 'remote': 'origin', 'branch': 'codex/demo', 'commit': commit}
            flow.save(path, record, 'test-fixture')
            with self.assertRaisesRegex(ValueError, 'does not match'):
                flow.transition('demo', 'merged')
            git(repo, 'push', 'origin', 'HEAD:refs/heads/codex/demo')
            self.assertEqual(flow.transition('demo', 'merged')['stage'], 'merged')


if __name__ == '__main__':
    unittest.main()
