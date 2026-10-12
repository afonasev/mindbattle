"""Exact source and literal preservation only; no generated editorial grade."""
import json,hashlib,gzip,subprocess,re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');BASE=ROOT/'docs/content-audits/question-quality-wave-6';OUT=BASE/'coordinator-continuation-01a13100';F=BASE/'middle-ages/repair2-2026-10-13-native-01a131a7-847b-7073-aa71-27ae12d45778';AP=F/'author-source-editorial-review-v3.json';SR=F/'source-register.json'
sha=lambda b:hashlib.sha256(b).hexdigest();H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
for p in [AP,SR]:assert p.read_bytes()==frozen('c76bdab',p)==frozen('HEAD',p)
a,s=json.loads(AP.read_text()),json.loads(SR.read_text());assert a['authorNativeId']==s['authorNativeId']=='01a131a7-847b-7073-aa71-27ae12d45778';assert sha(AP.read_bytes())=='cbb6b16d99490734839cb96397c7b20581a03f3b9faa6b924ed4e1726d247129'
sc=ROOT/a['scopeFreeze'];scope=json.loads(sc.read_text());assert sc.read_bytes()==frozen('7a2ffe2',sc);rt=ROOT/a['runtimePath'];assert rt.read_bytes()==frozen('e07f9d8',rt)==frozen('HEAD',rt)
qs={q['id']:q for q in json.loads(rt.read_text())['questions']};assert [q['id'] for q in json.loads(rt.read_text())['questions']]==scope['order'] and len(qs)==100
for c in scope['protected98']:assert H(qs[c['id']])==c['cardSHA256']
for c in scope['scopedBefore']:assert qs[c['id']]['difficulty']==c['difficulty'] and qs[c['id']]['correctIndex']==c['correctIndex'] and H(qs[c['id']])==a['wholeCardHashes'][c['id']] and H(c['currentCard'])==a['hashRoleSeparation']['originalScopeBefore']['cardHashes'][c['id']]

for role in a['hashRoleSeparation'].values():
 if isinstance(role,dict) and 'commit' in role:
  historical={q['id']:q for q in json.loads(frozen(role['commit'],rt))['questions']}
  for ident,expectedSHA in role['cardHashes'].items():assert H(historical[ident])==expectedSHA
assert a['personalQualification']['authorNativeId']==a['authorNativeId'] and a['personalQualification']['rereadCurrentWhole12']
v2=F/'author-source-editorial-review-v2.json';assert v2.read_bytes()==frozen('e07f9d8',v2)==frozen('HEAD',v2) and sha(v2.read_bytes())=='9c91f7616c2cab348e445ba4fa89d8a3160e7c685c5c0f08ba00ebb8cc8ec0c8'

class Visible(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=[]
 def handle_starttag(self,t,attrs):
  if t in ('script','style'):self.skip.append(t)
 def handle_endtag(self,t):
  if t in self.skip:self.skip.pop()
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def norm(t):return re.sub(r'\s+',' ',t).strip()
def visible(raw):
 p=Visible();p.feed(raw.decode('utf-8',errors='replace'));return norm(' '.join(p.parts))
raws={};register={};sourceproof=[]
for src in s['sources']:
 p=F/src['containerPath'];cb=p.read_bytes();raw=gzip.decompress(cb) if p.suffix=='.gz' else cb
 assert cb==frozen('c76bdab',p)==frozen('HEAD',p) and len(cb)==src['containerBytes']
 assert len(raw)==src['rawBytes'] and sha(raw)==src['rawSHA256']
 if src['containerSHA256']:assert sha(cb)==src['containerSHA256']
 assert raw==frozen(src['originalRepositoryCommit'],ROOT/src['originalRepositoryPath'])
 assert subprocess.check_output(['git','hash-object','--stdin'],input=raw,cwd=ROOT).decode().strip()==src['originalGitBlob']
 raws[src['id']]=raw;register[src['id']]=src;sourceproof.append({'id':src['id'],'fullOriginalPath':str(p.relative_to(ROOT)),'rawSHA256':sha(raw),'originGitBlob':src['originalGitBlob'],'originCommit':src['originalRepositoryCommit'],'diskFreezeHEADExact':True})
ctx={};quotes=[]
for e in a['evidence']:
 sid=e['sourceId'];raw=raws[sid];src=register[sid];original=e['fullOriginal'];assert original['rawSHA256']==sha(raw) and original['rawBytes']==len(raw)
 loc=e['typedLocator'];kind=loc['type'];quote=e['exactSufficientQuote'];assert sha(quote.encode())==e['quoteSHA256']
 if kind=='visual-scan-page':
  p=F/loc['visualEvidencePath'];assert p.read_bytes()==frozen('c76bdab',p)==frozen('HEAD',p) and sha(p.read_bytes())==loc['visualEvidenceSHA256'];assert e['offset'] is None
  assert sha((F/e['normalizedContext']['path']).read_bytes())==e['normalizedContext']['sha256'];quotes.append({'id':e['id'],'sourceSHA256':sha(raw),'quoteSHA256':e['quoteSHA256'],'visualLocator':loc,'quality':'Native visual-source claim; independent actual pixels review still required'});continue
 context=e['normalizedContext'];key=(sid,context['path'])
 if key not in ctx:
  if kind=='html-section':
   text=visible(raw);start=text.index("1. Urban II's Speech at Clermont");end=text.index('2. The Capture of Jerusalem',start);text=text[start:end].strip()
  elif kind=='raw-json-field':text=json.loads(raw)['header']['description']
  else:
   pdf=PdfReader(F/src['containerPath'],strict=False);pages=[1,2] if kind=='pdf-cover' else [21,22,23] if sid=='glasgow' else [12];text=norm('\n\n'.join(pdf.pages[n-1].extract_text() for n in pages))
  if kind!='raw-json-field':
   p=F/context['path'];assert p.read_bytes()==text.encode()==frozen('c76bdab',p)==frozen('HEAD',p)
  assert sha(text.encode())==context['sha256'];ctx[key]=text
 text=ctx[key];off=e['offset'];assert text[off:off+len(quote)]==quote,(e['id'],off);quotes.append({'id':e['id'],'sourceSHA256':sha(raw),'quoteSHA256':e['quoteSHA256'],'contextSHA256':sha(text.encode()),'offset':off,'locator':loc})
eids={e['id'] for e in a['evidence']};bindings=[]
for ident in a['scopeIds']:
 q=qs[ident];expected={'prompt-answers-key':{'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'],**{'note'+str(i):v['note'] for i,v in enumerate(q['answers'])}}
 groups=[g for g in a['groups'] if g['cardId']==ident];assert [g['group'] for g in groups]==list(expected)
 for g in groups:
  assert g['literal']==expected[g['group']] and H(g['literal'])==g['canonicalSHA256'] and g['sourceVerdict'] and g['editorialVerdict']
  for c in g['constituents']:
   assert c['sourceVerdict'] and c['editorialVerdict'] and c['evidenceRefs'] and all(e in eids for e in c['evidenceRefs'])
  if g['group']=='prompt-answers-key':
   for i,v in enumerate(q['answers']):assert next(c for c in g['constituents'] if c['field']==f'answers[{i}]')['literal']==v['text']
  bindings.append({'id':ident,'group':g['group'],'literalSHA256':H(g['literal']),'wholeCardSHA256':H(q),'evidenceRefs':sorted({e for c in g['constituents'] for e in c['evidenceRefs']})})
assert len(bindings)==12 and len(sourceproof)==5
report={'purpose':'Exact native current source/literal integrity; independent quality NotRun','authorNativeId':a['authorNativeId'],'authorFreeze':'c76bdab','authorReceiptSHA256':sha(AP.read_bytes()),'runtimeFreeze':'e07f9d8','protected98':'exact','groups':12,'fullOriginals':sourceproof,'quotes':quotes,'bindings':bindings,'errors':0,'newCredit':0,'requiredIndependentReview':'All current12 groups,8options,8notes/class/dedup and actual source contexts; separate manual adjudication'}
(OUT/'middle2-v3-author-qualification-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'currentCards':2,'groups':12,'fullOriginals':5,'exactQuotes':len(quotes),'protected98':'exact','errors':0})
