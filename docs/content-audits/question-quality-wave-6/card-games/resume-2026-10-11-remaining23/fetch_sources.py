"""Download full original responses, record failures; never creates verdicts."""
import urllib.request,json,hashlib,pathlib,sys,subprocess
root=pathlib.Path(__file__).parent;s=root/'sources';s.mkdir(exist_ok=True)
reg=root/'downloads.json'; rows=json.loads(reg.read_text()) if reg.exists() else []
for name,url in zip(sys.argv[1::2],sys.argv[2::2]):
 try:
  result=subprocess.check_output(['curl','--fail','--location','--silent','--show-error','--max-time','45','--output',str(s/name),'--write-out','%{http_code}\n%{url_effective}\n%{content_type}',url],text=True)
  status,final,ctype=result.split('\n');body=(s/name).read_bytes()
  (s/name).write_bytes(body);row={'file':name,'url':url,'finalUrl':final,'status':status,'contentType':ctype,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
 except Exception as e: row={'file':name,'url':url,'error':str(e)}
 rows.append(row); print(json.dumps(row))
reg.write_text(json.dumps(rows,indent=2)+'\n')
