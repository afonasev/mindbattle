"""Adapters only: preserves explicit author judgments; selects exact original passages and binds hashes."""
import json,hashlib,sys,re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
P=Path(__file__).resolve().parent; ROOT=P.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden:self.parts.append(d)
def proof(key):
 s=library[key];f=P/s['rawCapture'];b=f.read_bytes();loc=s['locator']
 if s.get('visual'):quote=s['visual']
 else:
  if f.suffix=='.pdf':text=PdfReader(f).pages[loc['pdfPage']-1].extract_text()
  elif f.suffix=='.html':parser=Text();parser.feed(b.decode());text=' '.join(parser.parts)
  else:text=b.decode()
  if s.get('exact'):quote=s['exact'];assert quote in text,key
  else:
   # Locate only declared whitespace variants, preserving exact scalar bytes in passage.
   normalized=[];positions=[]
   for m in re.finditer(r'\S+|\s+',text):
    token=' ' if m[0].isspace() else m[0]
    normalized.extend(token);positions.extend([m.start()] if token==' ' else range(m.start(),m.end()))
   nt=''.join(normalized);start=' '.join(s['start'].split());stop=' '.join(s['end'].split())
   a=nt.index(start);z=nt.index(stop,a)+len(stop);quote=text[positions[a]:positions[z-1]+1]
 return {k:v for k,v in s.items() if k not in ('start','end','exact','visual')}|{'passage':quote,'passageSha256':sha(quote.encode()),'rawCaptureSha256':sha(b),'readerRole':'author','proofKey':key}
library=json.loads((P/'passages.json').read_text());judgments=json.loads((P/'judgments.json').read_text());topic=json.loads((ROOT/'src/content/topics/card-games.json').read_text());catalog={c['id']:c for c in topic['questions']};limit=int(sys.argv[1]);rows=[]
for j in judgments[:limit]:
 c=catalog[j['questionId']];fields=[]
 for n,v in j['fields'].items():
  literal=[c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if n=='prompt-key' else c['explanation'] if n=='explanation' else c['answers'][int(n[-1])]['note']
  fields.append({'field':n,'actualLiteral':literal,'literalSha256':sha(canonical(literal) if n=='prompt-key' else literal.encode()),'verdict':v['verdict'],'substantiveRead':True,'claimAnalysis':v['analysis'],'proofs':[proof(k)|{'currentCardCanonicalSha256':sha(canonical(c))} for k in v['proofKeys']]})
 rows.append({'questionId':j['questionId'],'cardCanonicalSha256':sha(canonical(c)),'verdict':j['verdict'],'editorialAnalysis':j['editorialAnalysis'],'fields':fields})
r={'role':'author','agentIdentity':'01a12b13-9e51-76e2-b0aa-6f0e03f539f1','readDate':'2026-10-11','status':'author snapshot only; independent certification pending','cards':rows};(P/('author-pilot5.json' if limit==5 else 'author-current20.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
