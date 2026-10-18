"""Apply qualified exact parks24; guarded pre2. No quality credit."""
import pathlib,importlib.util,json
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(D/'activation.json')['ordinaryWorkActivated'];q=m.read(D/'qualification-parks26-cycle1-fresh.json');B=D/'qualified-parks26-cycle1-fresh';ps=m.read(B/'peer-snapshot.json')
for uid in [m.O,q['author'],'01a14483-ccd0-7321-bd23-2262fcb11e5b']:
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/16').glob('*'+uid+'.jsonl'));assert len(fs)==1;rows=[json.loads(l) for l in fs[0].open()];assert sum(r.get('type')=='compacted' for r in rows)<2
assert m.read(D/'queue.json')['activeOTHER']['stage']=='IDLE_AFTER26_GENUINE_FIRSTINITIAL_FIX_WAIT_SOLE_CYCLE1'
for p in ps['actualCurrentPeers']:
 live=next(c for c in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if c['id']==p['id']);assert live==p['card'] and m.sha(live)==p['sha256']
a.apply(B,q['author'],[26],D/'apply-parks26-cycle1-fresh.json',D/'qa-parks26-cycle1-fresh.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER'])
