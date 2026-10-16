"""Apply soleSOURCEpolar11cycle1 exactWeddell birth/mating scope repair."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'source-polar11-20/polar11-cycle1';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-0dc6-7740-9baf-4bc1f33f27ba',[11],D/'apply-polar11-cycle1.json',D/'qa-polar11-cycle1.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['SoleSOURCE11cycle1, onlynote2changes. AAPWeddellfullbody distinguishes rest/moult+femalesgivingbirth onfastice frommatingunderwater, exactnewnote2scope. IndependentFINAL mustexplicitlyresolvePOL11-INITIAL-01, noreset/noordinarycycle2.','All6canonicalgroups/fourFullPromptAnswerNoteAssessments arecurrentrequiredcontract; sourcelegacywholePromptAnswerNoteAssessments retainedhistory notauthoritativeupdatedliteral. Applyreceipt bindsactualnewnote2/triples, no rootsemanticwording.','OwnsameSOURCE+sameOTHER fullunchangedFWS/AAPprimaryreads mayreuseexplicitapplicability, all6literal4wholevariants/absoluteEASY/owncorrectnoteextra/taxonomy/globalMAIN/fullactualclosestpeers/bothwaysERVC/directreverse remainrequired. No supplementaryheader/error/searchoutput asproof.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-polar11-cycle1.json',r);print(m.savecode([D/'qualification-polar11-cycle1.json',D/'sourcefreeze-polar11-cycle1.json',pathlib.Path(__file__)],'Qualify soleSOURCEpolar11cycle1 exactnote2 scope fullcanonicalbindings'))
