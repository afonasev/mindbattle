"""Lossless technical qualification of pre2 frozen SOURCE24; no editorial credit."""
import pathlib,importlib.util,subprocess,json
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14455'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',OLD/'primary-inspectability-preflight.py')
J=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/16')
def native_guard():
 counts={}
 for name in ['rollout-2026-10-16T19-06-05-01a14508-c53b-7af2-881a-50801afe7870.jsonl','rollout-2026-10-16T15-20-26-01a1443a-30c4-73f1-bbf5-2df86115a910.jsonl','rollout-2026-10-16T16-40-50-01a14483-ccd0-7321-bd23-2262fcb11e5b.jsonl']:
  rows=[json.loads(l) for l in (J/name).open()];meta=next(r['payload'] for r in rows if r.get('type')=='session_meta');n=sum(r.get('type')=='compacted' for r in rows);assert n<2,(name,n);counts[meta['id']]=n
 return counts
counts=native_guard();assert m.read(D/'activation.json')['ordinaryWorkActivated']
R=OLD/'source-parks24-new-independent';B=D/'qualified-parks24-new-independent';B.mkdir(exist_ok=True);freeze='077aa26d7c90064de33909f245c2ad3607d3147f'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='sourceproof.json':
  original=doc['rawSources'][0];p=pathlib.Path(original['nativeOriginalRecordPath']);assert m.raw(p)==original['nativeOriginalRecordRawSHA256'];doc['rawSources'].append({'path':str(p),'url':original['url'],'sha256':original['nativeOriginalRecordRawSHA256'],'role':'Original native provenance corroboration of retained full substantive source; existing proof reference promoted to rawSources index without any new claim or judgment.'})
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers']+doc['fullRelevantHits'];seen={};combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert m.sha(p['card'])==p['sha256']
   if p['id'] in seen:assert seen[p['id']]==p['card'];continue
   seen[p['id']]=p['card'];live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
  for p in doc['latestProposals']:
   assert m.sha(p['card'])==p['canonicalSHA256'];source=m.read(pathlib.Path(p['path']));entry=next(e for e in source['entries'] if e['id']==p['id']);assert entry['proposedCard']==p['card']
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['GenuineNEW SOURCE24 after original proper-name absoluteEASY SOURCEHOLD; no prior INITIAL. FrozenEASY/key3/id/topic/order. Correctnote adds200feet approximate61m beyondwholeprompt/key. MAIN preservedexactauthor candidate ef9f. No unsupportedsoapchemistry claim.', 'Full retained NPS article L20-181 inside native-byteverifiedL0-195; retained footer196-209 not independently nativeverified andunused. Primary L61 direct washing water200feetaway +smallamount biodegradable soap +scatter straineddishwater. Not universallocalpermission; NPSrecommendation. Check6literal/4wholevariants/grammar/unique/plausibility/broadadultEASY withoutrareparknameorintervalmemory/taxonomy.', 'Full global11000 MAIN +100same/full18closest bodies/genuineproposals and bilateralERVC/directreverse; actionrelation distinctfrom22incomingseedvector beforetransport vs24off-water washing DURINGstay, not objectreskin. No genericvisitorformatban/no crossnoteban. Historical24b7unappliedHOLD retained, current27actualfullbody migrationDoñana not inferredfromID.', 'Source3a raw077aa pre2; root/source/OTHERguard<2; exactaffected19 afteractualapply before independentFIRSTINITIAL. No creditfromSOURCE/QA. One directedsubstantivefixcycle thenFINAL/unresolvedHOLD0, no ordinarycycle2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[24],D/'apply-parks24-new-independent.json',D/'qa-parks24-new-independent.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns)
r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze,nativeCompactions=counts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Union existing full live actual same-topic and global bodies without semantic changes; promote existing nativeOriginalRecordPath/hash as corroborating raw source index for already-referenced sourcePaths. Candidate/judgments unchanged.','files':provenance})
m.write(D/'qualification-parks24-new-independent.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks24-new-independent.json',pathlib.Path(__file__)],'Qualify pre2 original parks24 new independent SOURCE exact fullbody bindings'))
