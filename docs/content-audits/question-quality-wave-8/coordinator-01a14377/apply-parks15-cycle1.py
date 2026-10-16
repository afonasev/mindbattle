"""Exact freshSOURCE15 solecycle1 apply pendingOTHERFINAL; noqualitycredit."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'source-parks15-cycle1-adopt0';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p.get('sha256',p.get('canonicalSHA256'))
same=[]
for p in ps['actualCurrentPeers']:
 if p['topicId']=='national-parks-nature':same.append({**p,'sha256':p.get('sha256',p.get('canonicalSHA256'))})
r=a.apply(B,'01a143ee-4310-7b72-bd13-773da4151e3a',[15],D/'apply-parks15-cycle1.json',D/'qa-parks15-cycle1.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':same},concerns=['SoleSOURCE15cycle1 afterINITIALFIX PARK15-INITIAL-01/02; freshSOURCE0personallyadopted fullprimary/current17peers, priorSOURCEc5post2proof inputonly notsourcevalidcredit. Candidate chosenbySOURCE, rootdoesnotauthorsemanticreplacement.', 'NewMAIN conditional uncertainty about collectingfoundnaturalobjects, keyleaveinplace/askranger. NPSL131 limitedlocations/quantities exceptions mustnotbecomeuniversallegalban. Judgefourcontextualplausibledistractors, absoluteEASY and meaning/clearonekey.', 'Correctnote limitedplaces/quantities exceptions beyondprompt/key; compareeachwholevariant ownnote forgroundedtruth/usefulness. SourceflagsecondaryNPSfooter nativevisibletruncated afterL195 noquestionclaimusesfooter; fullprimaryfirstNPS L0-endbyteexactnative.', 'Fullglobal11000with4actualMAINdeltas includingpolar12 variant; all17actualfullsame/crosspeersverified beforeapplication. Comparevisitortrash vsnaturalobject, trailtrampling/feeding/wildlifedistance andotherrelevant body; latestblocked14Kilimanjaro proposal fullbodyhistory noactualPASS.', 'Noindependentparkreaderactive; OTHER12isreadingpolaronly, no polartopicmutation bythisapply. INITIAL15FIXconsumed, thisissolecycle1 FINAL next, unresolvedFINALHOLD0/noordinarycycle2/noreset.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-parks15-cycle1.json',r);print(m.savecode([D/'qualification-parks15-cycle1.json',pathlib.Path(__file__)],'Qualify freshSOURCE15cycle1 all17actualbodies standardliteralbindings'))
