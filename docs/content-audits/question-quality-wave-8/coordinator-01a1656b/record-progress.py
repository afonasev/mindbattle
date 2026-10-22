"""Project an already-bound certificate and confirmed author cleanup; no quality decisions."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);actorKey=sys.argv[2];status=sys.argv[3];certificateCommit=sys.argv[4]
x=m.read(D/'manifest.json');cpPath=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cpPath)
certificatePath=D/f'certification-history-russia{order}.json';certificate=m.read(certificatePath)
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][order-1]
n=len(cp['currentEligibleCompletedIds']);delta=n-x['ownIntakeCURRENT']
assert cp['owner']==m.O and certificate['CURRENT']==n and certificate['newQualityCredit']==1
assert [e['questionId'] for e in certificate['accepted']]==[q['id']]
assert q['id'] in cp['currentEligibleCompletedIds'] and m.sha(q)==certificate['accepted'][0]['cardCanonicalSha256']
assert m.h.git(m.C,'show',certificateCommit+':'+str(certificatePath.relative_to(m.C))).encode()==certificatePath.read_bytes().rstrip(b'\n')
assert q['id'] not in x['ownProgress']['accepted']
x['ownProgress']['accepted'].append(q['id']);x['ownProgress']['certificates'].append(str(certificatePath));x['ownProgress']['newlyCertified']=delta
assert len(x['ownProgress']['accepted'])==len(set(x['ownProgress']['accepted']))==delta
x.update(CURRENT=n,remaining=2000-n,newlyCertified=delta,phase=f'ACTIVE_FULL2000_CURRENT{n}')
x[f'pendingHistoryRussia{order}'].update(status=status,qualityCredit=1,certification=str(certificatePath),certificationCodeCommit=certificateCommit)
x['actors'][actorKey].update(stage=f'ARCHIVED_AFTER_CERTIFIED_SOURCE{order}',archived=True)
x['sourceActorKeys']=[k for k in x['sourceActorKeys'] if k!=actorKey]
x['coordinatorSlicesToPreserve']=m.read(pathlib.Path(x['predecessorHandoff']))['coordinatorSlicesToPreserve']+[{'intakeCURRENT':x['ownIntakeCURRENT'],'newlyCertified':delta}]
x['currentWork'].update(CURRENT=n,remaining=2000-n)
x['additionalRetainedSourceIndexes']=list(dict.fromkeys(x['additionalRetainedSourceIndexes']+[x['sourceIndex']]))
packet='qualified-source-history-russia'+str(order)+('-cycle1' if 'FINAL' in status else '')
x['sourceIndex']=str(D/packet/'sourceproof.json')
x['helpers']['record-progress.py']=str(pathlib.Path(__file__))
m.write(D/'manifest.json',x);print('code',m.savecode([D/'manifest.json',pathlib.Path(__file__)],f'Record exact CURRENT{n} certificate projection and author cleanup'))
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx)
assert expected==x['foreignIndexes']['planning']
with m.flow.locked():
 assert m.raw(idx)==expected;m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(idx)==expected and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
 cp=m.read(cpPath);assert len(cp['currentEligibleCompletedIds'])==n;cp['coordinatorSlicesToPreserve']=x['coordinatorSlicesToPreserve'];m.write(cpPath,cp)
 sp=m.P/'evidence/question-revision-process-v2/coordinator-state.json';st=m.read(sp);st.update(coordinatorSlicesToPreserve=x['coordinatorSlicesToPreserve'],ownedIntake={'CURRENT':x['ownIntakeCURRENT'],'newlyCertified':delta,'remaining':2000-n,'fullGoal':2000});m.write(sp,st)
 gp=m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=m.read(gp);g.update(coordinatorSlicesToPreserve=x['coordinatorSlicesToPreserve'],intakeCURRENT=x['ownIntakeCURRENT'],newlyCertified=delta,CURRENT=n,remaining=2000-n);m.write(gp,g)
 print('planning',m.h.save(m.P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(m.P)) for p in [cpPath,sp,gp]],f'Preserve CURRENT{n} exact successor slice accounting',expected))
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
