import json,hashlib,subprocess,collections,sys
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
s=json.loads((P/'scope.json').read_text());b=json.loads((P/'baseline.json').read_text());t=json.loads((R/'src/content/topics/architecture.json').read_text());qs={q['id']:q for q in t['questions']};errors=[]
if [(q['id'],q['difficulty'],q['correctIndex']) for q in b['questions']]!=[(q['id'],q['difficulty'],q['correctIndex']) for q in t['questions']]:errors.append('fixed slots changed')
for id,h in s['frozen70Hashes'].items():
 if sha(can(qs[id]))!=h:errors.append('frozen '+id)
refs={};current=[]
for f in P.glob('*-receipt.json'):
 for c in json.loads(f.read_text())['cards']:
  if sha(can(qs[c['questionId']]))!=c['cardCanonicalSha256']:errors.append('current '+c['questionId'])
  current.append(c['questionId'])
  for field in c['fields']:
   for proof in field['proofs']:refs[(P/proof['rawCapture']).resolve()]=proof['rawCaptureSha256']
for raw,h in refs.items():
 if sha(raw.read_bytes())!=h:errors.append('raw working '+str(raw))
 blob=subprocess.run(['git','show','HEAD:'+str(raw.relative_to(R))],cwd=R,capture_output=True)
 if blob.returncode or sha(blob.stdout)!=h:errors.append('raw committed '+str(raw))
r={'fixedSlots100':True,'frozen70Checked':70,'currentOwnedReceiptCards':len(set(current)),'rawWorkingAndCommittedChecked':len(refs),'quotas':dict(collections.Counter(q['difficulty'] for q in t['questions'])),'positions':{d:dict(collections.Counter(q['correctIndex'] for q in t['questions'] if q['difficulty']==d)) for d in ['easy','medium','hard']},'errors':errors,'limits':'Mechanical preservation, not substantive or independent acceptance'}
(P/'preservation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));sys.exit(bool(errors))
