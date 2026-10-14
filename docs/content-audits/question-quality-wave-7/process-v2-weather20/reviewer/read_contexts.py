import json,subprocess,hashlib,re,pathlib
from html.parser import HTMLParser
P=pathlib.Path('docs/content-audits/question-quality-wave-7/process-v2-weather20');R=P/'reviewer'
def git(x):return subprocess.check_output(['git','show',x])
def sha(b):return hashlib.sha256(b).hexdigest()
idx=json.loads(git('12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json'))['primaryContextIndex']
a=json.load(open(P/'author/candidate.json')); keys=set(k for e in a['entries'] for k in e['sourceLocators']);keys|={'nws-radar','nws-radiosonde','nws-ceilometer','nws-key-glossary','nws-occluded','spc-shear'}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.data=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.data.append(d.strip())
texts={};validation=[]
for k in sorted(keys):
 if k in ['noaa-weather-satellites','metoffice-climate-zones']:
  m=next(x for x in json.load(open(P/'author/sources/manifest.json'))['sources'] if x['locator']==k)
  b=git('55db9891:'+str(P/'author/sources'/m['bodyPath']));h=git('55db9891:'+str(P/'author/sources'/m['headersPath']))
  s={'sourceUrl':m['url'],'gitCommit':'55db9891798bcaf38abc20f6ea3b215c0b3e8626','body':{'path':str(P/'author/sources'/m['bodyPath']),'bytes':m['bodyBytes'],'sha256':m['bodySha256']},'headers':{'path':str(P/'author/sources'/m['headersPath']),'bytes':m['headersBytes'],'sha256':m['headersSha256']}}
 else:
  s=idx[k];b=git(s['body']['gitBlob']);h=git(s['headers']['gitBlob'])
 assert len(b)==s['body']['bytes'] and sha(b)==s['body']['sha256'],k
 assert len(h)==s['headers']['bytes'] and sha(h)==s['headers']['sha256'],k
 validation.append({'locator':k,**s,'verifiedBytesAndSHA256':True})
 if b.startswith(b'%PDF'):
  f=R/'source-extraction.pdf';f.write_bytes(b)
  from pypdf import PdfReader
  txt='\n'.join(page.extract_text() for page in PdfReader(f).pages);f.unlink()
 else:
  parser=Text();parser.feed(b.decode('utf-8',errors='replace'));txt='\n'.join(parser.data)
 texts[k]=txt
(R/'context-texts.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2)+'\n')
(R/'source-integrity.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
for k,v in texts.items(): print(k,len(v))
