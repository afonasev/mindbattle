import subprocess,json,hashlib,concurrent.futures,datetime
from pathlib import Path
B=Path(__file__).resolve().parent
urls={'sochi':'https://olympic.ca/games/2014-sochi/','vancouver':'https://olympic.ca/games/2010-vancouver/','turin':'https://olympic.ca/games/2006-turin/','beijing':'https://olympic.ca/games/beijing-2022/','pyeongchang':'https://olympic.ca/games/2018-pyeongchang/','nagano':'https://olympic.ca/games/1998-nagano/','plushenko':'https://www.isu-skating.com/en/figure-skating/skaters/evgeni-plushenko/','gretzky':'https://olympic.ca/team-canada/wayne-gretzky/'}
def fetch(x):
 k,u=x;p=B/'originals'/f'new-{k}.html';r=subprocess.run(['curl','-L','--compressed','--max-time','45','-sS','-o',str(p),'-w','%{http_code} %{content_type} %{url_effective}',u],capture_output=True,text=True);return k,dict(url=u,curlReadback=r.stdout,error=r.stderr,exit=r.returncode,rawCapture='originals/'+p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,fetchedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='curl -L --compressed full original decoded HTTP body without content selection')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:results=dict(e.map(fetch,urls.items()))
(B/'new-http.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v['curlReadback'] for k,v in results.items()},indent=2))
