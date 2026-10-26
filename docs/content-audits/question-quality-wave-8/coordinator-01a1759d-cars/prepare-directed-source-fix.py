"""Prepare one same-author sole directed fix from its exact independent INITIAL."""
from pathlib import Path
import importlib.util,sys,json
D=Path(__file__).parent;s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);snapshot=D/sys.argv[2];assert snapshot.parent==D
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId'];assert topic=='cars-road-transport'
original_task=m.read(D/f'source-{topic}{order}-task.json')
keys=[k for k,a in x['actors'].items() if k.startswith('author') and a['threadId']==original_task['authorNativeId']]
assert len(keys)==1, 'The original author must resolve to one actual native actor'
key=keys[0];a=x['actors'][key];audit=m.read(snapshot);v=audit['actors'][a['threadId']]
assert audit['owner']==m.O and audit['actors'][m.O]['actualCompactions']<2 and v['actualCompactions']<2 and v['lastTaskEvent']=='task_complete'
receipt=D/f'independent-{topic}{order}-initial/receipt.json';e=m.read(receipt)['entries'][0]
assert e['stage']=='INITIAL' and e['status']=='FIX' and e['defects']
q=m.read(m.C/f'src/content/topics/{topic}.json')['questions'][order-1];assert q==e['currentCard'] and m.sha(q)==e['currentCardCanonicalSHA256']
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
label=f'{topic}{order}';out=D/f'source-{label}-cycle1';assert not out.exists()
t=m.read(D/f'source-{label}-task.json');pending=x[f'pendingCarsRoadTransport{order}']
t.update(phase=f'START_SOURCE_{label.upper()}_SOLE_CYCLE1',cycle=1,beforeHash=m.sha(q),baselineCode=m.h.git(m.C,'rev-parse','HEAD'),catalogCandidate=m.h.git(m.C,'rev-parse','HEAD'),outputDirectory=str(out),previousIndependentInitial=str(receipt),previousIndependentInitialSHA256=m.raw(receipt),initialRawPacket=pending.get('rawPacket',str(D/f'source-{label}')),initialQualifiedPacket=pending.get('qualifiedPacket',str(D/f'qualified-source-{label}')),initialRawFreeze=pending['rawFreeze'],directedDefects=e['defects'],scope='SOLE directed cycle1 on the exact independent INITIAL defects only. Preserve all unchanged good literal fields and frozen contracts; no broad rewrite or adjacent repair.',currentContext=f'CURRENT{x["CURRENT"]}/2000 remaining{x["remaining"]}; exact applied INITIAL FIX, quality0. All prior originals, HOLDs and attempt fences persist. This is its sole ordinary fix; unresolved FINAL becomes terminal HOLD0.',limits=f'Write ONLY {out} and descendants. Initial raw and saved primary bodies immutable, reuse exact pointers. No catalog/P/Git/index/QA/chats/messages/subagents. Same genuine author identity/model/budget; actual{v["actualCompactions"]}/input{v["lastInput"]}/remaining{v["remaining"]}. Do not dump unchanged whole snapshots or repeat bootstrap. First compaction finishes this card only; second preservation STOP.',history='Own exact SOURCE INITIAL was independently FIX; preserve that receipt. Single directed cycle1, never new INITIAL/reset/cycle2.',deliver='One complete standard entries[0]/dict6/four canonical triples packet, cycle1 exact CURRENT beforeCard/hash. READY_FOR_SAME_READER_FINAL or READY_FOR_INDEPENDENT_REVIEW or HOLD, then final here and STOP. Full100 current technical bindings; source/ground changes only for directed defects, applicable own unchanged grounds preserved.',inventoryUsage=f'python3 -B {D}/current-inventory.py {topic} {out}/fresh-inventory.json')
t['inadmissibleRetainedSources']=x.get('inadmissibleRetainedSources',[])
t['allCurrentAttemptFences']={'path':str(D/'manifest.json'),'pointer':'/newAttemptFences','count':len(x['newAttemptFences']),'rule':'All binding; no refetch/retry/reset of consumed claim/URL attempts, cycle2 or adjacent workaround.'}
p=D/f'source-{label}-cycle1-task.json';m.write(p,t)
a.update(stage=f'START_SOURCE_{label.upper()}_SOLE_CYCLE1',task=str(p),nativePreflightVerifiedBy=m.O,lastTaskEvent='task_complete',actualCompactions=v['actualCompactions'],lastInput=v['lastInput'],modelWindow=v['window'])
pending.update(status='INITIAL_FIX_DIRECTED_SOLE_CYCLE1',cycle1Task=str(p),cycle1PreassignmentNativeSnapshot=str(snapshot))
x['sourceActorKeys']=[k for k in x.get('sourceActorKeys',[]) if k!=key and x['actors'][k]['stage'].startswith('START')]+[key];assert len(x['sourceActorKeys'])<=2
x['readyQueue']=[v for v in x.get('readyQueue',[]) if v['sourceOrder']!=order]
x['currentWork']={'id':q['id'],'topicId':topic,'sourceOrder':order,'stage':a['stage'],'CURRENT':x['CURRENT'],'remaining':x['remaining']}
x['helpers'][Path(__file__).name]=str(Path(__file__));m.write(D/'manifest.json',x)
print(m.savecode([p,D/'manifest.json',Path(__file__)],f'Prepare exact SOURCE{order} sole directed fix under fresh native budget'))
