"""Frozen literal/raw/quote preservation only, no quality verdict generation."""
import hashlib
import json
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
OUT=BASE/'coordinator-continuation-01a12f20'
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
compact=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','-C',str(ROOT),'show',rev+':'+str(p.relative_to(ROOT))])
ar=BASE/'winter-sports/resume-2026-10-12-current30-repair/author-correction-after-47690a4-native.json'
rr=BASE/'independent-pilot/resume-2026-10-12-winter-current30-pilot5/independent-reader-current30.json'
rawa,rawr=git('aff2efa',ar),git('8ed8cff',rr)
assert rawa==ar.read_bytes() and rawr==rr.read_bytes()
a,r=json.loads(rawa),json.loads(rawr)
assert a['authorThreadId']==r['authorThreadId']=='01a12f31-8e33-7440-9ae8-7cb9ddddcca6'
assert r['readerThreadId']=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'!=a['authorThreadId']
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']}
class Nodes(HTMLParser):
    def __init__(self):super().__init__();self.nodes=[]
    def handle_data(self,d):self.nodes.append(d)
paths={}; records=[];bindings=0
for ac,rc in zip(a['cards'],r['cards']):
    id=ac['questionId'];assert id==rc['questionId'];q=qs[id]
    assert sha(cj(q))==ac['cardCanonicalSha256']==rc['cardCanonicalSha256']
    assert len(ac['fields'])==len(rc['individualFields'])==6
    for role,card,receipt,raw,rev in [('author',ac,ar,rawa,'aff2efa'),('reader',rc,rr,rawr,'8ed8cff')]:
        for f in card['fields' if role=='author' else 'individualFields']:
            name=f['field'];literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
            assert literal==f['literal'];assert sha(compact(literal) if isinstance(literal,list) else literal.encode())==f['literalSha256']
            for b in f['proofBindings' if role=='author' else 'sourceProofs']:
                p=b['rawCapture' if role=='author' else 'rawPath'];cap=ROOT/p; data=cap.read_bytes()
                assert data==git(rev,cap)==git('HEAD',cap)
                assert sha(data)==b['rawSha256' if role=='author' else 'sha256']
                blob=subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(cap)],text=True).strip()
                assert blob==b['gitBlobCandidate' if role=='author' else 'gitBlob']
                if p not in paths:
                    if p.endswith('.pdf'):text=[page.extract_text() for page in PdfReader(cap).pages]
                    else:parser=Nodes();parser.feed(data.decode());text=parser.nodes
                    paths[p]=text
                loc=b['locator'];text=paths[p][loc['pdfPhysicalPage']-1 if p.endswith('.pdf') else loc['htmlTextNodeIndex0Based']]
                quote=b['exactQuote'];assert sha(quote.encode())==b['exactQuoteSha256'];assert ' '.join(quote.split()) in ' '.join(text.split())
                bindings+=1
            records.append({'questionId':id,'actualRole':role,'actualThreadId':a['authorThreadId'] if role=='author' else r['readerThreadId'],'receipt':str(receipt.relative_to(ROOT)),'receiptCommit':rev,'receiptSha256':sha(raw),'cardCanonicalSha256':sha(cj(q)),'field':name,'nativeField':f})
result={'purpose':'Preservation only, manual quality decisions separate','cards':5,'roleFields':len(records),'quoteBindings':bindings,'originals':list(paths),'records':records,'errors':0}
(OUT/'winter-current5-pair-bindings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print({'cards':5,'roleFields':len(records),'quoteBindings':bindings,'originals':len(paths),'errors':0})
