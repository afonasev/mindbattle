"""Apply only qualified original polar25-original; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-polar25-original.json');B=D/'qualified-polar25-original';ps=m.read(B/'peer-snapshot.json')
assert m.read(D/'queue.json')['activeOTHER']['stage']=='PARKS23_FIRSTINITIAL_ACTIVE'
activePeers=m.read(D/'qualified-parks23-original/peer-snapshot.json');assert 'polar-regions-frazil-crystals' not in m.json.dumps(activePeers)
assert m.read(D/'consume-polar26-firstinitial-fix.json')['status']=='CONSUMED_INITIAL_FIX_ONE_DIRECTED_SOURCE_CYCLE1_PENDING'
a.apply(B,q['author'],[25],D/'apply-polar25-original.json',D/'qa-polar25-original.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
