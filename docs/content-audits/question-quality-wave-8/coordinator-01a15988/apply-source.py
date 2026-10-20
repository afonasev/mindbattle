import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
s=importlib.util.spec_from_file_location('apply',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
B=D/sys.argv[1];candidate=m.read(B/'candidate.json');topic=candidate['entries'][0]['topicId'];peers=m.read(B/'peer-snapshot.json')
a.apply(B,candidate['sourceNativeId'],[candidate['entries'][0]['sourceOrder']],D/(sys.argv[1]+'-apply.json'),D/('qa-content'+str(candidate['entries'][0]['sourceOrder'])+'.json'),pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in peers['actualCurrentPeers'] if p['topicId']==topic]})
