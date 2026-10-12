import pathlib,json,hashlib,subprocess
from html.parser import HTMLParser
from pypdf import PdfReader
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';AP=B/'middle-ages/resume-2026-10-12-current-fix3-indulgence-reconquista-jihad/author-sourcebound-freeze-v4-01a12fe9.json';D=B/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/middle-current-fix3-b420f9b';RP=D/'reader-receipt.json'
sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();ij=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+str(p)])
A=json.loads(AP.read_text());R=json.loads(RP.read_text());assert AP.read_bytes()==git('b420f9b',AP)==git('HEAD',AP);assert RP.read_bytes()==git('a42003c',RP)==git('HEAD',RP);assert sha(AP.read_bytes())==R['authorReceiptSHA256']
assert R['authorIdentity']==A['authorIdentity']=='01a12fe9-74d9-7272-a1d2-f26317e06001';assert R['readerIdentity']=='01a12f3d-8ec1-78b3-b153-5f2a62967421' and R['readerIdentity']!=R['authorIdentity']
Q={q['id']:q for q in json.loads(pathlib.Path(A['topicPath']).read_text())['questions']};AF={(f['questionId'],f['field']):f for f in A['fieldReviews']};records=[];cards=[];sources={};pdfs={};html={}
class H(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.n=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip and s.strip():self.n.append(s.strip())
for src in R['sources']:
 path=pathlib.Path(src['path']);raw=path.read_bytes();assert raw==git(src['durableAt'],path)==git('HEAD',path);assert sha(raw)==src['rawSHA256'] and len(raw)==src['bytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(path)],text=True).strip()==src['GitBlob'];sources[str(path)]=src
 if path.suffix=='.pdf':pdfs[str(path)]=PdfReader(path)
 else:h=H();h.feed(raw.decode());html[str(path)]=h.n
for name in ['html-independent-context.json','pdf-independent-extractions.json']:
 p=D/name;assert p.read_bytes()==git('a42003c',p)==git('HEAD',p)
for ctx in json.loads((D/'html-independent-context.json').read_text()):
 nodes=html[ctx['source']['path']]
 for rec in ctx['nodes']:assert nodes[rec['index0']]==rec['text'] and sha(rec['text'].encode())==rec['exactNodeUTF8SHA256']
for rec in json.loads((D/'pdf-independent-extractions.json').read_text()):
 text=pdfs[rec['sourcePath']].pages[rec['physicalPage1']-1].extract_text();assert text==rec['pageText'] and sha(text.encode())==rec['exactPageTextUTF8SHA256']
selected=['middle-ages-indulgence','middle-ages-reconquista'];bindings=fragments=0;unique=set();used=set()
for c in R['cards']:
 if c['id'] not in selected:continue
 id=c['id'];q=Q[id];assert sha(cj(q))==c['canonicalCardSHA256'];assert sha(ij(q))==c['insertionCardSHA256'];assert c['wholeSourceVerdict']==c['wholeEditorialVerdict']==c['wholeVerdict']=='PASS'
 vals={'prompt-key':dict(prompt=q['prompt'],orderedAnswerTexts=[v['text'] for v in q['answers']],correctIndex=q['correctIndex'],correctAnswerText=q['answers'][q['correctIndex']]['text']),'explanation':q['explanation'],**{f'answers[{i}].note':v['note'] for i,v in enumerate(q['answers'])}}
 assert {f['field'] for f in c['fields']}==set(vals)
 for rf in c['fields']:
  n=rf['field'];af=AF[(id,n)];assert rf['currentLiteral']==af['literal']==vals[n];assert sha(ij(vals[n]))==rf['insertionJSONSHA256']==af['literalSHA256'];assert sha(cj(vals[n]))==rf['canonicalJSONSHA256'];assert rf['sourceVerdict']==rf['editorialVerdict']=='PASS';assert af['sourceAnalysis'] and af['editorialAnalysis'] and rf['manualSourceReason'] and rf['manualEditorialReason'];assert len(af['sourceBindings'])==len(rf['bindings'])
  for ab,rb in zip(af['sourceBindings'],rf['bindings']):
   path=rb['sourcePath'];src=sources[path];assert path==ab['sourcePath'];assert rb['sourceRawSHA256']==ab['rawSHA256']==src['rawSHA256'];assert rb['sourceGitBlob']==ab['gitBlob']==src['GitBlob'];quote=rb['historicalCitationQuote'];assert quote==ab['exactQuote'] and sha(quote.encode())==rb['historicalCitationQuoteSHA256']==ab['quoteSHA256'];used.add(path);unique.add((path,rb['historicalCitationQuoteSHA256']))
   if path in pdfs:
    for p in rb['actualProofs']:
     text=pdfs[path].pages[p['physicalPage1']-1].extract_text();assert sha(text.encode())==p['exactOriginalPageTextSHA256'];start,end=p['UnicodeCodePointRange0'];assert text[start:end]==p['exactActualDerivedQuote'] and sha(p['exactActualDerivedQuote'].encode())==p['exactActualDerivedQuoteSHA256'];fragments+=1
   else:assert ' '.join(quote.split()) in ' '.join(' '.join(html[path]).split())
   bindings+=1
  records.append(dict(id=id,field=n,author=af,reader=rf))
 cards.append(dict(questionId=id,cardCanonicalSha256=sha(cj(q))))
out=dict(purpose='Strict actual pair binding preservation; manual decision separate',ids=selected,authorReceipt=str(AP),readerReceipt=str(RP),authorFreeze='b420f9b',readerFreeze='a42003c',runtimeFreeze='88c84f4',roleFields=len(records)*2,readerQuoteBindings=bindings,PDFNativeFragmentBindings=fragments,uniqueCitationQuotes=len(unique),proofOriginals=len(used),completeOriginalRegister=len(sources),errors=0,cards=cards,records=records)
(O/'middle-fix3-accepted2-current-pair-bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['records','cards']})
