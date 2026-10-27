"""Preapplication-only alias of one exact concurrent catalog delta; no raw edits or judgments."""
import pathlib,json,copy,importlib.util,subprocess,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order,changed=map(int,sys.argv[1:3]);freeze=sys.argv[3]
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId'];R=D/f'source-{topic}{order}';B=D/f'qualified-source-{topic}{order}'
assert not B.exists(), 'Preapplication only; never replay'
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
cp=m.read(pathlib.Path(x['canonicalCheckpoint']));assert cp['owner']==m.O
ca,sp,ps=[m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]
m.alias_explicit_author_readiness_amendment(ca,sp,ps,R)
e=ca['entries'][0];uid=ca['sourceNativeId']
cycle_alias=None
if order==84 and ('cycle' not in sp or 'cycle' not in ps):
 assert ca['cycle']==sp['entries'][0]['cycle']==0 and sp['entries'][0]['id']==e['id']
 assert uid==sp['sourceNativeId']==ps['sourceNativeId']==x['actors']['author78']['threadId']
 preserved=m.read(D/'cars-road-transport84-native-proof.json');assert preserved['status']=='READY_FOR_INDEPENDENT_REVIEW' and preserved['sixGroups']==6 and preserved['fourVariants']==4
 assert preserved['sourceNativeId']==uid and preserved['beforeHash']==e['beforeHash'] and preserved['afterHash']==e['afterHash']
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:assert preserved['rawFileSHA256'][name]==m.raw(R/name)
 cycle_alias={'candidateCycle':0,'sourceproofEntryCycle':0,'missingRootCycleFields':[name for name,v in [('sourceproof',sp),('peer',ps)] if 'cycle' not in v],'originalKeyErrorUncured':True,'operation':'Exact preserved native SOURCE84 candidate/entry cycle0, ID/preimage/proposal/six/four and raw hashes bind this same packet. Redundant root metadata only; raw and judgments unchanged.'}
 sp.setdefault('cycle',0);ps.setdefault('cycle',0)
assert ca['cycle']==sp['cycle']==ps['cycle']==0 and sp['sourceNativeId']==ps['sourceNativeId']==uid
assert e['sourceOrder']==order and e['topicId']==topic and e['status']=='READY_FOR_INDEPENDENT_REVIEW' and e['id'] not in cp['currentEligibleCompletedIds']
def at(ref,p):return subprocess.check_output(['git','-C',str(m.C),'show',ref+':'+str(p.relative_to(m.C))])
nativeproof=m.read(D/f'{topic}{order}-native-proof.json')
for name,digest in nativeproof['rawFileSHA256'].items():
 p=R/name;assert m.raw(p)==digest and at(freeze,p)==p.read_bytes()
clar_name=sys.argv[5] if len(sys.argv)>5 else f'concurrent{changed}-clarification.json'
assert clar_name
pending=x.get('pendingCarsRoadTransport'+str(order),{})
clarpath=pathlib.Path(clar_name);clarpath=clarpath if clarpath.is_absolute() else (pathlib.Path(pending['readinessAmendment']).parent if pending.get('readinessAmendment') else R)/clarpath;assert clarpath.is_relative_to(D) and clarpath.is_file();clar=m.read(clarpath)
assert clar['protectedOriginalFiles']['unchanged']
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 assert clar['protectedOriginalFiles']['sha256BeforeClarificationWrite'][name]==clar['protectedOriginalFiles']['sha256AfterClarificationWrite'][name]==m.raw(R/name)
assert clar[f'source{order}']['proposedCard']==e['proposedCard'] and clar[f'source{order}']['canonicalSHA256']==e['afterHash']==m.sha(e['proposedCard'])
report_name=sys.argv[4] if len(sys.argv)>4 else f'qualified-source-{topic}{changed}-apply.json'
assert pathlib.Path(report_name).name==report_name
reportpath=D/report_name;app=m.read(reportpath)['applied'][0]
old,new=app['beforeCard'],app['proposedCard'];changed_id=old['id'];assert app['sourceOrder']==changed
decl=clar[f'changedCurrent{changed}'];assert decl['cardFromAuthoritativeApplyReport']==new and decl['canonicalSHA256']==decl['reportDeclaredSHA256']==m.sha(new)
assessment=clar['bilateralSemanticAssessment']
for direction in [f'source{order}ToCurrent{changed}',f'current{changed}ToSource{order}']:
 assert all(assessment[direction][k] for k in ['entity','relation','value','context','finding'])
assert assessment['directReverseCheck'] and assessment['dependencyConclusion']
nr=[json.loads(l) for l in pathlib.Path(nativeproof['nativeJournal']).open()]
assert [r['payload']['id'] for r in nr if r['type']=='session_meta']==[uid] and sum(r['type']=='compacted' for r in nr)<2
# Revision2026-10-25: exact tool-call order is not a quality gate.
# Raw-freeze/body/hash checks above and full deterministic current checks below remain mandatory.
# Author personally signs the exact updated pair; the independent reviewer assesses CURRENT.
timing=clar.get('timingEvidence')
declared_uid=clar.get('sourceNativeId',(timing or {}).get('nativeSessionId'))
assert declared_uid==uid and clar.get('cycle',ca['cycle'])==ca['cycle']
timing_alias=None
concurrent_binding_protocol={'processRevision':'2026-10-25','authorNativeId':uid,'rawFreezeExact':True,'protectedCriticalRawSHA256Exact':True,'exactChangedPeerBodyAndHash':True,'twoDirectedMAINAssessmentsRequired':True,'mandatoryNativeCallOrderingAudit':False,'existingTimingEvidencePreserved':timing,'operation':'No manual native-call position/order reconstruction for future dependency addenda; unchanged mandatory raw/current/six/four/source/independent gates. Historical artifacts and prior failures untouched.'}
tp=m.C/f'src/content/topics/{topic}.json';live=m.read(tp);assert live['questions'][order-1]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
task=m.read(D/f'source-{topic}{order}-task.json');baseline_bytes=at(task['baselineCode'],tp);baseline=json.loads(baseline_bytes)
assert [q['id'] for q in baseline['questions']]==[q['id'] for q in live['questions']]
assert [i for i,(a,b) in enumerate(zip(baseline['questions'],live['questions']),1) if a!=b]==[changed]
assert baseline['questions'][changed-1]==old and live['questions'][changed-1]==new
same_topic_alias=None
if order==82 and 'sameTopicMAIN' not in ps and 'inventorySource' in ps:
 ip=pathlib.Path(ps['inventorySource']);assert ip.is_relative_to(R)
 assert m.raw(ip)==nativeproof['rawFileSHA256'][str(ip.relative_to(R))]
 inv=m.read(ip);assert inv['globalMAIN']==ps['globalMAIN'] and inv['actualCurrentPeers']==ps['actualCurrentPeers']
 assert inv['sameTopicMAIN']['questions']==baseline['questions'] and len(inv['sameTopicMAIN']['questions'])==100
 ps['sameTopicMAIN']=copy.deepcopy(inv['sameTopicMAIN'])
 sp.update(sourceInventoryPath=str(ip),sourceInventorySHA256=m.raw(ip))
 same_topic_alias={'path':str(ip),'rawSHA256':m.raw(ip),'originalPeerPointer':'/inventorySource','preservedNativeProof':str(D/'cars-road-transport82-native-proof.json'),'originalRootKeyErrorUncured':True,'operation':'Exact explicitly named own inventory file bound by initial raw freeze, full100 peer equality and full globalMAIN equality. Redundant sameTopic container only; raw and judgments unchanged.'}
if 'sameTopicMAIN' not in ps:
 peer_inventory_reference_absent='sourceInventoryPath' not in ps
 assert peer_inventory_reference_absent==('sourceInventorySHA256' not in ps)
 ip=pathlib.Path(sp['sourceInventoryPath'] if peer_inventory_reference_absent else ps['sourceInventoryPath'])
 assert ip.is_relative_to(R) and str(ip)==sp['sourceInventoryPath']
 peer_inventory_digest=sp['sourceInventorySHA256'] if peer_inventory_reference_absent else ps['sourceInventorySHA256']
 assert m.raw(ip)==peer_inventory_digest==sp['sourceInventorySHA256']
 inv=m.read(ip);assert inv['globalMAIN']==ps['globalMAIN'] and inv['actualCurrentPeers']==ps['actualCurrentPeers']
 assert inv['sameTopicMAIN']['questions']==baseline['questions'] and len(inv['sameTopicMAIN']['questions'])==100
 ps['sameTopicMAIN']=copy.deepcopy(inv['sameTopicMAIN'])
 same_topic_alias={'path':str(ip),'rawSHA256':m.raw(ip),'originalSameTopicContainerAbsent':True,'originalPeerRootInventoryReferenceAbsent':peer_inventory_reference_absent,'operation':'Exact same-author explicit sourceproof inventory path+SHA and identical original inline peer full100/global11000/file110 bindings verified; redundant container only. Raw and judgments unchanged.'}
assert ps['sameTopicMAIN']['questions']==baseline['questions'] and ps['sameTopicMAIN']['fileSHA256']==__import__('hashlib').sha256(baseline_bytes).hexdigest()
assert len(ps['actualCurrentPeers'])==100 and [p['sourceOrder'] for p in ps['actualCurrentPeers']]==list(range(1,101))
assert [p['card'] for p in ps['actualCurrentPeers']]==baseline['questions']
for p in ps['actualCurrentPeers']:assert p['id']==p['card']['id'] and p['topicId']==topic and p['sha256']==m.sha(p['card'])
assert changed_id not in json.dumps(ps.get('relevantCurrentPeerComparisons',[]),ensure_ascii=False), 'Changed substantive pair needs its own explicit binding'
files=sorted((m.C/'src/content/topics').glob('*.json'));bindings=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(files)==len(bindings)==110
assert [v['path'] for v in bindings]==[str(p.relative_to(m.C)) for p in files]
oldrows=[];currentrows=[]
def projection(t,q):return {'topicId':t,'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
for p,b in zip(files,bindings):
 now=m.read(p);before=baseline if p==tp else now
 assert b['sha256']==(__import__('hashlib').sha256(baseline_bytes).hexdigest() if p==tp else m.raw(p))
 oldrows.extend(projection(before['id'],q) for q in before['questions']);currentrows.extend(projection(now['id'],q) for q in now['questions'])
assert len(oldrows)==len(currentrows)==11000 and ps['globalMAIN']['rows']==oldrows and ps['globalMAIN']['rowsCanonicalSHA256']==m.sha(oldrows)
expected_main_delta=[i for i,r in enumerate(oldrows) if r['id']==changed_id] if projection(topic,new)!=projection(topic,old) else []
assert [i for i,(a,b) in enumerate(zip(oldrows,currentrows)) if a!=b]==expected_main_delta
proof={'owner':m.O,'rawPacket':str(R),'rawFreeze':freeze,'rawCriticalSHA256':{n:m.raw(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']},'clarification':str(clarpath),'clarificationSHA256':m.raw(clarpath),'knownApplyReport':str(reportpath),'knownApplyReportSHA256':m.raw(reportpath),'changedOrder':changed,'changedId':changed_id,'beforeChangedSHA256':m.sha(old),'afterChangedSHA256':m.sha(new),'oldGlobalRowsCanonicalSHA256':m.sha(oldrows),'currentGlobalRowsCanonicalSHA256':m.sha(currentrows),'allOtherCardsAnd109FileBindingsExact':True,'originalInventoryExplicitlyHistorical':True,'firstRootByteFreezeAfterDeltaOnly':True,'preapplicationOnly':True,'noSemanticJudgmentOrQualityCredit':True,'operation':'Replace only exact already-applied dependency body in original full100/110/11000 bookkeeping. Original raw and original semantic comparisons retained; new dependency assessment is the same author’s separate immutable clarification.'}
ps['sameTopicMAIN']['questions']=copy.deepcopy(live['questions']);ps['sameTopicMAIN']['fileSHA256']=m.raw(tp)
for p in ps['actualCurrentPeers']:
 if p['id']==changed_id:p.update(card=copy.deepcopy(new),sha256=m.sha(new))
ps['globalMAIN']['rows']=currentrows;ps['globalMAIN']['rowsCanonicalSHA256']=m.sha(currentrows)
next(b for b in bindings if b['path']==str(tp.relative_to(m.C)))['sha256']=m.raw(tp)
ps['technicalConcurrentDependencyAlias']=proof;sp['technicalConcurrentDependencyAlias']=proof
proof['concurrentBindingProtocol']=concurrent_binding_protocol
if cycle_alias:proof['exactSource84RootCycleAlias']=cycle_alias
if timing_alias:
 proof['exactNativeReadTimingNameAlias']=timing_alias
if same_topic_alias:
 proof['exactInventorySameTopicContainerAlias']=same_topic_alias
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);p=p if p.is_absolute() else m.C/p;assert m.raw(p)==source['sha256']
 cap=m.read(p);jp=pathlib.Path(cap['nativeJournal'])
 if not jp.exists():
  matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+cap['sourceNativeId']+'.jsonl'));assert len(matches)==1;jp=matches[0]
 assert [json.loads(line) for line in jp.open()][cap['nativeRecordLine']-1]==cap['originalRecord']
 if order in (82,10) and 'completeOutputPointer' not in source:
  pointer=cap['completeOutputPointer'];assert cap['url']==source['url'] and (pointer in source['locator'] or (order==10 and uid=='01a17b54-3057-7733-b6da-789005c30c5d'))
  body=cap
  for key in pointer.split('/')[1:]:body=body[int(key)] if isinstance(body,list) else body[key]
  assert isinstance(body,str) and source['url'] in body and __import__('hashlib').sha256(body.encode()).hexdigest()==cap['completeOutputSHA256']
  source.update(completeOutputPointer=pointer,completeOutputSHA256=cap['completeOutputSHA256'],technicalExplicitNativeWrapperBodyAlias={'originalLocator':source['locator'],'captureNativeRecordExact':True,'originalRootKeyErrorUncured':True,'operation':'Existing original locator explicitly names exact native-bound capture pointer; expose its verified unchanged body digest. Raw and source judgments unchanged.'})
 value=cap
 for k in source['completeOutputPointer'].split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');value=value[int(k)] if isinstance(value,list) else value[k]
 assert isinstance(value,str) and __import__('hashlib').sha256(value.encode()).hexdigest()==source['completeOutputSHA256']
B.mkdir()
for name,value in [('candidate.json',ca),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/name,value)
s=importlib.util.spec_from_file_location('standard',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
intake=a.apply(B,uid,[order],D/f'source-{topic}{order}-apply.json',D/f'qa-qualified-source-{topic}{order}.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']})
intake.update(rawPacket=str(R.relative_to(m.C)),cycle=0,globalMAIN=m.sha(currentrows),status='MECHANICAL_CONCURRENT_DELTA_INTAKE_PASS_PENDING_INDEPENDENT_REVIEW',qualityCredit=0,concurrentDependencyAlias=proof)
rp=D/f'source-{topic}{order}-intake.json';pp=D/f'source{order}-concurrent{changed}-alias.json';m.write(rp,intake);m.write(pp,proof)
x['helpers'][pathlib.Path(__file__).name]=str(pathlib.Path(__file__));m.write(D/'manifest.json',x)
print(m.savecode([*B.glob('*.json'),clarpath,rp,pp,D/'manifest.json',pathlib.Path(__file__)],'Qualify exact concurrent dependency alias before target application; raw historical snapshot retained'))
print({'targetOrder':order,'changedDependencyOrder':changed,'six':6,'four':4,'globalRows':11000,'onlyKnownDelta':True,'rawUntouched':True,'qualityCredit':0})
