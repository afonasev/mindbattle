"""Freeze a terminal AUTHOR HOLD, including malformed raw metadata.
No normalization, qualification, source adoption, apply, QA or independent review.
"""
import pathlib, json, importlib.util, sys, re
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);key=sys.argv[2];cursor=sys.argv[3]
cycle=1 if '--cycle1' in sys.argv[4:] else 0
suffix='-cycle1' if cycle else ''
x=m.read(D/'manifest.json');actor=x['actors'][key];uid=actor['threadId']
R=D/f'source-cars-road-transport{order}{suffix}';task=m.read(pathlib.Path(actor['task']))
assert task['owner']==m.O and task['authorNativeId']==uid and order in x['ownedSourceOrders']
assert task['cycle']==cycle
if cycle:
 initial=m.read(D/f'independent-cars-road-transport{order}-initial/receipt.json')['entries'][0]
 assert initial['stage']=='INITIAL' and initial['status']=='FIX' and initial['defects']
nr=[json.loads(l) for l in pathlib.Path(actor['nativeJournal']).open()]
assert [r['payload']['id'] for r in nr if r.get('type')=='session_meta']==[uid]
assert next(r['payload']['type'] for r in reversed(nr) if r.get('type')=='event_msg' and r['payload'].get('type') in ['task_started','task_complete'])=='task_complete'
ca,sp,ps=[m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]
e=ca['entries'][0];q=m.read(m.C/'src/content/topics/cars-road-transport.json')['questions'][order-1]
assert ca['sourceNativeId']==sp['sourceNativeId']==uid
assert e['status']=='HOLD' and e['sourceOrder']==order and e['id']==task['id']==q['id']
unapplied_proposal='--unapplied-proposal' in sys.argv[4:]
assert e['beforeCard']==q and e['beforeHash']==m.sha(q)==task['beforeHash']
assert m.sha(e['proposedCard'])==e['afterHash']
assert all(e['proposedCard'][k]==q[k] for k in ['id','difficulty','correctIndex'])
if not unapplied_proposal:assert e['proposedCard']==q and e['afterHash']==e['beforeHash']
assert ca['cycle']==sp['cycle']==cycle
if cycle:assert initial['currentCard']==q and initial['currentCardCanonicalSHA256']==m.sha(q)
entry=sp['entries'][0];assert entry['status']=='HOLD' and entry['id']==q['id']
variants=entry.get('fourFullPromptAnswerNoteAssessments',[])
variant_target=e['proposedCard'] if unapplied_proposal else q
variant_gaps=[]
for v in variants:
 a=variant_target['answers'][v['slot']]
 exact=v.get('fullPrompt')==variant_target['prompt'] and v.get('answer')==a['text'] and v.get('note')==a['note']
 if (unapplied_proposal or cycle) and not exact:variant_gaps.append(v['slot'])
 else:assert exact
defects=[]
if len(variants)!=4:
 defects.append({'file':'sourceproof.json','missingOrDifferentField':'fourFullPromptAnswerNoteAssessments','actualCount':len(variants),'requiredForQualification':4,'uncured':True})
if len(entry.get('literalGroups',[]))!=6:
 defects.append({'file':'sourceproof.json','missingOrDifferentField':'literalGroups','actualCount':len(entry.get('literalGroups',[])),'requiredForQualification':6,'uncured':True})
if unapplied_proposal:
 binding=ps.get('inventoryBinding',{})
 if isinstance(binding,dict) and 'sha256' not in binding and 'fileSHA256' not in binding:
  defects.append({'file':'peer-snapshot.json','missingOrDifferentField':'inventoryBinding SHA256','required':'Explicit original inventory file digest for qualification','uncured':True})
 if variant_gaps:defects.append({'file':'sourceproof.json','unalignedProposalVariantSlots':variant_gaps,'uncured':True})
if cycle and variant_gaps:defects.append({'file':'sourceproof.json','unalignedVariantSlots':variant_gaps,'uncured':True})
for k,expected in [('sourceNativeId',uid),('topicId','cars-road-transport'),('cycle',cycle)]:
 if ps.get(k)!=expected:defects.append({'file':'peer-snapshot.json','missingOrDifferentField':k,'actual':ps.get(k),'required':expected,'uncured':True})
cp=m.read(pathlib.Path(x['canonicalCheckpoint']));assert cp['owner']==m.O and q['id'] in cp['currentRemainingIds']
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
assert not (D/f'cars-road-transport{order}{suffix}-native-proof.json').exists()
last_turn_start=max(i for i,r in enumerate(nr,1) if r.get('type')=='event_msg' and r['payload'].get('type')=='task_started')
start=last_turn_start
continuation=x.get('pendingCarsRoadTransport'+str(order),{}).get('cycle1Continuation') if cycle else None
if continuation:
 continued=m.read(continuation)
 assert continued['owner']==m.O and continued['sourceNativeId']==uid
 assert continued['originalTask']==actor['task'] and m.raw(actor['task'])==continued['originalTaskSHA256']
 start=continued['firstTaskStartLine'];assert start<=last_turn_start and nr[start-1]==continued['originalFirstTaskStarted']
calls=[]
for i,r in enumerate(nr,1):
 p=r.get('payload',{});inp=re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())
 if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',inp):
  outs=[j for j,z in enumerate(nr,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']]
  assert len(outs)==1;calls.append({'callLine':i,'call':p['input'],'resultLine':outs[0]})
info=next(r['payload']['info'] for r in reversed(nr) if r['payload'].get('type')=='token_count')
proof={'owner':m.O,'sourceNativeId':uid,'nativeJournal':actor['nativeJournal'],'actualCompactions':sum(r.get('type')=='compacted' for r in nr),'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':'HOLD','beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'currentTaskStartLine':start,'networkCalls':[v for v in calls if v['callLine']>start],'priorTaskNetworkCalls':[v for v in calls if v['callLine']<start],'qualityCredit':0,'noQualification':True,'unapplied':True,'noIndependentInitial':True,'rawSchemaDefectsUncured':defects,'missingTripleHashes':[v['slot'] for v in variants if 'tripleSHA256' not in v],'rawBytesUnchanged':True}
proof['unappliedProposalPreservedWithoutQualification']=unapplied_proposal
proof['currentTaskLastTurnStartLine']=last_turn_start
if continuation:proof['sameCycleContinuation']={'path':continuation,'rawSHA256':m.raw(continuation),'noCycleReset':True}
proof.update(cycle=cycle,initialAlreadyApplied=bool(cycle),noIndependentInitial=not bool(cycle),noIndependentFinal=bool(cycle))
p=D/f'cars-road-transport{order}{suffix}-native-proof.json';m.write(p,proof)
actor.update(stage=f'IDLE_AFTER_SOURCE{order}{suffix}_AUTHORHOLD_UNQUALIFIED',actualCompactions=proof['actualCompactions'],lastTaskEvent='task_complete',lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],cursor=cursor,nativePreflightVerifiedBy=m.O)
if cycle:
 x[f'pendingCarsRoadTransport{order}'].update(status='APPLIED_INITIAL_FIX_TERMINAL_AUTHOR_CYCLE1_HOLD',qualityCredit=0,initialApplied=True,cycle1Applied=False,cycle1RawNativeProof=str(p),cycle1ActualCompactions=proof['actualCompactions'],cycle1NoQualificationApplyQAIndependentFINAL=True,cycle1RawSchemaDefectsUncured=defects,ordinaryCycle2Prohibited=True,cycle1AuthorHoldSourceproof=str(R/'sourceproof.json'))
else:
 x[f'pendingCarsRoadTransport{order}']={'id':q['id'],'status':'AUTHORHOLD_TERMINAL_UNAPPLIED','qualityCredit':0,'applied':False,'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'rawNativeProof':str(p),'sourceActualCompactions':proof['actualCompactions'],'noQualificationApplyQAInitial':True,'noQA':True,'noIndependentInitial':True,'ordinaryCycle2Prohibited':True,'rawSchemaDefectsUncured':defects,'authorHoldSourceproof':str(R/'sourceproof.json')}
x['readyQueue']=[v for v in x.get('readyQueue',[]) if v.get('sourceOrder')!=order]
x['sourceActorKeys']=[v for v in x['sourceActorKeys'] if v!=key]
m.write(D/'manifest.json',x)
cc=m.savecode([p,D/'manifest.json',pathlib.Path(__file__),*[p for p in R.rglob('*') if p.is_file()]],f'Preserve SOURCE{order}{suffix} terminal raw AUTHORHOLD without qualification')
print(json.dumps({'commit':cc,'order':order,'cycle':cycle,'qualityCredit':0,'unappliedProposal':True,'initialAlreadyApplied':bool(cycle),'rawSchemaDefects':len(defects),'actualCompactions':proof['actualCompactions'],'networkTotalCalls':len(calls),'CURRENT':x['CURRENT']},ensure_ascii=False))
