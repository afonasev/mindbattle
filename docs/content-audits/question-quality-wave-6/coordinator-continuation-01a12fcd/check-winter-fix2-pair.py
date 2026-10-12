import pathlib,json,hashlib,subprocess
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';AP=B/'winter-sports/resume-2026-10-12-last15-fresh-first5/repair059067/author-source-editorial-review-corrected.json';RP=B/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current-fix2-6b60a7b/reader-receipt.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(AP.read_text());R=json.loads(RP.read_text())
assert AP.read_bytes()==git('6b60a7b',AP)==git('HEAD',AP);assert RP.read_bytes()==git('26ce803',RP)==git('HEAD',RP);assert sha(AP.read_bytes())==R['authorReceiptSHA256'];assert R['authorReceipt']==str(AP)
assert A['authorIdentity']==R['authorIdentity']=='01a12fdb-8151-7890-9f51-8232f5f56bc2';assert R['readerIdentity']=='01a12f3d-8ec1-78b3-b153-5f2a62967421' and R['readerIdentity']!=R['authorIdentity']
Q={q['id']:q for q in json.loads(pathlib.Path(A['runtimePath']).read_text())['questions']};records=[];bindings=0;quotes=set();raws={};cards=[]
for s in R['sources']:
 p=pathlib.Path(s['path']);raw=p.read_bytes();assert raw==git(s['durableAt'],p)==git('HEAD',p);assert sha(raw)==s['SHA256'] and len(raw)==s['bytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==s['GitBlobSHA1'];raws[str(p)]=raw
for c in R['cards']:
 q=Q[c['id']];a=A['cards'][c['id']];assert q==a['nativeCardLiteral'];assert sha(cj(q))==a['nativeCardSha256']==c['canonicalCardSHA256'];assert sha(ij(q))==c['insertionCardSHA256'];assert c['wholeSourceVerdict']==c['wholeEditorialVerdict']==c['wholeVerdict']=='PASS'
 vals={'prompt-key':dict(prompt=q['prompt'],ordered4OptionTexts=[v['text'] for v in q['answers']],correctIndex=q['correctIndex'],key=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'note{i}':v['note'] for i,v in enumerate(q['answers'])}}
 assert [f['field'] for f in c['fields']]==list(vals)
 for af,rf in zip(a['groups'],c['fields']):
  n=rf['field'];assert n==af['group'];assert af['currentNativeLiteral']==rf['currentLiteral']==vals[n];assert sha(cj(vals[n]))==af['literalSha256']==rf['canonicalJSONSHA256'];assert sha(ij(vals[n]))==rf['insertionJSONSHA256'];assert rf['sourceVerdict']==rf['editorialVerdict']=='PASS'
  assert af['sourceAnalysis'] and af['editorialAnalysis'] and rf['manualSourceReason'] and rf['manualEditorialReason']
  for proof in rf['independentSourceProofs']:
   s=proof['source'];raw=raws[s['path']];start=proof['rawByteOffset0'];quote=proof['exactRawHTMLQuote'];assert raw[start:start+proof['rawByteLength']]==quote.encode();assert raw[:start].count(b'\n')+1==proof['HTMLLine1'];assert sha(quote.encode())==proof['quoteSHA256'];assert sha(raw)==s['SHA256'];quotes.add((s['path'],proof['quoteSHA256']));bindings+=1
  records.append(dict(id=c['id'],field=n,author=af,reader=rf))
 cards.append(dict(questionId=c['id'],cardCanonicalSha256=sha(cj(q))))
out=dict(purpose='Actual current pair preservation only; manual decision separate',ids=[c['questionId'] for c in cards],authorReceipt=str(AP),readerReceipt=str(RP),authorFreeze='6b60a7b',readerFreeze='26ce803',runtimeFreeze='3b33ae4',roleFields=len(records)*2,readerQuoteBindings=bindings,uniqueQuotes=len(quotes),proofOriginals=len({p for p,h in quotes}),fullOriginalCaptureRegister=len(raws),errors=0,cards=cards,records=records)
(O/'winter-fix2-current-pair-bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['records','cards']})
