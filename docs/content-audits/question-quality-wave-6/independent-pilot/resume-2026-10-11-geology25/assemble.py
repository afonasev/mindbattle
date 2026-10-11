"""Bind explicitly authored independent field decisions. Does not choose verdicts."""
import json,hashlib,os,sys,copy
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/geology-earth/resume-2026-10-11-remaining25/author-current.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/geology-earth.json').read_text())['questions']}
refs={c['questionId']:c for c in json.loads(AUTHOR.read_text())['cards']}
decisions=json.loads((OUT/sys.argv[1]).read_text())
r={'role':'independent','agentIdentity':'01a12b37-fb3e-7f63-a4ab-065730cc14f9','readDate':'2026-10-11','freezeCommit':'1e990f2022e83333e249a03632e2d772d8268ec1','limits':['Independent semantic judgments explicitly written in decisions; adapter binds literals and reuses source provenance only, never author judgments.','No root certification or whole-topic stamp.'],'cards':[]}
for d in decisions:
 qid='geology-earth-'+d['id'];q=qs[qid];ref=refs[qid];fs=[]
 literals={'prompt-key':canonical([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]),**{f'note{i}':a['note'].encode() for i,a in enumerate(q['answers'])},'explanation':q['explanation'].encode()}
 for name,(verdict,analysis) in zip(literals,d['fields'],strict=True):
  old=next(f for f in ref['fields'] if f['field']==name);proofs=copy.deepcopy(old['proofs'])
  for p in proofs:
   p['rawCapture']=os.path.relpath((AUTHOR.parent/p['rawCapture']).resolve(),OUT)
   p['independentReading']='Read original source text in this independent session; PDF page or HTML section as located. No author judgment adopted.'
  if (qid.endswith('magma-underground') and name=='note1') or (qid.endswith('pumice-floats') and name=='note3'):
   quote='Tephra\nis the general term now used by volcanologists for airborne volcanic ejecta of\nany size.'
   body=(OUT/'raw/usgs-tephra.html').read_bytes()
   proofs.append({'sourceClass':'primary USGS original institutional publication','title':'USGS Eruptions of Hawaiian Volcanoes — Fragmental volcanic products','url':'https://pubs.usgs.gov/gip/hawaii/page40.html','rawCapture':'raw/usgs-tephra.html','rawCaptureSha256':sha(body),'captureFormat':'html original bytes','captureMethod':'Independent curl -fL original full HTTP body 2026-10-11; 200 text/html 4024 bytes','locator':{'section':'Fragmental volcanic products, first paragraph'},'passage':quote,'passageSha256':sha(quote.encode()),'independentReading':'Actually read complete original HTML text; definition general airborne ejecta any size.'})
  fs.append({'field':name,'literalSha256':sha(literals[name]),'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis,'proofs':proofs})
 r['cards'].append({'questionId':qid,'cardCanonicalSha256':sha(canonical(q)),'verdict':d['verdict'],'editorialAnalysis':d['editorial'],'fields':fs})
(OUT/sys.argv[2]).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
