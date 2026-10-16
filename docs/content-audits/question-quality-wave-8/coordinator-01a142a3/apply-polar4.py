"""Apply SOURCE4 after consumed polar2 INITIAL; targeted data QA pending."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-polar4-sourced0';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
tp=C/'src/content/topics/polar-regions.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
a.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[4],D/'apply-polar4.json',D/'qa-polar4.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=['SOURCE flagged close polar2 pair. Independent exact full MAIN bilateral/direct reverse judgment required; inherited label is not evidence.','Polar2 INITIAL sourceURL/title FIX remains unapplied; exact MAIN and all text unchanged. Reader must bind actual full peer bytes.'])
