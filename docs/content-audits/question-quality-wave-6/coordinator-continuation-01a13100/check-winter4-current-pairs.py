"""Check current paired literal/source preservation. Manual quality is separate."""
import json, hashlib, subprocess
from pathlib import Path
from pypdf import PdfReader
from html.parser import HTMLParser
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6'; OUT=BASE/'coordinator-continuation-01a13100'
AF=BASE/'winter-sports/repair4-2026-10-12-native-01a1312b-54e1-7171-9a1f-b0d31c0c8a56'
RF=BASE/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current-repair4-c522b82'
AP=AF/'author-current-review.json'; SP=AF/'qualification-attestation-2026-10-12.json'; RP=RF/'reader-receipt.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
for p,rev in [(AP,'50a7d10'),(SP,'906bd04'),(RP,'600c3c4')]:assert p.read_bytes()==frozen(rev,p)==frozen('HEAD',p)
a,s,r=[json.loads(p.read_text()) for p in [AP,SP,RP]]
assert a['authorNativeId']==s['authorNativeId']==r['authorIdentity']=='01a1312b-54e1-7171-9a1f-b0d31c0c8a56'
assert r['readerIdentity']=='01a12f3d-8ec1-78b3-b153-5f2a62967421'!=r['authorIdentity']
assert r['authorReceiptSHA256']==s['previousReceiptSha256']==sha(AP.read_bytes())=='f213e3e8010b30e8085a039929553da444bd1fc3a7db889768097f038ec8d244'
assert r['targetedAttestation']['SHA256']==sha(SP.read_bytes())=='c88e900d5653b0211732b0a3881ac0c09d778fe7d7f9c07e50d5ded6f6b74054'
class Visible(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.skip=[];self.nodes=[]
 def handle_starttag(self,t,attrs):
  if t in ('script','style'):self.skip.append(t)
 def handle_endtag(self,t):
  if t in self.skip:self.skip.pop()
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(' '.join(d.split()))
sources={x['sourceId']:x for x in r['rawSources']};ctx={};raws={};pages={}
for sid,src in sources.items():
 p=ROOT/src['raw'];raw=p.read_bytes();assert raw==frozen('50a7d10',p)==frozen('600c3c4',p)==frozen('HEAD',p)
 assert sha(raw)==src['rawSha256'] and len(raw)==src['rawBytes']
 assert subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip()==src['gitBlobSha1'];raws[sid]=raw
 if p.suffix=='.pdf':ctx[sid]=PdfReader(p,strict=False)
 else:
  parser=Visible();parser.feed(raw.decode());ctx[sid]=' '.join(parser.nodes)
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']}
replacement={(g['id'],g['group']):g for g in s['targetedQualifications']};records=[]
for ac,rc in zip(a['cards'],r['cards']):
 ident=ac['id'];assert ident==rc['id'];q=qs[ident]
 assert q==ac['currentCardSnapshot'] and H(q)==ac['wholeCardCanonicalSha256']==rc['canonicalCardSHA256']
 assert rc['wholeSourceVerdict']==rc['wholeEditorialVerdict']==rc['wholeVerdict']=='PASS'
 literals={'prompt-answers-key':{'prompt':q['prompt'],'orderedAnswerTexts':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'correctAnswerText':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'],**{'note'+str(i):x['note'] for i,x in enumerate(q['answers'])}}
 assert [g['group'] for g in ac['groups']]==[g['group'] for g in rc['fields']]==list(literals)
 for original,rg in zip(ac['groups'],rc['fields']):
  g=replacement.get((ident,original['group']),original);name=g['group'];lit=literals[name]
  assert lit==g['currentNativeLiteral']==rg['currentNativeLiteral'] and H(lit)==g['literalSha256']==rg['canonicalJSONSHA256']
  assert rg['sourceVerdict']==rg['editorialVerdict']=='PASS'
  assert g['sourceReason'] and g['editorialReason'] and rg['manualSourceReason'] and rg['manualEditorialReason']
  if name=='prompt-answers-key':
   assert len(rg['individualOrderedAnswerReviews'])==4
   for i,v in enumerate(rg['individualOrderedAnswerReviews']):assert v['index']==i and v['text']==q['answers'][i]['text'] and v['canonicalLiteralSHA256']==H(v['text']) and v['sourceVerdict']==v['editorialVerdict']=='PASS'
  proofs=[]
  for p in rg['sourceProofs']:
   src=p['source'];sid=src['sourceId'];assert src['rawSha256']==sources[sid]['rawSha256'];ip=p['independentProof']
   if ip['kind']=='PDFCollapsedUnicode':
    key=(sid,ip['physicalPage1'])
    if key not in pages:pages[key]=' '.join(ctx[sid].pages[key[1]-1].extract_text().split())
    text=pages[key];ch=ip['collapsedPageSHA256']
   else:text=ctx[sid];ch=ip['contextSHA256']
   assert sha(text.encode())==ch
   offset=ip['codepointOffset0'];quote=text[offset:offset+ip['codepointLength']]
   assert quote==ip['exactDerivedQuote']==p['historicalQuote'] and sha(quote.encode())==ip['quoteUTF8SHA256']==p['historicalExactUTF8SHA256']
   bound=[b for b in g['sourceBindings'] if b['rawSha256']==src['rawSha256']]
   authorquotes=[(aq,ah) for b in bound for aq,ah in zip(b['exactSourceQuotes'],b['quoteSha256']) if quote in aq or aq in quote]
   assert authorquotes, (ident,name,quote)
   for aq,ah in authorquotes:assert sha(aq.encode())==ah and aq in text
   proofs.append({'sourceSHA256':src['rawSha256'],'quoteSHA256':sha(quote.encode()),'contextSHA256':ch,'offset':offset,'readerExactQuote':quote,'authorBoundExactQuotes':[{'quote':aq,'SHA256':ah} for aq,ah in authorquotes],'relation':'independently exact same original passage; each declared quote remains unchanged'})
  records.append({'id':ident,'group':name,'cardSHA256':H(q),'literalSHA256':H(lit),'proofs':proofs})
assert len(records)==24
report={'purpose':'Exact paired preservation; quality requires separate manual adjudication','author':'50a7d10','actualTargetedAttestation':'906bd04','reader':'600c3c4','authorNativeId':a['authorNativeId'],'readerNativeId':r['readerIdentity'],'authorReceiptSHA256':sha(AP.read_bytes()),'attestationSHA256':sha(SP.read_bytes()),'readerReceiptSHA256':sha(RP.read_bytes()),'roleGroups':48,'bindings':records,'fullOriginals':len(sources),'errors':0,'newUniqueIds':['winter-sports-089','winter-sports-097'],'rebindingsWithoutRepeatedCredit':['winter-sports-076','winter-sports-098']}
(OUT/'winter4-current-pair-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'cards':4,'roleGroups':48,'sourceQuoteBindings':sum(len(g['proofs']) for g in records),'errors':0})
