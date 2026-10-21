"""Exact CURRENT945 handoff metadata verification; no content review or tests."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']))
cat={};orders={}
for p in (m.C/'src/content/topics').glob('*.json'):
 t=m.read(p)
 for n,q in enumerate(t['questions'],1):cat[q['id']]=q;orders[q['id']]=(t['id'],n)
a,b=cp['currentEligibleCompletedIds'],cp['currentRemainingIds'];ids=[r['questionId'] for r in cp['selectedCards']]
assert len(a)==len(set(a))==len(cp['completedCardHashes'])==945
assert len(b)==len(set(b))==1055 and len(ids)==len(set(ids))==2000
assert set(a).isdisjoint(b) and set(a)|set(b)==set(ids)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {r['topicId'] for r in cp['selectedCards']}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'))
 frozen={q['id']:(n,q['difficulty'],q['correctIndex']) for n,q in enumerate(old['questions'],1)}
 for e in (r for r in cp['selectedCards'] if r['topicId']==topic):
  q=cat[e['questionId']];assert frozen[q['id']]==(orders[q['id']][1],q['difficulty'],q['correctIndex'])
  assert q['difficulty']==e['difficulty'] and q['correctIndex']==e['correctIndex']
polar=m.read(m.C/'src/content/topics/polar-regions.json')['questions']
for k,h in x['protectedHeldHashes'].items():assert k.isdecimal() and m.sha(polar[int(k)-1])==h
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
for n in [22,23,24]:assert m.sha(history[n-1])==x['pendingHistoryRussia'+str(n)]['beforeHash']
assert m.sha(history[24])==x['pendingHistoryRussia25']['currentHash']
assert x['nextUntouched']==x['readScope']['nextUntouched'] and x['nextUntouched']['sourceOrder']==30
assert m.sha(history[29])==x['nextUntouched']['hash']
prior='8f877a5b89bd21297615c48c9558cd2360bad9bd'
old=json.loads(m.h.git(m.C,'show',prior+':src/content/topics/history-russia.json'))
assert [n for n,(a,b) in enumerate(zip(old['questions'],history),1) if a!=b]==[28,29]
assert m.h.git(m.C,'diff','--name-only',prior,'HEAD','--','src/content/topics').splitlines()==['src/content/topics/history-russia.json']
assert x['ownProgress']['intake']==943 and x['ownProgress']['newlyCertified']==2
assert len(x['coordinatorSlicesToPreserve'])==28 and x['coordinatorSlicesToPreserve'][-1]=={'intakeCURRENT':943,'newlyCertified':2}
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims'])
assert cp['owner']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys']
assert all(x['actors'][k]['archived'] for k in ['author28','author29'])
ra=x['retainedIdleReviewer'];rows=[json.loads(l) for l in pathlib.Path(ra['nativeJournal']).open()]
assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==ra['threadId']
assert sum(r['type']=='compacted' for r in rows)==0
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
assert info['last_token_usage']['input_tokens']==128292 and info['model_context_window']==475000
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()]
assert next(r['payload']['id'] for r in root if r['type']=='session_meta')==m.O and sum(r['type']=='compacted' for r in root)==0
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
qa=m.read(D/'qa-source28-29-shared.json');assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
mainsha=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0]
main=json.loads(m.h.git(m.C,'show',mainsha+':src/content/topics/history-russia.json'));mq={q['id']:q for q in main['questions']}
presence={str(n):m.sha(mq[history[n-1]['id']])==m.sha(history[n-1]) for n in [13,14,18,19,20,21,26,27,28,29]};assert not any(presence.values())
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();files=[p for p in D.rglob('*') if p.is_file()]
assert set(tracked)=={str(p.relative_to(m.C)) for p in files}
assert all(subprocess.check_output(['git','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
report={'CURRENT':945,'remaining':1055,'fullGoal':2000,'all945CurrentHashes':True,'exact945and1055Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'allOwnCatalogChangesExactly28And29':True,'protectedHeldHashes':x['protectedHeldHashes'],'ownIntakeCURRENT':943,'ownNewlyCertified':2,'ownCertificates':x['ownProgress']['certificates'],'coordinatorSlicesCount':28,'affectedContentRuns':1,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'mainRemoteSHA':mainsha,'mainAcceptedHashesPresent':presence,'mainIntegrated':False,'rootActualCompactions':0,'rootLastInputBeforeHandoffMetadata':x['rootNativeAudit']['lastInput'],'noActiveAuthorsOrReview':True,'noRetainedIdleAuthor':True,'retainedIdleReviewer':{'threadId':ra['threadId'],'actualCompactions':0,'lastInput':128292,'window':475000,'taskComplete':True,'cursor':ra['cursor']}}
m.write(D/'handoff-verification.json',report);x['verifiedNow'].update(all945CurrentHashes=True,exact945and1055Partition=True,all2000FrozenOrderDifficultyNumericKey=True)
m.write(D/'manifest.json',x);m.write(D/'handoff-next.json',x)
print(m.savecode([D/'handoff-verification.json',D/'manifest.json',D/'handoff-next.json'],'Verify CURRENT945 exact2000 preservation and live idle reviewer before handoff'))
print(json.dumps(report,ensure_ascii=False))
