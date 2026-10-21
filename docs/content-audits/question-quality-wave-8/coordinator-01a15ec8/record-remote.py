import pathlib,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');head=m.h.git(m.C,'rev-parse','HEAD');remote=m.h.git(m.C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0];assert head==remote
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 with m.flow.locked():
  for cid in x['claims']:
   m.flow.evidence(cid,'remote_push',{'repo':str(m.C),'remote':'origin','branch':x['codeBranch'],'commit':remote,'readbackVerified':True,'mainIntegrated':False,'CURRENT':x['CURRENT'],'remaining':x['remaining']})
 paths=[m.flow.get(cid)[0] for cid in x['claims']]
 print('planningRemoteEvidence',m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in paths],'Record exact source-branch remote push and fresh readback',x['foreignIndexes']['planning']))
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={}
print('sourceRemote',remote)
