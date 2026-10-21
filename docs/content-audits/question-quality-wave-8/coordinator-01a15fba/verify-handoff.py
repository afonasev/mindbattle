"""Read-only exact CURRENT956 snapshot; no source review or QA replay."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=x['CURRENT']
assert n==956 and x['remaining']==1044 and x['fullGoal']==2000 and x['ownIntakeCURRENT']==952
assert x['ownProgress']['newlyCertified']==x['newlyCertified']==4 and len(x['ownProgress']['accepted'])==4
cat={};orders={}
for p in sorted((m.C/'src/content/topics').glob('*.json')):
 for i,q in enumerate(m.read(p)['questions'],1):cat[q['id']]=q;orders[q['id']]=i
a,b=cp['currentEligibleCompletedIds'],cp['currentRemainingIds'];sel=cp['selectedCards'];ids=[e['questionId'] for e in sel]
assert len(cat)==11000 and len(a)==len(set(a))==len(cp['completedCardHashes'])==n and len(b)==len(set(b))==2000-n
assert len(ids)==len(set(ids))==2000 and set(a).isdisjoint(b) and set(a)|set(b)==set(ids)
assert {e['questionId'] for e in cp['completedCardHashes']}==set(a)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {e['topicId'] for e in sel}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'))
 frozen={q['id']:(i,q['difficulty'],q['correctIndex']) for i,q in enumerate(old['questions'],1)}
 for e in (z for z in sel if z['topicId']==topic):
  q=cat[e['questionId']];assert frozen[q['id']]==(orders[q['id']],q['difficulty'],q['correctIndex'])
  assert (q['difficulty'],q['correctIndex'])==(e['difficulty'],e['correctIndex'])
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
old=json.loads(m.h.git(m.C,'show','5e66867c6d1438715baf207c1968145c00eb015c:src/content/topics/history-russia.json'))['questions']
assert [i for i,(l,r) in enumerate(zip(old,history),1) if l!=r]==[45,46,47,48]
assert set(x['ownProgress']['accepted'])=={history[i-1]['id'] for i in [45,46,47,48]}
for order in [45,46,47,48]:
 p=x[f'pendingHistoryRussia{order}'];assert p['status'].startswith('CERTIFIED') and p['qualityCredit']==1
 assert m.sha(history[order-1])==p['currentHash']
 cert=m.read(D/f'certification-history-russia{order}.json')
 assert cert['newQualityCredit']==1 and len(cert['accepted'])==1 and cert['accepted'][0]['questionId']==history[order-1]['id']
 assert cert['accepted'][0]['cardCanonicalSha256']==m.sha(history[order-1])
assert x['pendingHistoryRussia47']['status']=='CERTIFIED_SAME_READER_FINAL_SOLE_CYCLE1_PASS'
assert m.read(D/'verification-history-russia47-initial-fix.json')['acceptedOrders']==[]
for name,freeze in [('45','b853ea99bf39dfb785aca409de5da45a8a5c29fd'),('46','f3069904348a94881c02f3491b911937aab19c53'),('47','409ad8d1051a0ee7d2b8e53ce406ea208b32fb43'),('48','e56011e854791b5e055d04aa26c68f79a1742dc7'),('47-cycle1','612582c756ee3b40b8982552865fc6214050768f')]:
 for fn in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=D/('source-history-russia'+name)/fn
  assert p.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
diag=m.read(D/'source48-original-format-diagnostics.json')
for fn,digest in diag['rawFileSHA256'].items():assert m.raw(D/'source-history-russia48'/fn)==digest
c=m.read(D/'source-history-russia48/candidate.json');sp=m.read(D/'source-history-russia48/sourceproof.json')
m.alias_full_prompt_answer_concatenation(c,sp)
assert all(v['fullPrompt']+' '+v['answer']==v['originalPromptAnswerConcatenationLiteral'] for v in sp['entries'][0]['fourFullPromptAnswerNoteAssessments'])
assert m.read(D/'history-russia47-network-accounting.json')['actualWebCalls']==0
assert m.read(D/'history-russia47-cycle1-network-accounting.json')['actualWebCalls']==2
assert [m.read(D/f'history-russia{o}-network-accounting.json')['actualWebCalls'] for o in [45,46,48]]==[4,4,7]
assert len(x['coordinatorSlicesToPreserve'])==34 and cp['coordinatorSlicesToPreserve']==x['coordinatorSlicesToPreserve']
sl=x['coordinatorSlicesToPreserve'];assert sl[-1]=={'intakeCURRENT':952,'newlyCertified':4}
assert all(r['intakeCURRENT']==l['intakeCURRENT']+l['newlyCertified'] for l,r in zip(sl,sl[1:])) and sl[-1]['intakeCURRENT']+sl[-1]['newlyCertified']==n
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims']) and cp['owner']==m.O
assert m.read(m.P/'.flow-leases.json')=={} and not cp['currentSourceActors'] and not cp['currentIndependentActors']
def native(actor):
 p=pathlib.Path(actor['nativeJournal'])
 if not p.exists():
  matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+actor['threadId']+'.jsonl'));assert len(matches)==1;p=matches[0]
 rows=[json.loads(l) for l in p.open()];assert rows[0]['payload']['id']==actor['threadId']
 assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
 count=sum(r['type']=='compacted' for r in rows);assert count==actor['actualCompactions'];return rows,count
for k in ['author45','author46','author47','author48','author47Fix']:
 assert x['actors'][k]['archived'] and native(x['actors'][k])[1]==0
ra=x['actors']['reviewer'];rr,count=native(ra);assert count==0 and not ra.get('archived',False) and cp['nativeActorsCurrent']==[ra]
ri=next(r['payload']['info'] for r in reversed(rr) if r.get('payload',{}).get('type')=='token_count')
assert ri['last_token_usage']['input_tokens']==ra['lastInput']==387615 and ri['model_context_window']==475000
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert root[0]['payload']['id']==m.O
rootCount=sum(r['type']=='compacted' for r in root);assert rootCount==0
rootInfo=next(r['payload']['info'] for r in reversed(root) if r.get('payload',{}).get('type')=='token_count')
for r,k in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][k]
assert len(x['ownAffectedRuns'])==5
for path in x['ownAffectedRuns']:
 qa=m.read(path);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
q=x['nextUntouched'];assert q['sourceOrder']==49 and q==x['readScope']['nextUntouched'] and m.sha(history[48])==q['hash']
assert not (D/'source-history-russia49-task.json').exists() and not (D/'source-history-russia49').exists()
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mainCat={}
for topic in {e['topicId'] for e in sel}:mainCat.update({q['id']:q for q in json.loads(m.h.git(m.C,'show',main+':src/content/topics/'+topic+'.json'))['questions']})
presence={e['questionId']:m.sha(mainCat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes']}
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines()
disk=[p for p in D.rglob('*') if p.is_file() and p.name!='handoff-verification.json']
assert set(tracked)=={str(p.relative_to(m.C)) for p in disk}
assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'diff','--check','5e66867c6d1438715baf207c1968145c00eb015c','HEAD'])
report={'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'all956CurrentHashes':True,'exact956and1044Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownCatalogDeltaOnly45to48':True,'ownIntakeCURRENT':952,'ownNewlyCertified':4,'coordinatorSlicesCount':34,'ownSOURCEStatuses':{str(o):x[f'pendingHistoryRussia{o}']['status'] for o in [45,46,47,48]},'affectedContentRuns':5,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreservedAtCurrentBaseline':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'mainRemoteSHA':main,'mainCurrentEligibleExactHashMatches':sum(presence.values()),'mainCurrentEligibleExactHashMissing':len(presence)-sum(presence.values()),'ownAcceptedOnMain':{i:presence[i] for i in x['ownProgress']['accepted']},'mainIntegrated':all(presence.values()),'rootActualCompactions':rootCount,'rootLastInputBeforeVerificationMetadata':rootInfo['last_token_usage']['input_tokens'],'rootWindow':rootInfo['model_context_window'],'noActiveAuthorsOrReview':True,'noRetainedIdleAuthor':True,'retainedIdleReviewer':ra,'nextUntouched':q,'source48OriginalFAILRetainedAndInvertibleAliasOnly':True,'source47SoleCycle1RoleTransferAndPolicyReadDiagnosticRetained':True}
print(json.dumps(report,ensure_ascii=False,indent=2))
