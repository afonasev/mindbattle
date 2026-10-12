"""Current author native/raw roundtrip only, never a quality PASS generator."""
import json, hashlib, subprocess, re
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
OUT=BASE/'coordinator-continuation-01a12f20'
AB=BASE/'winter-sports/resume-2026-10-12-fresh-fix3-remaining15'
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','-C',str(ROOT),'show',rev+':'+str(p.relative_to(ROOT))])
ar=AB/'author-current3-receipt-v2.json';sr=AB/'source-context-v2.json'
rawa,raws=git('f7f7caf',ar),git('f7f7caf',sr)
assert rawa==ar.read_bytes() and raws==sr.read_bytes()
a,s=json.loads(rawa),json.loads(raws)
assert a['authorIdentity']['nativeThreadId']==s['authorThreadId']=='01a12f7f-61a0-7062-904d-bbbb787deefc'
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']}
pdfs={};records=[];sources=set()
for c in a['cards']:
 q=qs[c['questionId']];assert sha(cj(q))==c['cardCanonicalSha256'];assert sha(cj(q,True))==c['sortedCardSha256'];assert len(c['fields'])==6
 for f in c['fields']:
  name=f['field'];lit={'prompt':q['prompt'],'options':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']} if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
  assert lit==f['literal'];assert sha(cj(lit) if isinstance(lit,dict) else lit.encode())==f['literalSha256']
  proofs=[]
  for ref in f['proofs']:
   si,ei=map(int,re.fullmatch(r'source-context-v2.json#sources\[(\d+)\].extracts\[(\d+)\]',ref).groups());src=s['sources'][si];e=src['extracts'][ei];p=ROOT/src['rawCapturePath'];raw=p.read_bytes()
   assert raw==git('f7f7caf',p)==git('HEAD',p);assert len(raw)==src['rawSize'];assert sha(raw)==src['rawSha256'];assert subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(p)],text=True).strip()==src['gitBlob']
   quote=e['exactQuote'];assert sha(quote.encode())==e['exactQuoteSha256'];sources.add(src['rawCapturePath'])
   if str(p) not in pdfs:pdfs[str(p)]=PdfReader(p)
   actual=pdfs[str(p)].pages[e['locator']['pdfPhysicalPage1Based']-1].extract_text();assert quote in actual
   proofs.append({'sourceRef':src['rawCapturePath'],'rawSha256':sha(raw),'gitBlob':src['gitBlob'],'originalURL':src['originalUrl'],'actualCaptureURL':src['captureUrl'],'locator':e['locator'],'quoteSha256':e['exactQuoteSha256']})
  records.append({'id':q['id'],'authorIdentity':a['authorIdentity'],'receipt':str(ar.relative_to(ROOT)),'receiptCommit':'f7f7caf','receiptSha256':sha(rawa),'sourceContextReceiptSha256':sha(raws),'cardNativeSha256':sha(cj(q)),'cardSortedSha256':sha(cj(q,True)),'field':name,'literalSha256':f['literalSha256'],'proofs':proofs})
old={q['id']:q for q in json.loads(git('2fd0941',ROOT/'src/content/topics/winter-sports.json'))['questions']};ids={c['questionId'] for c in a['cards']};assert len(ids)==3
assert all(q==old[id] for id,q in qs.items() if id not in ids)
report={'purpose':'Preservation only, not quality grading','cards':3,'fields':18,'originals':sorted(sources),'records':records,'protected97Unchanged':True,'errors':0}
(OUT/'winter-fresh3-v2-author-roundtrip.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'cards':3,'fields':18,'originals':len(sources),'protected97':True,'errors':0})
