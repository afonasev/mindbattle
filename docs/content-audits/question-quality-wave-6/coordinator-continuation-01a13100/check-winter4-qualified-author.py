"""Check declared actual freezes and quote/literal integrity; no quality inference."""
import json, hashlib, subprocess, re
from pathlib import Path
from pypdf import PdfReader
from html.parser import HTMLParser

ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
FOLDER=BASE/'winter-sports/repair4-2026-10-12-native-01a1312b-54e1-7171-9a1f-b0d31c0c8a56'
AP=FOLDER/'author-current-review.json'
SP=FOLDER/'qualification-attestation-2026-10-12.json'
OUT=BASE/'coordinator-continuation-01a13100'
sha=lambda b:hashlib.sha256(b).hexdigest()
H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def gitbytes(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
a,s=json.loads(AP.read_text()),json.loads(SP.read_text())
assert AP.read_bytes()==gitbytes('50a7d10',AP)==gitbytes('HEAD',AP)
assert SP.read_bytes()==gitbytes('906bd04',SP)==gitbytes('HEAD',SP)
assert s['previousReceiptSha256']==sha(AP.read_bytes())=='f213e3e8010b30e8085a039929553da444bd1fc3a7db889768097f038ec8d244'
assert a['authorNativeId']==s['authorNativeId']=='01a1312b-54e1-7171-9a1f-b0d31c0c8a56'
runtime=ROOT/a['runtimePath'];assert runtime.read_bytes()==gitbytes('c522b82',runtime)
qs={q['id']:q for q in json.loads(runtime.read_text())['questions']}
scope=json.loads((ROOT/a['scopeFile']).read_text())
assert sha((ROOT/a['scopeFile']).read_bytes())==a['scopeFileSha256']
assert [q['id'] for q in json.loads(runtime.read_text())['questions']]==scope['order']
for p in scope['protected96']:assert H(qs[p['id']])==p['sha256']
for p in scope['scopedBefore']:assert qs[p['id']]['difficulty']==p['difficulty'] and qs[p['id']]['correctIndex']==p['correctIndex']
class Visible(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=[];self.nodes=[]
    def handle_starttag(self,t,attrs):
        if t in ('script','style'):self.skip.append(t)
    def handle_endtag(self,t):
        if t in self.skip:self.skip.pop()
    def handle_data(self,d):
        if not self.skip and d.strip():self.nodes.append(' '.join(d.split()))
replacement={(g['id'],g['group']):g for g in s['targetedQualifications']}
records=[];sources={};cache={}
for c in a['cards']:
    q=qs[c['id']];assert q==c['currentCardSnapshot'] and H(q)==c['wholeCardCanonicalSha256']
    lit={'prompt-answers-key':{'prompt':q['prompt'],'orderedAnswerTexts':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'correctAnswerText':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'],**{'note'+str(i):x['note'] for i,x in enumerate(q['answers'])}}
    assert [g['group'] for g in c['groups']]==list(lit)
    for original in c['groups']:
        key=(c['id'],original['group']);g=replacement.get(key,original)
        assert g['currentNativeLiteral']==lit[g['group']] and g['literalSha256']==H(lit[g['group']])
        assert g['wholeCardCanonicalSha256']==H(q) and g['sourceReason'] and g['editorialReason']
        proofs=[]
        for b in g['sourceBindings']:
            src=ROOT/b['rawCapture'];raw=src.read_bytes()
            assert len(raw)==b['rawByteLength'] and sha(raw)==b['rawSha256']
            assert raw==gitbytes('50a7d10',src)==gitbytes('HEAD',src)
            assert subprocess.check_output(['git','hash-object',str(src)],cwd=ROOT,text=True).strip()==b['gitBlobSha1']
            sources[b['rawCapture']]=b['rawSha256']
            ctx=ROOT/b['selectedFullContext'];assert sha(ctx.read_bytes())==b['selectedFullContextSha256']
            assert ctx.read_bytes()==gitbytes('50a7d10',ctx)==gitbytes('HEAD',ctx)
            if src.suffix=='.pdf':
                loc=re.sub(r'\(printed\s+p\.\d+\)', '', b['locator'])
                pages=[int(x) for x in re.findall(r'\bp\.(\d+)',loc)];assert pages,b['locator']
                if str(src) not in cache:cache[str(src)]=PdfReader(src,strict=False)
                texts=[(p,' '.join(cache[str(src)].pages[p-1].extract_text().split())) for p in pages]
            else:
                parser=Visible();parser.feed(raw.decode());texts=[('HTML',' '.join(parser.nodes))]
            for quote,qhash in zip(b['exactSourceQuotes'],b['quoteSha256']):
                assert sha(quote.encode())==qhash
                found=next(((page,text.find(quote),sha(text.encode())) for page,text in texts if quote in text),None)
                assert found,(c['id'],g['group'],quote,b['locator'])
                proofs.append({'source':b['rawCapture'],'quoteSHA256':qhash,'physicalPage':found[0],'unicodeOffset0':found[1],'contextSHA256':found[2]})
        records.append({'id':c['id'],'group':g['group'],'literalSHA256':g['literalSha256'],'cardSHA256':H(q),'nativeAttestationApplied':key in replacement,'proofs':proofs})
assert len(records)==24 and len(sources)==3
history=[]
for rev in ['c522b82','427dbe3','92eb2d0','50a7d10']:
    b=gitbytes(rev,AP);history.append({'revision':rev,'receiptSHA256':sha(b),'retainedGit':True})
report={'purpose':'Source/literal preservation only, manualeditorial/independentreview separate','authorNativeId':a['authorNativeId'],'runtimeFreeze':'c522b82','actualAuthorReceiptFreeze':'50a7d10','attestationFreeze':'906bd04','declaredActualReceiptSHA256':s['previousReceiptSha256'],'receiptHistory':history,'groups':24,'targetedActualQualifications':3,'protected96':'exact','fullOriginals':sources,'records':records,'errors':0,'independentReview':'NOTRUN','newCredit':0}
(OUT/'winter4-author-qualification-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'groups':24,'targetedQualifications':3,'completeOriginals':3,'quoteBindings':sum(len(x['proofs']) for x in records),'protected96':'exact','errors':0})
