"""Qualify personally completed SOURCE38, preserving transport-HOLD history."""
import pathlib,importlib.util,json,subprocess,hashlib
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar38-whole-variants';B=D/'qualified-polar38-complete';B.mkdir(exist_ok=True);freeze='c1b5724e3f7f4590983007aeef1b09d8a1ec35e7';author='01a1510b-a2de-73e3-ae86-b18b1d2d9827'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');e=candidate['entries'][0];b=e['beforeCard'];c=e['proposedCard']
assert sp['sourceNativeId']==candidate['sourceNativeId']==author and sp['status']=='READY_FOR_INDEPENDENT_REVIEW'
assert m.sha(c)==e['afterHash']=='4c44c971e95ef2d867960fc13e2408ee7554c8f36095337a7b8d20dea83da4fd';assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex','prompt','explanation']);assert all(b['answers'][k]==c['answers'][k] for k in [0,2,3])
for source in sp['rawSources']:
 p=C/source['path'];assert m.raw(p)==source['sha256'] and source['coverage']
 if 'decodedFullVisibleOutputSHA256' in source:
  saved=m.read(p);j=pathlib.Path(saved['nativeJournal']);record=json.loads(j.read_text().splitlines()[saved['nativeJournalLine1Based']-1]);assert saved['originalRecord']==record
  outputs=[]
  for block in record['payload']['output']:
   if block.get('type')=='input_text':
    try:value=json.loads(block['text'])
    except json.JSONDecodeError:continue
    if isinstance(value,str):outputs.append(value)
  assert len(outputs)==1 and hashlib.sha256(outputs[0].encode()).hexdigest()==source['decodedFullVisibleOutputSHA256']
g=ps['global11000MainAudit'];assert len(g['fileInventory'])==110;assert m.sha(g['fileInventory'])==g['fileInventoryCanonicalSha256']
topics={};drift=[]
for sf in g['fileInventory']:
 p=C/sf['path'];t=m.read(p);topics[t['id']]=t
 if m.raw(p)!=sf['fileSha256']:
  assert t['id']=='national-parks-nature';oldbytes=subprocess.check_output(['git','-C',str(C),'show','79479045a88555a782e2a7a773ec129da52ad752:'+sf['path']]);assert hashlib.sha256(oldbytes).hexdigest()==sf['fileSha256'];old=json.loads(oldbytes)
  changed=[(x,y) for x,y in zip(old['questions'],t['questions']) if x!=y];app=m.read(D/'apply-parks28-fresh.json')['applied'][0];assert changed==[(app['beforeCard'],app['proposedCard'])];assert m.sha(app['proposedCard'])=='b9faf23b4d4c8b4718a7076ee1d953ac19fa25793616666deb762173bfdd448a'
  assert all(app['beforeCard'][k]==app['proposedCard'][k] for k in ['id','difficulty','correctIndex','prompt','explanation']);assert [x['text'] for x in app['beforeCard']['answers']]==[x['text'] for x in app['proposedCard']['answers']]
  drift.append({'path':sf['path'],'historicalSOURCEFileSHA256':sf['fileSha256'],'currentFileSHA256':m.raw(p),'change':'Only exact applied28 notes0/2/source metadata; MAIN unchanged. Original historical metadata retained, not relabeled current.'})
rows=[];cat={}
for topicid in g['runtimeTopicOrder']:
 for q in topics[topicid]['questions']:cat[q['id']]=q;rows.append({'topicId':topicid,'id':q['id'],'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']})
assert len(rows)==g['questionCount']==11000 and m.sha(rows)==g['canonicalRowsSHA256']
actual=ps['currentTopicSnapshot']['allCurrentCards'];assert len(actual)==100
for p in actual:assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
byid={p['id']:p for p in actual}
for pair in ps['relevantProposedPairs']:
 assert pair['candidate']['id']==e['id'] and pair['candidate']['sha256']==e['afterHash'];assert byid[pair['peer']['id']]['sha256']==pair['peer']['sha256'];assert pair['candidateToPeerAndPeerToCandidateAssessment'] and pair['entityRelationValueContextAndDirectReverse']
ps['actualCurrentPeers']=actual;ps['ROOTPostSOURCEFileOnlyChanges']=drift;ps['technicalNormalization']={'rawSourceDirectory':str(R.relative_to(C)),'rawFreeze':freeze,'operation':'Exact candidate/sourceproof unchanged; existing fullcurrent100 snapshot aliased asactualCurrentPeers. Historicalparks28rawfile transition independentlybytechecked against exactapply145c49; all11000 MAINrows remainexactSOURCEhash. Original wholevariant judgments and nearby fullbodies preserved, no source judgments added.'}
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
concerns=['Original38 FIRSTINITIAL not reviewed/no fixcycle. RawtransportHOLD ad3ba9 preserved; exactoriginalsuccessfulNASA/NOAAwrappers recovered47d998 withoutnetwork; authorpersonal fullreadcompletee6f1 thenwholevariantgrounds c1b572, nowcompleteSOURCE authoractual1. Exact4c44 changesONLYcorrectnote1adds220DU +sourceverifieddate, MAIN/4labels/key1/EASY/explanation/goodnotes0/2/3 preserved. No inheritedSOURCE/QA/othercardverdict.', 'Independent6literal/4WHOLEvariants four separatejudgments/fullNASA48labels0-47/science22-39 plusNOAA77labels426-502 completeQ11science452-491 andretainedNOAAFAQ258. Captures originalnative616/714 exactwholeobjects/hashnotparaphrasedtranscripts; allqualifiers, Arcticvariable/rarestrong1997/2011/2020 vsrecurrentAntarctic andexceptional2020 chemicalvsobservedtotalozone retained. Correctnote NASA220DUorlower operationalboundary beyondWHOLEprompt/key, no mathematicalgradecriterion. Explanationcoldwintervortex/PSC/sunlightreturnandSouthernHemisphere spring actualscope; questioneachspring placeuniqueness/plausibility/geographicparallelism/grammar independentlyjudge, noArcticneverdepletion claim. AbsoluteadultEASY broadschoolphenomenonlocation, taxonomygeography/polarenvironment.', 'Authorfresh11000MAIN taxonomymanifestorderhash07e245, same100fullcurrent includingfocus before. Historicalparks28file084c nowf404 dueonlyapplied28notes/source; allMAINrows unchanged/liveexacthash, nearbyfullpolarbody unchanged, accuratehistorical metadata notcurrentlabel. FourclosestpolarPSC/vortex/inversion/diamonds bilateral/directreverse fullbodies; cross152 lexicalMAINscreen retrievalnotqualitycredit. Readerfreshglobal/same100/fullclosestcross ifrelevant+genuineproposals required. Source29 maycreateunappliedproposal; no invented/forcedirrelevantpairs/no notevsMAIN orformatban. Onlystrictrootbindingafterapply/QA19/independentINITIAL cancount.']
r=a.apply(B,author,[38],D/'apply-polar38-complete.json',D/'qa-polar38-complete.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':actual},concerns=concerns);r.update(rawSourceFreeze=freeze,sourceNativeCompactions=1,qualityCredit=0,CURRENT=884,remaining=1116,fullGoal=2000,ROOTPostSOURCEFileOnlyChanges=drift)
m.write(D/'qualification-polar38-complete.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar38-complete.json',pathlib.Path(__file__)],'Qualify complete SOURCE38 originalcaptures and four focusedwholevariant grounds'))
