"""Exact SOURCE phaseB parks9 data-only application; credit0."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=C/'docs/content-audits/question-quality-wave-8/process-v2-parks6-15-fresh-01a142a3/author/next9-15-resumed';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
tp=C/'src/content/topics/national-parks-nature.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);kw={'peerSnapshot':{'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},'concerns':['Frozen EASY requires absolute broad adult audience justification; source calls LakeLouise tourist association broad general geography. Independently assess complete question and alternatives, no onehop==EASY shortcut.','SourceURL exact park overview vs precise LakeLouise supportingpage; both original fullbodies retained; personally check directMAIN support.']}
r=a.apply(B,'01a142d8-32ad-7621-83d1-4865c76c51f5',[9],D/'apply-parks9.json',D/'qa-parks9.json',pathlib.Path(__file__),qualifyOnly=True,**kw)
m.write(D/'qualification-parks9.json',{'qualifiedStructure':True,'literalGroups':len(r['finalGroupBindings']),'wholeVariants':len(r['finalVariantBindings']),'sourceFreeze':'c1a3ce5fa9da03eef181ab19ef00f97cc711510e','credit':0})
a.apply(B,'01a142d8-32ad-7621-83d1-4865c76c51f5',[9],D/'apply-parks9.json',D/'qa-parks9.json',pathlib.Path(__file__),**kw)
