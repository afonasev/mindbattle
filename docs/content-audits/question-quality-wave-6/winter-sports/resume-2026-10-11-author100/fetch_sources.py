import urllib.request,json,hashlib,concurrent.futures,datetime
from pathlib import Path
ROOT=Path(__file__).parent
urls={s:'https://olympic.ca/sports/'+s+'/' for s in ['alpine-skiing','cross-country-skiing','figure-skating','ice-hockey','snowboard','ski-jumping','nordic-combined','freestyle-skiing','biathlon','speed-skating','short-track-speed-skating','bobsleigh','skeleton','luge']}
urls['curling']='https://worldcurling.org/about/curling/'
def fetch(item):
 name,url=item;dest=ROOT/'sources'/f'{name}.html'
 if dest.exists():return name,'exists'
 try:
  import subprocess
  result=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','45','--output',str(dest),'--write-out','%{http_code} %{content_type} %{url_effective}',url],capture_output=True,text=True)
  if result.returncode: return name,result.stderr
  body=dest.read_bytes();meta={'url':url,'curlReadback':result.stdout,'fetchedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'method':'curl verified HTTPS full response bytes, no content selection'}
  dest.with_suffix('.http.json').write_text(json.dumps(meta,indent=2)+'\n');return name,len(body)
 except Exception as e:return name,str(e)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for result in pool.map(fetch,urls.items()):print(result)
