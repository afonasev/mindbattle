"""Exact current author/reader preservation, never automated quality grading."""
import json, hashlib, subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
OUT=BASE/'coordinator-continuation-01a13100'
AP=BASE/'winter-sports/repair8-2026-10-12-author-01a13060/author-review-v1.json'
RP=BASE/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current-repair8-8941ff8/reader-receipt.json'
IDS=['winter-sports-'+s for s in ['076','082','090','091','095','100']]
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
assert AP.read_bytes()==frozen('8941ff8',AP)==frozen('HEAD',AP)
assert RP.read_bytes()==frozen('ea92a04',RP)==frozen('HEAD',RP)
assert sha(AP.read_bytes())=='447aadf9375a8cc2c82094b551dd46a5ed603408ee331502ebb2b345a8805f69'
a,r=json.loads(AP.read_text()),json.loads(RP.read_text())
assert a['authorNativeId']==r['authorIdentity']=='01a13060-e844-7f11-968f-06d10ca1b229'
assert r['readerIdentity']=='01a12f3d-8ec1-78b3-b153-5f2a62967421'!=r['authorIdentity']
assert r['authorReceiptSHA256']==sha(AP.read_bytes())
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']}
class Visible(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=[];self.nodes=[]
    def handle_starttag(self,t,attrs):
        if t.lower() in ('script','style'):self.skip.append(t.lower())
    def handle_endtag(self,t):
        if t.lower() in self.skip:self.skip.pop()
    def handle_data(self,d):
        if not self.skip and d.strip():self.nodes.append(' '.join(d.split()))
sources={s['id']:s for s in r['rawSources']};contexts={};sourceproof=[]
for sid,s in sources.items():
    path=ROOT/s['capturePath'];raw=path.read_bytes()
    assert raw==frozen('8941ff8',path)==frozen('ea92a04',path)==frozen('HEAD',path)
    assert len(raw)==s['rawByteLength'] and sha(raw)==s['rawSha256']
    assert subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()==s['gitBlobSha1']
    if s.get('physicalPageCount'):contexts[sid]=PdfReader(path,strict=False)
    else:
        parser=Visible();parser.feed(raw.decode());contexts[sid]=' '.join(parser.nodes)
    sourceproof.append({'id':sid,'path':s['capturePath'],'rawSHA256':sha(raw),'gitBlob':s['gitBlobSha1']})
records=[];pagecache={}
for qid in IDS:
    q=qs[qid];ac=next(c for c in a['cards'] if c['id']==qid);rc=next(c for c in r['cards'] if c['id']==qid)
    assert q==ac['cardSnapshot'] and sha(cj(q))==ac['wholeCardCanonicalSha256']==rc['canonicalCardSHA256']
    assert rc['wholeSourceVerdict']==rc['wholeEditorialVerdict']==rc['wholeVerdict']=='PASS'
    expected={'prompt-answers-key':{'prompt':q['prompt'],'orderedAnswerTexts':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex'],'correctAnswerText':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'],**{'note'+str(i):v['note'] for i,v in enumerate(q['answers'])}}
    assert [g['group'] for g in ac['groups']]==[g['group'] for g in rc['fields']]==list(expected)
    for ag,rg in zip(ac['groups'],rc['fields']):
        name=ag['group'];literal=expected[name]
        assert literal==ag['nativeLiteral']==rg['currentNativeLiteral']
        assert sha(cj(literal))==ag['literalSha256']==rg['canonicalJSONSHA256']
        assert ag['sourceReason'] and ag['editorialReason'] and rg['manualSourceReason'] and rg['manualEditorialReason']
        assert rg['sourceVerdict']==rg['editorialVerdict']=='PASS'
        proofs=[]
        for p in rg['sourceProofs']:
            s=p['source'];sid=s['id'];assert s['rawSha256']==sources[sid]['rawSha256'] and s['capturePath']==sources[sid]['capturePath']
            ip=p['actualProof']
            if ip['kind']=='PDFCollapsedUnicode':
                key=(sid,ip['physicalPage1'])
                if key not in pagecache:pagecache[key]=' '.join(contexts[sid].pages[key[1]-1].extract_text().split())
                text=pagecache[key]
            else:text=contexts[sid]
            assert sha(text.encode())==ip['contextSHA256']
            start=ip['codepointOffset0'];quote=text[start:start+ip['codepointLength']]
            assert quote==ip['exactDerivedQuote']==p['historicalQuote'] and sha(quote.encode())==p['historicalQuoteUTF8SHA256']==ip['derivedQuoteUTF8SHA256']
            ab=next(b for b in ag['sourceBindings'] if b['quoteId']==p['quoteId'])
            assert ab['exactQuote']==quote and ab['quoteSha256']==sha(quote.encode()) and ab['rawSha256']==s['rawSha256']
            proofs.append({'quoteId':p['quoteId'],'sourceSHA256':s['rawSha256'],'quoteSHA256':sha(quote.encode()),'contextSHA256':ip['contextSHA256'],'offset':start})
        records.append({'id':qid,'group':name,'cardSHA256':sha(cj(q)),'literalSHA256':sha(cj(literal)),'proofs':proofs})
report={'purpose':'Exact preservation, manual adjudication is separate','ids':IDS,'roleGroups':72,'authorCommit':'8941ff8','readerCommit':'ea92a04','authorReceiptSHA256':sha(AP.read_bytes()),'readerReceiptSHA256':sha(RP.read_bytes()),'originals':sourceproof,'bindings':records,'errors':0,'pendingQAFormat':['winter-sports-076','winter-sports-098'],'notCertified':['winter-sports-089','winter-sports-097']}
(OUT/'winter6-current-pair-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'cards':6,'roleGroups':72,'readerQuoteBindings':sum(len(x['proofs']) for x in records),'fullOriginals':len(sources),'PDFPages':len(pagecache),'errors':0})
