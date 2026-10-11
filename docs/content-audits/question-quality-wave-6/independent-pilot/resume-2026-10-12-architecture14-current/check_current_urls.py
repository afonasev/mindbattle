"""HTTP evidence only; no factual or editorial verdicts."""
import json, pathlib, hashlib, subprocess, tempfile, concurrent.futures, datetime
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT.parents[4]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-rework30'
urls=set()
for name in ['pilot5-receipt.json','batch2-4-receipt.json','batch3-2-receipt.json','batch4-3-receipt.json']:
    for c in json.loads((AUTHOR/name).read_bytes())['cards']:
        for f in c['fields']:
            for p in f['proofs']: urls.add(p['url'])
ids=set(json.loads((AUTHOR/'HANDOFF.json').read_bytes())['completedIds'])
for q in json.loads((ROOT/'src/content/topics/architecture.json').read_bytes())['questions']:
    if q['id'] in ids: urls.add(q['source']['url'])
urls.add('https://gramota.ru/meta/pirs')
def capture(url):
    result={'url':url,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'system curl GET -L --max-time20; system certificate verification enabled'}
    try:
        with tempfile.TemporaryDirectory(prefix='architecture14-url-') as temp:
            path=pathlib.Path(temp)/'response'
            r=subprocess.run(['/usr/bin/curl','-sS','-L','--max-time','20','-A','Mozilla/5.0','-o',str(path),'--write-out','%{http_code}\t%{url_effective}\t%{content_type}',url],capture_output=True)
            if r.returncode: raise RuntimeError(r.stderr.decode())
            status, final, content=r.stdout.decode().split('\t'); b=path.read_bytes()
        result.update(status=int(status),finalUrl=final,contentType=content,bytes=len(b),responseSha256=hashlib.sha256(b).hexdigest())
        if url=='https://gramota.ru/meta/pirs':
            (OUT/'sources').mkdir(exist_ok=True); (OUT/'sources/gramota-pirs.html').write_bytes(b)
            result['rawCapture']='sources/gramota-pirs.html'
    except Exception as e: result['error']=str(e)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(capture,sorted(urls)))
(OUT/'current-url-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checked':len(results),'success':sum(r.get('status')==200 for r in results),'failures':[r for r in results if r.get('status')!=200]},ensure_ascii=False))
