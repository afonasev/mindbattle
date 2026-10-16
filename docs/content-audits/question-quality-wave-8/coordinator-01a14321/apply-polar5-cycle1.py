"""Apply exact singleSOURCEcycle1 polar5 independent MAIN, no quality credit."""
import pathlib,importlib.util,subprocess,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-polar5-cycle1';ps=m.read(B/'peer-snapshot.json');e=m.read(B/'candidate.json')['entries'][0]
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
six=m.read(D.parent/'process-v2-polar5-6-8-10-fresh-01a14321/author/remaining6-8-10-current841/candidate.json')['entries'][0]['proposedCard']
for p in ps['cycle1RelevantPairs']:
 assert p['candidate']['card']==e['proposedCard'] and p['candidate']['sha256']==m.sha(e['proposedCard']);assert p['candidateToPeer'] and p['peerToCandidate']
 if p['peer'].get('status','').startswith('READY'):assert p['peer']['card']==six and p['peer']['sha256']==m.sha(six)
 else:assert p['peer']['card']==next(q for q in m.read(C/'src/content/topics/polar-regions.json')['questions'] if q['id']==p['peer']['id'])
tp=C/'src/content/topics/polar-regions.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
r=a.apply(B,'01a14327-fb48-70e1-8d55-3db044c2d83b',[5],D/'apply-polar5-cycle1.json',D/'qa-polar5-cycle1.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=['Polar5 soleSOURCEcycle1 afterINITIALFIX: genuinelynewMAIN nowNorthPole continuous-nightduration, not90Nendpoint. Fullactual6 andunapplied6 proposal bothcomparedwithnew5 in SOURCEcycle1RelevantPairs. IndependentFINAL must personally assess globalMAIN and fullclosestpolar-night/day facts, no automaticdistinct fromchangedtopiclabel.','All4timevalues require actualEASY/plausiblequantities/ownnotes; correctnotecontinuousdayaddsownfact; monthnote nowfullUSNOsynodicmonthdefinition/29.5days, notgenericwrongmonth+repeatcorrectanswer. FulloriginalUSNO SOURCEwebopen mechanicallypreserved, no SOURCE/rootverdictinherited.','Directuser-facingNOAAPMELsourceURLmustsubstantiatenewnightduration MAIN; all6literal4wholevariants/fullprimary/realpeers required. UnresolvedFINAL HOLD0, no unchangedsecondcycle.'])
if '--qualify-only' in sys.argv:
 p=D/'qualification-polar5-cycle1.json';m.write(p,{'owner':m.O,'qualified':True,'qualityCredit':0,'sourceFreeze':'be02a8c094d903f68bac3a333062039e308ee7c4','groups':len(r['finalGroupBindings']),'wholeVariants':len(r['finalVariantBindings']),'fullActualPeers':len(ps['actualCurrentPeers']),'fullMutualActualAndProposed6Bound':True});print(m.savecode([p,pathlib.Path(__file__)],'Qualify polar5 newMAIN solecycle1 exactgroups/variants/fullmutual6'))
