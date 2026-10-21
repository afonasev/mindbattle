"""Save source31 AUTHOR HOLD and original capture accounting; no content adoption."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');R=D/'source-history-russia31';e=m.read(R/'candidate.json')['entries'][0]
rows=[json.loads(l) for l in pathlib.Path(x['actors']['author31']['nativeJournal']).open()]
combined=m.read(R/'raw/native-web-attempts.json');assert combined['networkCallCount']==3
for c in combined['calls']:
 for key,typ in [('requestRecord','custom_tool_call'),('resultRecord','custom_tool_call_output')]:
  found=[r for r in rows if r.get('payload',{}).get('type')==typ and r['payload'].get('call_id')==c['callId']]
  assert len(found)==1 and found[0]==c[key]
assert e['status']=='HOLD' and e['beforeCard']==e['proposedCard'] and e['beforeHash']==e['afterHash']
report={'owner':m.O,'actualWebCalls':3,'allThreeAuthorCombinedOriginalRecordsExact':True,'combinedRaw':str(R/'raw/native-web-attempts.json'),'combinedSHA256':m.raw(R/'raw/native-web-attempts.json'),'helperWrapperRecognitionLimitation':'verify-network additionally wraps original discovery/failure from exact stored native, network0; all three author originals were already present in combined calls/resultRecord. No capture loss or retry.','originalPreservationFAIL':str(D/'source31-preservation-attempt1.json'),'pathAlias':'Only missing docs prefix; original file SHA, URL, full output SHA and native record all checked before read; raw unchanged.','policyReadGap':'Author reported failing to read planning specs at obsolete mindbattle-planning path. Source31 remains unqualified AUTHOR HOLD; no retroactive policy/full-quality claim. Future tasks receive explicit canonical P aliases.','qualityCredit':0}
m.write(D/'history-russia31-network-container-verification.json',report)
x['pendingHistoryRussia31']={'id':e['id'],'status':'AUTHOR_HOLD0_UNAPPLIED_NO_INITIAL','beforeHash':e['beforeHash'],'currentHash':e['beforeHash'],'unappliedCandidateHash':e['afterHash'],'rawPacket':str(R),'rawCommit':'8a64befe7dc6531230ed248150f290f406dbc5bd','sourceNetworkAccounting':str(D/'history-russia31-network-accounting.json'),'networkContainerVerification':str(D/'history-russia31-network-container-verification.json'),'actualWebCalls':3,'noIndependentInitial':True,'reason':'Author: EBID primary timeout; single PRlib item372573 alternative is bibliographic metadata without law text. Explanation and notes insufficiently sourced; correct-note own fact repeats prompt. Unattempted distractor claims are not broadly exhausted.','policyReadGap':report['policyReadGap'],'QA':'NotRun unapplied HOLD','applied':False,'qualityCredit':0}
x['historyRussia31SourceAttemptMetadata']={'accounting':str(D/'history-russia31-network-accounting.json'),'actualCalls':3,'noAutomaticRetryOrAdjacentAdoption':True,'corePrimaryPlusAlternativeConsumed':True,'noBroadExhaustionOfUnattemptedNotes':True}
for k in ['ownHeldOrders','ownHeldHistoryRussiaOrders','ownNewHeldHistoryRussiaOrders']:x[k]=list(dict.fromkeys(x.get(k,[])+[31]))
x['additionalRetainedSourceIndexes']=list(dict.fromkeys([str(R/'sourceproof.json')]+x['additionalRetainedSourceIndexes']))
x['sourceActorKeys']=[]
x['actors']['author31'].update(stage='RETIRED_AFTER_SOURCE31_HOLD_CONTEXT_MARGIN',retirementReason='Actual0 last154357/258400 leaves104043. Observed source31 cost102499 leaves insufficient margin for another complete source and required policy reads; preserve only, no reuse.',cursor='f0bfc97c-4d60-459a-ba5b-1fe7cc65ec25:43')
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][31]
x['nextUntouched']={'id':q['id'],'topicId':'history-russia','sourceOrder':32,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)};x['readScope']['nextUntouched']=x['nextUntouched']
x['currentWork']={'stage':'SOURCE31_AUTHOR_HOLD0_SAVED_NEXT32','CURRENT':945,'remaining':1055};x['next']='Fresh SOURCE32 one card with explicit canonical planning policy reads. Preserve SOURCE30/31 HOLDs and attempts; idle reviewer80 for actual READY only.'
m.write(D/'manifest.json',x)
print(m.savecode([D/'manifest.json',D/'history-russia31-network-container-verification.json',D/'source31-preservation-attempt1.json',pathlib.Path(__file__)],'Preserve SOURCE31 unchanged HOLD, original failed attempt and policy-read gap'))
print('NEXT',json.dumps(x['nextUntouched'],ensure_ascii=False))
