"""Focused binding/invariant QA only; never determines manual source/editorial verdicts."""
import json,hashlib,subprocess,collections
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle23-current'
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
r=json.loads((OUT/'reader-receipt.json').read_text());frozen=r['frozenReviewCommit']
def blob(p):return subprocess.check_output(['git','show',frozen+':'+p],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()
topic=json.loads(blob('src/content/topics/middle-ages.json'));current=json.loads((ROOT/'src/content/topics/middle-ages.json').read_bytes());assert current==topic
scope=json.loads(blob(r['scopePath']));assert r['exactIdsInScopeOrder']==scope['exactIds']
assert len(r['cards'])==23 and len({x['questionId'] for x in r['cards']})==23
assert r['actualNativeAgentIdentity']['distinctFromAuthor']
author=json.loads(blob(r['authorReceiptPath']))
fields=['prompt-key','note0','note1','note2','note3','explanation'];quoted=0
for card in r['cards']:
 q=next(q for q in topic['questions'] if q['id']==card['questionId']);assert card['cardLiteral']==q
 assert card['cardCanonicalSha256']==sha(canon(q))
 assert [f['field'] for f in card['fields']]==fields
 ac=next(c for c in author['cards'] if c['questionId']==card['questionId'])
 for f in card['fields']:
  assert f['sourceAnalysis'] and f['editorialAnalysis'] and f['manualIndividualAnalysis']
  af=next(af for af in ac['fields'] if af['field']==f['field']);assert f['literal']==af['literal'] and f['literalSha256']==af['literalSha256']==sha(canon(f['literal']))
  assert f['verdict']==('PASS' if f['sourceVerdict']==f['editorialVerdict']=='PASS' else 'FIX')
  assert f['proofs']
  for p in f['proofs']:
   assert p['sourceURL'] and p['actualCaptureURL'] and p['captureFormat'] and p['sourceClass']
   for pp in p['quotedPassages']:assert sha(pp['passage'].encode())==pp['passageSha256'];quoted+=1
 assert card['verdict']==('PASS' if all(f['verdict']=='PASS' for f in card['fields']) else 'FIX')
assert sum(len(c['fields']) for c in r['cards'])==138
stats={'cards':dict(collections.Counter(c['verdict'] for c in r['cards'])),'fields':dict(collections.Counter(f['verdict'] for c in r['cards'] for f in c['fields'])),'sourceFields':dict(collections.Counter(f['sourceVerdict'] for c in r['cards'] for f in c['fields'])),'editorialFields':dict(collections.Counter(f['editorialVerdict'] for c in r['cards'] for f in c['fields']))};assert stats==r['counts']
inv=json.loads((OUT/'source-inventory.json').read_text());assert len(inv['sources'])==40
roundtrip=[]
for s in inv['sources']:
 b=blob(s['rawCapture']);assert b==(ROOT/s['rawCapture']).read_bytes();assert sha(b)==s['rawCaptureSha256']
 assert subprocess.check_output(['git','rev-parse',frozen+':'+s['rawCapture']],cwd=ROOT).decode().strip()==s['frozenGitBlob']
 assert subprocess.check_output(['git','check-attr','text','--',s['rawCapture']],cwd=ROOT).decode().strip().endswith(': unset'),s['rawCapture']
 roundtrip.append({'path':s['rawCapture'],'bytes':len(b),'sha256':sha(b),'gitBlob':s['frozenGitBlob'],'textAttribute':'unset','localEqualsFrozenGitBlobBytes':True})
for x in inv['excludedCaptures']:assert sha(blob(x['path']))==x['actualRawSha256']
expected={p['questionId']:p['cardCanonicalSha256'] for p in scope['protected77']}
for q in topic['questions']:
 if q['id'] in expected:assert sha(json.dumps(q,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode())==expected[q['id']]
assert len(expected)==77
parent=json.loads(subprocess.check_output(['git','show','c20daf0^:src/content/topics/middle-ages.json'],cwd=ROOT));ids=set(scope['exactIds'])
assert [q['id'] for q in parent['questions']]==[q['id'] for q in topic['questions']]
assert {q['id'] for q,old in zip(topic['questions'],parent['questions']) if q!=old}==ids
assert all((q['id'],q['difficulty'],q['correctIndex'])==(old['id'],old['difficulty'],old['correctIndex']) for q,old in zip(topic['questions'],parent['questions']))
levels=collections.Counter(q['difficulty'] for q in topic['questions']);assert dict(levels)=={'easy':40,'medium':40,'hard':20}
slots={level:[sum(q['difficulty']==level and q['correctIndex']==i for q in topic['questions']) for i in range(4)] for level in ['easy','medium','hard']};assert slots=={'easy':[10]*4,'medium':[10]*4,'hard':[5]*4}
partner=r['duplicateFinding'];pq=next(q for q in json.loads(blob(partner['partnerPath']))['questions'] if q['id']=='history-spain-easy-01-04');assert pq==partner['partnerLiteral'] and sha(canon(pq))==partner['partnerCanonicalSha256']
report={'role':'focused independent receipt binding and invariant verification','frozenGitCommit':frozen,'exactCards':23,'exactPairedFields':138,'counts':stats,'manualDecisionsNotComputedByQA':True,'rawOriginalsVerified':40,'protected77MatchScopeHashes':True,'authorContentChangedExactly23VsParent':True,'topicIdOrderDifficultyKeySlotsPreserved':True,'levelCounts':dict(levels),'keySlotCounts':slots,'literalHashesMatchAuthorAndFrozenCurrent':True,'quotedPassageHashBindingsChecked':quoted,'sourceGitRoundtrip':roundtrip,'fullSuiteBuildDeploy':'NotRun; evidence-only scope','command':'python3 '+str(OUT/'verify_receipt.py'),'scopeReason':'Only reader evidence is changed; verify138 literal/source bindings, exact23 order and protected77/slot invariants. No runtime changed, no tests relevant beyond these checks.'}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'PASS':True,'cards':23,'fields':138,'counts':stats,'sources':40,'protected':77,'slots':slots}))
