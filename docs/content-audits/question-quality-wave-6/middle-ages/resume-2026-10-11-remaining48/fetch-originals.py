"""HTTP capture only; never supplies source eligibility or editorial verdicts."""
import sys,json,hashlib,subprocess,concurrent.futures
from pathlib import Path
R=Path(__file__).resolve().parent/'sources'
def fetch(x):
 name,url=x;path=R/(name+'.html');meta=R/(name+'.http.json')
 if meta.exists(): raise RuntimeError('Do not overwrite capture history: '+name)
 result=subprocess.run(['curl','--compressed','--http1.1','-L','--max-time','40','-sS','-D',str(R/(name+'.headers')),'-o',str(path),'-w','%{http_code} %{url_effective}',url],capture_output=True,text=True)
 info={'url':url,'method':'curl --compressed --http1.1','curlExit':result.returncode,'statusAndFinalUrl':result.stdout,'error':result.stderr,'path':path.name}
 if path.exists():info.update(bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 meta.write_text(json.dumps(info,indent=2)+'\n');return info
if __name__=='__main__':
 for result in concurrent.futures.ThreadPoolExecutor(5).map(fetch,json.load(open(sys.argv[1])).items()):print(json.dumps(result),flush=True)
