"""Apply original12 onlyafter11FINALconsumed; existingauthormutual fullpeerdelta."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks12-source-corrected';ps=m.read(B/'peer-snapshot.json');delta=m.read(D/'peer-delta-parks12-current848.json');dp={e['id']:e for e in delta['actualCurrentPeers']};mc=delta['sourceAuthoredMutualClosure'];assert m.raw(C/mc['originalPath'])==mc['originalRawSHA256']
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicPeers']:
 p=dp.get(p['id'],p);q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
if '--qualify-only' not in sys.argv:
 f=m.read(D/'parks11-final-consumed.json');assert f['consumed'] and f['current11CanonicalSHA256']==m.sha(m.read(C/'src/content/topics/national-parks-nature.json')['questions'][10])
r=a.apply(B,'01a14381-11dc-7bc3-9892-ac7f310f7171',[12],D/'apply-parks12.json',D/'qa-parks12.json',pathlib.Path(__file__),peerAddendum=D/'peer-delta-parks12-current848.json',qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Original12 firstINITIAL, SOURCEprequalification repairedsameBanff/CONAFscopeissuesbeforeanyapply; noindependent12fixcycle usedyet. Full6literal4wholevariants andallprimary fullcontexts personallyjudge.','Serengeti migrationMAIN vslandmarks-wonders-serengeti-tanzania area/habitatMAIN mustfullbothwaysERVC/directreverse; sharedpropername/relatednotes alone neitherduplicate nor distinctproof. Correctownnote1.5millionhectares addsbeyondmigrationMAIN evenifelsewherekey.','Fullactual11correctedOldFaithful/10bison/9feedingrules/closestotheractualpeers, exactfullstate/hash. SOURCEmutual11/12proofexists, independentreaderno inheritance. AbsoluteEASYand4parksplausibility independentlyjudge.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks12-current848.json',r);print(m.savecode([D/'qualification-parks12-current848.json',D/'sourcefreeze-parks12-current848.json',pathlib.Path(__file__)],'Qualify originalSOURCE12 correctednotes exactcurrent11 peerbinding noapply'))
