"""Bind explicitly written editorial decisions to current bytes. No generated verdicts."""
import json,hashlib,os,sys
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
name=sys.argv[1];ds=json.loads((P/(name+'-decisions.json')).read_text());topic=R/'src/content/topics/architecture.json';t=json.loads(topic.read_text());baseline=json.loads((P/'baseline.json').read_text());scope=json.loads((P/'scope.json').read_text());byid={q['id']:q for q in t['questions']};rows=[]
for d in ds:
 id=d['questionId'];assert id in scope['owned30'];q=byid[id];q.update(d['content']);row={k:d[k] for k in ['questionId','verdict','editorialAnalysis','fields']};row['cardCanonicalSha256']=sha(can(q))
 for f in row['fields']:
  namef=f['field'];value=can([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]) if namef=='prompt-key' else (q['explanation'] if namef=='explanation' else q['answers'][int(namef[-1])]['note']).encode();f['literalSha256']=sha(value)
 rows.append(row)
assert [(q['id'],q['difficulty'],q['correctIndex']) for q in t['questions']]==[(q['id'],q['difficulty'],q['correctIndex']) for q in baseline['questions']]
assert all(sha(can(byid[id]))==h for id,h in scope['frozen70Hashes'].items())
topic.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n');(P/(name+'-receipt.json')).write_text(json.dumps({'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'cards':rows,'limits':'Current author verdicts only; no independent/root certification.'},ensure_ascii=False,indent=2)+'\n')
