"""Qualify exact original polar20-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar19-20-sol-original';B=D/'qualified-polar20-original';B.mkdir(exist_ok=True);freeze='fceb6bf9e1a3cfee453e65369e0303ffa687dd05'
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
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only existing101 full actual body/hash rows copied without semantic change. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalpolar20 FIRSTINITIAL beforeanypriorreview. ValidMAIN/labels/key3/MEDIUM/explanation retained, correctnotepasttensefalseallgoneimplication repairedpresenttense+exact easternPeninsula/Weddellborder extra beyondwholeprompt/key. ActualhistoricalA/B collapses1995/2002 distinctfromgeneraliceshelfdefinitionorregionalice-shelfrecognizers.', 'PersonallyfullNSIDC originalopen context retained EXACToldnative67 toolrecords663call/666fullpageL67-L155 article in211lines; search659explicitlyexcluded, no inheritedLuna/readerPASS. FullBASforecastRonne, AAPAmery/NASAAmery/Prydz, NASAGetzMarieByrdLand contexts eachwrongoptionnote precisegeography. JudgepresentremainingLarsen parts vs A/Bhistoricalcollapse, no allLarsengoneclaim/currentclimateprojections.', 'FourrealcomparableAntarcticiceshelves/uniqueA-Bhistory, absoluteMEDIUM thematicpolar/news geography withoutnumericmemory/specialistfractureparameter. Approvedpolar geography/nature. Full100sameMAIN/11000retrieval/101actualfullbodyhashes/16meaningfulbothdirectionERVC/directreverse inclcurrent19southernWeddelltuple/mutual19-20. Genericsharedfouralternatives do notsamefactduplicate. No cross-note collisionban.', '19stillUNFINISHEDspecificsourcegap continuation19 noSOURCEHOLDverdict yet/noquality. FailedBASPDFchallenge andDOIalternative closed no retry/bypass; no snippetsasdivision-proof. Qualify20only, sourcecritical3/fullrawpre2 required. Unapplieduntil16FIRSTFINALpolartopicfencelifts; checkpreimage/actualpeerfreshness. One directedfix thenFINAL unresolvedHOLD0/noordinarycycle2/reset.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[20],D/'apply-polar20-original.json',D/'qa-polar20-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=101,sourceOriginalFreeze=freeze);m.write(D/'qualification-polar20-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar20-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar20-original exact SOURCE fullbody bindings no quality credit'))
