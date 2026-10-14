import subprocess,json,hashlib,pathlib,datetime
P=pathlib.Path('docs/content-audits/question-quality-wave-7/process-v2-weather20/reviewer/sources');P.mkdir(exist_ok=True)
if (P/'manifest.json').exists():
 raise SystemExit('Existing complete source manifest retained; do not recapture.')
rows=[]
for name,url in [('nws-accretion','https://forecast.weather.gov/glossary.php?word=accretion'),('nws-aggregation','https://forecast.weather.gov/glossary.php?word=aggregation'),('nws-cumulus','https://forecast.weather.gov/glossary.php?word=cumulus')]:
 b=P/(name+'.body');h=P/(name+'.headers')
 r=subprocess.run(['curl','--max-time','30','--retry','0','-sS','-D',str(h),'-o',str(b),url],capture_output=True)
 row={'locator':name,'url':url,'capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempt':1,'exitCode':r.returncode,'stderr':r.stderr.decode(),'body':{'path':str(b),'bytes':b.stat().st_size,'sha256':hashlib.sha256(b.read_bytes()).hexdigest()},'headers':{'path':str(h),'bytes':h.stat().st_size,'sha256':hashlib.sha256(h.read_bytes()).hexdigest()}}
 rows.append(row)
 print(name,b.stat().st_size,r.returncode)
(P/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
