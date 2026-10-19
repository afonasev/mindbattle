"""Apply already qualified original parks28 fresh personal SOURCE; no editorial quality credit."""
import pathlib, importlib.util, json, subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14508'
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('owned',D/'owned-tools.py');a=mod('apply',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
assert m.read(D/'activation.json')['ordinaryWorkActivated']
q=m.read(D/'qualification-parks28-fresh.json');B=D/'qualified-parks28-fresh';freeze='95b96689cb1552f0125ea50cb9372fb08c2eb191'
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=B/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
for uid,date in [(m.O,'19'),(q['author'],'19'),('01a150d1-3383-7d30-ad23-76d70ec18813','19')]:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 live=next(c for c in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if c['id']==p['id']);assert live==p['card'] and m.sha(live)==p['sha256']
assert len(m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')['currentEligibleCompletedIds'])==884
a.apply(B,q['author'],[28],D/'apply-parks28-fresh.json',D/'qa-parks28-fresh.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER'])
