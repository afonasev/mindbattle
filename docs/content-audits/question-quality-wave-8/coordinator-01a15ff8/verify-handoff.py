"""Read-only CURRENT961/own50-54 snapshot; not a successor takeover route."""
import pathlib,json,importlib.util,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=x['CURRENT'];assert n==961 and x['remaining']==1039 and x['fullGoal']==2000 and x['ownIntakeCURRENT']==956 and x['newlyCertified']==5
cat={};order={}
for p in sorted((m.C/'src/content/topics').glob('*.json')):
 for i,q in enumerate(m.read(p)['questions'],1):cat[q['id']]=q;order[q['id']]=i
assert len(cat)==11000;a=cp['currentEligibleCompletedIds'];b=cp['currentRemainingIds'];sel=cp['selectedCards'];ids=[e['questionId'] for e in sel]
assert len(a)==len(set(a))==len(cp['completedCardHashes'])==n and len(b)==len(set(b))==2000-n and len(ids)==len(set(ids))==2000
assert set(a).isdisjoint(b) and set(a)|set(b)==set(ids) and {e['questionId'] for e in cp['completedCardHashes']}==set(a)
assert all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for t in {e['topicId'] for e in sel}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+t+'.json'));frozen={q['id']:(i,q['difficulty'],q['correctIndex']) for i,q in enumerate(old['questions'],1)}
 for e in (z for z in sel if z['topicId']==t):
  q=cat[e['questionId']];assert frozen[q['id']]==(order[q['id']],q['difficulty'],q['correctIndex']);assert (q['difficulty'],q['correctIndex'])==(e['difficulty'],e['correctIndex'])
history=m.read(m.C/'src/content/topics/history-russia.json')['questions'];old=json.loads(m.h.git(m.C,'show','5508df6f6873d38d08539b2cee1ae488d223cc0d:src/content/topics/history-russia.json'))['questions'];assert [i for i,(l,r) in enumerate(zip(old,history),1) if l!=r]==[50,51,52,53,54]
assert set(x['ownProgress']['accepted'])=={history[o-1]['id'] for o in [50,51,52,53,54]} and x['ownProgress']['newlyCertified']==5
for o in [50,51,52,53,54]:
 cert=m.read(D/f'certification-history-russia{o}.json');assert cert['newQualityCredit']==1 and len(cert['accepted'])==1 and cert['accepted'][0]['questionId']==history[o-1]['id'] and cert['accepted'][0]['cardCanonicalSha256']==m.sha(history[o-1]);assert x[f'pendingHistoryRussia{o}']['qualityCredit']==1
assert x['pendingHistoryRussia54']['status']=='CERTIFIED_SAME_READER_FINAL_SOLE_CYCLE1_PASS' and x['pendingHistoryRussia54']['cycle1NetworkCalls']==0
for o in [49,55]:assert history[o-1]==old[o-1] and x[f'pendingHistoryRussia{o}']['qualityCredit']==0 and not x[f'pendingHistoryRussia{o}']['applied'] and x[f'pendingHistoryRussia{o}']['noIndependentInitial'];assert not (D/f'qualified-source-history-russia{o}').exists()
assert x['ownHeldThisSlice']==[49,55] and not (D/'independent-history-russia55-initial').exists() and not (D/'qa-qualified-source-history-russia55.json').exists()
freezes={'49':'9a454e64611365994cee76eb96e0a851ce3c4fea','50':'c44bce68e14be08a31418b663b0c52fca4fdaa09','51':'97e2ba216420e3a8a23949cc145815c28e53b021','52':'2e00f18b087f83bec7891bdfa16e22b69ec21cb7','53':'8309c5c1e26a203dd214a8a877a65d6aacecfeee','54':'aee17e431dc0a7e177be4da096e143dd4cbb18a2','54-cycle1':'96dae8eb6908f1d00f5616c9aadcf0f772c6a3fc','55':'ecd8004938d81397b88128f115e4b40c954bd274'}
for name,freeze in freezes.items():
 for f in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=D/('source-history-russia'+name)/f;assert p.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
assert [m.read(D/f'history-russia{o}-network-accounting.json')['actualWebCalls'] for o in [49,50,51,52,53,54,55]]==[2,3,4,0,4,2,4]
net55=m.read(D/'history-russia55-network-accounting.json');assert net55['candidateExecModules']==5 and len(net55['preDispatchCompilationFailures'])==1 and net55['preDispatchCompilationFailures'][0]['actualWebCalls']==0
assert m.read(D/'history-russia54-cycle1-network-accounting.json')['actualWebCalls']==0
sl=x['coordinatorSlicesToPreserve'];assert len(sl)==35 and sl[-1]=={'intakeCURRENT':956,'newlyCertified':5} and cp['coordinatorSlicesToPreserve']==sl
assert all(r['intakeCURRENT']==l['intakeCURRENT']+l['newlyCertified'] for l,r in zip(sl,sl[1:])) and sl[-1]['intakeCURRENT']+sl[-1]['newlyCertified']==n
assert set(d['id'] for p,d in m.flow.records().values() if d['owner']==m.O)==set(x['claims']) and cp['owner']==cp['activeCoordinator']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys']
def native(actor):
 uid=actor['threadId'];ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(ps)==1;rows=[json.loads(l) for l in ps[0].open()];assert rows[0]['payload']['id']==uid;assert sum(r['type']=='compacted' for r in rows)==actor['actualCompactions']==0;assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete';return rows
for key in ['author49','author51','author52','author53','author54','author55']:assert x['actors'][key]['archived'];native(x['actors'][key])
reviewer=x['actors']['reviewer'];rr=native(reviewer);info=next(r['payload']['info'] for r in reversed(rr) if r.get('payload',{}).get('type')=='token_count');assert info['last_token_usage']['input_tokens']==reviewer['lastInput']==273937 and info['model_context_window']==475000 and not reviewer.get('archived',False);assert cp['nativeActorsCurrent']==[reviewer]
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert root[0]['payload']['id']==m.O;rootCount=sum(r['type']=='compacted' for r in root);rootInfo=next(r['payload']['info'] for r in reversed(root) if r.get('payload',{}).get('type')=='token_count')
for r,k in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][k]
assert m.h.git(m.P,'rev-parse','HEAD')=='01e3cb6f1195ac1b3b5b16be458a3428ee89e6bd' and m.h.git(m.P,'branch','--show-current')=='main'
assert len(x['ownAffectedRuns'])==5
for path in x['ownAffectedRuns']:
 qa=m.read(path);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==qa.get('numTodoTests',0)==0
q=x['nextUntouched'];assert q['sourceOrder']==56 and q['hash']==m.sha(history[55]) and not (D/'source-history-russia56-task.json').exists() and not (D/'source-history-russia56').exists()
remote=m.flow.get(x['claims'][0])[1]['evidence']['remote_push'];assert remote['CURRENT']==n and remote['remaining']==2000-n and all(m.flow.get(cid)[1]['evidence']['remote_push']==remote for cid in x['claims']);assert m.h.git(m.C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0]==remote['commit']
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mc={}
for t in {e['topicId'] for e in sel}:mc.update({q['id']:q for q in json.loads(m.h.git(m.C,'show',main+':src/content/topics/'+t+'.json'))['questions']})
presence={e['questionId']:m.sha(mc[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes']};assert sum(presence.values())==0
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();disk=[p for p in D.rglob('*') if p.is_file()];assert set(tracked)=={str(p.relative_to(m.C)) for p in disk};assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'diff','--check','5508df6f6873d38d08539b2cee1ae488d223cc0d','HEAD'])
print(json.dumps({'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'all961CurrentHashes':True,'exact961and1039Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownIntakeCURRENT':956,'ownNewlyCertified':5,'ownCatalogDeltaOnly50to54':True,'coordinatorSlicesCount':35,'ownSOURCEStatuses':{str(o):x[f'pendingHistoryRussia{o}']['status'] for o in [49,50,51,52,53,54,55]},'affectedContentRuns':5,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'authorArchiveConfirmed':6,'allAuthorsActualCompactions':0,'noActiveSourceOrReviewTask':True,'retainedIdleReviewer':reviewer,'reviewerRemaining':201063,'rootActualCompactions':rootCount,'rootLastInputAtVerification':rootInfo['last_token_usage']['input_tokens'],'rootWindow':rootInfo['model_context_window'],'mainRemoteSHA':main,'mainCurrentEligibleExactHashMatches':sum(presence.values()),'mainCurrentEligibleExactHashMissing':len(presence)-sum(presence.values()),'ownAcceptedOnMain':{i:presence[i] for i in x['ownProgress']['accepted']},'mainIntegrated':False,'remotePushAuthority':remote,'nextUntouched':q,'source49OriginalFormatFAILRetained':True,'source55PreDispatchSyntax0AndOmittedExtraAlternativeHOLDRetained':True,'source54SoleCycle1OnlyNote2AndSameReaderFINALPASS':True,'noNewHumanGoForRemaining':True},ensure_ascii=False))
