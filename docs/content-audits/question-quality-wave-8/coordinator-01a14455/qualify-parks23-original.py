"""Qualify exact original parks23-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks23-24-original';B=D/'qualified-parks23-original';B.mkdir(exist_ok=True);freeze='0017e446282190f2add0d671864f354ce79e49ac'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers']+doc['fullRelevantHits'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert m.sha(p['card'])==p['sha256']
   if p['id'] in seen:
    assert next(x for x in combined if x['id']==p['id'])['card']==p['card'];continue
   seen.add(p['id'])
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers unions existing full actual same-topic and relevant global hit bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalparks23 FIRSTINITIAL, no priorreview. MAIN/all4labels/EASYkey2 retained. FullofficialPlitviceAmazingFacts page supportschangingturquoisechain notalwaysallturquoise; UNESCO98fullOUV/integrity supportsCroatia/cascadinglakes/travertinebarrierdepositionandongoinggrowth/erosion. Correctnotevalidtravertinefactsretainedextra beyondWHOLEprompt/keyturquoiselakes; explanationonlyrusla→lakes directsourcegrowth/erosionlakechanges, no broadunboundriverclaim.', 'All6literal/4wholevariants exactcachedUNESCO303/355/98/1604plusnewfullparkownedAmazingFactspage primary, source23ownsame-nativepersonalrereadactualclaimapplicability not21PASSinheritance. WrongIguazunotesunsupportedwest/eastbank replacedsharedforest/Paranaadjacency, Icelandnoteonlyunestablishedlargestrankremoved namesakeicecap/subglacialactivevolcanoespreciselygrounded. Preservegoodlabels/othertext nottemplatechurn.', 'IndependentlyjudgeabsoluteEASY broadCroatianANDneighboringBalkan largeculturalaudience iconicPlitvicebasicgeography, notnichetravertinechemistry/date. Fourrealprotectedwaterlandscapes crediblecomparables/uniqueCroatiacondition/grammar/taxonomy, promptdoesnotgivePlitvicename. Fullglobal11000/same100/allclosestwholeactualbodyhashes/genuineproposals+mutual23/24 andcurrent21DevilsThroat/held22panoramagiveaway, meaningfulbothdirectionsERVC/directreverse vswaterfall/river/geologyfacts; sharedtemplate/notes notautomaticMAINdup/no crossnoteban.', 'ROOTqualifies/applies23ONLY: originalsource24READYraw retained butabsoluteEASYbasisIcelandalone smallculturalgroup unresolved; source24preINITIALgradecompletionactivelyassigned, no24acceptance/relabel/contentrewrite/creditfrom23. Reader23compare24actualoldbody AND fullgenuine24proposalwhenrelevantbothdirections butdo notreview/accept24. Original22SOURCEHOLD retained. Source3aactual1/raw0017pre2critical3, testedtopicQA19/independentINITIAL/root<2/preleaseCAS required. One directedSOURCEfixthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[23],D/'apply-parks23-original.json',D/'qa-parks23-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks23-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks23-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks23-original exact SOURCE fullbody bindings no quality credit'))
