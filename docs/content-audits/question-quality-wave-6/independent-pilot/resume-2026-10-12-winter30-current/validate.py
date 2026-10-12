import json,hashlib,subprocess,re,sys
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter30-current';MODE=sys.argv[1] if len(sys.argv)>1 else 'disk';sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':')).encode()
class Nodes(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
r=json.loads((OUT/'independent-receipt.json').read_text());pre=json.loads((OUT/'preflight.json').read_text());data=(ROOT/'src/content/topics/winter-sports.json').read_bytes();frozen=subprocess.check_output(['git','show','b31dc20:src/content/topics/winter-sports.json'],cwd=ROOT);assert data==frozen and sha(data)==r['topicSha256'];current={q['id']:q for q in json.loads(data)['questions']};baseline={q['id']:q for q in json.loads(subprocess.check_output(['git','show','134cb42:src/content/topics/winter-sports.json'],cwd=ROOT))['questions']}
assert set(r['scopeIds'])=={c['questionId'] for c in r['cards']} and len(r['cards'])==30
assert all(canon(q)==canon(baseline[k]) for k,q in current.items() if k not in r['scopeIds'])
assert all(current[k]['difficulty']==baseline[k]['difficulty'] and current[k]['correctIndex']==baseline[k]['correctIndex'] for k in r['scopeIds'])
assert r['readerThreadId']=='01a12ed4-9c6d-7900-aa8c-06949c95a63e' and r['authorThreadId']=='01a12eaf-5d14-7043-9b9e-a8bbb435a7f9'
manifest=json.loads((OUT/'sources-manifest.json').read_text());rawcount=0
for m in manifest:
 path=ROOT/m['path'];raw=path.read_bytes();assert len(raw)==m['size'] and sha(raw)==m['sha256'];blob=subprocess.check_output(['git','hash-object','--no-filters','--stdin'],input=raw,cwd=ROOT).decode().strip();assert blob==m['gitBlob'];attr=subprocess.check_output(['git','check-attr','text','--',m['path']],cwd=ROOT).decode().strip();assert attr.endswith('unset')
 if MODE in ('staged','committed'):
  ref=':'+m['path'] if MODE=='staged' else 'HEAD:'+m['path'];stored=subprocess.check_output(['git','show',ref],cwd=ROOT);assert stored==raw
 rawcount+=1
fields=quotes=0;seen=set()
for c in r['cards']:
 q=current[c['questionId']];assert sha(canon(q))==c['wholeCardSha256'];assert c['difficulty']==q['difficulty'] and c['correctIndex']==q['correctIndex'];assert len(c['fields'])==6;names={f['field'] for f in c['fields']};assert names=={'prompt-key','explanation','note0','note1','note2','note3'}
 sentence_count=len([x for x in re.split(r'[.!?]+(?:\s|$)',q['explanation']) if x.strip()]);assert 2<=sentence_count<=4
 for f in c['fields']:
  name=f['field'];lit={'prompt':q['prompt'],'options':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']} if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[-1])]['note'];assert lit==f['literal'];assert sha(canon(lit) if isinstance(lit,dict) else lit.encode())==f['literalSha256'];assert f['sourceVerdict'] in ('PASS','FIX','HOLD') and f['editorialVerdict'] in ('PASS','FIX','HOLD');assert f['sourceAnalysis'] and f['editorialAnalysis'] and f['substantiveRead'];assert f['proofBindings'];fields+=1
  for b in f['proofBindings']:
   assert b['id']!='skate-terms180.html';assert sha(b['exactQuote'].encode())==b['exactQuoteSha256'];raw=(ROOT/b['path']).read_bytes();assert sha(raw)==b['sha256'] and len(raw)==b['size'];locator=b['locator']
   if 'htmlTextNodeIndex0Based' in locator:
    parser=Nodes();parser.feed(raw.decode('utf8',errors='replace'));assert b['exactQuote']==parser.nodes[locator['htmlTextNodeIndex0Based']]
   else:
    # Compare against fresh extraction of the original complete PDF, not a supplied excerpt.
    from pypdf import PdfReader
    key=(b['path'],locator['pdfPhysicalPage1Based'])
    if key not in seen:seen.add(key)
    text=PdfReader(ROOT/b['path']).pages[locator['pdfPhysicalPage1Based']-1].extract_text();assert b['exactQuote'] in text
   quotes+=1
assert fields==180
counts={'cards':30,'fields':fields,'cardVerdicts':dict(Counter(c['independentVerdict'] for c in r['cards'])),'fieldSourceVerdicts':dict(Counter(f['sourceVerdict'] for c in r['cards'] for f in c['fields'])),'fieldEditorialVerdicts':dict(Counter(f['editorialVerdict'] for c in r['cards'] for f in c['fields']))};assert counts==r['counts']
# Check only owned authored metadata/scripts. Original source whitespace is deliberately excluded.
for path in OUT.rglob('*'):
 if path.is_file() and path.suffix in ('.py','.json','.md') and 'sources' not in path.relative_to(OUT).parts:
  for n,line in enumerate(path.read_text().splitlines(),1):assert line==line.rstrip(' \t'),(str(path),n)
owned_files=[p for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
if MODE in ('staged','committed'):
 for p in owned_files:
  rel=str(p.relative_to(ROOT));ref=':'+rel if MODE=='staged' else 'HEAD:'+rel
  assert subprocess.check_output(['git','show',ref],cwd=ROOT)==p.read_bytes(),rel
result={'mode':MODE,'structuralResult':'PASS','substantiveCertification':False,'topicDiskEqualsFrozen':True,'protectedCardsUnchanged':70,'difficultyAndKeyUnchanged':30,'literalHashesAndReadings':fields,'proofQuotesVerified':quotes,'sourceRecordsVerified':rawcount,'ownedPersistentFilesVerified':len(owned_files),'rawStorageBytesMatch':MODE,'counts':counts,'checksReason':'Own receipts, actual full literals, frozen-current invariants, original-byte SHA/blob/locator integrity only. No catalog-full or runtime test route.'}
if MODE=='committed':result['commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
print(json.dumps(result,ensure_ascii=False))
