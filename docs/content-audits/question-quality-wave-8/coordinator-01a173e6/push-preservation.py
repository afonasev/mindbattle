"""Push preserved feature HEAD and bind authoritative remote_push under a short P lease."""
import pathlib,importlib.util,datetime,sys,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=len(cp['currentEligibleCompletedIds']);released='--released' in sys.argv;expectedOwner=None if released else m.O;assert cp['owner']==expectedOwner and n==x['CURRENT'];assert all(m.flow.get(cid)[1]['owner']==expectedOwner for cid in x['claims']);
if released:assert x['phase']=='EXACT4_RELEASED_PENDING_SUCCESSOR_CLAIM' and x['successorThreadId'] and cp['pendingSuccessor']==x['successorThreadId']
assert m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
ref='refs/heads/codex/question-quality-wave-6';head=m.h.git(m.C,'rev-parse',ref)
base=m.read(D/'takeover.json')['predecessorRemotePush']['commit']
gate=subprocess.run(['git','-C',str(m.C),'diff','--check',base,head],text=True,capture_output=True)
diff_check={'fullExitCode':gate.returncode,'fullStdout':gate.stdout,'fullStderr':gate.stderr}
if gate.returncode:
 exception=m.read(D/'frozen-raw-whitespace-exception.json')
 artifact=pathlib.Path(exception['artifactPath']);rel=exception['repoRelativePath']
 assert artifact==D/'source-video-game-history62/museumofplay-relevant-context.txt' and str(artifact.relative_to(m.C))==rel
 assert gate.returncode==2 and gate.stdout==exception['expectedDiffCheckStdout'] and not gate.stderr
 assert m.raw(artifact)==exception['rawFileSHA256']==m.read(exception['nativeProof'])['rawFileSHA256']['museumofplay-relevant-context.txt']
 assert subprocess.check_output(['git','-C',str(m.C),'show',exception['immutableRawFreeze']+':'+rel])==artifact.read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',head+':'+rel])
 others=[p for p in m.h.git(m.C,'diff','--name-only',base,head).splitlines() if p!=rel]
 assert others
 m.h.git(m.C,'diff','--check',base,head,'--',*others)
 diff_check.update(status='FAIL_UNCURED_FROZEN_ORIGINAL_WHITESPACE',exactImmutableException=str(D/'frozen-raw-whitespace-exception.json'),allOtherChangedPathsExitCode=0,allOtherChangedPaths=len(others))
else:diff_check['status']='PASS'
m.h.git(m.C,'push','origin',ref+':'+ref);remote=m.h.git(m.C,'ls-remote','origin',ref).split()[0];assert remote==head
payload={'repo':str(m.C),'remote':'origin','branch':'codex/question-quality-wave-6','commit':head,'readbackVerified':True,'mainIntegrated':False,'CURRENT':n,'remaining':2000-n}
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx);assert expected==x['foreignIndexes']['planning']
with m.flow.locked():
 assert m.raw(idx)==expected;m.flow.lease('acquire','planning',m.O)
try:
 with m.flow.locked():
  for cid in x['claims']:
   assert m.raw(idx)==expected and m.flow.get(cid)[1]['owner']==expectedOwner;m.flow.evidence(cid,'remote_push',payload)
 report=m.P/f'evidence/question-revision-process-v2/preservation-push-{m.O[:8]}.json';m.write(report,{'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_push':payload,'claims':x['claims'],'authority':'delivery.evidence.remote_push plus fresh origin; historical manifest snapshots not authoritative','noIntegrationOrDeploy':True,'diff_check':diff_check});assert m.raw(idx)==expected
 pc=m.h.save(m.P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(m.P)) for p in [report,*[m.flow.get(cid)[0] for cid in x['claims']]]],f'Record authoritative preserved feature push CURRENT{n}',expected);print('planning',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={};print('featureRemote',head,'CURRENT',n,'remaining',2000-n)
