"""Qualify exact original polar27-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar27-40-original';B=D/'qualified-polar27-original';B.mkdir(exist_ok=True);freeze='689b6c6826021eb1d999ebf7b9366dc513b7821e'
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
concerns=['Originalpolar27 FIRSTINITIAL firstREADYportionoforiginalunit27-40, no priorreview. MAIN/labels/EASYkey0/explanationretained, correctnotepreviouslyrepeatfloating-margin MAIN replacedspecificseawardcalvingicebergs process/product beyondWHOLEprompt/key. SourceURL/title exactNSIDCScienceIceShelves, no othertextchurn. Otherunit28-40NOT_REVIEWED notfakeHOLD/noquality.', 'Full4scientificprimarycontexts NSIDCScienceShelves192, GlacierScienceactual0-301inclcompletearticle/resources65-261 notall318footerpage, ScienceSeaIcecomplete541threewindowcomposite afterSOURCE25correction, originalLarsenOPEN666fullarticle67-155 personallyread/source-owncontinuity/exact27claimapplicability. Shelf68/Glacier195land-fedfloatingmargin commoncase andLarsen72attachedslab grounds MAIN/explanation, notuniversalall-shelveslandprovenance. Larsen123seaice-originexceptions respected. Shelf75/87seawardcalvingdirectowncorrectnote; icebergcalving/drifting/glacierlandflow/seaicefreezing exactwrongnotes.', 'All6literal4wholevariants/4credibleiceforms/unique/grammar/polarphysicaltaxonomy, independentlyjudgeabsoluteEASY basicadultphysical connectedmargin/detachedmass/landflow/oceandirectfreeze distinctions one-step, notHARDyoungicewording. Concretekeynote calvingextra allowedoverlapwithothericebergMAIN/notes no crossnoteban/templatealoneban. Fullglobal11000/same100/allactualwholeclosestbodyhashes/genuineproposals/bothdirectionsERVC/directreverse, genericseaice26vsicyshelf27morphology separatedefinitions/entitiesrelations, namedRonne/Amery/Getzgeographicfacts notgenericclass.', 'Actual26now55ca fixedexplanation underFIRSTFINAL atsourcepacket butthenindependentlycert869, actual25fullsource066ccert868, no neighboringqualityinheritedto27. Allsourceactualpeerbodies verifiedfreshwholelive beforequalification, oneREADY27onlysourceunit14 firstportion; source7factual1/raw689pre2critical3/testedtopicQA19/independentFIRSTINITIAL/root<2/preleasedCAS required. One directedSOURCEfixafterINITIALthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[27],D/'apply-polar27-original.json',D/'qa-polar27-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar27-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar27-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar27-original exact SOURCE fullbody bindings no quality credit'))
