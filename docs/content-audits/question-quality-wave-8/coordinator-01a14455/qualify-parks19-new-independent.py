"""Qualify exact original parks19-new-independent SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks19-20-new-independent';B=D/'qualified-parks19-new-independent';B.mkdir(exist_ok=True);freeze='26a438d517a15e465fb4c32f3559ae6a971d7672'
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
concerns=['GenuineNEW parks19 FIRSTINITIAL after originalSOURCEHOLD19 source/EASY defects, no priorINITIAL. FrozenEASY/key2/id/topic/order alltextmutable. Real park-specific BigThicket campfire management: permittedfirepit conditional notuniversalpermission, wateravailable exactcondition. Existing19rareparkfortress taxonomy/EASYsource defects justify newMAIN, no hiddengradechange.', 'Full originalNPS CampfireSafety86visiblelines personallyread L23-L34 exactwater/drownALLcoals/sticks/stir/morewater/untilcooltotouch; donotbury coalscan smolder/reignite. Correctnote no-water backup MIXsoil/sandUNTILcool is distinctfromincorrectburyandleave, concreteadditionalownoptionfact beyond wholeprompt/keywateravailable. All6actualgroups/4fullvariants individuallygrounded, comparableprocedures notabsurdentities.', 'AbsoluteEASY broadadultcampfirecompetence notknowingBigThicketrarelabel. Protectednature reservatevisitor/firepreventionrule taxonomy, noturban/generalecology. Global11000/all100sameMAIN/full15cross/relevantpeers inclheldparks14plannedburningdifferentrelation, parks17/18petwaste/dogcontrol, oxygencombustion, archaeologyhearth/soot/charred, reactorECCS,metalquenching. Wholebodyhashes andmeaningfulbilateralERVC/directreverse plus17/18current/historical19/20proposals, no sourcePASSinheritance/no crossnoteban.', '20newsolution NOTREVIEWED stayszero originalHOLDretained; qualify/apply19only. Otheractualpolar20siblingnewnote notamongrelevantpol1/2peers, allactualpeerfreshhashesverified. Source3aactual1/pre2raw26a438+critical3 required. One directedSOURCEfix afterINITIAL thenFINAL unresolvedHOLD0/noordinarycycle2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[19],D/'apply-parks19-new-independent.json',D/'qa-parks19-new-independent.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks19-new-independent.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks19-new-independent.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks19-new-independent exact SOURCE fullbody bindings no quality credit'))
