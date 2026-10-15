"""Four affected lease-control paths against real Flow in an owned temporary root."""
import pathlib,json,tempfile,importlib.util,types,hashlib
D=pathlib.Path(__file__).parent;C=pathlib.Path(__file__).resolve().parents[4]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
guard=load('guard',D/'planning-certification-guard.py');Flow=load('flow_under_test',C/'tools/flow.py').Flow
out=[]
with tempfile.TemporaryDirectory(prefix='mindbattle-certguard-01a13f31-') as td:
 p=pathlib.Path(td);(p/'openspec/changes').mkdir(parents=True);flow=Flow(p);read=lambda path:json.loads(path.read_text());m=types.SimpleNamespace(P=p,O='owned-test',flow=flow,read=read)
 def owner():return read(p/'.flow-leases.json').get('planning',{}).get('owner')
 calls=[]
 m.certify=lambda:calls.append('unexpected')
 with flow.locked():flow.lease('acquire','planning','simulated-other')
 try:guard.certify_preleased(m)
 except ValueError:pass
 else:raise AssertionError('Foreign lease must reject before certificate callback')
 assert not calls and owner()=='simulated-other';out.append('foreign_lease_prevents_any_certificate_write')
 with flow.locked():flow.lease('release','planning','simulated-other')
 def success():
  assert owner()==m.O
  with flow.locked():flow.lease('acquire','planning',m.O)
  with flow.locked():flow.lease('release','planning',m.O)
  return 'code_and_checkpoint_saved'
 m.certify=success;assert guard.certify_preleased(m)=='code_and_checkpoint_saved' and owner() is None;out.append('existing_helper_same_owner_reacquire_and_release')
 def fail():
  assert owner()==m.O
  raise RuntimeError('simulated failure before helper lease try')
 m.certify=fail
 try:guard.certify_preleased(m)
 except RuntimeError:pass
 else:raise AssertionError('Expected propagated certificate failure')
 assert owner() is None;out.append('early_exception_releases_only_still_owned_lease')
 def acquired_after_helper():
  with flow.locked():flow.lease('release','planning',m.O)
  with flow.locked():flow.lease('acquire','planning','simulated-other')
  return 'saved'
 m.certify=acquired_after_helper;assert guard.certify_preleased(m)=='saved' and owner()=='simulated-other';out.append('foreign_owner_after_helper_return_preserved')
report={'guardRawSHA256':hashlib.sha256((D/'planning-certification-guard.py').read_bytes()).hexdigest(),'passed':len(out),'failed':0,'cases':out,'command':'python3 '+str(pathlib.Path(__file__).resolve()),'reason':'Only new internal certification lease wrapper. Real Flow isolated in owned temp root verifies no callback under foreign lease and no foreign-release cleanup; no production planning leases or indexes touched.','temporaryRootRemoved':not pathlib.Path(td).exists(),'noProjectFullSuiteRuntimeBuild':True}
(D/'planning-certification-guard-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
