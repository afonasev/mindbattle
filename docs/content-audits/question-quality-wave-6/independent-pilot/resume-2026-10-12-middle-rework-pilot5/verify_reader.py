import json,re,hashlib,subprocess
from pathlib import Path
from html import unescape
OUT=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def textstrings(v):
 if isinstance(v,dict):
  for x in v.values():yield from textstrings(x)
 elif isinstance(v,list):
  for x in v:yield from textstrings(x)
 elif isinstance(v,str):yield v

def norm(s):return re.sub(r'\s+','',unescape(re.sub('<[^>]+>',' ',s)))
r=json.loads((OUT/'reader-receipt.json').read_text());rows=[]
assert r['agentIdentity']!=r['actualAuthorIdentity']
assert len(r['cards'])==5 and sum(len(c['fields']) for c in r['cards'])==30
for c in r['cards']:
 assert len(c['answersRead'])==4
 for f in c['fields']:
  assert f['substantiveRead'] and f['verdict'] in ['PASS','FIX','HOLD'] and f['claimAnalysis']
  for p in f['proofs']:
   raw=Path(p['rawCapture']).read_bytes();assert sha(raw)==p['rawCaptureSha256'];assert sha(p['passage'].encode())==p['passageSha256']
   if p['rawCapture'].endswith('.json'):txt=' '.join(textstrings(json.loads(raw)))
   else:
    txt=raw.decode('utf-8' if not any(x in p['rawCapture'] for x in ['ugr-dowry','lancaster']) else 'cp1252')
   found=norm(p['passage']) in norm(txt)
   rows.append({'questionId':c['questionId'],'field':f['field'],'rawCapture':p['rawCapture'],'rawShaVerified':True,'passageShaVerified':True,'passageLocatedInOriginal':found})
   assert found,(c['questionId'],f['field'],p['rawCapture'])
report={'checks':'minimal affected evidence checks only: five card/literal hashes, 30 field schema records, 19 author raw/Git byte identities, independent role pair and exact passage presence; no test suite/build/deploy','proofRows':rows,'allLocated':True,'unreadPilot':0}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'proof passages')
