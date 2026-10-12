import json,pathlib,hashlib,subprocess
from pypdf import PdfReader
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd'
AP=B/'winter-sports/resume-2026-10-12-last15-fresh-first5/editorial-revision-feedback1/author-grouped6-source-editorial-review.json'
RP=B/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current-first5-90cb82f/reader-receipt.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode()
git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(AP.read_text());R=json.loads(RP.read_text())
assert AP.read_bytes()==git('aede73a',AP)==git('HEAD',AP)
assert RP.read_bytes()==git('bedbc5e',RP)==git('HEAD',RP)
assert sha(AP.read_bytes())==R['authorReceiptSHA256']
assert A['authorIdentity']==R['authorIdentity']=='01a12fdb-8151-7890-9f51-8232f5f56bc2'
assert R['readerIdentity']['nativeThreadId']=='01a12f3d-8ec1-78b3-b153-5f2a62967421'
assert A['authorIdentity']!=R['readerIdentity']['nativeThreadId']
Q={q['id']:q for q in json.loads(pathlib.Path(A['runtimePath']).read_text())['questions']}
selected=['winter-sports-060','winter-sports-068','winter-sports-073'];records=[];bindings=0;unique=set();raws={};pdfs={}
for c in R['cards']:
 if c['id'] not in selected:continue
 q=Q[c['id']];ar=A['correctedWholeSixSourceEditorialReread']['reviews'][c['id']]
 assert q==ar['nativeCardLiteral']
 assert sha(cj(q))==c['canonicalCardSHA256']==ar['nativeCardSha256']
 assert sha(ij(q))==c['insertionCardSHA256']
 assert c['wholeSourceVerdict']==c['wholeEditorialVerdict']==c['wholeVerdict']=='PASS'
 vals={'prompt-key':dict(prompt=q['prompt'],ordered4OptionTexts=[x['text'] for x in q['answers']],correctIndex=q['correctIndex'],key=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'note{i}':v['note'] for i,v in enumerate(q['answers'])}}
 assert [f['field'] for f in c['fields']]==list(vals)
 for af,rf in zip(ar['groups'],c['fields']):
  name=rf['field'];assert af['group']==name
  assert af['currentNativeLiteral']==rf['currentLiteral']==vals[name]
  assert sha(cj(vals[name]))==af['literalSha256']==rf['authorSortedJSONSHA256']
  assert sha(ij(vals[name]))==rf['readerInsertionJSONSHA256']
  assert af['sourceAnalysis'] and af['editorialAnalysis'] and rf['manualSourceReason'] and rf['manualEditorialReason']
  assert rf['sourceVerdict']==rf['editorialVerdict']==rf['verdict']=='PASS'
  for p in rf['actualProofs']:
   path=pathlib.Path(p['rawPath']);raw=path.read_bytes()
   assert raw==git(p['GitDurableAt'],path)==git('HEAD',path)
   assert sha(raw)==p['rawSHA256'] and len(raw)==p['rawBytes']
   assert subprocess.check_output(['git','rev-parse','HEAD:'+str(path)],text=True).strip()==p['gitBlob']
   raws[str(path)]=p['rawSHA256'];loc=p['locator']
   if loc['kind']=='RawHTMLBytes':
    quote=p['exactRawQuote'];assert raw[loc['byteOffset0Based']:loc['byteOffset0Based']+loc['byteLength']]==quote.encode()
   else:
    assert loc['kind']=='PDFDerivedUnicode'
    reader=pdfs.setdefault(str(path),PdfReader(path));assert len(reader.pages)==p['physicalPageCount']
    text=reader.pages[loc['physicalPage1Based']-1].extract_text();derived=' '.join(text.split())
    assert sha(text.encode())==p['rawExtractTextSHA256'] and sha(derived.encode())==p['derivedPageTextSHA256']
    quote=p['exactDerivedQuote'];start=loc['UnicodeCodePointOffset0Based'];assert derived[start:start+loc['UnicodeCodePointLength']]==quote
   assert sha(quote.encode())==p['quoteSHA256'];unique.add((str(path),p['quoteSHA256']));bindings+=1
  records.append({'id':c['id'],'field':name,'author':af,'reader':rf})
out={'purpose':'Strict preservation/current pair binding only; manual coordinator decision separate','ids':selected,'authorFreeze':'aede73a','readerFreeze':'bedbc5e','runtimeFreeze':'90cb82f','authorReceipt':str(AP),'readerReceipt':str(RP),'authorReceiptSHA256':sha(AP.read_bytes()),'readerReceiptSHA256':sha(RP.read_bytes()),'roleFields':len(records)*2,'readerQuoteBindings':bindings,'uniqueQuotes':len(unique),'fullOriginals':len(raws),'errors':0,'cards':[{'questionId':id,'cardCanonicalSha256':sha(cj(Q[id]))} for id in selected],'records':records}
(O/'winter-first5-accepted3-pair-bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in out.items() if k not in ['records','cards']})
