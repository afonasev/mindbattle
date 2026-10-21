"""Verify CURRENT948 metadata and preservation, without content review or test reruns."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));cat={};orders={}
for p in (m.C/'src/content/topics').glob('*.json'):
 t=m.read(p)
 for n,q in enumerate(t['questions'],1):cat[q['id']]=q;orders[q['id']]=(t['id'],n)
assert len(cat)==11000
a,b=cp['currentEligibleCompletedIds'],cp['currentRemainingIds'];selected=cp['selectedCards'];ids=[e['questionId'] for e in selected]
assert len(a)==len(set(a))==len(cp['completedCardHashes'])==x['CURRENT']==948
assert len(b)==len(set(b))==x['remaining']==1052 and len(ids)==len(set(ids))==2000
assert set(a).isdisjoint(b) and set(a)|set(b)==set(ids)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {e['topicId'] for e in selected}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'));f={q['id']:(n,q['difficulty'],q['correctIndex']) for n,q in enumerate(old['questions'],1)}
 for e in (v for v in selected if v['topicId']==topic):
  q=cat[e['questionId']];assert f[q['id']]==(orders[q['id']][1],q['difficulty'],q['correctIndex']);assert (q['difficulty'],q['correctIndex'])==(e['difficulty'],e['correctIndex'])
polar=m.read(m.C/'src/content/topics/polar-regions.json')['questions']
for k,v in x['protectedHeldHashes'].items():assert m.sha(polar[int(k)-1])==v
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
for n in [22,23,24,30,31]:assert m.sha(history[n-1])==x['pendingHistoryRussia'+str(n)]['beforeHash']
assert m.sha(history[24])==x['pendingHistoryRussia25']['currentHash']
assert x['nextUntouched']==x['readScope']['nextUntouched'] and x['nextUntouched']['sourceOrder']==35
assert m.sha(history[34])==x['nextUntouched']['hash']
old=json.loads(m.h.git(m.C,'show','a72a5d03a5f79b5068bddbabb4e4ba0a8aad65cd:src/content/topics/history-russia.json'))
assert [n for n,(l,r) in enumerate(zip(old['questions'],history),1) if l!=r]==[33,34]
assert m.h.git(m.C,'diff','--name-only','a72a5d03a5f79b5068bddbabb4e4ba0a8aad65cd','HEAD','--','src/content/topics').splitlines()==['src/content/topics/history-russia.json']
assert x['ownProgress']['intake']==946 and x['ownProgress']['newlyCertified']==2 and len(x['coordinatorSlicesToPreserve'])==30
assert x['coordinatorSlicesToPreserve'][-2:]==[{'intakeCURRENT':945,'newlyCertified':1},{'intakeCURRENT':946,'newlyCertified':2}]
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims']) and cp['owner']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys']
assert all(x['actors'][k]['archived'] for k in ['author33','author34'])
ra=x['retainedIdleReviewer'];rr=[json.loads(l) for l in pathlib.Path(ra['nativeJournal']).open()]
assert next(r['payload']['id'] for r in rr if r['type']=='session_meta')==ra['threadId'];assert sum(r['type']=='compacted' for r in rr)==0
assert next(r['payload']['type'] for r in reversed(rr) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
ri=next(r['payload']['info'] for r in reversed(rr) if r.get('payload',{}).get('type')=='token_count');assert ri['last_token_usage']['input_tokens']==267814 and ri['model_context_window']==475000
rootpath=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T19-06-32-01a15ec8-fc23-7a73-8480-4099fa04f22e.jsonl');root=[json.loads(l) for l in rootpath.open()]
assert next(r['payload']['id'] for r in root if r['type']=='session_meta')==m.O and sum(r['type']=='compacted' for r in root)==0
info=next(r['payload']['info'] for r in reversed(root) if r.get('payload',{}).get('type')=='token_count')
for r,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
for qp in x['ownAffectedRuns']:
 qa=m.read(qp);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert len(x['ownAffectedRuns'])==4
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mt=json.loads(m.h.git(m.C,'show',main+':src/content/topics/history-russia.json'));mq={q['id']:q for q in mt['questions']}
presence={str(n):m.sha(mq[history[n-1]['id']])==m.sha(history[n-1]) for n in [13,14,18,19,20,21,26,27,28,29,32,33,34]};assert not any(presence.values())
remote=m.h.git(m.C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0]
assert all(m.flow.get(cid)[1]['evidence']['remote_push']['commit']==remote for cid in x['claims'])
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();files=[p for p in D.rglob('*') if p.is_file()]
assert set(tracked)=={str(p.relative_to(m.C)) for p in files};assert all(subprocess.check_output(['git','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
report={'CURRENT':948,'remaining':1052,'fullGoal':2000,'all948CurrentHashes':True,'exact948and1052Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownCatalogDeltaOnly33and34':True,'ownIntakeCURRENT':946,'ownNewlyCertified':2,'coordinatorSlicesCount':30,'SOURCE30':'AUTHORHOLD0_UNAPPLIED_NO_INITIAL','SOURCE31':'AUTHORHOLD0_UNCHANGED_UNAPPLIED_NO_INITIAL_POLICY_READ_GAP','SOURCE32':'CERTIFIED_INITIALPASS_9cc6e1c9','SOURCE33':'CERTIFIED_FINAL_SOLE_CYCLE1_dcbfc453','SOURCE34':'CERTIFIED_FINAL_SOLE_CYCLE1_05ca616c','affectedContentRuns':4,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'mainRemoteSHA':main,'mainAcceptedHashesPresent':presence,'mainIntegrated':False,'rootActualCompactions':0,'rootLastInputBeforeHandoffMetadata':info['last_token_usage']['input_tokens'],'rootWindow':info['model_context_window'],'noActiveAuthorsOrReview':True,'noRetainedIdleAuthor':True,'retainedIdleReviewer':{'threadId':ra['threadId'],'actualCompactions':0,'lastInput':267814,'window':475000,'taskComplete':True,'cursor':ra['cursor']},'lastVerifiedPushedSourceSHA':remote}
m.write(D/'handoff-verification.json',report)
x.update(phase='READY_FOR_READONLY_SUCCESSOR_CURRENT948',successorThreadId=None,successorNativeJournal=None,successorCreationProof=None,successorNativeProof=None,successorACK=None,successorStatus='PENDING_READONLY_SUCCESSOR',rootActualCompactions=0,actualCompactions=0,rootContextReason='Preventive bounded handoff after own33/34 certified solecycle1; no invented compaction',rootNativeAudit={'threadId':m.O,'nativeJournal':str(rootpath),'actualCompactions':0,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window']},handoffVerification=str(D/'handoff-verification.json'))
# Historical SOURCE32 prose diagnostic preserved unchanged.
x['verifiedNow'].update(all948CurrentHashes=True,exact948and1052Partition=True,all2000FrozenOrderDifficultyNumericKey=True)
m.write(D/'manifest.json',x);m.write(D/'handoff-next.json',x)
print(m.savecode([D/'manifest.json',D/'handoff-next.json',D/'handoff-verification.json'],'Verify exact CURRENT948 and preserve bounded read-only successor handoff'))
print(json.dumps(report,ensure_ascii=False))
