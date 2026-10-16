"""Qualify exact original parks18-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks18-20-original';B=D/'qualified-parks18-original';B.mkdir(exist_ok=True);freeze='7ccbd59743a3e71cdadb8934e103602e6bff0b57'
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
concerns=['Original18 FIRSTINITIAL, no priorindependentreview. ActualoriginalKomodo giantlizardrecognizer duplicatesislands015; genuineNEW protectednature MAIN petrestraint aroundwildlife addressesactualdefect, notwordingchurn. Frozen18easykey1 alltext/labelsmutable.', 'FullNPS BigThicket+SequoiaKingsCanyon contexts personallyread/reusedexact ownsource; actualBigThicketwildlife interaction andleash6ft bound, Sequoiaeven developedareas andbothwildlife/dog danger. Judgeexactscope, notuniversalallparkslaw. Correctnote 6ft upperlimit addsfact beyondshortleash/key/prompt; allwrongvariantnotes ownfact relevanttoaction.', 'BroadadultEASY responsiblevisitor dogcontrol vs obscureKomodoidentity. Fourcredible actionmisconceptions: greeting/photo/chasing vsrestraint, unique key/noabsurdentities. Protectednature visitor-wildlife conflicttaxonomy, notgeneralcitydogtraining. Global11000/all100sameMAIN/13closestfullbodies, mutablehistoricIDs maynotdescribecurrentanimalfactlabels; verifyactualwholebodies and each bilateralERVC/directreverse inclcurrent17petwaste andgenericwildlifedistance.', '19/20samepacket remainSOURCEHOLD0 only; ROOTselect18only, no partialfixpromotesheldcards. Their missingRanthambore/absoluteEASY unresolved preserved, nevergrade-relabel. All6literal4wholevariants/primary/frozen5/percard hashes pluspre2freeze required, noSOURCE READY/QAqualitycredit. One directedfix thenFINAL unresolvedHOLD0/noordinarycycle2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[18],D/'apply-parks18-original.json',D/'qa-parks18-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks18-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks18-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks18-original exact SOURCE fullbody bindings no quality credit'))
