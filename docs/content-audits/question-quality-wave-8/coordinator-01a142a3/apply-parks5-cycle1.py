"""Apply exact SOURCE-directed one note fix after INITIAL FIX; quality0."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P;B=C/'docs/content-audits/question-quality-wave-8/process-v2-parks5-cycle1-sourceb7-01a142a3/author';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id'])and m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256'))
tp=C/'src/content/topics/national-parks-nature.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);app.apply(B,'01a142b7-50b2-7d11-8dd8-0585e2e11218',[5],D/'apply-parks5-cycle1.json',D/'qa-parks5-cycle1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[{**p,'sha256':p.get('sha256',p.get('canonicalSHA256'))}for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']})
