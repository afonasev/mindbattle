"""Mechanical serialization only. All verdicts and analyses come from manual.json."""
import json,pathlib,hashlib,subprocess,re,html
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[5]
OUT=pathlib.Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.data=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.data.append(d)
def norm(s):return re.sub(r'\s+',' ',s).strip()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def content(raw):
 b=raw.read_bytes()
 if raw.suffix=='.pdf':
  from pypdf import PdfReader
  return '\n'.join(p.extract_text() for p in PdfReader(raw).pages)
 s=b.decode()
 if s.lstrip().startswith('{'):
  return html.unescape(s)+ '\n' + '\n'.join(str(x) for x in json.loads(s).values())
 t=Text();t.feed(s);return ''.join(t.data)
manual=json.loads((OUT/'manual.json').read_text())
for group,spec in manual.items():
 receipt=ROOT/spec['receipt']; author=json.loads(receipt.read_text());topic=ROOT/spec['topic'];working=json.loads(topic.read_text());frozen=json.loads(subprocess.check_output(['git','show',spec['freeze']+':'+spec['topic']]))
 records=[];files={}
 for decision in spec['decisions']:
  c=next(c for c in author['cards'] if c['questionId']==decision['id']);q=next(q for q in working['questions'] if q['id']==decision['id']);fq=next(q for q in frozen['questions'] if q['id']==decision['id']);assert q==fq;assert sha(canon(q))==c['cardCanonicalSha256']
  literals=[[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]]+[a['note'] for a in q['answers']]+[q['explanation']]
  fields=[]
  for index,entry in enumerate(decision['fields']):
   name=['prompt-key','note0','note1','note2','note3','explanation'][index];proofs=[]
   if spec.get('proofMode')=='author-original':
    for p in c['fields'][index]['proofs']:
     p=dict(p);raw=(receipt.parent/p['rawCapture']).resolve();b=raw.read_bytes();git=subprocess.check_output(['git','show',spec['freeze']+':'+str(raw.relative_to(ROOT))]);assert b==git and sha(b)==p['rawCaptureSha256'];assert norm(p['passage']) in norm(content(raw)),(q['id'],name,raw)
     p['rawCapture']=str(raw.relative_to(ROOT));p['gitFreeze']=spec['freeze'];p['independentOriginalRead']=True;proofs.append(p);files[str(raw.relative_to(ROOT))]={'diskSha256':sha(b),'gitSha256':sha(git),'exact':b==git,'bytes':len(b)}
   else:
    for p in entry.get('proofs',[]):
     p=dict(p);raw=OUT/p['rawCapture'];b=raw.read_bytes();assert '</html>' in b.decode().lower();assert norm(p['passage']) in norm(content(raw)),(q['id'],name,p['passage']);p['rawCapture']=str(raw.relative_to(ROOT));p['rawCaptureSha256']=sha(b);p['passageSha256']=sha(p['passage'].encode());p['captureFormat']='complete original HTML, curl --compressed successful response';p['independentOriginalRead']=True;proofs.append(p)
   fields.append({'field':name,'literal':literals[index],'literalSha256':sha(canon(literals[index])),'verdict':entry['verdict'],'claimAnalysis':entry['analysis'],'substantiveRead':True,'proofs':proofs,**({'rule':entry['rule']} if 'rule' in entry else {})})
  assert len(fields)==6
  records.append({'questionId':q['id'],'cardCanonicalSha256':sha(canon(q)),'sourceUrl':q['source']['url'],'verdict':decision['verdict'],'editorialAnalysis':decision['analysis'],'fields':fields,'sourceRole':'independent-reader','authorIdentity':spec['author'],'currentCard':q})
 result={'role':'independent-reader','agentIdentity':'01a12c38-65ee-75d0-bec1-05ae39103798','date':'2026-10-11','decisionMethod':'Manual original and literal reading; serializer supplies no substantive verdicts. No root certification.','freeze':spec['freeze'],'cards':records}
 (OUT/group/'reader-receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (OUT/group/'input-byte-readback.json').write_text(json.dumps({'files':files,'cards':len(records),'fields':len(records)*6,'hashesMatched':True},indent=2)+'\n')
 print(group,len(records),{v:sum(c['verdict']==v for c in records) for v in ['PASS','FIX','HOLD']})
