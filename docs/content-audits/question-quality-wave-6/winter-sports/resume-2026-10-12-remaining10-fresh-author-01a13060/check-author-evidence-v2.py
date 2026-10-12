#!/usr/bin/env python3
"""Exact-scope WinterSports native-field/source-binding preservation check."""
import hashlib
import html
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd().resolve()==ROOT.resolve()
def git(*args): return subprocess.run(['git',*args],check=True,capture_output=True,text=True).stdout.strip()
assert Path(git('rev-parse','--show-toplevel')).resolve()==ROOT.resolve()
def load(path): return json.loads(Path(path).read_text())
def h(value): return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
scope=load('docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12fcd/winter-remaining10-fresh-author-01a13060-scope.json')
report=load('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/author-review-v2.json')
rt=load('src/content/topics/winter-sports.json'); baseline=json.loads(subprocess.run(['git','show','d4df6be:src/content/topics/winter-sports.json'],check=True,capture_output=True,text=True).stdout)
ids=scope['scopeIds']; assert ids==report['scopeIds'] and len(ids)==10
assert report['sixGroupDefinition']==['prompt','orderedAnswers','key','explanation','notes','difficulty']
assert rt['id']==baseline['id'] and rt['title']==baseline['title']
assert len(rt['questions'])==100 and [c['id'] for c in rt['questions']]==[c['id'] for c in baseline['questions']]
by={c['id']:c for c in rt['questions']}; base={c['id']:c for c in baseline['questions']}
assert len(scope['protected90'])==90
for qid,expected in scope['protected90'].items():
 assert qid not in ids and h(by[qid])==expected and h(base[qid])==expected, f'protected card changed: {qid}'
for qid,expected in scope['baselineCards'].items(): assert h(base[qid])==h(expected),f'scope baseline mismatch: {qid}'
for qid,slot in scope['preservedSlots'].items(): assert by[qid]['difficulty']==slot['difficulty'] and by[qid]['correctIndex']==slot['correctIndex'],qid
assert [c['difficulty'] for c in rt['questions']].count('easy')==40
assert [c['difficulty'] for c in rt['questions']].count('medium')==40
assert [c['difficulty'] for c in rt['questions']].count('hard')==20
assert {i:sum(c['correctIndex']==i for c in rt['questions']) for i in range(4)}=={0:25,1:25,2:25,3:25}
assert len(report['cards'])==10 and [c['id'] for c in report['cards']]==ids
quote_by={q['id']:q for q in report['quoteRegistry']}; sources={s['id']:s for s in report['sourceFiles']}
assert len(quote_by)==len(report['quoteRegistry'])
for sid,s in sources.items():
 data=Path(s['capturePath']).read_bytes()
 assert len(data)==s['rawByteLength'] and hashlib.sha256(data).hexdigest()==s['rawSha256']
 assert git('hash-object',s['capturePath'])==s['gitBlobSha1']
 assert s['registerCrosscheck']['allMatch'] is True
 git('ls-files','--error-unmatch',s['capturePath'])
# Exact source quote existence plus quote/raw identities and per-source quote limits.
word_counts={sid:0 for sid in sources}
for qid,q in quote_by.items():
 s=sources[q['sourceId']]; raw=Path(s['capturePath']).read_bytes()
 assert q['sourceUrl']==s['url'] and q['capturePath']==s['capturePath']
 assert q['rawSha256']==s['rawSha256'] and q['gitBlobSha1']==s['gitBlobSha1'] and q['rawByteLength']==s['rawByteLength']
 assert hashlib.sha256(q['quote'].encode()).hexdigest()==q['derivation']['quoteSha256']
 word_counts[q['sourceId']]+=len(q['quote'].split())
 if q['derivation']['kind']=='normalized PDF page text':
  text=' '.join((PdfReader(s['capturePath'],strict=False).pages[q['derivation']['physicalPageOneBased']-1].extract_text() or '').split())
  assert q['quote'] in text and hashlib.sha256(text.encode()).hexdigest()==q['derivation']['normalizedPageSha256']
 else: assert q['quote'] in html.unescape(raw.decode('utf-8',errors='replace'))
assert word_counts==report['quoteWordCountsBySource'] and all(n<=25 for n in word_counts.values())
for context in report['pdfPageContexts']:
 s=sources[context['sourceId']]
 assert context['rawCaptureSha256']==s['rawSha256'] and context['gitBlobSha1']==s['gitBlobSha1']
 text=' '.join((PdfReader(s['capturePath'],strict=False).pages[context['physicalPageOneBased']-1].extract_text() or '').split())
 assert len(text)==context['normalizedTextLengthCodePoints']
 assert hashlib.sha256(text.encode()).hexdigest()==context['normalizedTextSha256']
for cardproof in report['cards']:
 c=by[cardproof['id']]; groups=cardproof['groups']; assert len(groups)==6
 assert [g['group'] for g in groups]==report['sixGroupDefinition']
 assert cardproof['wholeCardCanonicalSha256']==h(c)
 for g in groups:
  assert g['nativeFieldLiteralSha256']==h(g['nativeFieldLiteral'])
  assert g['sourceAnalysis'] and g['sourceBindings']
  for b in g['sourceBindings']:
   q=quote_by[b['quoteId']]; s=sources[b['sourceId']]
   assert b['sourceId']==q['sourceId'] and b['sourceUrl']==s['url'] and b['capturePath']==s['capturePath']
   assert b['rawSha256']==s['rawSha256'] and b['gitBlobSha1']==s['gitBlobSha1'] and b['locator']==q['locator']
  for item_key,literal_key,analysis_key in [('individualAnswerBindings','nativeAnswerLiteral','editorialAnalysis'),('individualNoteBindings','nativeNoteLiteral','editorialAnalysis')]:
   for item in g.get(item_key,[]):
    assert item[literal_key] and item[analysis_key] and item['sourceBindings']
    hash_key='nativeAnswerLiteralSha256' if item_key=='individualAnswerBindings' else 'nativeNoteLiteralSha256'
    assert item[hash_key]==h(item[literal_key])
    for b in item['sourceBindings']: assert b['quoteId'] in quote_by and b['sourceUrl']==sources[b['sourceId']]['url']
 assert groups[0]['nativeFieldLiteral']==c['prompt']
 assert groups[1]['nativeFieldLiteral']==[a['text'] for a in c['answers']]
 assert groups[2]['nativeFieldLiteral']=={'correctIndex':c['correctIndex'],'correctAnswerText':c['answers'][c['correctIndex']]['text']}
 assert groups[3]['nativeFieldLiteral']==c['explanation']
 assert groups[4]['nativeFieldLiteral']==[{'noteIndex':i,'text':a['note']} for i,a in enumerate(c['answers'])]
 assert groups[5]['nativeFieldLiteral']==c['difficulty']
 assert len(groups[1]['individualAnswerBindings'])==4 and len(groups[4]['individualNoteBindings'])==4
# Focused authored repair: all alternatives are ski-mounted neighbors, with stable Hard/key slot.
c=by['winter-sports-076']; assert c['difficulty']=='hard' and c['correctIndex']==3
assert all('лыж' in a['text'].lower() or i==2 for i,a in enumerate(c['answers']))
assert all('ботинок' not in a['text'].lower() and 'палк' not in a['text'].lower() for a in c['answers'])
assert c['answers'][3]['text']=='Лыжу, интерфейс и крепление'
assert sum(len(c['groups']) for c in report['cards'])==60
result={'result':'PASS','baselineRuntime':'d4df6be','scopedCards':10,'nativeGroups':60,'individualAnswerBindings':40,'individualNoteBindings':40,'protected90':'exact','sourceOriginals':len(sources),'quoteWordsBySource':word_counts,'pdfContexts':len(report['pdfPageContexts']),'difficultyQuota':'40/40/20','keyIndexQuota':'25 each','checkedBy':'check-author-evidence-v2.py'}
(ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/verification-result-v2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
