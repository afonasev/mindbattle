"""Complete HTTP captures; retain changed responses, reuse byte-identical Git originals."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
AUTHOR = ROOT / 'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/author-receipt.json'
receipt = json.loads(AUTHOR.read_text())
urls = {p['url']: p['rawCapture'] for c in receipt['cards'] for f in c['fields'] for p in f['proofs']}
urls['https://isu-d8g8b4b7ece7aphs.a03.azurefd.net/isudamcontainer/CMS/Corporate-Site/Governance/Isu-Regulations/2026-Speed-Skating-Sports-Rules-20260514-FINAL-as-of-12-June-2026--1--1780932044-4787.pdf'] = None

def capture(item):
    url, old = item
    try:
        with tempfile.NamedTemporaryFile(dir=OUT, suffix='.headers') as headers_file:
            result = subprocess.run(['curl', '-fsSL', '--max-time', '45', '-D', headers_file.name, url], capture_output=True)
            if result.returncode:
                raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
            raw = result.stdout
            headers_file.seek(0)
            headers = headers_file.read().decode('iso-8859-1')
        sha = hashlib.sha256(raw).hexdigest()
        old_sha = hashlib.sha256((ROOT / old).read_bytes()).hexdigest() if old else None
        reused = sha == old_sha
        if reused:
            target = old
        else:
            name = Path(old).name if old else 'isu-speed-skating-rules-2026.pdf'
            path = OUT / 'current-url-originals' / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(raw)
            target = str(path.relative_to(ROOT))
        statuses = [line for line in headers.splitlines() if line.startswith('HTTP/')]
        return {'url': url, 'status': int(statuses[-1].split()[1]),
                'sizeBytes': len(raw), 'sha256': sha, 'rawCapture': target,
                'byteIdenticalToFrozenOriginal': reused, 'frozenOriginalSha256': old_sha,
                'captureMethod': 'curl -fsSL; complete unmodified response body; system TLS verification',
                'headers': headers}
    except Exception as exc:
        return {'url': url, 'error': str(exc), 'status': 'HOLD'}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(capture, sorted(urls.items())))
(OUT / 'current-url-readback.json').write_text(json.dumps({'checkedAt': '2026-10-12', 'sources': results}, ensure_ascii=False, indent=2) + '\n')
for result in results:
    print(result['url'], result['status'], result.get('sizeBytes'), result.get('sha256'), result.get('byteIdenticalToFrozenOriginal'), result.get('error', ''))
