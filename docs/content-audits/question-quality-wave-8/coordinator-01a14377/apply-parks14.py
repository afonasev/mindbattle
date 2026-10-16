"""Apply originalparks14 exactqualifiedSOURCE fullMAIN/primary proof."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks14';ps=m.read(B/'peer-snapshot.json');seen={}
for p in ps['actualCurrentPeers']+ps['fullRelevantHits']+ps['closestPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p.get('sha256',p.get('canonicalSHA256'));seen[p['id']]=p
r=a.apply(B,'01a14381-11dc-7bc3-9892-ac7f310f7171',[14],D/'apply-parks14.json',D/'qa-parks14.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Original14 firstINITIAL. SourceinitialHOLD incompleteglobal/relevantMAIN retained; newcompleteproof contains fullactual11000prompt-key retrieval andpersonallyassessed fullrelevanthits/closestpeerbothways, notglobalcountasqualitycredit.','Kakadu NorthernTerritory rockart+wetlands conjunction MAIN mustjudge exacttaxonomy/absoluteEASY/4realparkplausibility. SourcefameorUNESCOlisting alone notEASYproof. Owncorrectnote continuous40kyearsettlement additionalbeyondrockart/wetlands MAIN.','All6literal4wholevariants fullUNESCOKakadu/Uluru/GBR+DOCFiordlandprimary personalread, exactclause/number/landformscope notinheritedsourcePASS. FullactualcrossUluru/GBR/otherwetlands andactual11/12/13/15 fullbodies/hashes/bothwaysERVC/directreverse includinglatestretainedproposalstatus vsactuals.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks14.json',r);print(m.savecode([D/'qualification-parks14.json',pathlib.Path(__file__)],'Qualify originalSOURCE14 fullprimary6literal4variants/fullactualMAINpeers'))
