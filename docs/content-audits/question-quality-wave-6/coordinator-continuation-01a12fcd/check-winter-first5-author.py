import subprocess
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip() == '/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
import pathlib,json,hashlib,subprocess
from pypdf import PdfReader
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';S=B/'winter-sports/resume-2026-10-12-last15-fresh-first5';P=S/'editorial-revision-feedback1/author-grouped6-source-editorial-review.json';A=json.loads(P.read_text());G=A['correctedWholeSixSourceEditorialReread'];sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();git=lambda rev,p:subprocess.check_output(['git','show',rev+':'+str(p)]);assert P.read_bytes()==git('aede73a',P)==git('HEAD',P);assert A['authorIdentity']==G['authorIdentity']=='01a12fdb-8151-7890-9f51-8232f5f56bc2';qpath=pathlib.Path(A['runtimePath']);assert sha(qpath.read_bytes())==G['runtimeSha256AssertedUnchanged']==A['runtimeAfterSha256'];qs=json.loads(qpath.read_text())['questions'];by={q['id']:q for q in qs};assert qpath.read_bytes()==git('90cb82f',qpath)
for id,x in A['protected95FullCardHashes'].items():assert sha(cj(by[id]))==x
raws={};pdfs={};pageTexts={}
oldSourceManifest=json.loads(git('8d2a1f2',S/'author-field-review.json'))['sourceFiles']
for name,src in A['sourceFiles'].items():
 p=pathlib.Path(src['path']);raw=p.read_bytes();assert raw==git('aede73a',p)==git('HEAD',p);assert sha(raw)==src['sha256'] and len(raw)==src['bytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==src['gitBlobSha1'];raws[str(p)]=raw
 if p.suffix=='.html':assert b'</html>' in raw.lower()
 else:
  assert raw.startswith(b'%PDF') and b'%%EOF' in raw[-1024:];reader=PdfReader(p);assert src['sha256']==oldSourceManifest[name]['sha256'];assert len(reader.pages)==oldSourceManifest[name]['pdfPageCount'];pdfs[str(p)]=reader
provenance=A['pdfLocatorProvenanceCorrection']
for path,s in provenance['pdfSources'].items():
 assert sha(raws[path])==s['rawSourceSha256Unchanged']
 for pg,rec in s['pageTextRecords'].items():
  text=pdfs[path].pages[int(pg)-1].extract_text();derived=' '.join(text.split());assert sha(text.encode())==rec['rawExtractTextSha256Utf8'];assert sha(derived.encode())==rec['derivedPageTextSha256Utf8'];assert len(text)==rec['rawExtractTextLengthUnicodeCodePoints'] and len(derived)==rec['derivedPageTextLengthUnicodeCodePoints'];pageTexts[(path,int(pg))]=derived
 for key,rec in s['quoteLocators'].items():
  q=A['exactSourceQuotes'][key];assert rec['quoteSha256Unchanged']==q['quoteSha256']==sha(q['quote'].encode());d=pageTexts[(path,rec['physicalPage'])];assert d[rec['derivedPageTextOffsetZeroBasedUnicodeCodePoints']:rec['derivedPageTextOffsetZeroBasedUnicodeCodePoints']+rec['quoteLengthUnicodeCodePoints']]==q['quote']
for key,q in A['exactSourceQuotes'].items():
 assert sha(q['quote'].encode())==q['quoteSha256'];assert sha(raws[q['rawPath']])==q['sourceSha256'];assert subprocess.check_output(['git','rev-parse','aede73a:'+q['rawPath']],text=True).strip()==q['sourceGitBlobSha1']
 if q['rawPath'].endswith('.html'):assert raws[q['rawPath']][q['rawByteOffset']:q['rawByteOffset']+q['rawByteLength']]==q['quote'].encode()
fields=0;bindings=0
for id,review in G['reviews'].items():
 q=by[id];assert q==review['nativeCardLiteral'];assert sha(cj(q))==review['nativeCardSha256'];assert q['source']==review['sourceMetadataLiteral'];assert sha(cj(q['source']))==review['sourceMetadataSha256'];vals=dict(explanation=q['explanation'],**{f'note{i}':x['note'] for i,x in enumerate(q['answers'])});vals['prompt-key']=dict(prompt=q['prompt'],ordered4OptionTexts=[x['text'] for x in q['answers']],correctIndex=q['correctIndex'],key=q['answers'][q['correctIndex']]['text']);assert [f['group'] for f in review['groups']]==['prompt-key','explanation','note0','note1','note2','note3']
 for f in review['groups']:
  assert f['currentNativeLiteral']==vals[f['group']];assert sha(cj(f['currentNativeLiteral']))==f['literalSha256'];assert f['sourceAnalysis'] and f['editorialAnalysis'];assert len(f['sourceQuoteIDs'])==len(f['sourceQuoteBindings'])
  for key,binding in zip(f['sourceQuoteIDs'],f['sourceQuoteBindings']):
   orig=A['exactSourceQuotes'][key];assert binding['quoteId']==key
   for k in ['rawPath','locator','quote','quoteSha256','sourceSha256','sourceGitBlobSha1']:assert binding[k]==orig[k]
   bindings+=1
  fields+=1
out=dict(authorThreadId=A['authorIdentity'],freeze='aede73a',runtimeFreeze='90cb82f',cards=5,actualGroupedFields=fields,quoteBindings=bindings,uniqueQuotes=len(A['exactSourceQuotes']),fullOriginals=len(raws),pdfRawPreserved=True,pdfDeclaredDerivationVerified=True,htmlRawByteLocatorsVerified=True,protected95=True,errors=0,qualityPASS=False,knownEditorialHold=G['medium067Disposition'])
(O/'winter-first5-current-author-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(out)
