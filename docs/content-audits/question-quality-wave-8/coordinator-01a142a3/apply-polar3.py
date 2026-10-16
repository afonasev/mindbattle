"""Apply SOURCE3 after strictbound polar2 FINAL840, disjoint OTHER9 underway; targeted data QA pending."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-polar3-sourced0';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
tp=C/'src/content/topics/polar-regions.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
a.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[3],D/'apply-polar3.json',D/'qa-polar3.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=['SOURCE3 genuine new icecover predicate replaces largestisland question after SOURCE-HOLD0 prior globalduplicate; canonical independentINITIAL not yet run. FrozenEASY/key0/ID/order unchanged.','islands-001 also keysGreenland on largestisland MAIN. Independent actual full semantic comparison must distinguish predicate/context or flagFIX; sharedanswer not automaticduplicate or automaticdistinct. Absolute broadadultEASY and full four alternatives/ownnote require personal primaryground.'])
