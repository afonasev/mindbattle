import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
s=importlib.util.spec_from_file_location('apply',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
B=D/sys.argv[1];candidate=m.read(B/'candidate.json');topic=candidate['entries'][0]['topicId'];peers=m.read(B/'peer-snapshot.json')
x=m.read(D/'manifest.json')
assert B.parent==D and B.name.startswith('qualified-source-fashion') and topic==x['activeRoute']['topicId'] and x['activeRoute']['wave']==9
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:
 assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
assert not x['actors']['reviewer']['stage'].startswith('START'), 'Catalog frozen during independent verdict'
peer_addendum=D/sys.argv[2] if len(sys.argv)>2 else None
if peer_addendum:assert peer_addendum.parent==D and peer_addendum.is_file()
a.apply(B,candidate['sourceNativeId'],[candidate['entries'][0]['sourceOrder']],D/(sys.argv[1]+'-apply.json'),D/('qa-'+B.name+'.json'),pathlib.Path(__file__),peerAddendum=peer_addendum,peerSnapshot={'actualCurrentPeers':[p for p in peers['actualCurrentPeers'] if p['topicId']==topic]})
