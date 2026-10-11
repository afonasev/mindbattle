"""Mechanical serialization only. Explicit author decisions are in editorial.py.
Never invents/infers PASS, claim analysis, or source passage.
"""
import json,hashlib,sys,copy
from pathlib import Path
from editorial import ROOT,REVISIONS,DECISIONS
from proof_catalog import PROOFS
repo=ROOT.resolve().parents[4]
p=repo/'src/content/topics/card-games.json'
d=json.loads(p.read_text());manifest=json.loads((ROOT/'manifest.json').read_text());allowed=set(manifest['ids'])
assert set(REVISIONS)<=allowed and set(DECISIONS)==set(REVISIONS)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
for c in d['questions']:
 if c['id'] in REVISIONS: c.update(REVISIONS[c['id']])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cards=[]
for c in d['questions']:
 if c['id'] not in DECISIONS:continue
 decision=DECISIONS[c['id']];row={'questionId':c['id'],'cardCanonicalSha256':sha(canon(c)),**{k:decision[k] for k in ['verdict','editorialAnalysis']},'fields':[]}
 literals={'prompt-key':canon([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),**{f'note{i}':a['note'].encode() for i,a in enumerate(c['answers'])},'explanation':c['explanation'].encode()}
 for (name,literal),fd in zip(literals.items(),decision['fields']):
  f={k:fd[k] for k in ['verdict','substantiveRead','claimAnalysis']};f.update(field=name,literalSha256=sha(literal),proofs=[])
  for pid in fd['proofIds']:
   pr=copy.deepcopy(PROOFS[pid]);pr['rawCaptureSha256']=sha((ROOT/pr['rawCapture']).read_bytes());pr['passageSha256']=sha(pr['passage'].encode());pr['role']='author';pr['agentIdentity']='01a12b44-4beb-7aa3-8c23-2916b767b7f1';pr['currentCardSha256']=row['cardCanonicalSha256'];pr['fieldLiteralSha256']=f['literalSha256'];f['proofs'].append(pr)
  row['fields'].append(f)
 cards.append(row)
receipt={'role':'author','agentIdentity':'01a12b44-4beb-7aa3-8c23-2916b767b7f1','date':'2026-10-11','cards':cards,'limits':['Substantive decisions written manually after actual reading; adapter only binds hashes.','Independent review and root certification pending.']}
out=ROOT/sys.argv[1];out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(out,len(cards))
