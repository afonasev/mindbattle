"""Verify actual current source/literal pairs. No automatic quality grading."""
import json,hashlib,subprocess,gzip,runpy
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');BASE=ROOT/'docs/content-audits/question-quality-wave-6';OUT=BASE/'coordinator-continuation-01a13100'
AF=BASE/'middle-ages/repair6-2026-10-12-fresh-writable-author-01a13116';RF=BASE/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/middle-current6-f547afe-v4'
AP=AF/'author-review-v4.json';RP=RF/'reader-receipt.json';PT=RF/'independent-source-proofs.json';MT=RF/'all-author-bindings-integrity.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
for p,rev in [(AP,'39c907b'),(RP,'47d7341'),(PT,'47d7341'),(MT,'47d7341')]:assert p.read_bytes()==frozen(rev,p)==frozen('HEAD',p)
a,r=json.loads(AP.read_text()),json.loads(RP.read_text());ps=json.loads(PT.read_text());assign=json.loads(MT.read_text())
assert a['authorNativeId']==r['authorNativeId']=='01a13116-9ab1-7062-9219-08765b2ab65e'
assert r['readerNativeId']=='01a12f3d-8ec1-78b3-b153-5f2a62967421'!=r['authorNativeId'];assert r['authorReceiptSHA256']==sha(AP.read_bytes())
# New reader proof supplies an independent preservation dependency; old author checks rerun only for this pair.
st=runpy.run_path(str(OUT/'check-middle6-v4-author.py'));assert not st['errors']
for src in r['originalSources']:
 p=ROOT/src['path'];container=p.read_bytes();raw=gzip.decompress(container) if src['gzipContainer'] else container
 assert container==frozen('39c907b',p)==frozen('47d7341',p)==frozen('HEAD',p)
 assert len(container)==src['trackedContainerByteLength'] and sha(container)==src['trackedContainerSHA256']
 assert len(raw)==src['rawDecodedByteLength'] and sha(raw)==src['rawDecodedSHA256']
 assert subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip()==src['trackedContainerGitBlobSHA1']
 assert raw==frozen(src['originCommit'],ROOT/src['originRepositoryPath'])
proofs={p['proofId']:p for p in ps}
verified=[]
for pid,p in proofs.items():
 ip=p['independentProof'];src=ip['sourceInfo'];assert p['historicalQuoteIdentityUnchanged'] and sha(p['historicalAuthorQuote'].encode())==p['historicalAuthorQuoteUTF8SHA256']
 if ip['kind']=='ScannedPDFPersonalVisualTranscription':
  img=ROOT/ip['renderPath'];assert img.read_bytes()==frozen('47d7341',img)==frozen('HEAD',img) and sha(img.read_bytes())==ip['renderSHA256'];assert ip['exactPersonalTranscription']==p['historicalAuthorQuote'] and sha(ip['exactPersonalTranscription'].encode())==ip['transcriptionUTF8SHA256']
  v=json.loads((OUT/'middle-v4-coordinator-lapidus-visual-source.json').read_text());assert v['exactObservedQuote']==ip['exactPersonalTranscription'] and v['rawSHA256']==src['rawDecodedSHA256'];verified.append({'proofId':pid,'kind':ip['kind'],'verifiedBy':'actual reader plus coordinator direct pixels, exact original SHA/page locator'});continue
 if ip['kind']=='PDFPageHeaderCompositeUnicode':
  pdf=PdfReader(ROOT/src['path'],strict=False);text='\n\n'.join('===== physical PDF page '+str(n)+' =====\n'+pdf.pages[n-1].extract_text() for n in [21,22,23])+'\n'
  assert text.encode()==(AF/'glasgow-pages21-23-pypdf-derived.txt').read_bytes()==(RF/'glasgow-independent-composite.txt').read_bytes()
 elif ip['kind']=='ExactNativePDFPageUnicode':text=PdfReader(ROOT/src['path'],strict=False).pages[11].extract_text()
 else:
  possible=[t for (path,basis),t in st['contexts'].items() if path==str(ROOT/src['path']) and sha(t.encode())==ip['contextUTF8SHA256']];assert possible,(pid,ip['kind']);text=possible[0]
 assert sha(text.encode())==ip['contextUTF8SHA256'];quote=text[ip['codepointOffset0']:ip['codepointOffset0']+ip['codepointLength']]
 assert quote==ip['exactDerivedQuote']==p['historicalAuthorQuote'] and sha(quote.encode())==ip['quoteUTF8SHA256']==p['historicalAuthorQuoteUTF8SHA256'];verified.append({'proofId':pid,'kind':ip['kind'],'sourceSHA256':src['rawDecodedSHA256'],'contextSHA256':ip['contextUTF8SHA256'],'quoteSHA256':ip['quoteUTF8SHA256']})
for entry in assign:
 b=a
 for k in entry['authorRecordPath'].split('/'):b=b[int(k)] if isinstance(b,list) else b[k]
 p=proofs[entry['proofId']];assert b['quote']==p['historicalAuthorQuote'] and b['quoteSha256']==p['historicalAuthorQuoteUTF8SHA256'];assert b['completeOriginal']['rawSHA256']==p['independentProof']['sourceInfo']['rawDecodedSHA256']
assert len(assign)==120
ids=['middle-ages-'+s for s in ['market-town','toll','dancing-mania','sweating-sickness']];records=[]
for ident in ids:
 ac=next(c for c in a['cards'] if c['id']==ident);rc=next(c for c in r['cards'] if c['id']==ident);q=st['qs'][ident]
 assert q==ac['wholeCard'] and H(q)==ac['wholeCardCanonicalSha256']==rc['canonicalCardSHA256'];assert rc['wholeSourceVerdict']==rc['wholeEditorialVerdict']==rc['wholeVerdict']=='PASS'
 ags=[g for g in a['groups'] if g['id']==ident];assert len(ags)==len(rc['fields'])==6
 for ag,rg in zip(ags,rc['fields']):
  assert ag['group']==rg['group'] and ag['literal']==rg['currentLiteral'] and H(ag['literal'])==ag['canonicalSha256']==rg['canonicalJSONSHA256'];assert rg['sourceVerdict']==rg['editorialVerdict']=='PASS' and rg['manualSourceReason'] and rg['manualEditorialReason']
  if rg['group']=='prompt-answers-key':
   assert len(rg['orderedOptionReviews'])==4
   for i,opt in enumerate(rg['orderedOptionReviews']):assert opt['index']==i and opt['text']==q['answers'][i]['text'] and H(opt['text'])==opt['canonicalLiteralSHA256'] and opt['manualSourceReason'] and opt['manualEditorialReason']
  for pid in rg['independentSourceProofIds']:assert pid in proofs
  records.append({'id':ident,'group':ag['group'],'literalSHA256':H(ag['literal']),'cardSHA256':H(q),'independentProofIds':rg['independentSourceProofIds']})
report={'purpose':'Literal/source preservation, explicit manual editorial adjudication separate','authorFreeze':'39c907b','runtimeFreeze':'f547afe','readerFreeze':'47d7341','authorNativeId':a['authorNativeId'],'readerNativeId':r['readerNativeId'],'authorReceiptSHA256':sha(AP.read_bytes()),'readerReceiptSHA256':sha(RP.read_bytes()),'ids':ids,'roleGroups':48,'bindings':records,'all120SourceAssignmentsExact':True,'typedProofs':verified,'fullOriginals':len(r['originalSources']),'notCertified':['middle-ages-crusade','middle-ages-pilgrimage-armed'],'errors':0}
(OUT/'middle4-current-pair-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'currentPassCards':4,'roleGroups':48,'sourceAssignments':120,'typedProofs':len(verified),'fullOriginals':10,'errors':0})
