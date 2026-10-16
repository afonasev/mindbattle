"""Apply only qualified original polar16-17-binding-fix; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-polar16-17-binding-fix.json');B=D/'qualified-polar16-17-binding-fix';ps=m.read(B/'peer-snapshot.json')
# Active parks17 reader has no polar16/17 whole-body dependency and no same-topic read.
parks=m.read(D/'qualified-parks17-new-independent/peer-snapshot.json')
for key in ['polar-regions-laptev-lena','polar-regions-beaufort-mackenzie']:assert key not in m.json.dumps(parks)
assert m.read(D/'queue.json')['activeOTHER']['stage']=='parks17GENUINE_NEW_FIRSTINITIAL'

a.apply(B,q['author'],[16,17],D/'apply-polar16-17-binding-fix.json',D/'qa-polar16-17-binding-fix.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
