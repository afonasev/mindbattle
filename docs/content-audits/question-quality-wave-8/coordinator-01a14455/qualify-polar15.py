"""Qualify exact original polar15 SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=OLD/'source-polar15-original';B=D/'qualified-polar15';B.mkdir(exist_ok=True);freeze='c48bd692884f0490bf42e6a0b5dbf4468c4a74d8'
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
concerns=['Original polar15 FIRSTINITIAL, no prior independent stage. Largest species rank NPS explicit; brown/Kodiak ranges overlap and sex/season caveats: cannot infer every polar outranks every Kodiak or a computed global average. Reader independently judge unique key/scope, not authority wording alone.', 'Owncorrectnote swimming adaptation beyond size rank; all4notes concrete own bear facts. Source gives native SouthAmerica for spectacled; independent reader assess Russian habitat scope. Broad adult absoluteEASY, polar taxonomy vs generic superlative wrapper.', 'Source retained six complete primary contexts including full FWS10page personal reread; primary byte/header check is only inspectability. All6literal4wholevariant/actual107 fullbodies/global11000MAIN with8 directcross and latest12actual13HOLD14actual bothways independently judge. No cross-note collision ban.', 'Native SOURCE1 freeze critical3+rawsources pre2 required; no SOURCE READY or QA credit. One directed fix after INITIAL then FINAL HOLD0 unresolved, no ordinarycycle2/reset.']
r=a.apply(B,'01a14413-e1e7-7e71-a582-eeacf3b53189',[15],D/'apply-polar15.json',D/'qa-polar15.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=107,sourceOriginalFreeze=freeze);m.write(D/'qualification-polar15.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar15.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar15 exact SOURCE fullbody bindings no quality credit'))
