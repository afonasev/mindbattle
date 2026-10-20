"""Apply the two mechanically qualified packets; independent quality credit stays zero."""
import pathlib, importlib.util
D = pathlib.Path(__file__).parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('owned',D/'owned-tools.py')
a=load('apply_standard',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(D/'manifest.json')['ordinaryWorkActivated']
assert len(m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')['currentEligibleCompletedIds']) == 890
for name in ['source-polar41-cycle1-fresh','source-parks31-complete']:
    B=D/('qualified-'+name);p=m.read(B/'candidate.json');e=p['entries'][0];peers=m.read(B/'peer-snapshot.json')
    a.apply(B,p['sourceNativeId'],[e['sourceOrder']],D/(name+'-apply.json'),D/'qa-content.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[v for v in peers['actualCurrentPeers'] if v['topicId']==e['topicId']]})
