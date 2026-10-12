"""Preserve frozen native fields and complete sources; no quality grading."""
import json, hashlib, subprocess
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
OUT=BASE/'coordinator-continuation-01a12f20'
ar=OUT/'turn2-remaining25/first5-author-whole6.json'
rr=BASE/'independent-pilot/resume-2026-10-12-winter-current30-pilot5/turn2-first5/independent-reader-current30.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
def frozen(rev,p):return subprocess.check_output(['git','-C',str(ROOT),'show',rev+':'+str(p.relative_to(ROOT))])
rawa,rawr=frozen('f92f42a',ar),frozen('513268e',rr)
assert rawa==ar.read_bytes() and rawr==rr.read_bytes()
a,r=json.loads(rawa),json.loads(rawr)
assert a['authorThreadId']==r['authorThreadId']=='01a12f31-8e33-7440-9ae8-7cb9ddddcca6'
assert r['readerThreadId']=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'!=a['authorThreadId']
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']}
ids=['winter-sports-035','winter-sports-036'];records=[];sources=set();bindingcount=0
for id in ids:
 q=qs[id];ac=next(c for c in a['cards'] if c['questionId']==id);rc=next(c for c in r['cards'] if c['questionId']==id)
 assert sha(cj(q,True))==ac['currentCanonicalSha256']==rc['cardCanonicalSha256']
 for role,c,receipt,raw,rev in [('author',ac,ar,rawa,'f92f42a'),('reader',rc,rr,rawr,'513268e')]:
  fields=c['fields' if role=='author' else 'individualFields'];assert len(fields)==6
  for f in fields:
   name=f['field'];lit=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
   assert lit==f['literal'];assert sha(cj(lit) if isinstance(lit,list) else lit.encode())==f['literalSha256']
   proofs=[]
   for p in f['proofBindings' if role=='author' else 'sourceProofs']:
    path=p['capturePath' if role=='author' else 'rawPath'];cap=ROOT/path;rawsource=cap.read_bytes()
    assert rawsource==frozen(rev,cap)==frozen('HEAD',cap)
    assert sha(rawsource)==p['rawSha256'];assert subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(cap)],text=True).strip()==p['gitBlob']
    assert sha(p['exactQuote'].encode())==p['exactQuoteSha256'];assert p['locator'];sources.add(path);bindingcount+=1
    proofs.append({'source':path,'sourceSha256':sha(rawsource),'gitBlob':p['gitBlob'],'locator':p['locator'],'quoteSha256':p['exactQuoteSha256']})
   records.append({'id':id,'role':role,'threadId':a['authorThreadId'] if role=='author' else r['readerThreadId'],'receipt':str(receipt.relative_to(ROOT)),'receiptCommit':rev,'receiptSha256':sha(raw),'cardSortedSha256':sha(cj(q,True)),'field':name,'literalSha256':f['literalSha256'],'proofs':proofs})
report={'purpose':'Preservation only; manual substantive approval separate','cards':2,'roleFields':24,'quoteBindings':bindingcount,'completeOriginals':sorted(sources),'records':records,'errors':0,'nativeNormalization':'compact sortedwholecard; prompt arraycompact; otherUTF8raw. AuthorSkateCanadaquoteNBSPflattened, reader independentlyexactNBSPquote nativekept.'}
(OUT/'winter-remaining-pass2-pair-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'cards':2,'roleFields':24,'quotes':bindingcount,'completeOriginals':len(sources),'errors':0})
