"""Continue an already authorized bounded author batch; no new scope or bootstrap."""
from pathlib import Path
import importlib.util,sys,json
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
key=sys.argv[1];n=int(sys.argv[2]);completion='--initial-completion' in sys.argv
x=m.read(D/'manifest.json');a=x['actors'][key];batch=x['activeAuthorBatches'][key]
assert n in batch['orders'] and not a.get('archived')
rows=[json.loads(l) for l in Path(a['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[a['threadId']]
comp=sum(r.get('type')=='compacted' for r in rows);assert comp==0
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
t=m.read(batch['assignment']);card=next(v for v in t.pop('cards') if v['sourceOrder']==n)
q=m.read(m.C/'src/content/topics/cars-road-transport.json')['questions'][n-1]
assert m.sha(q)==card['beforeHash']
out=D/(f'source-cars-road-transport{n}-initial-complete' if completion else f'source-cars-road-transport{n}')
assert not out.exists()
if not completion:assert not x.get(f'pendingCarsRoadTransport{n}')
t.update(card);t.update(authorNativeId=a['threadId'],authorNativeJournal=a['nativeJournal'],outputDirectory=str(out),originalBatch=batch['assignment'],baselineCode=m.h.git(m.C,'rev-parse','HEAD'),catalogCandidate=m.h.git(m.C,'rev-parse','HEAD'),phase=f'CONTINUE_SAME_BATCH_SOURCE{n}',frozen={k:card[k] for k in ['id','topicId','sourceOrder','difficulty','correctIndex']},inventoryUsage=f'python3 -B {D}/current-inventory.py cars-road-transport {out}/fresh-inventory.json')
t['inadmissibleRetainedSources']=x.get('inadmissibleRetainedSources',[])
t['editorialClarification']='Perform editorial corrections, not only audit the original. Prompt/answer TEXTS (including correct answer text), explanation, notes and source can change when necessary; frozen fields are ONLY ID/topic/order/difficulty/integer correctIndex. Resolve ordinary repairable draft defects before spending sources. Use already available source context to choose a supported unique MAIN and comparable row; do not keep an unsupported or wrong-level original merely because it existed. Never change MAIN to evade an already exhausted claim or historical terminal HOLD.'
t.update(owner=m.O,CURRENT=x['CURRENT'],remaining=x['remaining'],fullGoal=2000,recentRetainedSources=x.get('continuationRetainedSourceMetadata',t.get('recentRetainedSources',[])),manifest=str(D/'manifest.json'),sourceIndex=x['sourceIndex'],freshInventoryHelper=str(D/'current-inventory.py'),captureHelper=str(D/'capture-native.py'),captureMethod=str(D/'capture-method.md'))
t['sourceBudget']=x.get('canonicalSourceBudgetClarification',t['sourceBudget'])
t['sourceBudgetClarification']=x.get('canonicalSourceBudgetClarificationEvidence')
t['knownExhaustedClaims']=x.get('knownExhaustedClaimsCurrentRoute',[])
t['knownRetainedCaptureCaveats']=x.get('knownRetainedCaptureCaveats',[])
t['attemptFences']={'path':str(D/'manifest.json'),'pointer':'/ownConsumedSourceFences','count':len(x['newAttemptFences'])}
files=[]
task=D/(f'source{n}-initial-completion-task.json' if completion else f'source-cars-road-transport{n}-task.json')
if completion:
 proof=m.read(D/f'cars-road-transport{n}-native-proof.json')
 assert proof['status']=='HOLD' and not x.get(f'pendingCarsRoadTransport{n}')
 t.update(phase=f'COMPLETE_SAME_INITIAL_SOURCE{n}',cycle=0,originalRawPacket=proof['packet'],originalRawFreeze=sys.argv[-1])
 t['scope']='Finish existing initial editorial task once: original HOLD reported repairable incomparable options and unsupported notes; source MAIN is already confirmed. Preserve original raw/HOLD and its attempts; no independent INITIAL or spent fix-cycle exists. Make the necessary coherent source-backed proposal, or identify an actual unresolvable gate.'
 t['networkRestriction']='Reuse already confirmed MAIN source with no new MAIN request. Only genuinely distinct necessary option/note claims may use their existing per-claim budget; check saved contexts first. No reset/third source or historical HOLD repair.'
 m.write(task,t)
 scope=D/f'source{n}-initial-continuation-scope.json'
 line=proof['currentTaskStartLine']
 m.write(scope,{'owner':m.O,'sourceNativeId':a['threadId'],'originalTask':str(task),'originalTaskSHA256':m.raw(task),'firstTaskStartLine':line,'originalFirstTaskStarted':rows[line-1],'cycle':0,'sourceOrder':n,'originalRawFreeze':t['originalRawFreeze'],'originalRawPacket':proof['packet'],'noReset':True})
 x[f'pendingCarsRoadTransport{n}']={'id':card['id'],'actorKey':key,'status':'SAME_INITIAL_EDITORIAL_COMPLETION_PENDING','qualityCredit':0,'beforeHash':card['beforeHash'],'initialContinuation':str(scope),'originalRawFreeze':t['originalRawFreeze'],'originalAuthorHOLDPreserved':True,'noIndependentInitial':True}
 files.append(scope)
else:m.write(task,t)
a.update(stage=f'START_SOURCE{n}'+('_SAME_INITIAL_COMPLETION' if completion else ''),task=str(task),actualCompactions=comp,lastTaskEvent='task_complete',lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'],expected=f'Atomic SOURCE{n} edited READY or specific gateHOLD, then end turn')
batch.update(currentOrder=n,status='ACTIVE')
x['sourceActorKeys']=list(dict.fromkeys([k for k in x['sourceActorKeys'] if x['actors'][k]['stage'].startswith('START')]+[key]))
assert len(x['sourceActorKeys'])<=2
x['currentWork']={'stage':'FULL2000_AUTHORS_ACTIVE','orders':[x['activeAuthorBatches'][k]['currentOrder'] for k in x['sourceActorKeys']],'CURRENT':x['CURRENT'],'remaining':x['remaining']}
x['ownedSourceOrders']=sorted(set(x.get('ownedSourceOrders',[])+[n]))
x['helpers'][Path(__file__).name]=str(Path(__file__))
m.write(D/'manifest.json',x)
print(m.savecode([task,D/'manifest.json',Path(__file__),*files],'Continue authorized author batch with explicit editorial scope'))
