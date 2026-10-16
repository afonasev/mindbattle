"""Apply originalSOURCE11 aftersole10FINAL consumed; existingauthoredmutualpeer delta."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks11';ps=m.read(B/'peer-snapshot.json');delta=m.read(D/'peer-delta-parks11-current846.json');dp={e['id']:e for e in delta['actualCurrentPeers']};f=m.read(D/'parks10-final-consumed.json');assert f['consumed'] and f['current10CanonicalSHA256']==m.sha(m.read(C/'src/content/topics/national-parks-nature.json')['questions'][9])
mc=ps['sourceAuthoredMutualClosure'];assert m.raw(C/mc['originalPath'])==mc['originalRawSHA256']
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicPeers']:
 p=dp.get(p['id'],p);q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-11dc-7bc3-9892-ac7f310f7171',[11],D/'apply-parks11.json',D/'qa-parks11.json',pathlib.Path(__file__),peerAddendum=D/'peer-delta-parks11-current846.json',qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Original11 firstINITIAL, SOURCE replacedrareportgeography byOldFaithfulparklandmark toseekabsoluteEASY. Reader mustpersonallyjudge broadadultEASY/actual4parksplausibility; knownparkentity notautomaticallyeasy.','FullNPSOldFaithful/ParksCanadaBanff/CONAFChile/SwissNationalPark completeprimary for EVERYliteral/note notsourcePASS. Owncorrectnote60percent geysers concretebeyondlocationMAIN, overlapcurrent1ownnote permitted.','Fullactual10bison under23m FINALcert846 vs11landmark distinctrelations alreadybothdirectionSOURCEauthoredmutual; readerpersonallyjudge bothactuals. CURRENT1firstpark and37GrandTeton plusgenericgeyser peers needfullMAINbothways/directreverse, parknamewrapperalone neverproof.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks11.json',r);print(m.savecode([D/'qualification-parks11.json',D/'sourcefreeze-parks11.json',pathlib.Path(__file__)],'Qualify exactSOURCE11 firstINITIAL fullprimary/groupvariant/currentpeers'))
