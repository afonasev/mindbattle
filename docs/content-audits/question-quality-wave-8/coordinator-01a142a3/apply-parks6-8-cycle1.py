"""Apply qualified same single grade-fix cycle to three Nature questions; credit0 until FINAL."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
B=D/'qualified-parks6-8-cycle1-sourced8';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions']if q['id']==p['id']);assert p['card']==q and m.sha(q)==p['sha256']
for pair in ps['relevantProposedPairs']:
 assert pair['leftToRight']and pair['rightToLeft']
 for side in ['left','right']:assert m.sha(pair[side]['card'])==pair[side]['sha256']
tp=C/'src/content/topics/national-parks-nature.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
app.apply(B,'01a142d8-32ad-7621-83d1-4865c76c51f5',[6,7,8],D/'apply-parks6-8-cycle1.json',D/'qa-parks6-8-cycle1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']})
