"""Authorized exact3 takeover; preserve source evidence, foreign indexes and full goal."""
import pathlib,json,hashlib,importlib.util,ast,subprocess,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
O='01a15bcc-bb59-7060-a1d6-48c9b65f7d18';OLD='01a15bab-dac7-7741-aafb-9f7eeddc5513';S=D.with_name('coordinator-01a15bab')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase'].startswith('EXACT3_RELEASED')
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
idx={p: pathlib.Path(sv.git(p,'rev-parse','--path-format=absolute','--git-path','index')) for p in [C,P]};expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']}
for p in idx:assert raw(idx[p])==expected[p]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);assert read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==920 and len(cp['currentRemainingIds'])==1080
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='f9e19deac95ccf3cec64d6041be1bcd2655a8962'
assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in h['helpers']:
 original=(S/name).read_text();s=original.replace(OLD,O).replace('coordinator-01a15bab','coordinator-01a15bcc').replace('-01a15bab.json','-01a15bcc.json')
 if name=='bind-current-receipt.py':s=s.replace("'ownIntakeCURRENT':918","'ownIntakeCURRENT':920").replace('n-918','n-920')
 if name=='certification-common.py':s=s.replace('n-918','n-920')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert "coordinator-01a15a0f/reader-polar46-initial-task.json" in (D/'prepare-initial.py').read_text()
assert "packet_name = sys.argv[5]" in (D/'prepare-initial.py').read_text()
assert "D/('reader-polar'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])];x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT920',manifest=str(D/'manifest.json'),intakeCURRENT=920,ownIntakeCURRENT=920,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':920,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT920_BEFORE_SOURCE86','CURRENT':920,'remaining':1080},next='Native preflight retained idle sourceAuthor84 then assign untouched86; retained idle reviewer before next INITIAL',rootContextReason='Fresh successor actual0; previous preventive bounded handoff actual0; preserve all fences',successorThreadId=None,oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Exact owner/directory/suffix and intake918->920 substitutions; AST parsed; historical46 and optional fifth argument preserved; all aliases and naming-only guard retained.'
x['rootNativeAudit']={'threadId':O,'nativeJournal':'/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T05-11-46-'+O+'.jsonl','actualCompactions':0};x['currentWork'].update(CURRENT=920,remaining=1080);x['readScope']['ownD']=str(D);write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':920,'remaining':1080,'fullGoal':2000,'intakeCURRENT':920,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']}
write(D/'takeover.json',report)
files=clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in files],'Preserve fresh exact2000 successor CURRENT920 and owned helper instance',expected[C]);print('code',cc)
with flow.locked():
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[x['actors']['sourceAuthor84'],x['actors']['reviewer']],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':920,'remaining':1080,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':920,'remaining':1080},ownedIntake={'CURRENT':920,'newlyCertified':0,'remaining':1080,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':920,'CURRENT':920,'newlyCertified':0,'remaining':1080},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[x['actors']['sourceAuthor84']],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=[x['actors']['sourceAuthor84']],currentNativeActors={x['actors']['sourceAuthor84']['threadId']:x['actors']['sourceAuthor84']},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6–9; root intake920; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,intakeCURRENT=920,newlyCertified=0,CURRENT=918,remaining=1080,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15bcc.json';write(pp,{**report,'codeCommit':cc})
 pfiles=[cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in pfiles],'Record supported exact3 successor takeover with full CURRENT920 goal',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for p in idx:assert raw(idx[p])==expected[p]
print('owners exact3 verified; lease empty; FOREIGN indexes preserved')
