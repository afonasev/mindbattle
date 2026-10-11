"""Read-only source display. Does not assign verdicts or alter catalog/author receipts."""
import json,sys,hashlib
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[5]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-11-author100'
class Text(HTMLParser):
 def __init__(self): super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,s):
  if not self.hidden:self.parts.append(s)
qs=json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions'][:25]
rs={r['questionId']:r for r in json.loads((AUTHOR/'author100-receipt.json').read_text())['cards']}
seen=set()
for q in qs[int(sys.argv[1])-1:int(sys.argv[2])]:
 print('\nCARD',json.dumps(q,ensure_ascii=False))
 for f in rs[q['id']]['fields']:
  print('FIELD',f['field'])
  for p in f['proofs']:
   raw=AUTHOR/p['rawCapture'];sig=(str(raw),p['passageSha256']);print('BOUND',raw.name,p['locator'])
   if sig in seen:print('SAME ACTUAL RAW PASSAGE DISPLAYED ABOVE');continue
   seen.add(sig)
   if raw.suffix=='.pdf': s=PdfReader(raw).pages[p['locator']['pdfPage']-1].extract_text()
   else:
    s=raw.read_text()
    if raw.suffix=='.html': parser=Text();parser.feed(s);s=' '.join(parser.parts)
   s=' '.join(s.split());quoted=' '.join(p['passage'].split());i=s.find(quoted)
   if i<0: print('NO MATCH');continue
   print('ACTUAL RAW EXTRACT WITH CONTEXT:',s[max(0,i-180):i+len(quoted)+180])
