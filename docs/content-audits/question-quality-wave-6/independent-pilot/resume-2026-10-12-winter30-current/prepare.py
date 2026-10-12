import json,hashlib,subprocess,os,shutil
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter30-current'
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-author30/final-current-author-receipt.json'
r=json.loads(AUTHOR.read_bytes()); raw=(ROOT/'src/content/topics/winter-sports.json').read_bytes(); frozen=subprocess.check_output(['git','show','b31dc20:src/content/topics/winter-sports.json'],cwd=ROOT); assert raw==frozen
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':')).encode()
class Nodes(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.skip=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
(OUT/'sources').mkdir(exist_ok=True);(OUT/'readings').mkdir(exist_ok=True)
(OUT/'.gitattributes').write_text('sources/** -text\n')
q=json.loads(raw)['questions']; base=json.loads(subprocess.check_output(['git','show','134cb42:src/content/topics/winter-sports.json'],cwd=ROOT))['questions'];b={x['id']:x for x in base}
pre={'readerThreadId':os.environ['CODEX_THREAD_ID'],'authorThreadId':r['authorThreadId'],'frozenCommit':'b31dc20','topicSha256':sha(raw),'diskEqualsFrozen':True,'canonicalRecipe':'SHA256 UTF8 json.dumps(card,ensure_ascii=False,separators=(comma,colon)), property order preserved, no newline','promptLiteralRecipe':'compact JSON object {prompt,options:[all four answer texts],correctIndex,key}; UTF8 SHA256 no newline','otherLiteralRecipe':'UTF8 exact string, no newline','scopeIds':r['scopeIds'],'protected70UnchangedVs134cb42':all(canon(x)==canon(b[x['id']]) for x in q if x['id'] not in r['scopeIds']),'cards':[{'id':x['id'],'difficulty':x['difficulty'],'wholeCardSha256':sha(canon(x)),'actualCard':x} for x in q if x['id'] in r['scopeIds']]}
assert pre['protected70UnchangedVs134cb42']
(OUT/'preflight.json').write_text(json.dumps(pre,ensure_ascii=False,indent=2)+'\n')
manifest=[]
paths={p['rawCapture']:p for c in r['cards'] for f in c['fields'] for p in f['proofBindings']}
for path,p in sorted(paths.items()):
 data=(ROOT/path).read_bytes();assert sha(data)==p['rawSha256'];assert data==subprocess.check_output(['git','show','b31dc20:'+path],cwd=ROOT)
 name=Path(path).name;(OUT/'sources'/name).write_bytes(data)
 blob=subprocess.check_output(['git','hash-object','--no-filters','--stdin'],input=data,cwd=ROOT).decode().strip()
 m={'id':name,'originalUrl':p['url'],'captureUrl':p['url'],'captureOrigin':path,'readerAcquisition':'byte-identical full original frozen in author commit; independently extracted and read, no author verdict imported','sourceClass':p['sourceClass'],'rawFormat':p['rawFormat'],'size':len(data),'sha256':sha(data),'gitBlob':blob,'path':str((OUT/'sources'/name).relative_to(ROOT))}
 if name.endswith('.pdf'):
  pdf=PdfReader(OUT/'sources'/name);m['pages']=len(pdf.pages); pages={str(i+1):page.extract_text() for i,page in enumerate(pdf.pages)};out={'physicalPages1Based':pages}
 else:
  parser=Nodes();parser.feed(data.decode('utf8',errors='replace'));out={'recipe':'stdlib HTMLParser convert_charrefs=True; strip each nonempty handle_data outside script/style; indices zero based','textNodes':parser.nodes}
 (OUT/'readings'/(name+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');manifest.append(m)
(OUT/'sources-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('snapshot',len(pre['cards']),'sources',len(manifest),'protected',pre['protected70UnchangedVs134cb42'])
