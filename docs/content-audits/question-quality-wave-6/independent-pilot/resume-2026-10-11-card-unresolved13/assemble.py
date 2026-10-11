"""Serialize manually authored independent decisions; no inferred verdicts."""
import copy, hashlib, json, os
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
AUTHOR=REPO/'docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-unresolved13'
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
a=json.loads((AUTHOR/'author13.json').read_text())
t=json.loads((REPO/'src/content/topics/card-games.json').read_text())
d=json.loads((HERE/'decisions.json').read_text())
rows=[]
for decision in d:
 old=next(c for c in a['cards'] if c['questionId']==decision['questionId'])
 card=next(c for c in t['questions'] if c['id']==decision['questionId'])
 assert sha(canon(card))==old['cardCanonicalSha256'], 'Frozen card changed'
 row={'questionId':card['id'],'cardCanonicalSha256':sha(canon(card)),'verdict':decision['verdict'],'editorialAnalysis':decision['editorialAnalysis'],'fields':[]}
 for name, verdict, analysis in decision['fields']:
  oldfield=next(f for f in old['fields'] if f['field']==name)
  literal=[card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']] if name=='prompt-key' else card['explanation'] if name=='explanation' else card['answers'][int(name[-1])]['note']
  data=canon(literal) if name=='prompt-key' else literal.encode()
  proofs=copy.deepcopy(oldfield['proofs'])
  for pr in proofs:
   raw=(AUTHOR/pr['rawCapture']).resolve()
   assert sha(raw.read_bytes())==pr['rawCaptureSha256']
   pr['rawCapture']=os.path.relpath(raw,HERE)
   pr['independentReader']='01a12bb5-50b0-7e92-bdb2-31b665722c9d'
  row['fields'].append({'field':name,'literal':literal,'literalSha256':sha(data),'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis,'proofs':proofs})
 rows.append(row)
r={'role':'independent','agentIdentity':'01a12bb5-50b0-7e92-bdb2-31b665722c9d','authorIdentity':a['agentIdentity'],'date':'2026-10-11','frozenAuthorCommit':'e2ac59d','method':'Each literal, answer substitution and original source context was read by this independent reader. Source proof pointers are reused after actual rereading; decisions are explicitly authored in decisions.json. No inherited author verdicts. No root certification.','cards':rows}
name='pilot5.json' if len(rows)==5 else 'independent13.json'
(HERE/name).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(name,len(rows))
