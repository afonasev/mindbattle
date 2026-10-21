"""Apply inherited qualified19 from actual original path, without raw changes."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
s=importlib.util.spec_from_file_location('apply',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
B=D.with_name('coordinator-01a15db1')/'qualified-source-history-russia19'
candidate=m.read(B/'candidate.json');peers=m.read(B/'peer-snapshot.json')
a.apply(B,candidate['sourceNativeId'],[19],D/'qualified-source-history-russia19-apply.json',D/'qa-qualified-source-history-russia19.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in peers['actualCurrentPeers'] if p['topicId']=='history-russia']})
