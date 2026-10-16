"""Apply only qualified original polar15; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-polar15.json');B=D/'qualified-polar15';ps=m.read(B/'peer-snapshot.json')
# Active parks16 reader has no polar15 in its whole-body dependency snapshot.
parks=m.read(D.parent/'coordinator-01a14377/qualified-parks16/peer-snapshot.json');assert 'polar-regions-polar-bear-largest' not in m.json.dumps(parks)
a.apply(B,q['author'],[15],D/'apply-polar15.json',D/'qa-polar15.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
