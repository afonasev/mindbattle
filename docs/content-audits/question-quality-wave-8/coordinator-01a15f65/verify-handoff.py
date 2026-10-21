"""Exact metadata/current-byte handoff checks; no source or QA replay."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=x['CURRENT']
assert n==952 and x['remaining']==1048 and x['fullGoal']==2000
cat={};orders={}
for p in sorted((m.C/'src/content/topics').glob('*.json')):
 t=m.read(p)
 for order,q in enumerate(t['questions'],1):cat[q['id']]=q;orders[q['id']]=order
a,b=cp['currentEligibleCompletedIds'],cp['currentRemainingIds'];sel=cp['selectedCards'];ids=[e['questionId'] for e in sel]
assert len(cat)==11000 and len(a)==len(set(a))==len(cp['completedCardHashes'])==n and len(b)==len(set(b))==2000-n
assert len(ids)==len(set(ids))==2000 and set(a).isdisjoint(b) and set(a)|set(b)==set(ids)
assert {e['questionId'] for e in cp['completedCardHashes']}==set(a)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {e['topicId'] for e in sel}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'));f={q['id']:(i,q['difficulty'],q['correctIndex']) for i,q in enumerate(old['questions'],1)}
 for e in (z for z in sel if z['topicId']==topic):
  q=cat[e['questionId']];assert f[q['id']]==(orders[q['id']],q['difficulty'],q['correctIndex'])
  assert (q['difficulty'],q['correctIndex'])==(e['difficulty'],e['correctIndex'])
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
old=json.loads(m.h.git(m.C,'show','9a410b535770230e603768eed6cd1bebb65ed1d3:src/content/topics/history-russia.json'))['questions']
assert [i for i,(l,r) in enumerate(zip(old,history),1) if l!=r]==[42,43,44]
assert m.h.git(m.C,'diff','--name-only','9a410b535770230e603768eed6cd1bebb65ed1d3','HEAD','--','src/content/topics').splitlines()==['src/content/topics/history-russia.json']
for order in [42,43,44]:assert m.sha(history[order-1])==x['pendingHistoryRussia'+str(order)]['currentHash']
assert history[41]['id'] in a and history[42]['id'] in b and history[43]['id'] in b
assert x['pendingHistoryRussia43']['status']=='TERMINAL_SAME_READER_FINAL_SOLE_CYCLE1_HOLD0'
assert x['pendingHistoryRussia44']['status']=='AUTHOR_HOLD_SOLE_CYCLE1_UNCHANGED_UNAPPLIED_UNQUALIFIED_NO_QA_NO_FINAL'
hc=m.read(D/'source-history-russia44-cycle1/candidate.json')['entries'][0]
assert hc['status']=='HOLD' and hc['beforeCard']==hc['proposedCard']==history[43]
assert not (D/'qualified-source-history-russia44-cycle1').exists() and not (D/'independent-history-russia44-cycle1-final').exists()
assert m.read(D/'source44-cycle1-first-compaction-partial.json')['firstUnfinishedCycle1ActualWebCalls']==0
for order,initial_calls in [(42,3),(43,4),(44,2)]:
 assert m.read(D/f'history-russia{order}-network-accounting.json')['actualWebCalls']==initial_calls
 assert m.read(D/f'history-russia{order}-cycle1-network-accounting.json')['actualWebCalls']==0
q=x['nextUntouched'];assert q==x['readScope']['nextUntouched'] and q['sourceOrder']==45 and m.sha(history[44])==q['hash']
assert not (D/'source-history-russia45-task.json').exists() and not (D/'source-history-russia45').exists()
assert x['ownProgress']['intake']==x['ownIntakeCURRENT']==951 and x['ownProgress']['newlyCertified']==x['newlyCertified']==1
assert x['ownProgress']['accepted']==[history[41]['id']] and len(x['coordinatorSlicesToPreserve'])==33
slices=x['coordinatorSlicesToPreserve'];assert slices[-5:]==[{'intakeCURRENT':945,'newlyCertified':1},{'intakeCURRENT':946,'newlyCertified':2},{'intakeCURRENT':948,'newlyCertified':1},{'intakeCURRENT':949,'newlyCertified':2},{'intakeCURRENT':951,'newlyCertified':1}]
assert all(r['intakeCURRENT']==l['intakeCURRENT']+l['newlyCertified'] for l,r in zip(slices,slices[1:])) and slices[-1]['intakeCURRENT']+slices[-1]['newlyCertified']==n
assert cp['coordinatorSlicesToPreserve']==slices
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims']) and cp['owner']==m.O
assert m.read(m.P/'.flow-leases.json')=={} and not cp['currentSourceActors'] and not cp['currentIndependentActors']
assert not x['sourceActorKeys'] and not any(a['stage'].startswith('START') for a in x['actors'].values())
def native(a):
 p=pathlib.Path(a['nativeJournal'])
 if not p.exists():
  matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+a['threadId']+'.jsonl'));assert len(matches)==1;p=matches[0]
 rows=[json.loads(l) for l in p.open()];assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==a['threadId']
 assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
 count=sum(r['type']=='compacted' for r in rows);assert count==a['actualCompactions'];return rows,count
for key,count in [('author42',0),('author43',1),('author44',1)]:
 assert x['actors'][key]['archived'];assert native(x['actors'][key])[1]==count
ra=x['retainedIdleReviewer'];assert ra['threadId']=='01a15f88-378e-72f1-a9a5-16c2bfa437c7' and not ra.get('archived',False)
rows,count=native(ra);assert count==0 and cp['nativeActorsCurrent']==[ra]
ri=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count');assert ri['last_token_usage']['input_tokens']==ra['lastInput'] and ri['model_context_window']==ra['modelWindow']
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert next(r['payload']['id'] for r in root if r['type']=='session_meta')==m.O
root_comp=sum(r['type']=='compacted' for r in root);root_info=next(r['payload']['info'] for r in reversed(root) if r.get('payload',{}).get('type')=='token_count')
assert root_comp==0
for r,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
assert len(x['ownAffectedRuns'])==3
for p in x['ownAffectedRuns']:
 qa=m.read(p);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0]
main_cat={}
for topic in {e['topicId'] for e in sel}:main_cat.update({q['id']:q for q in json.loads(m.h.git(m.C,'show',main+':src/content/topics/'+topic+'.json'))['questions']})
presence={e['questionId']:m.sha(main_cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes']}
assert not presence[history[41]['id']]
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();disk=[p for p in D.rglob('*') if p.is_file()]
assert set(tracked)=={str(p.relative_to(m.C)) for p in disk}
assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
report={'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'all952CurrentHashes':True,'exact952and1048Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownCatalogDeltaOnly42and43and44':True,'ownIntakeCURRENT':951,'ownNewlyCertified':1,'coordinatorSlicesCount':33,'SOURCE42':'CERTIFIED_SAME_READER_FINAL_SOLE_CYCLE1_PASS_3fbc1943','SOURCE43':'TERMINAL_SAME_READER_FINAL_SOLE_CYCLE1_HOLD0_61f47a9f','SOURCE44':'INITIAL_FIX_SOLE_AUTHORCYCLE1_HOLD_UNCHANGED_UNAPPLIED_NO_QA_NO_FINAL_ff1c63c9','affectedContentRuns':3,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreservedAtCurrentBaseline':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'mainRemoteSHA':main,'mainCurrentEligibleExactHashMatches':sum(presence.values()),'mainCurrentEligibleExactHashMissing':len(presence)-sum(presence.values()),'mainOwnAccepted42HashPresent':presence[history[41]['id']],'mainIntegrated':False,'rootActualCompactions':root_comp,'rootLastInputBeforeVerificationMetadata':root_info['last_token_usage']['input_tokens'],'rootWindow':root_info['model_context_window'],'noActiveAuthorsOrReview':True,'noRetainedIdleAuthor':True,'retainedIdleReviewer':ra,'nextUntouched':q}
m.write(D/'handoff-verification.json',report);x.update(handoffVerification=str(D/'handoff-verification.json'),rootActualCompactions=root_comp,actualCompactions=root_comp)
x['rootNativeAudit'].update(actualCompactions=root_comp,lastInput=report['rootLastInputBeforeVerificationMetadata'],modelWindow=report['rootWindow'])
x['verifiedNow'].update(all952CurrentHashes=True,exact952and1048Partition=True,all2000FrozenOrderDifficultyNumericKey=True)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
print('code',m.savecode([D/'handoff-verification.json',D/'manifest.json',D/'handoff-next.json'],'Verify exact CURRENT952 at-rest preservation and one readonly successor handoff'))
print(json.dumps(report,ensure_ascii=False))
