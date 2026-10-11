"""Bounded raw capture / working-disk / committed Git blob binding. No verdicts."""
import json,hashlib,subprocess,io,sys,os
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
IDENTITY='01a12c3f-d480-76f2-89bd-c49dcc5becfe'
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(p,head):return subprocess.check_output(['git','show',head+':'+str(p.relative_to(REPO))],cwd=REPO)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden and d.strip():self.parts.append(' '.join(d.split()))
def extract(b,p):
 if p.suffix=='.pdf':return [x.extract_text() for x in PdfReader(io.BytesIO(b)).pages]
 if p.suffix in ('.json','.txt'):return b.decode()
 t=Text();t.feed(b.decode());return t.parts

def bind(topic,ids,authorDir,receiptMap,label):
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();path=REPO/'src/content/topics'/f'{topic}.json';disk=json.loads(path.read_text());git=json.loads(blob(path,head));byid={q['id']:q for q in disk['questions']};gitby={q['id']:q for q in git['questions']};captures={};rows=[];read=[]
 for qid in ids:
  q=byid[qid];rp=REPO/authorDir/receiptMap[qid];r=json.loads(rp.read_text());a=next(x for x in r['cards'] if x['questionId']==qid);h=sha(canonical(q));assert h==a['cardCanonicalSha256']==sha(canonical(gitby[qid])),qid
  assert r['agentIdentity']!=IDENTITY and r['role']=='author'
  row={'questionId':qid,'cardCanonicalSha256':h,'diskAndGitCardMatch':True,'authorIdentity':r['agentIdentity'],'authorReceipt':str(rp.relative_to(REPO)),'authorReceiptSha256':sha(rp.read_bytes()),'fields':[]};assert rp.read_bytes()==blob(rp,head)
  read.append('\nCARD '+json.dumps(q,ensure_ascii=False))
  for f in a['fields']:
   literal=canonical([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]) if f['field']=='prompt-key' else (q['explanation'] if f['field']=='explanation' else q['answers'][int(f['field'][-1])]['note']).encode();assert sha(literal)==f['literalSha256']
   proofs=[]
   for p in f['proofs']:
    raw=rp.parent/p['rawCapture'];b=raw.read_bytes();rawrel=str(raw.relative_to(REPO))
    if rawrel not in captures:
     gb=blob(raw,head);assert b==gb and sha(b)==p['rawCaptureSha256'];captures[rawrel]=(extract(b,raw),extract(gb,raw))
    dn,gn=captures[rawrel];loc=p['locator'];quote=p['passage'];assert sha(quote.encode())==p['passageSha256']
    if isinstance(loc,dict) and 'jsonPointer' in loc:
     actual=json.loads(dn);actualgit=json.loads(gn)
     for part in loc['jsonPointer'].split('/')[1:]:
      actual=actual[int(part)] if isinstance(actual,list) else actual[part];actualgit=actualgit[int(part)] if isinstance(actualgit,list) else actualgit[part]
     quote=p.get('decodedPassage',quote)
    elif isinstance(loc,dict) and 'pdfPage' in loc:actual=dn[loc['pdfPage']-1];actualgit=gn[loc['pdfPage']-1]
    elif isinstance(dn,list) and isinstance(loc,dict) and 'textNodeStart' in loc:actual=' '.join(dn[loc['textNodeStart']:loc['textNodeEnd']+1]);actualgit=' '.join(gn[loc['textNodeStart']:loc['textNodeEnd']+1])
    elif isinstance(dn,list):actual=' '.join(dn);actualgit=' '.join(gn)
    else:actual=dn;actualgit=gn
    assert actual==actualgit and (quote in actual or ' '.join(quote.split()) in ' '.join(actual.split())),(qid,f['field'],rawrel)
    pp={**p,'rawCapture':os.path.relpath(raw,ROOT/label),'diskGitRawMatch':True,'diskGitExtractMatch':True};proofs.append(pp)
    read.append(f"{f['field']} RAW {rawrel} LOC {loc}:\n{actual}")
   row['fields'].append({'field':f['field'],'literalSha256':sha(literal),'proofs':proofs})
  rows.append(row)
 out=ROOT/label;out.mkdir(exist_ok=True);(out/'bindings.json').write_text(json.dumps({'role':'independent','agentIdentity':IDENTITY,'sourceHead':head,'cards':rows,'mechanicalOnly':True},ensure_ascii=False,indent=2)+'\n');(out/'reading-pack.txt').write_text('\n'.join(x.rstrip() for x in '\n'.join(read).splitlines())+'\n');(out/'current-cards.json').write_text(json.dumps([byid[i] for i in ids],ensure_ascii=False,indent=2)+'\n');print(label,len(rows),'cards bound',len(captures),'originals')
if __name__=='__main__':
 topic,label,start,end=sys.argv[1:];p='docs/content-audits/question-quality-wave-6/'+topic+'/resume-2026-10-11-author100';m=json.loads((REPO/p/'author100-manifest.json').read_text());bind(topic,[f'winter-sports-{i:03}' for i in range(int(start),int(end)+1)],p,m['sourceReceipts'],label)
