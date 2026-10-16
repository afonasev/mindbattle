"""Qualify exact original polar16-17-fresh SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar16-17-fresh';B=D/'qualified-polar16-17-fresh';B.mkdir(exist_ok=True);freeze='d5b5d28e68779dc60958b3a2207ad365cc2896ad'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers']+doc['relevantCrossTopicCurrentPeers']+doc['globalMAINRetrieval']['rows'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert m.sha(p['card'])==p['sha256']
   if p['id'] in seen:
    assert next(x for x in combined if x['id']==p['id'])['card']==p['card'];continue
   seen.add(p['id'])
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers unions existing100 same-topic,3 cross-topic and53 full global hit bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Two ORIGINAL16/17 FIRSTINITIAL before any previous independent review. FreshSOURCE67 personalproof rawd5b5pre2. Original16 unnecessaryicefactories rewrite rejected/unapplied; valid Lena→Laptev originalMAIN andlabels retained, correctnote unsupportediceclause replaced by NASA annualfreshwater/sedimentnumbers. Original17 post2input personallyadopted, wrongoldactorID notused.', 'All5retained full primary NASA2/NOAA/NPI/Canada personallyread; incompleteNature672vsL191 explicitlyexcluded andnotclaimproof. NASA precise annualvolume/tonnage, Lena deltawidth/extents, Canada riveroutletmap+NOAA3input currents, Chukchi shallowshelf and organicoutflow actualscope must independentlyverify. No current literals rely on Nature or rejected16icefactories.', 'FrozenMEDIUM both, keys1/2, fourcredible Arcticseas percard. Distinctriver/receivingsea facts may share river-mouth question form; not structuralduplicate. Global11000/all100sameMAIN, existing53fullhits+3cross actualbodyhashes and meaningful selected16↔17, same/cross and rejectedproposal comparisons remain separate. Assess allrelevant wholebodies/ERVC/directreverse, especially Khatanga→Laptev and GreatSlave→Mackenzie do not collapse differentrelations.', 'Correctnotes add actualownfacts beyondwholeprompt/key. Source16 quantitativeannualdischarge;17 otheroceanographic inputs, notrepeatmouthonly. No new cross-note collisionban. Root onlylosslessfullbody/hashaliases fromexistingrows, noSOURCEjudgmentsinvented. One directedfix thenFINAL unresolvedHOLD0/noordinarycycle2/reset.']
r=a.apply(B,'01a14467-a471-7310-9ecb-dd4da5dde095',[16,17],D/'apply-polar16-17-fresh.json',D/'qa-polar16-17-fresh.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar16-17-fresh.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar16-17-fresh.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar16-17-fresh exact SOURCE fullbody bindings no quality credit'))
