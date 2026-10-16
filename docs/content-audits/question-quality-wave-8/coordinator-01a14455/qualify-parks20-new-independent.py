"""Qualify exact original parks20-new-independent SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks20-new-independent';B=D/'qualified-parks20-new-independent';B.mkdir(exist_ok=True);freeze='49651e5e8dc6ac440ba9633d14903196d7b91b9a'
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
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers unions existing100 same-topic and13 full relevant global hit bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['GenuineNEWparks20 FIRSTINITIAL afteroriginalSOURCEHOLD20 rareChitwan/EASY/sourceissues retained. FrozenEASY/key3/id/topic/order, actualdefectjustifies newindependentMAIN protectedshorebirdnestingaccessrule. No priorINITIAL/no ordinarycycle reset. Allold19/20SOURCEHOLD immutable.', 'FullNPSCapeLookout WildlifeProtectionZones128lines personallyread notselectedquotes. Sourceexplicitlydistinguishesvehicleonly/turtlepedestrianaccess, somebirdtideline/no-stopping areas, andsignall-entryban. Promptspecificallyall-entryclosednestingbirdarea signhypotheticalRussiantranslation notliteralphototext. Onlyrouteoutsideclosedarea valid; quiet/unseen-nest/quickcrossing stillenters forbiddenzone. No blanketpedestrianbanallprotectionzones ordatedseasonrule.', 'Correctnote threatenedchicksfreeze/blendwithsand concreteextra protectivebehaviourfact beyondwholeprompt/keyroutechoice perL40. All6literal/4wholevariant sourcegrounds, exactsourceprivacy/rawfullcapture, actualkey3/grammar/4crediblebehaviourmisconceptions. AbsoluteEASY broadadult obeysignedclosednestingarea no obscureplacerecognition/species/dates/bufferknowledge. Protectednatureaccessmanagementtaxonomy notgeneralurbanecology.', 'Global11000/same100/fullclosestactualbodies andallgenuineproposals/historical19/20wholebodyhashes, mutualactual19campfire distinct20nestaccess, parks9food10bison15foundobjects17waste18dogcontrol14plannedfire semanticrelations distinct. BothdirectionsERVC/directreverse, commonNPSvisitorformat notduplicate/no crossnoteban. Source3aactual1/pre2raw49651critical3 mandatory; independentINITIAL andQA19 beforecredit, one directedSOURCEfixthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[20],D/'apply-parks20-new-independent.json',D/'qa-parks20-new-independent.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks20-new-independent.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks20-new-independent.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks20-new-independent exact SOURCE fullbody bindings no quality credit'))
