"""Qualify exact original polar26-cycle1 SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar26-cycle1';B=D/'qualified-polar26-cycle1';B.mkdir(exist_ok=True);freeze='cfcd63f4a1b7e33f532737bb14a6552c578524c9'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert p['id'] not in seen;seen.add(p['id']);assert m.sha(p['card'])==p['sha256']
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only existing full actual body/hash rows copied without semantic change. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Solepolar26 directedSOURCEcycle1 afterFIRSTINITIALFIX4ac4/consume931b EXPLANATION_OVERBROAD_ORIGIN_CONTRAST. Onlyexplanation changed cf49→55ca, MAIN/all4labels/EASYkey0/allnotesretained. Distinguishimmediatesurfacewaterfreezing vsicebergcalving/detachment notcategoricalunderlyingmateriallandorigins. ExplicitlyrespectLarsenL123someseaice-onlyshelvesandShelfSciencecalving, no new namedcasefabricated.', 'All6literal/4wholevariants personallyregroundedfull4retainedNSIDCQuickFacts/glacier/shelves/LarsenoriginalOPEN666 context actualcycle1applicability. Ownkeynoteusualsolarreflectionextra unchangedbeyondWHOLEprompt/key; ordinaryshelfextensionnotequalifierusuallyretained, allwrongnotesexplicitownoptiongrounds. Explanationnotnewgenericcontrastcounterexamplegap, exactsource mechanism directfreezevsdetachment.', 'FrozenEASY basicadulticecategories/credible4/unique/grammar/polarphysicaltaxonomy, global11000/same100/allactualwholepeers/genuineproposals/bothdirectionERVC/directreverse. Source25nowactual066c peer freshSOURCEwholebodyhash vsoldbefore25 required/verified; not25qualityacceptance. Whole25/26MAINspecificinitialfrazilcrystal vsgenericgeneticseaice distinct, oceanphaseprocessvsgeneticmaterial terminology independent.', 'Apply26cycle1ONLYAFTER25FIRSTINITIALconsumed topreserve25readeractual26cf49body. Current25needsSOURCEfullcontextcompletion visibleNSIDCSciencewindow227/541 beforeanyINITIAL; thisdoesnotblockqualification26 usesother4fullcontexts butno26applytoforcereader25sourcepeerdrift. NeedactualaffectedQA19after26cardexplanationchange andindependentFIRSTFINAL26 sameonecycle. UnresolvedFINALHOLD0/noordinary2/reset, INITIALhistoryretained/currentcredit0untilcert. SOURCErawcfcdcritical3pre2/native0, readernative1/root<2/preleasedCAS mandatory.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[26],D/'apply-polar26-cycle1.json',D/'qa-polar26-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar26-cycle1.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar26-cycle1.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar26-cycle1 exact SOURCE fullbody bindings no quality credit'))
