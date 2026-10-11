"""Apply explicitly authored decisions; bind bytes. No generated substantive verdicts."""
import json,hashlib,pathlib,sys,os,importlib.util
P=pathlib.Path(__file__).resolve().parent
R=P.parents[4]
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('v',P.parents[1]/'verify-proof-format.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
name=sys.argv[1];data=json.loads((P/(name+'-decisions.json')).read_text());topicPath=R/'src/content/topics/architecture.json';topic=json.loads(topicPath.read_text());baseline=json.loads((P/'baseline.json').read_text());byid={q['id']:q for q in topic['questions']};rows=[]
for authored in data:
 q=byid[authored['questionId']];q.update(authored['content']);old=next(x for x in baseline['questions'] if x['id']==q['id'])
 assert all(q[k]==old[k] for k in ['id','difficulty','correctIndex'])
 row={k:authored[k] for k in ['questionId','verdict','editorialAnalysis']};row['cardCanonicalSha256']=sha(canon(q));row['fields']=[]
 for f in authored['fields']:
  field=f['field'];scalar=canon([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]) if field=='prompt-key' else (q['explanation'] if field=='explanation' else q['answers'][int(field[-1])]['note']).encode()
  out={k:f[k] for k in ['field','verdict','substantiveRead','claimAnalysis']};out['literalSha256']=sha(scalar);out['proofs']=[]
  for item in f['proofs']:
   raw=P/item['rawCapture'];body=raw.read_bytes();m=json.loads(pathlib.Path(str(raw)+'.http.json').read_text());assert m['exitCode']==0 and str(m.get('status',m.get('curlResult',''))).startswith('200')
   t=v.Text();t.feed(body.decode());assert ' '.join(item['passage'].split()) in ' '.join(' '.join(t.parts).split())
   out['proofs'].append({**item,'sourceClass':'primary university authored educational reference','title':item.get('title','University of Pittsburgh: Glossary of Medieval Art and Architecture'),'url':m['url'],'rawCaptureSha256':sha(body),'captureFormat':'html original bytes','captureMethod':m['captureMethod'],'passageSha256':sha(item['passage'].encode())})
  row['fields'].append(out)
 rows.append(row)
assert [(q['id'],q['difficulty'],q['correctIndex']) for q in topic['questions']]==[(q['id'],q['difficulty'],q['correctIndex']) for q in baseline['questions']]
topicPath.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n')
(P/(name+'-receipt.json')).write_text(json.dumps({'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'cards':rows,'limits':'Author only; no independent PASS or root certification inferred.'},ensure_ascii=False,indent=2)+'\n')
