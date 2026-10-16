"""Apply exact qualified SOURCE10 solecycle1; qualitycredit remains zero."""
import pathlib,importlib.util,sys,json
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
B=D/'qualified-parks10-cycle1';ps=m.read(B/'peer-snapshot.json');mc=ps['sourceAuthoredMutualClosure'];assert m.raw(C/mc['originalPath'])==mc['originalRawSHA256']
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-11dc-7bc3-9892-ac7f310f7171',[10],D/'apply-parks10-cycle1.json',D/'qa-parks10-cycle1.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Sole directedSOURCE10cycle1 responding NP10-INITIAL-01, concretebison under23m conditionNPSL170-172; allnew6literal4variants mustindependentlyread. Noordinarycycle2, unresolvedFINAL HOLD0.','Current9feedingrule unchanged, fullproposed11OldFaithful bysameSOURCE separatelymutualcompared bothdirections inoriginalsource10snapshot. Do not confuse actual11Sagarmatha andUNAPPLIED11 proposal; fullbody/hash/state required.','Full312lineprimary allwildlife andspecialspecies exceptions personallyread byauthor, no snippets. Actualcondition includesbisonapproach under23m; authorselectedkey turnandwalkotherway; independentFINAL judges exactkey/note3xfaster andtaxonomy/EASY.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks10-cycle1.json',r);print(m.savecode([D/'qualification-parks10-cycle1.json',pathlib.Path(__file__)],'Qualify exactSOURCE10 solecycle1 allprimary groupvariant peerbindings'))
