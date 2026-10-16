"""Apply exactSOURCE11 solecycle1 fullnotes repair; creditzero untilFINAL."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks11-cycle1';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-11dc-7bc3-9892-ac7f310f7171',[11],D/'apply-parks11-cycle1.json',D/'qa-parks11-cycle1.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['SoleSOURCE11cycle1 repairing NP11-INITIAL-01/02 onlynotes0/1/affectedvariants, full6literal4variants independentFINAL required. Banff note limitsalreadyprovedlakes; Torresnote landformshaped byglaciers notcreationofgranite.','NewUNAPPLIED12correctedsourceproposal separatelyfullread/bindstates/bothwaysERVC/directreverse alongsideactual9/10/1/37 andgenericgeysercrosspeers, no sourcePASSinheritance.','Frozen11/easy/key2 andMAIN unchanged; ownnotefact60percent geysers unchanged mayoverlapcurrent1note. Exactfullprimary NPS/ParksCanada/CONAF/Swissretained, ownreaderunchangedfullreads reuseexplicitapplicability allowed. Noordinarycycle2 unresolvedFINALHOLD0.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks11-cycle1.json',r);print(m.savecode([D/'qualification-parks11-cycle1.json',pathlib.Path(__file__)],'Qualify exactSOURCE11 solecycle1 fullprimary notesrepair'))
