"""Read bound originals and current literals; never creates decisions."""
import json,sys
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[5]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23'
r=json.loads((AUTHOR/'author23.json').read_text())
cards={x['id']:x for x in json.loads((ROOT/'src/content/topics/card-games.json').read_text())['questions']}
class T(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden:self.parts.append(d)
seen=set()
for row in r['cards'][int(sys.argv[1]):int(sys.argv[2])]:
 c=cards[row['questionId']];print('\nCARD',json.dumps(c,ensure_ascii=False,indent=2))
 for f in row['fields']:
  print('FIELD',f['field'])
  for p in f['proofs']:
   path=(AUTHOR/p['rawCapture']).resolve();key=(str(path),json.dumps(p['locator']),p['passage'])
   print('BOUND',path.name,p['locator'])
   if key in seen:print('(already displayed in this batch)');continue
   seen.add(key)
   if path.suffix=='.pdf':s=PdfReader(path).pages[p['locator']['pdfPage']-1].extract_text()
   else:
    s=path.read_text()
    if path.suffix=='.html':t=T();t.feed(s);s=' '.join(t.parts)
   s=' '.join(s.split());q=' '.join(p['passage'].split());pos=s.find(q)
   if pos<0:print('PASSAGE MISSING / VISUAL',q);continue
   print('RAW CONTEXT:',s[max(0,pos-240):pos+len(q)+300])
