"""Declared literal/hash/source preservation only; never grades quality."""
import json,hashlib,gzip,subprocess,re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');BASE=ROOT/'docs/content-audits/question-quality-wave-6';OUT=BASE/'coordinator-continuation-01a13100'
AP=BASE/'middle-ages/repair6-2026-10-12-fresh-writable-author-01a13116/author-review-v3.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
H=lambda v:sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def frozen(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
a=json.loads(AP.read_text());assert AP.read_bytes()==frozen('f547afe',AP)==frozen('HEAD',AP)
assert a['authorNativeId']=='01a13116-9ab1-7062-9219-08765b2ab65e'
rt=ROOT/a['runtimePath'];assert rt.read_bytes()==frozen('f547afe',rt)==frozen('HEAD',rt)
qs={q['id']:q for q in json.loads(rt.read_text())['questions']};before={q['id']:q for q in json.loads(frozen('c506101',rt))['questions']}
ids=a['scopeIds'];assert len(ids)==6 and all(qs[i]==q for i,q in before.items() if i not in ids)
for ident in ids:assert qs[ident]['difficulty']==before[ident]['difficulty'] and qs[ident]['correctIndex']==before[ident]['correctIndex']
for c in a['cards']:
 q=qs[c['id']];assert q==c['wholeCard'] and H(q)==c['wholeCardCanonicalSha256'];assert c['difficultyReason']
 expected={'prompt-answers-key':{'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'],**{'note'+str(i):x['note'] for i,x in enumerate(q['answers'])}}
 groups=[g for g in a['groups'] if g['id']==c['id']];assert [g['group'] for g in groups]==list(expected)
 for g in groups:assert g['literal']==expected[g['group']] and H(g['literal'])==g['canonicalSha256']==c['groupSha256'][g['group']] and g['sourceReason'] and g['editorialReason']
class Visible(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.skip=[];self.parts=[]
 def handle_starttag(self,t,attrs):
  if t in ('script','style'):self.skip.append(t)
 def handle_endtag(self,t):
  if t in self.skip:self.skip.pop()
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def visible(t):
 p=Visible();p.feed(t);return re.sub(r'\s+',' ',' '.join(p.parts)).strip()
def strings(v):
 if isinstance(v,str):yield visible(v)
 elif isinstance(v,dict):
  for x in v.values():yield from strings(x)
 elif isinstance(v,list):
  for x in v:yield from strings(x)
contexts={};sourceproof={};bindings=[];errors=[]
for g in a['groups']:
 entries=list(g['sourceBindings'])+[b for c in g['constituents'] for b in c['sourceBindings']]
 for b in entries:
  original=b['completeOriginal'];p=ROOT/original['path'];container=p.read_bytes();raw=gzip.decompress(container) if p.suffix=='.gz' else container
  assert container==frozen('f547afe',p)==frozen('HEAD',p)
  assert len(raw)==original['rawBytes'] and sha(raw)==original['rawSHA256']
  if original.get('containerSHA256'):assert sha(container)==original['containerSHA256'] and len(container)==original['containerBytes']
  if original.get('gitBlob'):assert subprocess.check_output(['git','hash-object',str(p)],cwd=ROOT,text=True).strip()==original['gitBlob']
  sourceproof[str(p.relative_to(ROOT))]={'rawSHA256':sha(raw),'containerSHA256':sha(container),'bytes':len(raw),'diskFreezeHEADExact':True}
  quote=b['quote'];assert sha(quote.encode())==b['quoteSha256']
  key=(str(p),b['offsetBasis'])
  if 'Visual page locator' in b['offsetBasis']:
   bindings.append({'id':g['id'],'group':g['group'],'quoteSHA256':b['quoteSha256'],'sourceSHA256':sha(raw),'locator':b['locator'],'status':'Native author visual claim; different reader visual inspection still required'});continue
  if key not in contexts:
   if b['source']=='pilgrimage':
    derived=AP.parent/'glasgow-pages21-23-pypdf-derived.txt';assert derived.read_bytes()==frozen('f547afe',derived)==frozen('HEAD',derived);text=derived.read_text();pdf=PdfReader(p,strict=False)
    assert all(pdf.pages[n-1].extract_text() in text for n in [21,22,23])
   elif b['source']=='Syed jihad chapter':text=PdfReader(p,strict=False).pages[11].extract_text()
   elif 'header.description' in b['offsetBasis']:text=json.loads(raw)['header']['description']
   elif b['source']=='toll':
    d=json.loads(raw);text=re.sub(r'\s+',' ',' '.join([visible(d['header']['description']),*strings(d['content'])])).strip()
   else:text=visible(raw.decode('utf-8',errors='replace'))
   contexts[key]=text
  text=contexts[key];offset=b['offset'];observed=text[offset:offset+len(quote)]
  if observed!=quote:errors.append({'id':g['id'],'group':g['group'],'source':b['source'],'offset':offset,'expectedQuoteSHA256':b['quoteSha256'],'expected':quote,'observed':observed})
  bindings.append({'id':g['id'],'group':g['group'],'sourceSHA256':sha(raw),'contextSHA256':sha(text.encode()),'offset':offset,'quoteSHA256':b['quoteSha256'],'exact':observed==quote})
report={'authorNativeId':a['authorNativeId'],'authorFreeze':'f547afe','authorReceiptSHA256':sha(AP.read_bytes()),'groups':36,'wholecards':6,'protected94':'exact','recipe':a['canonicalHashRecipe'],'completeOriginals':sourceproof,'bindingRecords':bindings,'errors':errors,'quality':'NOTRUN independent review and manual adjudication separate','newCredit':0}
(OUT/'middle6-v3-author-qualification-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'groups':36,'bindings':len(bindings),'completeOriginals':len(sourceproof),'errors':errors[:3],'errorCount':len(errors)})
