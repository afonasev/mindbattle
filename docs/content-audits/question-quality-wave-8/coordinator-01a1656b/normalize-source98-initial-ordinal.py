"""One exact initial ordinal alias; immutable author raw and judgments stay unchanged."""
import importlib.util, json, pathlib, subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');R=D/'source-history-russia98';B=D/'qualified-source-history-russia98'
task=m.read(D/'source-history-russia98-task.json');uid='01a1657f-307d-7430-97e6-853bf0d41ca4'
assert task['cycle']==0 and task['authorNativeId']==uid and task['phase']=='START_SOURCE_HISTORY_RUSSIA98'
assert not (D/'independent-history-russia98-initial/receipt.json').exists()
assert not (D/'qualified-source-history-russia98-apply.json').exists()
assert not (D/'source-history-russia98-cycle1-task.json').exists()
raw_freeze='388a6376cdf259abe50f4284740e72aca8ff9748';qualified_freeze='8544046f7ea8af9b24cfdafb99b62d27960cbab0'
raws={};qualified={}
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
    for p,freeze in [(R/name,raw_freeze),(B/name,qualified_freeze)]:
        assert p.read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
    raws[name]=m.read(R/name);qualified[name]=m.read(B/name)
    assert raws[name]['sourceNativeId']==qualified[name]['sourceNativeId']==uid
    assert raws[name]['cycle']==qualified[name]['cycle']==1
entry=raws['candidate.json']['entries'][0]
assert entry['id']==task['id']=='history-russia-june-third-coup' and entry['sourceOrder']==98
assert entry['status']=='READY_FOR_INDEPENDENT_REVIEW'
assert entry['beforeHash']==task['beforeHash'] and m.sha(entry['beforeCard'])==entry['beforeHash']
assert m.read(m.C/'src/content/topics/history-russia.json')['questions'][97]==entry['beforeCard']
cp=m.read(pathlib.Path(x['canonicalCheckpoint']));assert entry['id'] not in cp['currentEligibleCompletedIds']
native=pathlib.Path(x['rootNativeAudit']['nativeJournal']);rows=[json.loads(l)for l in native.open()]
calls={r['payload']['call_id']:(i,r)for i,r in enumerate(rows,1)if r.get('payload',{}).get('type')=='custom_tool_call'}
failed=[]
for i,r in enumerate(rows,1):
    p=r.get('payload',{})
    if p.get('type')!='custom_tool_call_output' or p['call_id'] not in calls:continue
    line,call=calls[p['call_id']]
    if 'apply-ready-batch.py qualified-source-history-russia98 qualified-source-history-russia99' not in call['payload']['input']:continue
    if 'AssertionError' in json.dumps(p.get('output'),ensure_ascii=False):failed.append({'callLine':line,'originalCall':call,'resultLine':i,'originalResult':r})
assert len(failed)==1
proof={'owner':m.O,'sourceNativeId':uid,'task':str(D/'source-history-russia98-task.json'),'taskSHA256':m.raw(D/'source-history-russia98-task.json'),'rawFreeze':raw_freeze,'priorQualifiedFreeze':qualified_freeze,'originalRawCycle':1,'actualInitialTaskCycle':0,'firstSOURCEOnly':True,'noInitialReceiptOrCycle1TaskOrPriorApply':True,'originalBatchFAIL':failed[0],'originalRawByteExact':{name:m.raw(R/name)for name in raws},'qualifiedBefore':{name:m.raw(B/name)for name in qualified},'operation':'Wrong one-based first-SOURCE ordinal1 exposed as authoritative task/native initial ordinal0 only. Original declared value retained. No card/literal/hash/ground/source/peer judgment changed; no author cycle, new INITIAL or reset.','qualityCredit':0,'proceduralComplianceNotAsserted':True}
for name,value in qualified.items():
    value['originalDeclaredCycle']=value['cycle'];value['cycle']=0
    value['technicalInitialOrdinalAlias']={'original':1,'actualTaskInitial':0,'task':proof['task'],'rawFreeze':raw_freeze,'originalBatchFAILPreserved':str(D/'source98-initial-ordinal-alias.json'),'noNewContentCycle':True}
    m.write(B/name,value)
proof['qualifiedAfter']={name:m.raw(B/name)for name in qualified}
out=D/'source98-initial-ordinal-alias.json';assert not out.exists();m.write(out,proof)
commit=m.savecode([pathlib.Path(__file__),out,*[B/name for name in qualified]],'Preserve original SOURCE98 ordinal FAIL and exact initial metadata alias')
x['pendingHistoryRussia98']['qualifiedFreeze']=commit
x['pendingHistoryRussia98']['initialOrdinalAlias']={'path':str(out),'rawSHA256':m.raw(out),'originalCycle':1,'actualInitialCycle':0,'noNewCycle':True}
m.write(D/'manifest.json',x)
print('qualifiedAliasFreeze',commit)
print('projection',m.savecode([D/'manifest.json'],'Record initial SOURCE98 ordinal alias without new source or quality credit'))
