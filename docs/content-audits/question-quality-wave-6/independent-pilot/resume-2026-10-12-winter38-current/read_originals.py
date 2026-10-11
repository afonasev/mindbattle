"""Independent byte/extraction/provenance mechanics. Never generates editorial verdicts."""
import json, hashlib, subprocess, os
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework31'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Visible(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:
   t=' '.join(data.split())
   if t:self.nodes.append(t)
def git(args):return subprocess.check_output(['git',*args],cwd=ROOT)
def main():
 topic=json.loads((ROOT/'src/content/topics/winter-sports.json').read_bytes());byid={c['id']:c for c in topic['questions']}
 sources={};binds=[];cards=[]
 for name in ('pilot-five','rework25','addendum7','073'):
  path=AUTHOR/(name+'-author-receipt.json');raw=path.read_bytes();rel=str(path.relative_to(ROOT));gitraw=git(['show','HEAD:'+rel]);assert raw==gitraw
  commit=git(['log','-1','--format=%H','--',rel]).decode().strip()
  receipt=json.loads(raw);binds.append({'path':rel,'sha256':sha(raw),'gitBlobSha256':sha(gitraw),'lastCommit':commit,'agentIdentity':receipt['agentIdentity'],'scopeCount':len(receipt['cards']),'frozenLiteralRecipe':{'prompt-key':"UTF-8(prompt + '\\n' + answers[correctIndex].text)",'note0..note3/explanation':'UTF-8 literal string','wholeCard':'UTF-8 JSON ensure_ascii=False sort_keys=True separators=(comma,colon)'}})
  for authored in receipt['cards']:
   c=byid[authored['questionId']];assert sha(canonical(c))==authored['cardCanonicalSha256']
   fields=[]
   for f in authored['fields']:
    literal=c['prompt']+'\n'+c['answers'][c['correctIndex']]['text'] if f['field']=='prompt-key' else c['explanation'] if f['field']=='explanation' else c['answers'][int(f['field'][-1])]['note']
    assert sha(literal.encode())==f['literalSha256']
    proofs=[]
    for proof in f['proofs']:
     s=dict(proof);s.pop('readerIdentity',None);path=AUTHOR/s['rawCapture'];rel=str(path.relative_to(ROOT));s['rawCapture']=rel
     if rel not in sources:
      raw=path.read_bytes();gitraw=git(['show','HEAD:'+rel]);assert raw==gitraw;assert sha(raw)==s['rawCaptureSha256']
      if path.suffix=='.pdf':nodes=[p.extract_text() or '' for p in PdfReader(path).pages];fmt='pdf'
      else: parser=Visible();parser.feed(raw.decode('utf-8',errors='replace'));nodes=parser.nodes;fmt='html'
      sources[rel]={'url':s['url'],'rawCaptureSha256':sha(raw),'gitBlobSha256':sha(gitraw),'format':fmt,'nodes':nodes,'lastCommit':git(['log','-1','--format=%H','--',rel]).decode().strip()}
     nodes=sources[rel]['nodes'];loc=s['locator']
     extracted=nodes[loc['pdfPage']-1] if 'pdfPage' in loc else ' '.join(nodes[loc['textNodeStart']:loc['textNodeEnd']+1])
     assert sha(s['passage'].encode())==s['passageSha256']
     s['independentLocatorMatches']=extracted==s['passage'];s['independentExtractedPassage']=extracted
     proofs.append(s)
    fields.append({'field':f['field'],'literal':literal,'authorLiteralSha256':f['literalSha256'],'proofs':proofs})
   cards.append({'card':c,'cardCanonicalSha256':sha(canonical(c)),'authorReceipt':rel if False else str((AUTHOR/(name+'-author-receipt.json')).relative_to(ROOT)),'fields':fields})
 data={'agentIdentity':os.environ.get('CODEX_THREAD_ID'),'authorIdentity':'01a12c87-f8e7-7232-823d-c0be717a70dc','snapshotCommit':git(['rev-parse','HEAD']).decode().strip(),'authorBindings':binds,'sources':sources,'cards':cards}
 assert data['agentIdentity']!=data['authorIdentity'];assert len(cards)==38
 (OUT/'originals-and-bindings.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('38 current hashes and 228 author literals bound;',len(sources),'complete originals disk/Git exact; locator mismatch count:',sum(not p['independentLocatorMatches'] for c in cards for f in c['fields'] for p in f['proofs']))
if __name__=='__main__':main()
