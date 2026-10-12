import json,pathlib,hashlib,subprocess
from pypdf import PdfReader
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';P=B/'winter-sports/resume-2026-10-12-last15-fresh-first5/repair059067/author-source-editorial-review-corrected.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();git=lambda rev,p:subprocess.check_output(['git','show',rev+':'+str(p)])
A=json.loads(P.read_text());assert P.read_bytes()==git('6b60a7b',P)==git('HEAD',P)
assert A['authorIdentity']=='01a12fdb-8151-7890-9f51-8232f5f56bc2'
sc=pathlib.Path(A['scopePath']);assert sc.read_bytes()==git(A['scopeGitCommit'],sc)==git('HEAD',sc);S=json.loads(sc.read_text());assert S['actualAuthor']==A['authorIdentity']
qp=pathlib.Path(A['runtimePath']);assert qp.read_bytes()==git('3b33ae4',qp)==git('6b60a7b',qp);assert sha(qp.read_bytes())==A['runtimeCurrentSha256']
Q={q['id']:q for q in json.loads(qp.read_text())['questions']};before={q['id']:q for q in json.loads(git(A['runtimeBaselineCommit'],qp))['questions']}
assert set(Q)==set(before);assert [id for id in Q if Q[id]!=before[id]]==A['scopeIds']
for id,h in S['protected98'].items():assert sha(cj(Q[id]))==h
raws={}
for name,s in A['originalSourceCaptures'].items():
 p=pathlib.Path(s['path']);raw=p.read_bytes();assert raw==git('6b60a7b',p)==git('HEAD',p);assert sha(raw)==s['sha256'] and len(raw)==s['bytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==s['gitBlobSha1']
 if p.suffix=='.html':assert b'</html>' in raw.lower()
 else:assert raw.startswith(b'%PDF') and b'%%EOF' in raw[-1024:];assert len(PdfReader(p).pages)==({'isu-sys-rules-2026.pdf':78,'fis-equipment-2026.pdf':35}[name])
 raws[str(p)]=raw
fields=bindings=0;unique=set()
for id,c in A['cards'].items():
 q=Q[id];assert q==c['nativeCardLiteral'];assert sha(cj(q))==c['nativeCardSha256'];assert q['source']==c['sourceMetadataLiteral'] and sha(cj(q['source']))==c['sourceMetadataSha256']
 vals={'prompt-key':dict(prompt=q['prompt'],ordered4OptionTexts=[x['text'] for x in q['answers']],correctIndex=q['correctIndex'],key=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'note{i}':v['note'] for i,v in enumerate(q['answers'])}}
 assert [f['group'] for f in c['groups']]==list(vals)
 for f in c['groups']:
  assert f['currentNativeLiteral']==vals[f['group']] and sha(cj(vals[f['group']]))==f['literalSha256'];assert f['sourceAnalysis'] and f['editorialAnalysis']
  assert len(f['sourceQuoteIDs'])==len(f['sourceQuoteBindings'])
  for key,p in zip(f['sourceQuoteIDs'],f['sourceQuoteBindings']):
   raw=raws[p['rawPath']];assert key==p['quoteId'];quote=p['quote'];assert raw[p['rawByteOffsetZeroBased']:p['rawByteOffsetZeroBased']+p['rawByteLength']]==quote.encode()
   assert sha(quote.encode())==p['quoteSha256Unchanged'];assert sha(raw)==p['sourceSha256Unchanged'];assert subprocess.check_output(['git','rev-parse','HEAD:'+p['rawPath']],text=True).strip()==p['sourceGitBlobSha1Unchanged'];unique.add((p['rawPath'],p['quoteSha256Unchanged']));bindings+=1
  fields+=1
out={'author':A['authorIdentity'],'receipt':str(P),'authorFreeze':'6b60a7b','runtimeFreeze':'3b33ae4','scopeDefinition':'7e3ea65','scopeAuthorityCorrectedHistoryPreserved':True,'currentCards':2,'nativeWhole6Fields':fields,'sourceQuoteBindings':bindings,'uniqueQuotes':len(unique),'fullOriginals':len(raws),'protected98':True,'errors':0,'qualityPASS':False,'readerPending':True,'counterIncrement':0,'receiptSHA256':sha(P.read_bytes())}
(O/'winter-fix2-corrected-author-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(out)
