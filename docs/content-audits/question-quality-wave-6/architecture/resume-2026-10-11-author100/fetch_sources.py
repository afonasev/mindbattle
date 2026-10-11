"""Save full HTTP originals and provenance; creates no substantive verdicts."""
import urllib.request,json,hashlib,pathlib,sys,concurrent.futures,datetime
P=pathlib.Path(__file__).resolve().parent
S=P/'sources';S.mkdir(exist_ok=True)
def fetch(item):
 key,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=45) as r:
   body=r.read(); meta={'requestedUrl':url,'finalUrl':r.url,'status':r.status,'contentType':r.headers.get('Content-Type'),'fetchedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'method':'urllib GET; complete response body retained without transformation'}
  (S/(key+'.html')).write_bytes(body);(S/(key+'.http.json')).write_text(json.dumps(meta,indent=2)+'\n');return key,meta['status'],len(body)
 except Exception as e:return key,str(e)
if __name__=='__main__':
 data=json.loads(pathlib.Path(sys.argv[1]).read_text())
 for row in concurrent.futures.ThreadPoolExecutor(max_workers=6).map(fetch,data.items()):print(row)
