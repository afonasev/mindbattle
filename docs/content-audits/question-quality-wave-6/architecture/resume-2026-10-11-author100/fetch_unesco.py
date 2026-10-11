"""Complete original UNESCO JSON records. No verdicts generated."""
import json,pathlib,subprocess,concurrent.futures,hashlib,urllib.parse
P=pathlib.Path(__file__).resolve().parent;S=P/'sources'
def fetch(i):
 name='unesco-'+str(i)+'.json';url='https://data.unesco.org/api/explore/v2.1/catalog/datasets/whc001/records?'+urllib.parse.urlencode({'where':f'id_no="{i}"','limit':1})
 a=subprocess.run(['curl','-L','--max-time','35','-sS','-D',str(S/(name+'.headers')),'-o',str(S/name),'-w','%{http_code}',url],capture_output=True,text=True);b=(S/name).read_bytes();meta={'url':url,'status':a.stdout,'exitCode':a.returncode,'error':a.stderr,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'captureMethod':'curl -L; complete original UNESCO DataHub API JSON response; only id filter, no manual assembly'};(S/(name+'.http.json')).write_text(json.dumps(meta,indent=2)+'\n')
 try:r=json.loads(b)['results'][0];return i,r['name_en'],len(b)
 except Exception:return i,'FAILED',a.stdout,a.stderr
if __name__=='__main__':
 import re
 qs=json.loads((P/'baseline.json').read_text())['questions'];ids={re.search(r'/list/(\d+)',q['source']['url']).group(1) for q in qs if '/list/' in q['source']['url']};ids.update(['252','404','91','86','166','1321','17','687','445'])
 for r in concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,sorted(ids)):print(r,flush=True)
