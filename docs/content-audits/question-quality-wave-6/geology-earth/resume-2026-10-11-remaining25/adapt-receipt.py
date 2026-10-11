"""Copies explicit author's decisions; computes identities only. Creates no verdict."""
import hashlib,json,importlib.util
from pathlib import Path
from pypdf import PdfReader
BASE=Path(__file__).resolve().parent
REPO=BASE.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(n):return json.loads((BASE/n).read_text())
spec=importlib.util.spec_from_file_location('verify',REPO/'docs/content-audits/question-quality-wave-6/verify-proof-format.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
readers={}
sources=load('source-selections.json');nodes={}
for key,d in sources.items():
 raw=BASE/d['rawCapture'];b=raw.read_bytes()
 if raw.suffix=='.pdf':
  if str(raw) not in readers:readers[str(raw)]=PdfReader(raw)
  text=readers[str(raw)].pages[d['locator']['pdfPage']-1].extract_text()
 elif raw.suffix=='.html':p=v.Text();p.feed(b.decode());text=' '.join(p.parts)
 else:text=b.decode()
 passage=d.get('passage')
 if passage is None:
  try:
   start=text.index(d['start']);end=text.index(d['end'],start)+len(d['end']);passage=text[start:end]
  except ValueError as error:
   normalized=v.norm(text);begin=normalized.index(v.norm(d['start']));finish=normalized.index(v.norm(d['end']),begin)+len(v.norm(d['end']));passage=normalized[begin:finish]
 assert v.norm(passage) in v.norm(text),key
 nodes[key]={k:val for k,val in d.items() if k not in ('start','end')};nodes[key].update(passage=passage,passageSha256=sha(passage.encode()),rawCaptureSha256=sha(b))
catalog={c['id']:c for c in json.loads((REPO/'src/content/topics/geology-earth.json').read_text())['questions']}
decisions=load('author-decisions.json');cards=[]
for decision in decisions['cards']:
 card=catalog[decision['questionId']];row={k:val for k,val in decision.items() if k!='fields'};row['cardCanonicalSha256']=sha(canon(card));row['fields']=[]
 for f in decision['fields']:
  name=f['field'];literal=canon([card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']]) if name=='prompt-key' else (card['explanation'] if name=='explanation' else card['answers'][int(name[4:])]['note']).encode()
  out={k:val for k,val in f.items() if k!='sourceNodes'};out['literalSha256']=sha(literal);out['proofs']=[nodes[n] for n in f['sourceNodes']];row['fields'].append(out)
 cards.append(row)
receipt={k:val for k,val in decisions.items() if k!='cards'};receipt['cards']=cards
(BASE/'author-current.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print({'copiedExplicitCardDecisions':len(cards),'createdSubstantiveVerdicts':0})
