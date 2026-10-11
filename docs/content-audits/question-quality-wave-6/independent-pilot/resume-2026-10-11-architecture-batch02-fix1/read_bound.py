"""Display current literals and original scalar contents. No substantive verdict creation."""
import json, hashlib, sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[5]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-11-author100'
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,s): self.parts.append(s)
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
rows=[]
for n in ('batch02','pilot-arch-fix1'):
 freeze=json.loads((AUTHOR/(n+'-freeze.json')).read_text()); receipt=json.loads((AUTHOR/freeze['receipt']).read_text()); rows.extend(receipt['cards'])
cards={c['id']:c for c in json.loads((ROOT/'src/content/topics/architecture.json').read_text())['questions']}
seen=set()
for row in rows[int(sys.argv[1]):int(sys.argv[2])]:
 c=cards[row['questionId']]; assert digest(canon(c))==row['cardCanonicalSha256']
 print('\nCARD',json.dumps(c,ensure_ascii=False))
 for f in row['fields']:
  print('FIELD',f['field'])
  for p in f['proofs']:
   raw=AUTHOR/p['rawCapture']; body=raw.read_bytes(); assert digest(body)==p['rawCaptureSha256']
   loc=p['locator']; key=(str(raw),str(loc),p['passage']); print('SOURCE',p['rawCapture'],loc)
   if key in seen: print('Same original passage and surrounding context displayed earlier in this read group'); continue
   seen.add(key)
   if raw.suffix=='.json':
    scalar=json.loads(body)
    for part in loc['jsonPointer'].split('/')[1:]: scalar=scalar[int(part)] if isinstance(scalar,list) else scalar[part]

    quote=p.get('decodedPassage',p['passage']); pos=scalar.find(quote); assert pos>=0
    print('ORIGINAL SCALAR CONTEXT',scalar[max(0,pos-120):pos+len(quote)+180])
   else:
    parser=Text(); parser.feed(body.decode()); print('ORIGINAL TEXT',' '.join(parser.parts))
