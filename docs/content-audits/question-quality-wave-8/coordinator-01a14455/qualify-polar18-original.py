"""Qualify exact original polar18-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar18-20-sol-fresh';B=D/'qualified-polar18-original';B.mkdir(exist_ok=True);freeze='d49845c3edbde22844d0d113865f324e9b1c4790'
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
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only existing108 full actual body/hash rows copied without semantic change. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalpolar18 FIRSTINITIAL beforeanypriorindependent. Sol7ffullpersonal SOURCE firstready18 only; previousLuna18-20scaffoldNotReviewed inputnotproof/HOLDdecision. 19/20stillunreviewed notpromoted. Frozen18MEDIUMkey2 andvalidcurrentMAIN/labels retained, genuineactualsource/note defects repairedonly.', 'NewcompleteNOAAPMEL official fullpage explicitlynorthBeringStrait/easternChukchi Pacificwater heat/nutrients input; oldcomparativelywarm unboundclaimreplacedgroundedtransport. Correctnote independentChukchi shelfdepthpredominantly<50m fromfullNOAAAFSC beyondwholeprompt/key. WrongLaptevnoteverifiedLena only, unsupportedicefactoryclauseexcluded; BeaufortverifiedMackenzie only, unboundAlaskaCanadadirectionalclauseomitted withoutfalsehoodclaim. FullNASA2/NOAAAFSC+newPMEL contexts exactscope.', 'FourcrediblecomparableArcticseas/key2unique, absoluteMEDIUM thematicmapknowledge not numericdepthretrieval. Approvedpolarphysicalgeography. Full100sameMAIN/global11000 retrieval28hits and108fullactualbody/hash aliases, 12meaningfulbilateralMAIN/ERVC/directreverse; current16Lenaand17Mackenzie actualwholebodies separately bound, globalBeringStraitconnection-question vs northadjacentsea semanticjudge. No cross-note collisionban.', 'Roottechnicalschema/fullbody/hashbindings only, no SOURCE/readerjudgments invented. QualifiedUNAPPLIED untilsame-topic16/17INITIAL fullyconsumed; sourcepeerpreimagesfreshnessmustrefreshif17cyclefixlater. One directedfix thenFINAL unresolvedHOLD0/noordinarycycle2/reset; pre2critical3/rawfreeze/exacttestedtopicQA19 required beforequalitycredit.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[18],D/'apply-polar18-original.json',D/'qa-polar18-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=108,sourceOriginalFreeze=freeze);m.write(D/'qualification-polar18-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar18-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar18-original exact SOURCE fullbody bindings no quality credit'))
