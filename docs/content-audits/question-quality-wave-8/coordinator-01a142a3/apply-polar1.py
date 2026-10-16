"""Apply qualified exact SOURCE polar1; credit0, pending independent INITIAL."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-polar1-source62';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
tp=C/'src/content/topics/polar-regions.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);a.apply(B,'01a14262-85b3-7bd3-be22-0c76b96bbc5a',[1],D/'apply-polar1.json',D/'qa-polar1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='polar-regions']})
