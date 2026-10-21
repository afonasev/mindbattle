"""Push preserved feature HEAD and bind authoritative remote_push under a short P lease."""
import pathlib,importlib.util,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=len(cp['currentEligibleCompletedIds']);assert cp['owner']==m.O and n==x['CURRENT'];assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']);assert m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
ref='refs/heads/codex/question-quality-wave-6';head=m.h.git(m.C,'rev-parse',ref);m.h.git(m.C,'diff','--check','5508df6f6873d38d08539b2cee1ae488d223cc0d',head);m.h.git(m.C,'push','origin',ref+':'+ref);remote=m.h.git(m.C,'ls-remote','origin',ref).split()[0];assert remote==head
payload={'repo':str(m.C),'remote':'origin','branch':'codex/question-quality-wave-6','commit':head,'readbackVerified':True,'mainIntegrated':False,'CURRENT':n,'remaining':2000-n}
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx);assert expected==x['foreignIndexes']['planning']
with m.flow.locked():
 assert m.raw(idx)==expected;m.flow.lease('acquire','planning',m.O)
try:
 with m.flow.locked():
  for cid in x['claims']:
   assert m.raw(idx)==expected and m.flow.get(cid)[1]['owner']==m.O;m.flow.evidence(cid,'remote_push',payload)
 report=m.P/f'evidence/question-revision-process-v2/preservation-push-{m.O[:8]}.json';m.write(report,{'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_push':payload,'claims':x['claims'],'authority':'delivery.evidence.remote_push plus fresh origin; historical manifest snapshots not authoritative','noIntegrationOrDeploy':True});assert m.raw(idx)==expected
 pc=m.h.save(m.P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(m.P)) for p in [report,*[m.flow.get(cid)[0] for cid in x['claims']]]],f'Record authoritative preserved feature push CURRENT{n}',expected);print('planning',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={};print('featureRemote',head,'CURRENT',n,'remaining',2000-n)
