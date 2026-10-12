import json,pathlib,hashlib,subprocess,unicodedata
from pypdf import PdfReader
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';D=B/'middle-ages/resume-2026-10-12-jihad-unique-alternative-repair';P=D/'author-freeze-01a12fe9.json';MP=D/'author-scope-metadata-correction-01a12fe9.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(P.read_text());M=json.loads(MP.read_text());assert P.read_bytes()==git('f00a60e',P)==git('HEAD',P);assert MP.read_bytes()==git('d1d2929',MP)==git('HEAD',MP);assert sha(P.read_bytes())==M['previousAuthorFreezeSHA256'];assert A['actualAuthorIdentity']==M['authorIdentity']=='01a12fe9-74d9-7272-a1d2-f26317e06001'
scope=pathlib.Path(M['scopeDefinitionFile']);assert scope.read_bytes()==git(M['scopeDefinitionCommit'],scope)==git('HEAD',scope);assert sha(scope.read_bytes())==M['scopeDefinitionSHA256'];SC=json.loads(scope.read_text())
qp=pathlib.Path(A['runtimePath']);assert qp.read_bytes()==git('f00a60e',qp);assert sha(qp.read_bytes())==A['runtimeSHA256'];Q={q['id']:q for q in json.loads(qp.read_text())['questions']};q=Q['middle-ages-jihad'];assert q==A['currentRecord']['record'] and sha(ij(q))==A['currentRecord']['wholeRecordSHA256']==M['currentTargetSHA256']
for id,h in SC['protected99'].items():assert sha(cj(Q[id]))==h
assert q['difficulty']=='medium' and q['correctIndex']==1
pdfs={};srcs={};pages={};align=lambda text:''.join(c for x in text for c in unicodedata.normalize('NFKC',x).casefold() if c.isalnum())
for s in A['completeOriginals']:
 p=pathlib.Path(s['path']);raw=p.read_bytes();assert raw==git('f00a60e',p)==git('HEAD',p);assert sha(raw)==s['rawSHA256'] and len(raw)==s['rawBytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==s['gitBlob'];assert raw.startswith(b'%PDF') and b'%%EOF' in raw[-1024:];pdfs[str(p)]=PdfReader(p);srcs[str(p)]=s
for pg in A['pageDerivations']:
 text=pdfs[pg['path']].pages[pg['physicalPage']-1].extract_text();assert sha(text.encode())==pg['pageTextSHA256'] and len(text)==pg['charCount'];pages[(pg['path'],pg['physicalPage'])]=text
vals={'prompt-key':dict(prompt=q['prompt'],orderedAnswerTexts=[v['text'] for v in q['answers']],correctIndex=q['correctIndex'],correctAnswerText=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'answers[{i}].note':v['note'] for i,v in enumerate(q['answers'])}}
assert len(A['fieldReviews'])==A['fieldReviewCount']==6 and {f['field'] for f in A['fieldReviews']}==set(vals)
bindings=0
for f in A['fieldReviews']:
 v=vals[f['field']];assert f['literal']==v and f['literalSerialization'].encode()==ij(v) and sha(ij(v))==f['literalSHA256'];assert f['sourceAnalysis'] and f['editorialAnalysis']
 for b in f['sourceBindings']:
  s=b['completeOriginal'];path=s['path'];assert s['rawSHA256']==srcs[path]['rawSHA256'] and s['gitBlob']==srcs[path]['gitBlob'];assert b['sourceURL']==srcs[path]['url'];h=b['historicalHumanCitationQuote'];assert sha(h.encode())==b['historicalCitationQuoteSHA256']
  der=b['nativePDFDerivation'];text=pages[(path,der['physicalPage'])];assert sha(text.encode())==der['originalPageTextSHA256'];start,end=der['charRange0BasedHalfOpen'];quote=der['exactActualDerivedQuote'];assert text[start:end]==quote and sha(quote.encode())==der['actualDerivedQuoteSHA256'];assert align(h)==align(quote);bindings+=1
out=dict(author=A['actualAuthorIdentity'],authorReceipt=str(P),metadataCorrection=str(MP),authorFreeze='f00a60e',metadataFreeze='d1d2929',scopeDefinition='c600b5e',nativeWhole6Fields=6,sourceQuoteBindings=bindings,fullOriginals=len(srcs),PDFDerivedPages=len(pages),protected99=True,errors=0,qualityPASS=False,readerPending=True,counterIncrement=0)
(O/'jihad-current-author-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(out)
