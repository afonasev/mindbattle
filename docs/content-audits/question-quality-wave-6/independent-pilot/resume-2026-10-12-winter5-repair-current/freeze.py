import json, subprocess, hashlib, io
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).parent
REV='70863ab'
sha=lambda b:hashlib.sha256(b).hexdigest()
class Visible(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:
   t=' '.join(d.split())
   if t:self.nodes.append(t)
def git(p):return subprocess.check_output(['git','show',f'{REV}:{p}'])
p31='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework31/sources/'
p100='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-11-author100/sources/'
paths=[p31+n for n in ['fis-equipment-2026.pdf','figure-skating.html','long-track.html','hockey-equipment-guide.pdf','biathlon.html','alpine-skiing.html','iihf-terminology.html','maine-ropeway-statute.html','snowboard.html']]+[p100+n for n in ['curling.html','cross-country-skiing.html','ski-jumping.html','bauer-sharpening.html','zamboni-faq-full.html']]+['docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/followup1/sources/white-ice-catalogue-2025.pdf']
(ROOT/'originals').mkdir(exist_ok=True)
manifest=[]
for p in paths:
 b=git(p);name=Path(p).name;dest=ROOT/'originals'/name;dest.write_bytes(b)
 m={'originalGitPath':p,'sourceRevision':subprocess.check_output(['git','rev-parse',REV]).decode().strip(),'frozenPath':str(dest),'rawSha256':sha(b),'bytes':len(b),'gitBlob':subprocess.check_output(['git','rev-parse',f'{REV}:{p}']).decode().strip(),'captureFormat':'complete original PDF bytes' if name.endswith('.pdf') else 'complete original HTML bytes'}
 if name.endswith('.html'):
  h=Visible();h.feed(b.decode('utf8'));m['visibleNodes']=h.nodes
 manifest.append(m)
(ROOT/'source-index.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'.gitattributes').write_text('originals/** -text -diff\nfailed/*.html -text -diff\nfailed/*.pdf -text -diff\n')
for name,p in [('author-receipt-frozen.json','docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/followup1/author-receipt.json'),('current-topic-frozen.json','src/content/topics/winter-sports.json')]: (ROOT/name).write_bytes(git(p))
for m in manifest:
 if 'visibleNodes' in m:
  print('\nSOURCE',Path(m['frozenPath']).name)
  for i,t in enumerate(m['visibleNodes']):
   if (Path(m['frozenPath']).name=='bauer-sharpening.html' and any(s in t.lower() for s in ['sharpen','blade','machine'])) or (Path(m['frozenPath']).name in ['figure-skating.html','biathlon.html','cross-country-skiing.html','alpine-skiing.html','ski-jumping.html'] and 70<=i<=115): print(i,t)
for name,pages in [('fis-equipment-2026.pdf',[11,12,16,24]),('hockey-equipment-guide.pdf',[8]),('white-ice-catalogue-2025.pdf',[])]:
 pdf=PdfReader(ROOT/'originals'/name)
 if not pages:pages=[i+1 for i,p in enumerate(pdf.pages) if 'MARK IV' in p.extract_text().upper() or 'MARKIV' in p.extract_text().upper()]
 for n in pages:print('\nPDF',name,'PAGE',n,'\n',pdf.pages[n-1].extract_text())
