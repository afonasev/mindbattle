import subprocess,json,hashlib,io,sys,logging
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)
R=Path(__file__).parent
REV=sys.argv[1] if len(sys.argv)>1 else 'HEAD'
def blob(p):
 p=Path(p)
 if p.is_absolute():p=p.relative_to(Path.cwd())
 return subprocess.check_output(['git','show',f'{REV}:{p}'])
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda q:json.dumps(q,ensure_ascii=False,separators=(',',':')).encode()
class Visible(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,t):
  t=' '.join(t.split())
  if not self.skip and t:self.nodes.append(t)
receipt=json.loads(blob(R/'reader-receipt.json'));index=json.loads(blob(R/'source-index.json'));sources={};nodes={};PDF={};rows=[]
for m in index:
 b=blob(m['frozenPath']);assert b==Path(m['frozenPath']).read_bytes();assert sha(b)==m['rawSha256'];assert b==subprocess.check_output(['git','show',m['sourceRevision']+':'+m['originalGitPath']]);assert subprocess.check_output(['git','hash-object','--stdin'],input=b).decode().strip()==m['gitBlob'];sources[m['frozenPath']]=b
 if m['frozenPath'].endswith('.html'):
  h=Visible();h.feed(b.decode());assert h.nodes==m['visibleNodes'];nodes[m['frozenPath']]=h.nodes
 rows.append({'path':m['frozenPath'],'rawSha256':sha(b),'bytes':len(b),'gitBlob':m['gitBlob'],'sourceAndEvidenceAndWorktreeBytesIdentical':True})
fieldcount=0;proofcount=0
for c in receipt['cards']:
 assert sha(canon(c['literalCard']))==c['cardCanonicalSha256']
 for f in c['fields']:
  assert sha(f['literal'].encode())==f['literalSha256'];assert f['agentIdentity']==receipt['agentIdentity'];fieldcount+=1
  for p in f['proofs']:
   b=sources[p['rawCapture']];assert sha(b)==p['rawSha256'];loc=p['locator']
   if 'physicalPdfPage' in loc:
    if p['rawCapture'] not in PDF:PDF[p['rawCapture']]=PdfReader(io.BytesIO(b))
    text=PDF[p['rawCapture']].pages[loc['physicalPdfPage']-1].extract_text()
   else:text=' '.join(nodes[p['rawCapture']][loc['textNodeStart']:loc['textNodeEnd']+1])
   assert text==p['quotedPassage'];assert sha(text.encode())==p['quotedPassageSha256'];proofcount+=1
assert fieldcount==30 and len(receipt['cards'])==5
for name,original in [('current-topic-frozen.json','src/content/topics/winter-sports.json'),('author-receipt-frozen.json','docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/followup1/author-receipt.json')]:assert blob(R/name)==subprocess.check_output(['git','show',receipt['authorRevision']+':'+original])
failed=[]
for f in sorted((R/'failed').glob('*')):
 b=blob(f);assert b==f.read_bytes();failed.append({'path':str(f),'sha256':sha(b),'bytes':len(b),'excludedFromProof':True})
print(json.dumps({'status':'PASS','evidenceRevision':REV,'agentIdentity':receipt['agentIdentity'],'authorRevision':receipt['authorRevision'],'cards':5,'fields':fieldcount,'proofs':proofcount,'rawOriginals':rows,'failedCaptures':failed,'cardVerdicts':receipt['cardVerdictCounts'],'fieldVerdicts':receipt['fieldVerdictCounts'],'note':'Byte/literal/passage preservation PASS does not upgrade editorial FIX/HOLD or confer human acceptance.'},indent=2))
