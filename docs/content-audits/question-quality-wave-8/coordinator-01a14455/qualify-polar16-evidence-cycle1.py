"""Qualify exact original polar16-evidence-cycle1 SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar16-evidence-cycle1';B=D/'qualified-polar16-evidence-cycle1';B.mkdir(exist_ok=True);freeze='bcd84f9d00701958f34da5af3c5c43b828d0f665'
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
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers unions existing100 same-topic and15 full relevant global hit bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['SOLE SOURCE16 evidence-only cycle1 after fresh83INITIALFIX SOURCE_LITERAL_BINDING_MISMATCH; CURRENTcontentalreadyindependentlyPASS. Exactcardfe0 andall6literal/4triplesunchanged, no catalogrewrite requested/performed. OldSOURCE67proofimmutable; freshSOURCE3a personallyfulladoptedallcurrent16claims.', 'Correctnote3primaryGround nowNOAAAFSC L83FIRSTclause actualChukchi/Bering/strait, notSECONDBeaufort/Mackenzieclause. Explicitunchangednote2 geography separatelygrounded in completeNOAAArctic supplementL103-L121/offshoreCanadaAlaska plusCanadaMackenzieoutlet/NOAAsecondclause. Supplementfulloriginaltooloutput embedded inreader83sources.json personallyread, rawhash/canonicalcapture/provenance retained; do not treat hash/readerPASS alone asprimarytruth.', 'All5currentprimaryNASA2/NOAAAFSC/Canada/completeNOAAsupplement fullpersonalread;6individualgroups4wholevariants andowncorrectnoteflow/sedimentextra, mediumkey1/credible4/unique/polartaxonomy. Current18alreadyapplied73bce fullfreshbody included; global11000/all100sameMAIN/15fullclosestbilateralERVC/directreverse andlatestproposals, no newcross-notecollisionban.', 'Sourceevidence-only no contentdiff: bindqualificationreturnedactualcurrentbody/proof notwritecatalog, reusecurrentpoltopic19QA5bf910/tested73bce, no unchangedQA rerun. IndependentFIRSTFINAL16 cycle1required beforecredit; unresolvedafterFINALHOLD0/noordinarycycle2/reset. Critical3/rawfreeze pre2 currentactualsource0, ROOTpreleaseprivateCAS beforecert.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[16],D/'apply-polar16-evidence-cycle1.json',D/'qa-polar16-evidence-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar16-evidence-cycle1.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar16-evidence-cycle1.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar16-evidence-cycle1 exact SOURCE fullbody bindings no quality credit'))
