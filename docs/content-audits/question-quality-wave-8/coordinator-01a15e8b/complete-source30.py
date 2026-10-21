"""Record unapplied author HOLD and exact original payload retention, no quality credit."""
import pathlib,importlib.util,json
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');R=D/'source-history-russia30';e=m.read(R/'candidate.json')['entries'][0]
rows=[json.loads(l) for l in pathlib.Path(x['actors']['author30']['nativeJournal']).open()]
checks=[]
for name,line in [('network-discovery-original.json',182),('network-ruler-search-original.json',243)]:
 z=m.read(R/'raw'/name);assert z['output']==rows[line-1]['payload']
 checks.append({'authorRaw':str(R/'raw'/name),'rawSHA256':m.raw(R/'raw'/name),'nativeLine':line,'fullOriginalPayloadEqual':True})
acc={'owner':m.O,'actualWebCalls':4,'rawAuthorDiscoveriesActuallyRetained':checks,'helperWrapperRecognitionLimitation':'Original author discovery files use call/output with full native payload rather than originalRecord; verify-network additionally wrapped exact stored original records, network0. No original loss, refetch, retry or quality adoption.','qualityCredit':0,'ownDiagnostics':['First container check compared retained payload against whole record and failed; corrected only to exact payload equality after shape inspection, raw unchanged.','Attempt to recover own command as JSON failed on JS object syntax; no mutation. Completion now uses this durable small script.']}
m.write(D/'history-russia30-network-container-verification.json',acc)
x['pendingHistoryRussia30']={'id':e['id'],'status':'AUTHOR_HOLD0_UNAPPLIED_NO_INITIAL','beforeHash':e['beforeHash'],'currentHash':e['beforeHash'],'unappliedCandidateHash':e['afterHash'],'rawPacket':str(R),'rawCommit':'ed07960eaf7d8576310b49f259ffe00fb38cea05','sourceNetworkAccounting':str(D/'history-russia30-network-accounting.json'),'networkContainerVerification':str(D/'history-russia30-network-container-verification.json'),'actualWebCalls':4,'noIndependentInitial':True,'reason':'Author reports direct reverse MAIN duplicate with history-russia-emancipation-event order20; candidate remains unadopted.','technicalFailures':str(R/'builder-diagnostics.json'),'QA':'NotRun unapplied HOLD','applied':False,'qualityCredit':0}
x['historyRussia30SourceAttemptMetadata']={'accounting':str(D/'history-russia30-network-accounting.json'),'actualCalls':4,'retried':False,'primaryBodies':'PRlib node802981 and romanovy_6 original returned contexts only','noBroadExhaustion':True,'noAutomaticRetryOrAdjacentAdoption':True}
for k in ['ownHeldOrders','ownHeldHistoryRussiaOrders','ownNewHeldHistoryRussiaOrders']:x[k]=list(dict.fromkeys(x.get(k,[])+[30]))
x['additionalRetainedSourceIndexes']=list(dict.fromkeys([str(R/'sourceproof.json')]+x['additionalRetainedSourceIndexes']))
x['sourceActorKeys']=[]
x['actors']['author30'].update(stage='RETIRED_AFTER_SOURCE30_HOLD_CONTEXT_MARGIN',retirementReason='Actual0 last164850/258400 leaves93550; observed SOURCE30 cost exceeds margin for another full source slice. No further task; HOLD and original sources saved.',cursor='65cf5a12-60b0-4d8f-b873-c9dc9b7d0401:44')
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][30]
x['nextUntouched']={'id':q['id'],'topicId':'history-russia','sourceOrder':31,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)}
x['readScope']['nextUntouched']=x['nextUntouched'];x['currentWork']={'stage':'SOURCE30_AUTHOR_HOLD0_SAVED_NEXT31','CURRENT':945,'remaining':1055};x['next']='Fresh SOURCE31 one card; SOURCE30 HOLD unadopted/noINITIAL/noQA; idle reviewer80 retained for next actual READY.'
m.write(D/'manifest.json',x)
print(m.savecode([D/'manifest.json',D/'history-russia30-network-container-verification.json',pathlib.Path(__file__)],'Preserve SOURCE30 HOLD original sources and unchanged CURRENT before SOURCE31'))
print('NEXT',json.dumps(x['nextUntouched'],ensure_ascii=False))
