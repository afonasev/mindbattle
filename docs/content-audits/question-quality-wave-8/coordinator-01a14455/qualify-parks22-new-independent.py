"""Qualify exact original parks22-new-independent SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks22-new-independent';B=D/'qualified-parks22-new-independent';B.mkdir(exist_ok=True);freeze='d520e13dcde8fcf6746462dcee6a04beaf126d24'
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
concerns=['GenuineNEWparks22 FIRSTINITIAL aftergroundedoriginalSOURCEHOLD panoramamajority/eastbankunproven/namecountrygiveaway retainedhistory, no priorINITIAL/noreset. FrozenEASY/key1/id/topic/order allMAIN/entities/labels/textmutable actualdefectauthorized newindependentprotectedislandbiosecurity fact. Notanotherrareparkrecognizer. NPSChannelIslandsbootbrushsign beforeboat and NPSBootBrushingarticle full70/106linepages exactactualcoverage rootrecomputed, noheader/partialcontext fakefullpage.', 'MAINgivenknownsolemud/seeds preventingnewislandplantintroductions: cleanbootswithbrushBEFOREboarding unique amongafterarrival/upperonly/cleanwornpairbutdirtybootstransported. FullNPSsignL28-L34directboots/clothes/gearremove soilseeds+beforeboardingprevention; generalNPSarticleL23-L36/L59-L66seedtransportdropwhilewalking. No allnonnativeplantsinvasive/guaranteedseedgermination/invasivedollarstatclaim. CorrectnoteMANYparksbrushstations fortrailENTRYandEXIT exactNPSL36 additionalconcreteinfrastructure/twoboundaries beyondwholeprompt/keybeforeboatbrushaction.', 'All6literal4wholevariants/credible4incompletecleaningandtransportmisconceptions/unique/grammar/taxonomyprotectedislandvisitorbiosecurity, broadadultEASY causalreasoninggivenmudseedsnotrarepark/species/interval. Wrongoptionnotes specificremainingvector/timing/allgear facts beyondstubfalse claim. Fullglobal11000/same100/fullclosestactualwholebodyhashes/genuineproposals+mutual22vs21/23/24 andall9food10bison14fire15find17waste18dog19campfire20nestactionrelations bothdirectionsERVC/directreverse, no genericvisitorformatban/no crossnoteban.', 'Only22 applyafteractualbefore227verified; SOURCE24gradeHOLD andalloriginal22HOLDproofretainednotacceptedby22. SOURCE3aactual1/rawd520pre2critical3, root<2/exactQA19/independentFIRSTINITIAL/preleasedCAS beforecredit. Independentreaderpolar25active: confirm22NOTinitsfullactualpeerDependencies ORqueued26SOURCEsnapshot beforecross-topicapply; no CURRENTpeerdrift. One directedSOURCEfixthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[22],D/'apply-parks22-new-independent.json',D/'qa-parks22-new-independent.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks22-new-independent.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks22-new-independent.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks22-new-independent exact SOURCE fullbody bindings no quality credit'))
