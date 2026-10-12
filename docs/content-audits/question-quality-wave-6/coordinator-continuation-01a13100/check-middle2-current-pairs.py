"""Literal/source integrity; substantive adjudication is recorded separately."""
import json,hashlib,subprocess,runpy,re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');BASE=ROOT/'docs/content-audits/question-quality-wave-6';OUT=BASE/'coordinator-continuation-01a13100';RF=BASE/'independent-pilot/middle-current2-e07f9d8-native-01a131c5-edfb-7b82-8ddf-bd88a8b95597-v2'
sha=lambda b:hashlib.sha256(b).hexdigest();H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
m=json.loads((RF/'manifest.json').read_text());assert sha((RF/'manifest.json').read_bytes())=='38932c1bea10e9267ed155265e0656d2760d28fce254c2c38952479df75d8406'
for f in m['files']:
 p=ROOT/f['intendedRepositoryPath'];b=p.read_bytes();assert b==frozen('b8527c1',p)==frozen('HEAD',p) and sha(b)==f['SHA256'] and len(b)==f['bytes'];assert b==(Path(m['sourceDirectory'])/f['relativePath']).read_bytes()
st=runpy.run_path(str(OUT/'check-middle2-v3-author.py'));a=st['a'];r=json.loads((RF/'reader-receipt-v2.json').read_text());sp=json.loads((RF/'source-proofs-v2.json').read_text())
assert r['readerNativeId']==sp['readerNativeId']=='01a131c5-edfb-7b82-8ddf-bd88a8b95597'!=a['authorNativeId'] and r['authorNativeId']==a['authorNativeId']
assert r['authorReceiptSHA256']==sha(st['AP'].read_bytes()) and r['wholeCardHashes']==a['wholeCardHashes'] and r['actualCompactions']==0 and r['counterDelta']==0
old=ROOT/sp['oldProofFile'];assert old.read_bytes()==frozen('d9a5ead',old) and sha(old.read_bytes())==sp['oldProofSHA256']
for src in sp['rawOriginals']:assert src['rawSHA256']==src['actualRawSHA256']==sha(st['raws'][src['id']]) and src['originalGitBlob']==st['register'][src['id']]['originalGitBlob']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,x):self.parts.append(x)
html=st['raws']['fulcher'].decode();parser=Parser();parser.feed(html[html.index('<a name="urban2"'):html.index('<a name="capture"')]);contexts={'fulcher-section1.txt':re.sub(r'\s+',' ',' '.join(parser.parts)).strip(),'cnrtl-full-header.json':json.dumps(json.loads(st['raws']['cnrtl-croisade'])['header'],ensure_ascii=False,indent=2)+'\n'}
for sid,pages,name in [('glasgow',[1,2],'glasgow-cover.txt'),('glasgow',[21,22,23],'glasgow-context21-23.txt'),('syed',[12],'syed-page12.txt')]:
 pdf=PdfReader(st['F']/st['register'][sid]['containerPath']);contexts[name]=re.sub(r'\s+',' ','\n\n'.join(pdf.pages[i-1].extract_text() for i in pages)).strip()
proofs={p['id']:p for p in sp['proofs']};verified=[]
for p in proofs.values():
 assert p['sourceSHA256']==sha(st['raws'][p['sourceId']]) and sha(p['exactSufficientQuote'].encode())==p['quoteSHA256']
 if p['typedLocator']['type']=='visual-scan-page':
  img=ROOT/p['renderPath'];assert img.read_bytes()==frozen('d9a5ead',img)==frozen('HEAD',img) and sha(img.read_bytes())==p['renderSHA256'];v=json.loads((OUT/'middle-v4-coordinator-lapidus-visual-source.json').read_text());assert v['exactObservedQuote']==p['exactSufficientQuote'] and v['rawSHA256']==p['sourceSHA256'] and p['offset'] is None
 else:
  cp=ROOT/p['contextPath'];text=contexts[cp.name];assert text.encode()==cp.read_bytes()==frozen('d9a5ead',cp)==frozen('HEAD',cp) and sha(cp.read_bytes())==p['contextSHA256'];assert text[p['offset']:p['offset']+len(p['exactSufficientQuote'])]==p['exactSufficientQuote']
 verified.append({'id':p['id'],'sourceSHA256':p['sourceSHA256'],'quoteSHA256':p['quoteSHA256'],'typedLocator':p['typedLocator']})
for ev in a['evidence']:
 assert sha(ev['exactSufficientQuote'].encode())==ev['quoteSHA256'] and ev['fullOriginal']['rawSHA256']==sha(st['raws'][ev['sourceId']])
 if ev['sourceId']=='lapidus':assert ev['exactSufficientQuote']==proofs['lapidus-granada']['exactSufficientQuote']
 else:assert any(ev['exactSufficientQuote'] in t for t in contexts.values())
bindings=[]
assert len(r['groups'])==12 and len(r['currentWholeCards'])==2
for q in r['currentWholeCards']:
 ident=q['id'];assert q==st['qs'][ident] and H(q)==r['wholeCardHashes'][ident];assert r['wholeCardVerdicts'][ident]=={'source':'PASS','editorial':'PASS'}
 ag=[g for g in a['groups'] if g['cardId']==ident];rg=[g for g in r['groups'] if g['cardId']==ident];assert len(ag)==len(rg)==6
 for x,y in zip(ag,rg):
  assert x['group']==y['group'] and x['literal']==y['currentLiteral'] and H(x['literal'])==x['canonicalSHA256']==y['currentCanonicalSHA256']==y['expectedAuthorCanonicalSHA256']
  assert y['sourceVerdict']==y['editorialVerdict']=='PASS' and y['sourceReason'] and y['editorialReason'] and y['personalCurrentWholeRead']
  for p in y['sourceProofs']:assert p==proofs[p['id']]
  assert y['proofRefs'] and all(p in proofs for p in y['proofRefs'])
  if y['group']=='prompt-answers-key':
   assert len(y['orderedChoices'])==4
   for i,o in enumerate(y['orderedChoices']):assert o['index']==i and o['text']==q['answers'][i]['text'] and o['sourceAssessment'] and o['plausibilityAndUniqueAnswerAssessment']
  bindings.append({'cardId':ident,'group':x['group'],'literalSHA256':H(x['literal']),'cardSHA256':H(q),'proofRefs':y['proofRefs']})
assert all(x['editorialVerdict']=='PASS' for x in r['difficulty']) and all(x['sourceVerdict']==x['editorialVerdict']=='PASS' for x in r['sourceMetadataVerdicts'])
d=json.loads((RF/'catalogue-current-retrieval.json').read_text());assert d['cards']==11000 and d['topicFiles']==110 and d['editorialDedupVerdict']=='PASS' and len(d['personallyReadFullRelevantNeighbors'])==10
report={'purpose':'Exact pair/source/literal preservation; manual editorial adjudication separate','authorFreeze':'c76bdab','readerFreeze':'b8527c1','runtimeFreeze':'e07f9d8','authorNativeId':a['authorNativeId'],'readerNativeId':r['readerNativeId'],'authorReceiptSHA256':sha(st['AP'].read_bytes()),'readerReceiptSHA256':sha((RF/'reader-receipt-v2.json').read_bytes()),'ids':a['scopeIds'],'roleGroups':24,'bindings':bindings,'typedProofs':verified,'fullOriginals':5,'protected98':'exact','originalHistoricalExpectedHashesUnchanged':True,'errors':0,'counterDelta':0}
(OUT/'middle2-current-pair-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':2,'roleGroups':24,'typedProofs':12,'rawOriginals':5,'errors':0,'credit':0})
