"""Bind existing manually written decisions to current scalars and original captures. Never decides verdicts."""
import json,hashlib,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('format',ROOT/'docs/content-audits/question-quality-wave-6/verify-proof-format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
manual=json.loads((HERE/'manual-review.json').read_text());sources=json.loads((HERE/'source-points.json').read_text());cards={c['id']:c for c in json.loads((ROOT/'src/content/topics/middle-ages.json').read_text())['questions']}
for row in manual['cards']:
 c=cards[row['questionId']];row['cardCanonicalSha256']=sha(canon(c))
 scalars={'prompt-key':canon([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),'explanation':c['explanation'].encode(),**{f'note{i}':a['note'].encode() for i,a in enumerate(c['answers'])}}
 for field in row['fields']:
  field['literalSha256']=sha(scalars[field['field']]);field['proofs']=[]
  for key in field.pop('sourcePoints'):
   proof=dict(sources[key]);proof['rawCaptureSha256']=sha((HERE/proof['rawCapture']).read_bytes());proof['passageSha256']=sha(proof['passage'].encode());proof['boundCardCanonicalSha256']=row['cardCanonicalSha256'];proof['boundFieldLiteralSha256']=field['literalSha256'];proof['readerRole']=manual['role'];proof['readerIdentity']=manual['agentIdentity'];field['proofs'].append(proof)
(HERE/'author-current.json').write_text(json.dumps(manual,ensure_ascii=False,indent=2)+'\n')
