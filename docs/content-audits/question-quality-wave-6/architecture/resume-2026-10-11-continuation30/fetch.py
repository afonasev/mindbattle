import subprocess,json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent/'sources';P.mkdir(exist_ok=True)
urls={'housing.pdf':'https://www.govinfo.gov/content/pkg/GOVPUB-C13-8c9655555fcb9640c8e7742d3b9b7622/pdf/GOVPUB-C13-8c9655555fcb9640c8e7742d3b9b7622.pdf','lehman.html':'https://www.lehman.edu/public-art-bronx/glossary/','dob.html':'https://www.nyc.gov/site/buildings/dob/dob-glossary1.page'}
for name,url in urls.items():
 out=P/name
 if out.exists():continue
 r=subprocess.run(['curl','-L','--max-time','45','--silent','--show-error','-o',str(out),'-w','%{http_code}',url],capture_output=True,text=True)
 m={'url':url,'status':r.stdout,'exitCode':r.returncode,'captureMethod':'curl -L complete original server response, no assembly','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':r.stderr,'sha256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None}
 Path(str(out)+'.http.json').write_text(json.dumps(m,indent=2)+'\n');print(name,m['status'],m['exitCode'],out.stat().st_size if out.exists() else 0)
