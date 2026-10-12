"""Preserve author current literal/raw/quote bindings only, no quality grading."""
import json,hashlib,subprocess,re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-6';OUT=BASE/'coordinator-continuation-01a12f20'
AB=BASE/'winter-sports/resume-2026-10-12-fresh-fix3-remaining15/source-only-057058'
sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','-C',str(ROOT),'show',rev+':'+str(p.relative_to(ROOT))])
ar=AB/'author-source-only-receipt-v2.json';sr=AB/'source-context.json'
ra,rs=git('fc2e8ff',ar),git('fc2e8ff',sr);assert ra==ar.read_bytes() and rs==sr.read_bytes()
a,s=json.loads(ra),json.loads(rs);assert a['authorIdentity']['nativeThreadId']==s['authorThreadId']=='01a12f7f-61a0-7062-904d-bbbb787deefc';assert a['sourceEvidence']==s['sources']
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.block=0
 def handle_starttag(self,t,attrs):
  if t in ['script','style']:self.block+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.block-=1
 def handle_data(self,d):
  if not self.block and d.strip():self.nodes.append(d.strip())
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']};texts={};records=[];sources=set();n=0
for c in a['cards']:
 q=qs[c['questionId']];assert sha(cj(q,True))==c['canonicalCardSha256'];assert len(c['fields'])==6
 for f in c['fields']:
  key=f['field'];lit={'prompt':q['prompt'],'options':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']} if key=='prompt-key' else q['explanation'] if key=='explanation' else q['answers'][int(key[4:])]['note']
  assert lit==f['literal'];assert sha(cj(lit) if isinstance(lit,dict) else lit.encode())==f['literalSha256'];proofs=[]
  for ref in f['proofs']:
   si,ei=map(int,re.fullmatch(r'source-context.json#sources\[(\d+)\].extracts\[(\d+)\]',ref).groups());src=s['sources'][si];e=src['extracts'][ei];p=ROOT/src['rawCapturePath'];raw=p.read_bytes()
   assert raw==git('fc2e8ff',p)==git('HEAD',p);assert len(raw)==src['rawSize'];assert sha(raw)==src['rawSha256'];assert subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(p)],text=True).strip()==src['gitBlob']
   if str(p) not in texts:x=Nodes();x.feed(raw.decode());texts[str(p)]=x.nodes
   assert texts[str(p)][e['locator']['htmlTextNodeIndex0Based']]==e['exactQuote'];assert sha(e['exactQuote'].encode())==e['exactQuoteSha256'];sources.add(src['rawCapturePath']);n+=1
   proofs.append({'sourceRef':src['rawCapturePath'],'rawSha256':sha(raw),'gitBlob':src['gitBlob'],'locator':e['locator'],'quoteSha256':e['exactQuoteSha256']})
  records.append({'id':q['id'],'authorIdentity':a['authorIdentity'],'receiptCommit':'fc2e8ff','receipt':str(ar.relative_to(ROOT)),'receiptSha256':sha(ra),'sourceContextSha256':sha(rs),'cardSortedSha256':sha(cj(q,True)),'field':key,'literalSha256':f['literalSha256'],'proofs':proofs})
scope=json.loads((OUT/'winter058-note1-precise-runtime-scope.json').read_text());assert all(sha(cj(qs[x['id']],True))==x['sha256'] for x in scope['protected99']);before=scope['beforeCard'];after=dict(qs['winter-sports-058']);assert after['answers'][1]['note']==scope['newLiteral'];after=json.loads(json.dumps(after));after['answers'][1]['note']=before['answers'][1]['note'];assert after==before
report={'purpose':'Preservation only; source/editorial approval requiresactualdifferentreader','cards':2,'fields':12,'quoteBindings':n,'originals':sorted(sources),'records':records,'protected99And058OtherFields':True,'errors':0}
(OUT/'winter-current057058-author-roundtrip.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':2,'fields':12,'quotes':n,'originals':len(sources),'protected99':True,'errors':0})
