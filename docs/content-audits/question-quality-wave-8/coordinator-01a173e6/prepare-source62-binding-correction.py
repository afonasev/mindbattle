from pathlib import Path
import json, importlib.util
D = Path(__file__).parent
s = importlib.util.spec_from_file_location('m', D/'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
x = m.read(D/'manifest.json')
a = x['actors']['author62']
R = D/'source-video-game-history62'
rows = [json.loads(l) for l in Path(a['nativeJournal']).open()]
start = next((i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='task_started' and r['payload'].get('turn_id')=='01a17426-ba83-7d51-b2f5-57d51ee95657')
assert sum(r.get('type')=='compacted' for r in rows)==0
info = next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
snapshot = D/'source62-prequalification-mismatch.json'
m.write(snapshot, {'owner':m.O, 'authorNativeId':a['threadId'], 'nativeJournal':a['nativeJournal'], 'firstTaskStartLine':start[0], 'originalFirstTaskStarted':start[1], 'originalTask':a['task'], 'originalTaskSHA256':m.raw(a['task']), 'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()}, 'failure':'preserve-packet line42: group literal has Tron slot1, candidate and4variants DonkeyKong', 'qualityCredit':0, 'noIndependentInitial':True, 'noQualificationOrApply':True, 'actualCompactions':0})
freeze = m.savecode([snapshot,*[p for p in R.rglob('*') if p.is_file()]], 'Preserve original SOURCE62 READY and prequalification literal mismatch without credit')
out = D/'source-video-game-history62-initial-bound'
t = m.read(a['task'])
t.update({'phase':'CONTINUE_SAME_INITIAL62_BINDING_CORRECTION', 'outputDirectory':str(out), 'originalInitialTask':a['task'], 'originalRawPacket':str(R), 'originalRawFreeze':freeze, 'originalMismatchSnapshot':str(snapshot), 'scope':'Resolve one exact internal literal binding mismatch in same initial62/cycle0. Personally verify intended existing proposal and all own literal/variant/source grounds; no new claim/source/content expansion. Original raw immutable.', 'limits':'Write only new outputDirectory. Original R and sources immutable. No new network/catalog/planning/Git/tests/newactors. Same initial62/cycle0/attempt scope, no reset. Three coherent standard JSONs then end turn;63/64 wait same-batch CONTINUE. Firstcompaction finish62 only; second preservationSTOP.'})
tp = D/'source62-initial-binding-correction-task.json'
m.write(tp,t)
scope = D/'source62-initial-continuation-scope.json'
m.write(scope, {'owner':m.O,'sourceNativeId':a['threadId'],'originalTask':str(tp),'originalTaskSHA256':m.raw(tp),'firstTaskStartLine':start[0],'originalFirstTaskStarted':start[1],'cycle':0,'sourceOrder':62,'originalRawFreeze':freeze,'originalRawPacket':str(R),'noReset':True})
x['pendingVideoGameHistory62'] = {'id':t['id'],'actorKey':'author62','status':'PREQUALIFICATION_BINDING_CORRECTION_SAME_INITIAL','qualityCredit':0,'initialContinuation':str(scope),'originalMismatchSnapshot':str(snapshot),'originalRawFreeze':freeze,'noIndependentInitial':True}
a.update(stage='START_SAME_INITIAL62_BINDING_CORRECTION',task=str(tp),cursor='54e7e790-09fd-448e-a709-a8f4d95cd42a:31',actualCompactions=0,lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'],expected='Same initial62 coherent binding in new packet, no network')
x['pilot2'].update(status='SOURCE62_BINDING_CORRECTION',proceduralReturns=1)
x['currentWork']['stage'] = a['stage']
m.write(D/'manifest.json',x)
print(m.savecode([tp,scope,D/'manifest.json',Path(__file__)], 'Return exact prequalification62 binding mismatch without resetting initial scope'))
print({'originalRawFreeze':freeze,'authorInput':a['lastInput'],'compactions':0})
