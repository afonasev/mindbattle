"""Apply only qualified original parks17-new-independent; affected QA and independent INITIAL remain required."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(m.P/f'evidence/question-revision-process-v2/active-full2000-goal-{m.O}.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-parks17-new-independent.json');B=D/'qualified-parks17-new-independent';ps=m.read(B/'peer-snapshot.json')
assert m.read(D/'queue.json')['activeOTHER']['stage'].startswith('IDLE')
a.apply(B,q['author'],[17],D/'apply-parks17-new-independent.json',D/'qa-parks17-new-independent.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER'])
