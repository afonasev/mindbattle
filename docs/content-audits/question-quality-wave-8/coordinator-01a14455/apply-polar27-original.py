"""Apply only qualified original polar27-original; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-polar27-original.json');B=D/'qualified-polar27-original';ps=m.read(B/'peer-snapshot.json')
assert m.read(D/'queue.json')['activeOTHER']['stage']=='IDLE_AFTER_GENUINE_NEW22_CERT870'
assert m.read(D/'certification-polar26-cycle1-final-pass.json')['verified']['acceptedCards']==1
a.apply(B,q['author'],[27],D/'apply-polar27-original.json',D/'qa-polar27-original.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
