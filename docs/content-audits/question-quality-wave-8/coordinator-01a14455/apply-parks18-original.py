"""Apply only qualified original parks18-original; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-parks18-original.json');B=D/'qualified-parks18-original';ps=m.read(B/'peer-snapshot.json')
pol=m.read(D/'qualified-polar16-17-binding-fix/peer-snapshot.json');assert 'national-parks-nature-018' not in m.json.dumps(pol)
assert m.read(D/'queue.json')['activeOTHER']['stage']=='POLAR16_17_FIRSTINITIAL'
a.apply(B,q['author'],[18],D/'apply-parks18-original.json',D/'qa-parks18-original.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER'])
