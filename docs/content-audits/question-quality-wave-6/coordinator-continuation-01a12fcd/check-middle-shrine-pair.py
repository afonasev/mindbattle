import json,pathlib,hashlib,subprocess
from html.parser import HTMLParser
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';D=B/'middle-ages/resume-2026-10-12-current-first2-fullproof'
AP=D/'author-current-receipt-01a12fe9.json';SP=D/'source-bindings-01a12fe9.json';MP=D/'author-review-01a12fe9.md';RP=B/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/middle-current-first2-5537e13/reader-receipt.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(AP.read_text());S=json.loads(SP.read_text());R=json.loads(RP.read_text())
for p in [AP,SP,MP]:assert p.read_bytes()==git('5537e13',p)==git('HEAD',p)
assert RP.read_bytes()==git('6a77e0f',RP)==git('HEAD',RP)
assert sha(AP.read_bytes())==R['authorPacket']['receiptRawSHA256'];assert sha(SP.read_bytes())==R['authorPacket']['bindingsRawSHA256']
assert A['authorThreadId']==S['authorThreadId']==R['authorIdentity']['trustedNativeThreadId']=='01a12fe9-74d9-7272-a1d2-f26317e06001'
assert R['readerIdentity']['trustedNativeThreadId']=='01a12f3d-8ec1-78b3-b153-5f2a62967421'
assert A['authorThreadId']!=R['readerIdentity']['trustedNativeThreadId']
Q={q['id']:q for q in json.loads(pathlib.Path('src/content/topics/middle-ages.json').read_text())['questions']};q=Q['middle-ages-shrine']
ac=next(c for c in A['cards'] if c['id']==q['id']);rc=next(c for c in R['cards'] if c['id']==q['id']);assert sha(cj(q))==rc['canonicalCardSHA256'];assert sha(ij(q))==rc['insertionCardSHA256']
assert rc['wholeSourceVerdict']==rc['wholeEditorialVerdict']==rc['wholeVerdict']=='PASS'
vals={'prompt-key':dict(prompt=q['prompt'],answerTexts=[x['text'] for x in q['answers']],correctIndex=q['correctIndex']),'explanation':q['explanation'],**{f'note{i}':v['note'] for i,v in enumerate(q['answers'])}}
class P(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.n=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.n.append(d.strip())
records=[];bindings=0;quotes=set();originals=set()
assert [f['field'] for f in rc['fields']]==list(vals)
for af,rf in zip(ac['groups'],rc['fields']):
 name=rf['field'];assert af['name']==name
 assert af['literal']==rf['currentLiteral']==vals[name]
 h=sha(cj(vals[name]) if name=='prompt-key' else vals[name].encode())
 assert h==af['sha256']==rf['authorNativeLiteralSHA256'];assert sha(ij(vals[name]))==rf['readerInsertionJSONSHA256']
 assert rf['sourceVerdict']==rf['editorialVerdict']==rf['verdict']=='PASS'
 assert rf['manualSourceReason'] and rf['manualEditorialReason']
 for proof in rf['actualProofs']:
  path=pathlib.Path(proof['rawPath']);raw=path.read_bytes();assert raw==git('5537e13',path)==git('HEAD',path)
  assert sha(raw)==proof['rawSHA256'] and len(raw)==proof['rawBytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(path)],text=True).strip()==proof['gitBlob'];assert b'</html>' in raw.lower()
  p=P();p.feed(raw.decode());text=' '.join(' '.join(p.n).split())
  assert sha(text.encode())==proof['HTMLDecodedVisibleBodySHA256'] and len(text)==proof['HTMLDecodedVisibleBodyUnicodeLength']
  loc=proof['locator'];start=loc['UnicodeCodePointOffset0Based'];quote=proof['exactDerivedQuote'];assert text[start:start+loc['UnicodeCodePointLength']]==quote and sha(quote.encode())==proof['quoteSHA256']
  assert proof['sourceId'] in S['fieldBindings'][q['id']][name]
  quotes.add((str(path),proof['quoteSHA256']));originals.add(str(path));bindings+=1
 records.append({'field':name,'author':af,'authorManualReview':str(MP)+'#middle-ages-shrine/'+name,'authorSourceIDs':S['fieldBindings'][q['id']][name],'reader':rf})
out={'purpose':'Strict actual pair preservation only; separate manual decision required','id':q['id'],'authorReceipt':str(AP),'authorBindings':str(SP),'authorManualReview':str(MP),'readerReceipt':str(RP),'authorFreeze':'5537e13','readerFreeze':'6a77e0f','roleFields':12,'readerQuoteBindings':bindings,'uniqueQuotes':len(quotes),'fullOriginals':len(originals),'errors':0,'cardCanonicalSha256':sha(cj(q)),'authorManualReviewSHA256':sha(MP.read_bytes()),'records':records}
(O/'middle-shrine-current-pair-bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in out.items() if k!='records'})
