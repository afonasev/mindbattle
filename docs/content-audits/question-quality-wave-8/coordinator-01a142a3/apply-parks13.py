"""Apply exact completed SOURCE13 after consumed NP9 INITIAL; no editorial credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=C/'docs/content-audits/question-quality-wave-8/process-v2-parks6-15-fresh-01a142a3/author/remaining10-15-current839/proof-completion13';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
tp=C/'src/content/topics/national-parks-nature.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
a.apply(B,'01a142d8-32ad-7621-83d1-4865c76c51f5',[13],D/'apply-parks13.json',D/'qa-parks13.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=m.read(D/'qualification-parks13.json')['independentConcerns'])
