import subprocess
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()=='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
import pathlib,json,hashlib,subprocess
from html.parser import HTMLParser
from pypdf import PdfReader
B=pathlib.Path('docs/content-audits/question-quality-wave-6');O=B/'coordinator-continuation-01a12fcd';D=B/'middle-ages/resume-2026-10-12-current-first2-fullproof';AP=D/'author-current-receipt-01a12fe9.json';SP=D/'source-bindings-01a12fe9.json';MP=D/'author-review-01a12fe9.md';sha=lambda b:hashlib.sha256(b).hexdigest();cj=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();git=lambda rev,p:subprocess.check_output(['git','show',rev+':'+str(p)])
a=json.loads(AP.read_text());s=json.loads(SP.read_text());assert a['authorThreadId']==s['authorThreadId']=='01a12fe9-74d9-7272-a1d2-f26317e06001';assert a['environmentThreadId']!=a['authorThreadId'];assert AP.read_bytes()==git('5537e13',AP)==git('HEAD',AP);assert SP.read_bytes()==git('5537e13',SP)==git('HEAD',SP);assert MP.read_bytes()==git('5537e13',MP)==git('HEAD',MP)
qpath=pathlib.Path('src/content/topics/middle-ages.json');qs=json.loads(qpath.read_text())['questions'];by={q['id']:q for q in qs};sc=json.load(open(a['scopeFile']));assert git(a['scopeDefinitionCommit'],pathlib.Path(a['scopeFile']))==pathlib.Path(a['scopeFile']).read_bytes()
for rec in sc['protected98']:assert sha(cj(by[rec['id']]))==rec['sha256']
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.n=[]
 def handle_starttag(self,t,attrs):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.n.append(d)
originals={};quotes=0
for src in s['completeRawOriginals']:
 p=pathlib.Path(src['path']);raw=p.read_bytes();assert raw==git('5537e13',p)==git('HEAD',p);assert sha(raw)==src['rawSha256'] and len(raw)==src['rawBytes'];assert subprocess.check_output(['git','rev-parse','HEAD:'+str(p)],text=True).strip()==src['gitBlobSha1']
 if p.suffix=='.pdf':assert raw.startswith(b'%PDF');reader=PdfReader(p);text=reader.pages[16].extract_text()
 elif p.suffix=='.json':
  leaves=[]
  def walk(v):
   if isinstance(v,str):leaves.append(v)
   elif isinstance(v,list):
    for x in v:walk(x)
   elif isinstance(v,dict):
    for x in v.values():walk(x)
  walk(json.loads(raw));h=P();h.feed(' '.join(leaves));text=' '.join(h.n)
 else:assert b'</html>' in raw.lower();h=P();h.feed(raw.decode());text=' '.join(h.n)
 for c in src.get('citations', [src] if 'quote' in src else []):
  assert sha(c['quote'].encode())==c['quoteSha256'];assert ' '.join(c['quote'].split()) in ' '.join(text.split()),(src['id'],c['quote']);quotes+=1
 originals[src['id']]=src
records=[]
for card in a['cards']:
 q=by[card['id']];assert q['difficulty']=='easy';assert q['correctIndex']==sc['preservedSlots'][q['id']]['correctIndex'];vals=dict(explanation=q['explanation'],**{f'note{i}':x['note'] for i,x in enumerate(q['answers'])});vals['prompt-key']=dict(prompt=q['prompt'],answerTexts=[x['text'] for x in q['answers']],correctIndex=q['correctIndex']);assert len(card['groups'])==6
 for f in card['groups']:
  name=f['name'];v=vals[name];assert f['literal']==v;assert sha(cj(v) if name=='prompt-key' else v.encode())==f['sha256'];refs=s['fieldBindings'][q['id']][name];assert refs and all(id in originals for id in refs);records.append(dict(id=q['id'],nativeField=f,sourceIds=refs))
out=dict(authorThreadId=a['authorThreadId'],environmentDiscrepancyPreserved=a['environmentThreadId'],freeze='5537e13',cards=2,nativeFields=len(records),sourceOriginals=len(originals),quoteContextBindings=quotes,protected98=True,receiptSha256=sha(AP.read_bytes()),sourceBindingsSha256=sha(SP.read_bytes()),manualReviewSha256=sha(MP.read_bytes()),cardCanonicalHashes=[dict(id=c['id'],sha256=sha(cj(by[c['id']]))) for c in a['cards']],sourceContextCheck='Exact stored quote hashes; whitespace-equivalent decoded original HTML/PDF context under descriptive chapter/annotation locators. Original bytes unchanged.',qualityPASS=False,errors=0,records=records)
(O/'middle-first2-current-author-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k!='records'})
