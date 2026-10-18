"""Apply exact two complete SOURCE originals; no quality credit."""
import pathlib,importlib.util,json
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(D/'activation.json')['ordinaryWorkActivated'];q=m.read(D/'qualification-polar36-minimal.json');B=D/'qualified-polar36-minimal';ps=m.read(B/'peer-snapshot.json')
for uid,date in [(m.O,'16'),(q['author'],'19'),('01a150d1-3383-7d30-ad23-76d70ec18813','19')]:
 p=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in p.open())<2
assert m.read(D/'queue.json')['activeOTHER']['stage']=='IDLE_AFTER27_FIRSTINITIAL_FIX_WAIT_SOLE_CYCLE1'
for p in ps['actualCurrentPeers']:
 live=next(c for c in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if c['id']==p['id']);assert live==p['card'] and m.sha(live)==p['sha256']
a.apply(B,q['author'],[36],D/'apply-polar36-minimal.json',D/'qa-polar36-minimal.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=q['editorialConcernsForOTHER'])
