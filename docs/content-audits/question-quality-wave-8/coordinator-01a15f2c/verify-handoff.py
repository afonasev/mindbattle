"""Deterministic exact CURRENT951 handoff verification; no semantic review or QA rerun."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));cat={};orders={}
for p in (m.C/'src/content/topics').glob('*.json'):
 t=m.read(p)
 for n,q in enumerate(t['questions'],1):cat[q['id']]=q;orders[q['id']]=(t['id'],n)
a,b=cp['currentEligibleCompletedIds'],cp['currentRemainingIds'];sel=cp['selectedCards'];ids=[e['questionId'] for e in sel]
assert len(cat)==11000 and len(a)==len(set(a))==len(cp['completedCardHashes'])==951 and len(b)==len(set(b))==1049
assert len(ids)==len(set(ids))==2000 and set(a).isdisjoint(b) and set(a)|set(b)==set(ids)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {e['topicId'] for e in sel}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'));f={q['id']:(n,q['difficulty'],q['correctIndex']) for n,q in enumerate(old['questions'],1)}
 for e in (z for z in sel if z['topicId']==topic):
  q=cat[e['questionId']];assert f[q['id']]==(orders[q['id']][1],q['difficulty'],q['correctIndex']);assert (q['difficulty'],q['correctIndex'])==(e['difficulty'],e['correctIndex'])
polar=m.read(m.C/'src/content/topics/polar-regions.json')['questions']
for k,v in x['protectedHeldHashes'].items():assert m.sha(polar[int(k)-1])==v
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
for n in [22,23,24,30,31,36,37,38,41]:assert m.sha(history[n-1])==x['pendingHistoryRussia'+str(n)]['beforeHash']
assert m.sha(history[24])==x['pendingHistoryRussia25']['currentHash']
assert x['nextUntouched']==x['readScope']['nextUntouched'] and x['nextUntouched']['sourceOrder']==42 and m.sha(history[41])==x['nextUntouched']['hash']
old=json.loads(m.h.git(m.C,'show','3d9433761d8c4259d57d95298da478b9b4be26de:src/content/topics/history-russia.json'))
assert [n for n,(l,r) in enumerate(zip(old['questions'],history),1) if l!=r]==[39,40]
assert m.h.git(m.C,'diff','--name-only','3d9433761d8c4259d57d95298da478b9b4be26de','HEAD','--','src/content/topics').splitlines()==['src/content/topics/history-russia.json']
assert x['ownProgress']['intake']==949 and x['ownProgress']['newlyCertified']==2 and len(x['coordinatorSlicesToPreserve'])==32
assert x['coordinatorSlicesToPreserve'][-4:]==[{'intakeCURRENT':945,'newlyCertified':1},{'intakeCURRENT':946,'newlyCertified':2},{'intakeCURRENT':948,'newlyCertified':1},{'intakeCURRENT':949,'newlyCertified':2}]
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims']) and cp['owner']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys']
assert all(x['actors'][k]['archived'] for k in ['author38','author39','author40','author41'])
ra=x['retainedIdleReviewer'];rr=[json.loads(l) for l in pathlib.Path(ra['nativeJournal']).open()]
assert next(r['payload']['id'] for r in rr if r['type']=='session_meta')==ra['threadId'];assert sum(r['type']=='compacted' for r in rr)==0
assert next(r['payload']['type'] for r in reversed(rr) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
ri=next(r['payload']['info'] for r in reversed(rr) if r.get('payload',{}).get('type')=='token_count');assert ri['last_token_usage']['input_tokens']==377074 and ri['model_context_window']==475000
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert next(r['payload']['id'] for r in root if r['type']=='session_meta')==m.O and sum(r['type']=='compacted' for r in root)==0
for r,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
for qp in x['ownAffectedRuns']:
 qa=m.read(qp);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert len(x['ownAffectedRuns'])==3
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mt=json.loads(m.h.git(m.C,'show',main+':src/content/topics/history-russia.json'));mq={q['id']:q for q in mt['questions']}
presence={str(n):m.sha(mq[history[n-1]['id']])==m.sha(history[n-1]) for n in [13,14,18,19,20,21,26,27,28,29,32,33,34,35,39,40]};assert not any(presence.values())
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();files=[p for p in D.rglob('*') if p.is_file()]
assert set(tracked)=={str(p.relative_to(m.C)) for p in files};assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
report={'CURRENT':951,'remaining':1049,'fullGoal':2000,'all951CurrentHashes':True,'exact951and1049Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownCatalogDeltaOnly39and40':True,'ownIntakeCURRENT':949,'ownNewlyCertified':2,'coordinatorSlicesCount':32,'SOURCE38':'AUTHORHOLD0_UNQUALIFIED_UNAPPLIED_NO_INITIAL','SOURCE39':'CERTIFIED_INITIAL_PASS_b11294ad','SOURCE40':'CERTIFIED_FINAL_SOLE_CYCLE1_PASS_56b46de7','SOURCE41':'AUTHORHOLD0_UNCHANGED_UNQUALIFIED_UNAPPLIED_NO_INITIAL','affectedContentRuns':3,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreservedAtCurrentBaseline':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'mainRemoteSHA':main,'mainAcceptedHashesPresent':presence,'mainIntegrated':False,'rootActualCompactions':0,'rootLastInputBeforeHandoffMetadata':x['rootNativeAudit']['lastInput'],'rootWindow':475000,'noActiveAuthorsOrReview':True,'noRetainedIdleAuthor':True,'retainedIdleReviewer':{'threadId':ra['threadId'],'actualCompactions':0,'lastInput':377074,'window':475000,'taskComplete':True,'cursor':ra['cursor']}}
m.write(D/'handoff-verification.json',report);x.update(phase='READY_FOR_READONLY_SUCCESSOR_CURRENT951',rootActualCompactions=0,actualCompactions=0,handoffVerification=str(D/'handoff-verification.json'),successorStatus='PENDING_READONLY_SUCCESSOR',successorThreadId=None,successorACK=None)
x['verifiedNow'].update(all951CurrentHashes=True,exact951and1049Partition=True,all2000FrozenOrderDifficultyNumericKey=True)
m.write(D/'manifest.json',x);m.write(D/'handoff-next.json',x)
print(m.savecode([D/'manifest.json',D/'handoff-next.json',D/'handoff-verification.json'],'Verify exact CURRENT951 and preserve bounded readonly successor handoff'))
print(json.dumps(report,ensure_ascii=False))
