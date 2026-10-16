"""Qualify exact original polar16 SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar16-original';B=D/'qualified-polar16';B.mkdir(exist_ok=True);freeze='080cf41ce39b1cf8636297c46c61f26f9ed44e15'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers']+doc['relevantCrossTopicCurrentPeers'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert p['id'] not in seen;seen.add(p['id']);assert m.sha(p['card'])==p['sha256']
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers concatenates existing100 same-topic+7 full cross-topic bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Original polar16 FIRSTINITIAL, no prior independent stage. Frozen MEDIUM/key1; original Lena mouth MAIN replaced by concrete Laptev ice-production role. Nature primary calls Laptev AND Kara ice factories; Kara is not an answer alternative. Independently assess unique key among Chukchi/Laptev/Barents/Beaufort without treating quote label as exclusive global designation.', 'Correct note Lena sediment delta/7000years adds concrete extra beyond seaice MAIN; four own sea-oceanographic notes including Atlantic inflow/Beaufort Mackenzie/Chukchi Bering exactscope. Fullprimary personallyread required for each actual variant, not raw header/DOI as proof. Medium broad thematic audience, approved polar physical-ocean geography vs general climate wrapper.', 'SOURCE100 same+4cross fullactualbodies/global11000 and11closestbilateral +latest12actual13HOLD14actual comparisons; full primary Nature/NASA2/NOAA/NPI. Source15actual newlyapplied97f02 included, no ordinary15mutation whileOTHERactive. Exact frozen5 only; no cross-note collisionban. One directed fix thenFINAL unresolvedHOLD0, noordinarycycle2/reset.']
r=a.apply(B,'01a14413-e1e7-7e71-a582-eeacf3b53189',[16],D/'apply-polar16.json',D/'qa-polar16.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=104,sourceOriginalFreeze=freeze);m.write(D/'qualification-polar16.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar16.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar16 exact SOURCE fullbody bindings no quality credit'))
