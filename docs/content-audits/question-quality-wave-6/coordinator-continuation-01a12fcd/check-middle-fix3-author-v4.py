import pathlib,json,hashlib,subprocess,unicodedata
from html.parser import HTMLParser
from pypdf import PdfReader
import pypdf
assert pypdf.__version__=='6.19.0'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';D=B/'middle-ages/resume-2026-10-12-current-fix3-indulgence-reconquista-jihad';P=D/'author-sourcebound-freeze-v4-01a12fe9.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(P.read_text());V3=json.loads(git('065f223',D/'author-sourcebound-freeze-v3-01a12fe9.json'));assert P.read_bytes()==git('b420f9b',P)==git('HEAD',P);assert A['authorIdentity']=='01a12fe9-74d9-7272-a1d2-f26317e06001' and A['coordinatorIdentity']!=A['authorIdentity']
scope=pathlib.Path(A['scopePath']);assert scope.read_bytes()==git('03ef8df',scope)==git('HEAD',scope);SC=json.loads(scope.read_text())
qp=pathlib.Path(A['topicPath']);assert qp.read_bytes()==git('b420f9b',qp);assert sha(qp.read_bytes())==A['topicSHA256'];Q={q['id']:q for q in json.loads(qp.read_text())['questions']};before={q['id']:q for q in json.loads(git(A['baselineFreeze'],qp))['questions']};assert list(Q)==list(before)
for id,h in SC['protected97'].items():assert sha(cj(Q[id]))==h
for id in A['scopeIds']:assert Q[id]['difficulty']==before[id]['difficulty'] and Q[id]['correctIndex']==before[id]['correctIndex']
class H(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.n=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.n.append(s)
align=lambda text:''.join(c for x in text for c in unicodedata.normalize('NFKC',x).casefold() if c.isalnum())
sources={};pdfs={};html={}
for s in A['completeOriginalSources']:
 p=pathlib.Path(s['path']);raw=p.read_bytes();assert raw==git('b420f9b',p)==git('HEAD',p);assert sha(raw)==s['rawSHA256'] and len(raw)==s['rawBytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==s['gitBlob'];sources[str(p)]=s
 if p.suffix=='.pdf':assert raw.startswith(b'%PDF') and b'%%EOF' in raw[-1024:];pdfs[str(p)]=PdfReader(p)
 else:assert b'</html>' in raw.lower();h=H();h.feed(raw.decode());html[str(p)]=' '.join(' '.join(h.n).split())
pages={}
for rec in A['pdfDerivationMap']['pages']:
 path=rec['sourcePath'];assert sources[path]['rawSHA256']==rec['sourceRawSHA256'] and sources[path]['gitBlob']==rec['sourceGitBlob'];text=pdfs[path].pages[rec['physicalPage']-1].extract_text();assert sha(text.encode())==rec['originalPageTextSHA256'] and len(text)==rec['textCharCount'];pages[(path,rec['physicalPage'])]=text
byfields={(f['questionId'],f['field']):f for f in A['fieldReviews']};old={(f['questionId'],f['field']):f for f in V3['fieldReviews']};assert len(byfields)==A['fieldReviewCount']==18
bindings=pdfbindings=0;records=[]
for rec in A['records']:
 id=rec['id'];q=Q[id];assert rec['currentRecord']==q and sha(ij(q))==rec['wholeRecordSHA256'];vals={'prompt-key':dict(prompt=q['prompt'],orderedAnswerTexts=[v['text'] for v in q['answers']],correctIndex=q['correctIndex'],correctAnswerText=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'answers[{i}].note':v['note'] for i,v in enumerate(q['answers'])}}
 for name,value in vals.items():
  f=byfields[(id,name)];assert f['literal']==value;assert f['literalSerialization'].encode()==ij(value) and sha(ij(value))==f['literalSHA256'];assert f['sourceAnalysis'] and f['editorialAnalysis'];assert f['sourceBindings']
  assert len(f['sourceBindings'])==len(old[(id,name)]['sourceBindings'])
  for sb,historical in zip(f['sourceBindings'],old[(id,name)]['sourceBindings']):
   path=sb['sourcePath'];src=sources[path];assert sb['rawSHA256']==src['rawSHA256'] and sb['rawBytes']==src['rawBytes'] and sb['gitBlob']==src['gitBlob'] and sb['url']==src['url']
   quote=sb['exactQuote'];assert quote==historical['exactQuote'];assert sb['quoteSHA256']==historical['quoteSHA256']==sha(quote.encode())
   if path in pdfs:
    der=sb['pdfDerivation'];assert der['historicalCitationQuote']==quote and der['historicalCitationQuoteSHA256']==sb['quoteSHA256'];pieces=[]
    for frag in der['fragments']:
     text=pages[(path,frag['physicalPage'])];assert sha(text.encode())==frag['originalPageTextSHA256'];start,end=frag['charRange'];actual=frag['actualDerivedQuote'];assert text[start:end]==actual and sha(actual.encode())==frag['actualDerivedQuoteSHA256'];pieces.append(actual)
    assert align(quote)==align(''.join(pieces));pdfbindings+=1
   else:assert ' '.join(quote.split()) in html[path]
   bindings+=1
  records.append(dict(id=id,field=name,nativeField=f))
siyar=byfields[('middle-ages-jihad','answers[3].note')]['sourceBindings'][0];assert 'p.3' in siyar['locator'] and siyar['pdfDerivation']['fragments'][0]['physicalPage']==3
out=dict(author=A['authorIdentity'],receipt=str(P),authorFreeze='b420f9b',runtimeFreeze='88c84f4',currentCards=3,nativeWhole6Fields=18,sourceQuoteBindings=bindings,pdfBindings=pdfbindings,fullOriginals=len(sources),faithfulPDFRawPageFragmentDerivations=True,historicalCitationQuotesAndSHAUnchanged=True,protected97=True,errors=0,qualityPASS=False,readerPending=True,counterIncrement=0,receiptSHA256=sha(P.read_bytes()),records=records)
(O/'middle-fix3-current-v4-author-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k!='records'})
