"""Verify, switch atomically and retain exactly one complete published release."""
import fcntl
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
kind, release = sys.argv[1:]
assert kind in ('content', 'shell', 'installers') and re.fullmatch(r'\d{8}T\d{6}-[a-f0-9]{12}', release)
base = Path('/var/lib/mindbattle-desktop') / kind
with (base / '.publish.lock').open('w') as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    source = base / ('incoming-' + release)
    if kind == 'content':
        envelope = json.loads((source / 'latest.json').read_text())
        manifest = json.loads(envelope['payload'])
        current = base / 'current' / 'latest.json'
        if current.exists():
            assert manifest['sequence'] > json.loads(json.loads(current.read_text())['payload'])['sequence'], 'Sequence must increase'
        entries = [(source / 'objects' / item['sha256'], item) for item in manifest['files']]
    elif kind == 'shell':
        entries = []
        for platform in ('darwin-universal', 'win32-x64'):
            envelope = json.loads((source / platform / 'latest.json').read_text())
            manifest = json.loads(envelope['payload'])
            assert manifest['platform'] == platform
            current = base / 'current' / platform / 'latest.json'
            if current.exists():
                assert manifest['sequence'] > json.loads(json.loads(current.read_text())['payload'])['sequence'], 'Sequence must increase'
            entries.extend((source / 'objects' / item['sha256'], item) for item in manifest['files'])
    else:
        catalog = json.loads((source / 'downloads.json').read_text())
        assert set(catalog) == {'mac', 'windows'}
        entries = []
        for item in catalog.values():
            assert re.fullmatch(r'/desktop/installers/[A-Za-z0-9_.-]+', item['url'])
            entries.append((source / 'installers' / item['url'].rsplit('/', 1)[1], item))
    for file, item in entries:
        assert re.fullmatch(r'[a-f0-9]{64}', item['sha256'])
        assert file.stat().st_size == item['size']
        with file.open('rb') as stream:
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
            assert digest.hexdigest() == item['sha256']
    target = base / ('release-' + release)
    source.rename(target)
    for root, dirs, files in os.walk(target):
        os.chmod(root, 0o755)
        for name in files:
            os.chmod(Path(root) / name, 0o644)
    temporary = base / ('link-' + release)
    temporary.symlink_to(target.name, target_is_directory=True)
    temporary.replace(base / 'current')
    for old in base.glob('release-*'):
        if old != target and old.is_dir() and not old.is_symlink():
            shutil.rmtree(old)
    print(json.dumps({'published': kind, 'release': release, 'path': str(target)}))
