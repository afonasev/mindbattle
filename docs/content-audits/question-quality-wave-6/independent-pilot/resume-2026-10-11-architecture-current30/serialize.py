"""Serialize explicitly written independent decisions; never infer substantive verdicts."""
import json,hashlib,os,sys
from pathlib import Path
OWN=Path(__file__).resolve().parent
REPO=next(p for p in OWN.parents if (p/'src/content/topics/architecture.json').exists())
AUTHOR=REPO/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-11-continuation30'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
name=sys.argv[1]; decisions=json.loads((OWN/(name+'-decisions.json')).read_text());source=json.loads((AUTHOR/('fix5-receipt.json' if name=='pilot' else 'easy25-receipt.json')).read_text()); cards={c['id']:c for c in json.loads((REPO/'src/content/topics/architecture.json').read_text())['questions']}
rows=[]
for row in source['cards']:
 qid=row['questionId']
 if qid not in decisions:continue
 decision=decisions[qid];card=cards[qid]; fields=[]
 assert len(decision['fields'])==6
 for field,analysis in zip(row['fields'],decision['fields']):
  f=field['field'];proofs=[]
  for proof in field['proofs']:
   p=dict(proof);raw=(AUTHOR/p['rawCapture']).resolve();p['rawCapture']=os.path.relpath(raw,OWN);assert sha(raw.read_bytes())==p['rawCaptureSha256'];proofs.append(p)
  literal=canon([card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']]) if f=='prompt-key' else (card['explanation'] if f=='explanation' else card['answers'][int(f[-1])]['note']).encode()
  verdict=decision.get('fieldVerdicts',{}).get(f,'PASS')
  fields.append(dict(field=f,literalSha256=sha(literal),verdict=verdict,substantiveRead=True,claimAnalysis=analysis,proofs=proofs))
 rows.append(dict(questionId=qid,cardCanonicalSha256=sha(canon(card)),verdict=decision['verdict'],editorialAnalysis=decision['editorial'],fields=fields))
out=dict(role='independent',agentIdentity=os.environ['CODEX_THREAD_ID'],method='Independent current field and original source reading. Author proof locators reused only after actual reading; all analyses and decisions authored independently. Serializer does not decide PASS.',cards=rows)
(OWN/(name+'-receipt.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
