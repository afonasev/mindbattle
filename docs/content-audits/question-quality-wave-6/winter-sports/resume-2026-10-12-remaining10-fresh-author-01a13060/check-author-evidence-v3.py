#!/usr/bin/env python3
"""Validate the six-group WinterSports fresh-author evidence packet."""
import hashlib, html, json, subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd().resolve()==ROOT.resolve()
def git(*args): return subprocess.run(['git',*args],check=True,capture_output=True,text=True).stdout.strip()
def load(p): return json.loads(Path(p).read_text())
def h(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
scope=load('docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12fcd/winter-remaining10-fresh-author-01a13060-scope.json')
report=load('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/author-review-v3.json')
rt=load('src/content/topics/winter-sports.json'); base=json.loads(subprocess.run(['git','show','d4df6be:src/content/topics/winter-sports.json'],check=True,capture_output=True,text=True).stdout)
ids=scope['scopeIds']; assert report['scopeIds']==ids and len(ids)==10
assert report['sixGroupDefinition']==['prompt-answers-key','explanation','note0','note1','note2','note3']
assert rt['id']==base['id'] and rt['title']==base['title'] and len(rt['questions'])==100
by={c['id']:c for c in rt['questions']}; bb={c['id']:c for c in base['questions']}
assert len(scope['protected90'])==90
for qid,digest in scope['protected90'].items(): assert qid not in ids and h(by[qid])==digest and h(bb[qid])==digest,qid
for qid,expected in scope['baselineCards'].items(): assert h(bb[qid])==h(expected),qid
for qid,s in scope['preservedSlots'].items(): assert by[qid]['difficulty']==s['difficulty'] and by[qid]['correctIndex']==s['correctIndex'],qid
assert [c['difficulty'] for c in rt['questions']].count('easy')==40 and [c['difficulty'] for c in rt['questions']].count('medium')==40 and [c['difficulty'] for c in rt['questions']].count('hard')==20
assert {i:sum(c['correctIndex']==i for c in rt['questions']) for i in range(4)}=={0:25,1:25,2:25,3:25}
sources={s['id']:s for s in report['sourceFiles']}; quotes={q['id']:q for q in report['quoteRegistry']}; assert len(quotes)==len(report['quoteRegistry'])
words={sid:0 for sid in sources}
for sid,s in sources.items():
 data=Path(s['capturePath']).read_bytes(); assert len(data)==s['rawByteLength'] and hashlib.sha256(data).hexdigest()==s['rawSha256'] and git('hash-object',s['capturePath'])==s['gitBlobSha1'] and s['registerCrosscheck']['allMatch'] is True; git('ls-files','--error-unmatch',s['capturePath'])
for qid,q in quotes.items():
 s=sources[q['sourceId']]; assert q['sourceUrl']==s['url'] and q['capturePath']==s['capturePath'] and q['rawSha256']==s['rawSha256'] and q['gitBlobSha1']==s['gitBlobSha1'] and q['rawByteLength']==s['rawByteLength'] and hashlib.sha256(q['quote'].encode()).hexdigest()==q['derivation']['quoteSha256']; words[q['sourceId']]+=len(q['quote'].split())
 if q['derivation']['kind']=='normalized PDF page text':
  txt=' '.join((PdfReader(s['capturePath'],strict=False).pages[q['derivation']['physicalPageOneBased']-1].extract_text() or '').split()); assert q['quote'] in txt and hashlib.sha256(txt.encode()).hexdigest()==q['derivation']['normalizedPageSha256']
 else: assert q['quote'] in html.unescape(Path(s['capturePath']).read_text(errors='replace'))
assert words==report['quoteWordCountsBySource'] and all(n<=25 for n in words.values())
for ctx in report['pdfPageContexts']:
 s=sources[ctx['sourceId']]; txt=' '.join((PdfReader(s['capturePath'],strict=False).pages[ctx['physicalPageOneBased']-1].extract_text() or '').split()); assert ctx['rawCaptureSha256']==s['rawSha256'] and ctx['gitBlobSha1']==s['gitBlobSha1'] and ctx['normalizedTextLengthCodePoints']==len(txt) and ctx['normalizedTextSha256']==hashlib.sha256(txt.encode()).hexdigest()
assert len(report['cards'])==10 and [c['id'] for c in report['cards']]==ids
def check_bindings(bindings):
 assert bindings
 for b in bindings:
  q=quotes[b['quoteId']]; src=sources[b['sourceId']]
  assert b['sourceId']==q['sourceId'] and b['sourceUrl']==src['url'] and b['capturePath']==src['capturePath']
  assert b['rawByteLength']==src['rawByteLength'] and b['rawSha256']==src['rawSha256'] and b['gitBlobSha1']==src['gitBlobSha1']
  assert b['locator']==q['locator'] and b['quoteSha256']==q['derivation']['quoteSha256']
for proof in report['cards']:
 c=by[proof['id']]; groups=proof['groups']; assert [g['group'] for g in groups]==report['sixGroupDefinition'] and proof['wholeCardCanonicalSha256']==h(c)
 g=groups[0]; check_bindings(g['sourceBindings']); assert g['nativeLiteral']=={'prompt':c['prompt'],'orderedAnswerTexts':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'correctAnswerText':c['answers'][c['correctIndex']]['text']} and g['literalSha256']==h(g['nativeLiteral'])
 assert [x['field'] for x in g['fieldReviews'][-2:]]==['correctIndex','correctAnswerText']
 p,a,k=g['fieldReviews'][0],g['fieldReviews'][1],g['fieldReviews'][2:]
 check_bindings(p['sourceBindings']); assert p['nativeLiteral']==c['prompt'] and p['literalSha256']==h(c['prompt']) and p['sourceEditorialAnalysis'] and p['sourceBindings']
 assert a['nativeLiteral']==[x['text'] for x in c['answers']] and a['literalSha256']==h(a['nativeLiteral']) and len(a['answerReviews'])==4
 for i,x in enumerate(a['answerReviews']): check_bindings(x['sourceBindings']); assert x['index']==i and x['nativeLiteral']==c['answers'][i]['text'] and x['literalSha256']==h(x['nativeLiteral']) and x['isKey']==(i==c['correctIndex']) and x['sourceBindings'] and x['sourceEditorialAnalysis']
 assert k[0]['nativeLiteral']==c['correctIndex'] and k[1]['nativeLiteral']==c['answers'][c['correctIndex']]['text']
 for x in k: check_bindings(x['sourceBindings']); assert x['literalSha256']==h(x['nativeLiteral']) and x['sourceBindings'] and x['sourceEditorialAnalysis']
 for group,expect in zip(groups[1:], [c['explanation'],*[a['note'] for a in c['answers']]]):
  check_bindings(group['sourceBindings'])
  literal=group['nativeLiteral'] if 'nativeLiteral' in group else None
  if 'noteIndex' in group: literal=group['nativeLiteral']
  assert literal==expect and group['literalSha256']==h(literal) and group['sourceBindings'] and group['sourceEditorialAnalysis']
  for b in group['sourceBindings']:
   q=quotes[b['quoteId']]; s=sources[b['sourceId']]; assert b['sourceUrl']==s['url'] and b['capturePath']==s['capturePath'] and b['rawByteLength']==s['rawByteLength'] and b['rawSha256']==s['rawSha256'] and b['gitBlobSha1']==s['gitBlobSha1'] and b['locator']==q['locator'] and b['quoteSha256']==q['derivation']['quoteSha256'] and b['quoteId']==q['id']
 d=proof['difficultyEditorialAssessment']; check_bindings(d['sourceBindings']); assert d['difficulty']==c['difficulty'] and d['literalSha256']==h(c['difficulty']) and d['assessment'] and d['sourceBindings']
# Focused authored repair remains intact.
c=by['winter-sports-076']; assert c['difficulty']=='hard' and c['correctIndex']==3 and c['answers'][3]['text']=='Лыжу, интерфейс и крепление'; assert all('ботинок' not in a['text'].lower() and 'палк' not in a['text'].lower() for a in c['answers'])
assert sum(len(c['groups']) for c in report['cards'])==60
result={'result':'PASS','baselineRuntime':'d4df6be','scopedCards':10,'nativeGroups':60,'groupDefinition':report['sixGroupDefinition'],'individualAnswerReviews':40,'individualNoteGroups':40,'protected90':'exact','sourceOriginals':len(sources),'quoteWordsBySource':words,'pdfContexts':len(report['pdfPageContexts']),'difficultyQuota':'40/40/20','keyIndexQuota':'25 each','checker':'check-author-evidence-v3.py'}
Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/verification-result-v3.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
