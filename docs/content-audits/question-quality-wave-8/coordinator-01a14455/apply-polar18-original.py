"""Apply only qualified original polar18-original; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-polar18-original.json');B=D/'qualified-polar18-original';ps=m.read(B/'peer-snapshot.json')
parks=m.read(D/'qualified-parks18-original/peer-snapshot.json');assert 'polar-regions-chukchi-bering-strait' not in m.json.dumps(parks)
assert m.read(D/'queue.json')['activeOTHER']['stage']=='PARKS18_FIRSTINITIAL_ACTIVE'
a.apply(B,q['author'],[18],D/'apply-polar18-original.json',D/'qa-polar18-original.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
