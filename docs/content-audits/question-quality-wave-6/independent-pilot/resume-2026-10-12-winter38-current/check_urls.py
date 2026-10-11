"""Fetch current original URLs; preserve frozen SHA, never substitute it."""
import concurrent.futures,subprocess,hashlib,json,tempfile,os
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent
def one(item):
 path,s=item
 with tempfile.NamedTemporaryFile(prefix='winter38-reader-') as f:
  r=subprocess.run(['curl','--compressed','--http1.1','-L','--max-time','20','-sS','-o',f.name,'-w','%{http_code}\n%{url_effective}\n%{content_type}',s['url']],capture_output=True,text=True)
  parts=r.stdout.split('\n');data=Path(f.name).read_bytes();return {'rawCapture':path,'url':s['url'],'checkedAtUTC':datetime.now(timezone.utc).isoformat(),'exitCode':r.returncode,'httpStatus':parts[0] if parts else '', 'effectiveUrl':parts[1] if len(parts)>1 else '', 'contentType':parts[2] if len(parts)>2 else '', 'responseBytes':len(data),'currentResponseSha256':hashlib.sha256(data).hexdigest(),'frozenRawCaptureSha256':s['rawCaptureSha256'],'currentBytesMatchFrozen':hashlib.sha256(data).hexdigest()==s['rawCaptureSha256'],'stderr':r.stderr.strip(),'method':'curl --compressed --http1.1 -L; complete response; task-owned temporary response deleted after hash; frozen bytes untouched'}
def main():
 d=json.loads((OUT/'originals-and-bindings.json').read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,d['sources'].items()))
 (OUT/'current-url-readback.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 for r in rows:print(r['rawCapture'].split('/')[-1],r['httpStatus'],r['exitCode'],r['contentType'],r['currentBytesMatchFrozen'])
if __name__=='__main__':main()
