#!/usr/bin/env python3
"""Exact-scope content freeze, source identity, and 48-group author evidence check."""
import hashlib, html.parser, json, subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd().resolve()==ROOT.resolve()
def git(*args): return subprocess.run(['git',*args],check=True,capture_output=True,text=True).stdout.strip()
def read(path): return json.loads(Path(path).read_text())
def sha(data): return hashlib.sha256(data).hexdigest()
def H(value): return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
scopePath='docs/content-audits/question-quality-wave-6/coordinator-continuation-01a13100/winter8-exact-repair-scope.json'
reportPath='docs/content-audits/question-quality-wave-6/winter-sports/repair8-2026-10-12-author-01a13060/author-review-v1.json'
scope=read(scopePath); report=read(reportPath); runtimePath=report['runtimePath']; runtimeBytes=Path(runtimePath).read_bytes(); runtime=read(runtimePath)
assert sha(Path(scopePath).read_bytes())==report['scopeFileSha256']
assert sha(runtimeBytes)==report['postRepairRuntimeRawSha256'] and H(runtime)==report['postRepairRuntimeCanonicalSha256']
assert sha(Path(report['readerReceipt']).read_bytes())==report['readerReceiptSha256']==report['readerReceiptDeclaredSha256']
assert report['baselineCommit']==scope['baseline'] and git('rev-parse',scope['baseline']+':'+runtimePath)
base=json.loads(subprocess.run(['git','show',scope['baseline']+':'+runtimePath],check=True,capture_output=True).stdout)
assert H(base)==report['baselineRuntimeCanonicalSha256']==report['preRepairRuntimeCanonicalSha256']
assert sha(subprocess.run(['git','show',scope['baseline']+':'+runtimePath],check=True,capture_output=True).stdout)==report['preRepairRuntimeRawSha256']
assert runtime['id']==base['id'] and runtime['title']==base['title']
assert [q['id'] for q in runtime['questions']]==scope['order']==report['cardOrder']
assert len(runtime['questions'])==100 and len(scope['protected92'])==92
by={q['id']:q for q in runtime['questions']}; old={q['id']:q for q in base['questions']}; ids=scope['ids']
assert ids==report['scopeIds'] and ids==[c['id'] for c in report['cards']] and len(ids)==8
expected={x['id']:x for x in scope['scopedBefore']}; assert set(expected)==set(ids)
for qid,proof in expected.items():
 assert H(old[qid])==proof['sha256'] and old[qid]['difficulty']==proof['difficulty'] and old[qid]['correctIndex']==proof['correctIndex']
 c=by[qid]; b=old[qid]
 assert c['difficulty']==b['difficulty']==proof['difficulty'] and c['correctIndex']==b['correctIndex']==proof['correctIndex']
 assert c['source']==b['source'] and set(c)==set(b) and len(c['answers'])==4
 for key in set(c)-{'prompt','answers','explanation'}: assert c[key]==b[key],(qid,key)
 assert all(set(c['answers'][i])==set(b['answers'][i]) for i in range(4))
for item in scope['protected92']:
 qid=item['id']; assert qid not in ids and H(by[qid])==item['sha256']==H(old[qid]),qid
assert [q['difficulty'] for q in runtime['questions']].count('easy')==40
assert [q['difficulty'] for q in runtime['questions']].count('medium')==40
assert [q['difficulty'] for q in runtime['questions']].count('hard')==20
assert {i:sum(q['correctIndex']==i for q in runtime['questions']) for i in range(4)}=={0:25,1:25,2:25,3:25}
# Every source original and independent context is byte-identical to tracked Git content.
sources={s['id']:s for s in report['sourceFiles']}; assert len(sources)==5
for s in sources.values():
 raw=Path(s['capturePath']).read_bytes(); assert len(raw)==s['rawByteLength'] and sha(raw)==s['rawSha256']
 assert git('hash-object',s['capturePath'])==s['gitBlobSha1'] and s['registerCrosscheck']['allMatch'] is True
 git('ls-files','--error-unmatch',s['capturePath'])
quoteBy={q['id']:q for q in report['quoteRegistry']}; assert len(quoteBy)==len(report['quoteRegistry'])
wordCounts={sid:0 for sid in sources}
for q in quoteBy.values():
 s=sources[q['sourceId']]; assert sha(q['exactQuote'].encode())==q['exactQuoteSha256'] and q['wordCount']==len(q['exactQuote'].split())
 assert s['rawSha256'] and Path(s['capturePath']).exists()
 if q['contextPath'].startswith('PDF physical page '):
  page=int(q['contextPath'].split()[3].rstrip(';')); r=PdfReader(s['capturePath'],strict=False); text=' '.join((r.pages[page-1].extract_text() or '').split()); contextSha=sha(text.encode())
 else:
  contextPath=q['contextPath']; saved=Path(contextPath); git('ls-files','--error-unmatch',contextPath); contextData=read(contextPath); entry=next(x for x in contextData if x['sourceId']==q['sourceId']); nodes=[]
  class Visible(html.parser.HTMLParser):
   def __init__(self): super().__init__(convert_charrefs=True); self.skip=[]; self.nodes=[]
   def handle_starttag(self,t,a):
    if t.lower() in ('script','style'): self.skip.append(t.lower())
   def handle_endtag(self,t):
    if t.lower() in self.skip: self.skip.pop()
   def handle_data(self,d):
    if not self.skip:
     v=' '.join(d.split())
     if v:self.nodes.append(v)
  parser=Visible(); parser.feed(Path(s['capturePath']).read_text(encoding='utf8',errors='replace')); visible=' '.join(parser.nodes); contextSha=sha(visible.encode())
  assert len(entry['nodes'])==next(x for x in report['htmlContexts'] if x['sourceId']==q['sourceId'])['savedNodeCount']
  assert sha(saved.read_bytes())==next(x for x in report['htmlContexts'] if x['sourceId']==q['sourceId'])['savedIndependentContextSha256']
 assert contextSha==q['contextSha256']
 # Re-read exact codepoint span within the source's normalized context.
 if q['contextPath'].startswith('PDF physical page '):
  phrase=text[q['contextCodePointOffset0']:q['contextCodePointOffset0']+q['contextCodePointLength']]
 else: phrase=visible[q['contextCodePointOffset0']:q['contextCodePointOffset0']+q['contextCodePointLength']]
 assert phrase==q['exactQuote']
 wordCounts[q['sourceId']]+=q['wordCount']
assert wordCounts==report['quoteWordCountsBySource'] and all(n<=25 for n in wordCounts.values())
for ctx in report['pdfPageContexts']:
 s=sources[ctx['sourceId']]; r=PdfReader(s['capturePath'],strict=False); rawtext=r.pages[ctx['physicalPageOneBased']-1].extract_text() or ''; text=' '.join(rawtext.split())
 assert sha(rawtext.encode())==ctx['rawExtractedTextSha256'] and sha(text.encode())==ctx['normalizedTextSha256'] and len(text)==ctx['normalizedTextLengthCodePoints']
# Six exact native groups/card; every field carries individual exact hash and source/editorial analysis.
for proof in report['cards']:
 c=by[proof['id']]; assert proof['cardSnapshot']==c and H(c)==proof['wholeCardCanonicalSha256']
 groups=proof['groups']; assert [g['group'] for g in groups]==report['groupDefinition'] and len(groups)==6
 combined={'prompt':c['prompt'],'orderedAnswerTexts':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'correctAnswerText':c['answers'][c['correctIndex']]['text']}
 g=groups[0]; assert g['nativeLiteral']==combined and g['literalSha256']==H(combined) and g['sourceReason'] and g['editorialReason']
 expectedFields=['prompt',*[f'answerText[{i}]' for i in range(4)],'correctIndex','correctAnswerText']; assert [x['field'] for x in g['fieldReviews']]==expectedFields
 for x in g['fieldReviews']:
  name=x['field']; val=x['nativeLiteral']
  expectedVal={'prompt':c['prompt'],'correctIndex':c['correctIndex'],'correctAnswerText':c['answers'][c['correctIndex']]['text']}.get(name)
  if name.startswith('answerText['): expectedVal=c['answers'][int(name[11:-1])]['text']
  assert val==expectedVal and x['literalSha256']==H(val) and x['sourceReason'] and x['editorialReason'] and x['sourceBindings']
  if name.startswith('answerText['): assert x['isCorrect']==(int(name[11:-1])==c['correctIndex'])
 for i,g in enumerate(groups[1:]):
  if i==0: expectedVal=c['explanation']
  else: expectedVal=c['answers'][i-1]['note']
  assert g['nativeLiteral']==expectedVal and g['literalSha256']==H(expectedVal) and g['sourceReason'] and g['editorialReason']
  assert (g.get('addsBeyondPromptAndKey') is True)==(i>0 and i-1==c['correctIndex'])
  assert (g.get('usefulToOwnOption') is True)==(i>0 and i-1!=c['correctIndex'])
 diff=proof['difficultyEditorialAssessment']; assert diff['difficulty']==c['difficulty'] and diff['literalSha256']==H(c['difficulty']) and diff['editorialReason']
 for group in groups:
  bindingsToCheck=list(group['sourceBindings'])
  for fld in group.get('fieldReviews',[]): bindingsToCheck.extend(fld['sourceBindings'])
  for b in bindingsToCheck:
   q=quoteBy[b['quoteId']]; s=sources[b['sourceId']]
   assert b['sourceId']==q['sourceId'] and b['originalURL']==s['originalURL'] and b['capturePath']==s['capturePath']
   assert b['rawByteLength']==s['rawByteLength'] and b['rawSha256']==s['rawSha256'] and b['gitBlobSha1']==s['gitBlobSha1']
   assert b['locator']==q['locator'] and b['exactQuote']==q['exactQuote'] and b['quoteSha256']==q['exactQuoteSha256'] and b['contextSha256']==q['contextSha256']
assert sum(len(c['groups']) for c in report['cards'])==48
assert report['catalogueDedupAudit']['result'].startswith('No same-concept')
# Preserve the source-reader's supporting artifacts in Git; no substitutes or untracked copies.
for p in [scopePath,report['readerReceipt'],str(Path(RECEIPT:=report['readerReceipt']).parent/'html-independent-context.json'),str(Path(report['readerReceipt']).parent/'pdf-independent-extractions.json'),str(Path(report['readerReceipt']).parent/'independent-quote-proofs.json')]:
 git('ls-files','--error-unmatch',p)
result={'result':'PASS','baseline':report['baselineCommit'],'scopeIds':len(ids),'sixPartGroups':48,'individualSubfieldReviews':sum(len(c['groups'][0]['fieldReviews']) for c in report['cards']),'sourceOriginals':len(sources),'quoteWordsBySource':wordCounts,'pdfPageContexts':len(report['pdfPageContexts']),'htmlContexts':len(report['htmlContexts']),'protected92':'exact','cardOrder':'exact','difficultyQuota':'40/40/20','correctIndexQuota':'25 each','pairedCardsUnchanged':'092,098','tests':'not run by scope','buildDeploy':'not run by scope','checker':'check-author-repair-v1.py'}
Path('docs/content-audits/question-quality-wave-6/winter-sports/repair8-2026-10-12-author-01a13060/verification-result-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
