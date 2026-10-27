"""Prepare a bounded assignment within the existing full2000 manifest."""
from pathlib import Path
import importlib.util, sys, datetime
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
key=sys.argv[1];orders=[int(v) for v in sys.argv[2].split(',')]
x=m.read(D/'manifest.json');cp=m.read(Path(x['canonicalCheckpoint']))
assert cp['owner']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert all(m.flow.get(c)[1]['owner']==m.O for c in x['claims'])
qs=m.read(m.C/'src/content/topics/fashion.json')['questions']
selected={v['questionId']:v for v in cp['selectedCards']}
cards=[]
for order in orders:
 q=qs[order-1];f=selected[q['id']]
 assert not x.get(f'pendingFashion{order}'), 'Never replay an already processed card'
 assert not any(isinstance(v,dict) and q['id'] in [v.get('id'),v.get('questionId')] for v in x['newAttemptFences'])
 assert q['id'] in cp['currentRemainingIds'] and m.sha(q)==f['baselineCanonicalSha256']
 out=D/f'source-fashion{order}';assert not out.exists()
 cards.append({'id':q['id'],'topicId':'fashion','sourceOrder':order,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'beforeHash':m.sha(q),'cycle':0,'outputDirectory':str(out),'currentCardLocator':{'path':str(m.C/'src/content/topics/fashion.json'),'jsonPointer':f'/questions/{order-1}'},'designatedSourceURL':q['source']['url']})
task={
 'owner':m.O,'role':'SOURCE author bounded batch within full exact2000',
 'phase':'WAIT_SUPPORTED_IDENTITY_AND_START','C':str(m.C),'P':str(m.P),
 'manifest':str(D/'manifest.json'),'processRevision':'2026-10-25',
 'canonicalProcess':'/Users/eaafonasev/Projects/mindbattle/.agents/references/question-review-process.md',
 'authorNativeId':None,'authorNativeJournal':None,'cards':cards,
 'baselineCode':cp['baselineSHA'],'catalogCandidate':m.h.git(m.C,'rev-parse','HEAD'),
 'CURRENT':x['CURRENT'],'remaining':x['remaining'],'fullGoal':2000,
 'sourceIndex':x['sourceIndex'],
 'additionalRetainedSourceIndexesReference':{'path':str(D/'manifest.json'),'pointer':'/additionalRetainedSourceIndexes'},
 'recentRetainedSources':[
  {'path':str(D/'source-fashion64/sourceproof.json'),'purpose':'Exact retained museum Donkey Kong/Tomb Raider primary contexts; inspect metadata and personally read relevant full original before any new request. HOLD64 concerned different Pokemon claims, not a blanket source ban.'},
  {'path':str(D/'source-fashion63/sourceproof.json'),'purpose':'Retained dictionary and Nintendo contexts; Mario occupation HOLD does not invalidate independently grounded occupation definitions. No refetch for role.'}],
 'attemptFences':{'path':str(D/'manifest.json'),'pointer':'/ownConsumedSourceFences','count':len(x['newAttemptFences'])},
 'policyReads':[str(m.C/'docs/content-audits/question-authoring-guide-2026-09-02.md'),str(m.P/'docs/GAME_SPEC.md')+' Content questions section',str(m.P/'openspec/specs/question-catalog/spec.md')+':21-33'],
 'packetContract':str(m.C/'docs/content-audits/question-quality-wave-8/coordinator-01a13f31/packet-contract.json'),
 'formatReference':str(m.C/'docs/content-audits/question-quality-wave-8/coordinator-01a1593a/packet-format.md'),
 'freshInventoryHelper':str(D/'current-inventory.py'),
 'captureHelper':str(D/'capture-native.py'),'captureMethod':str(D/'capture-method.md'),
 'workflow':'After one START, process only current ID; return atomic READY/HOLD and end turn. Remaining IDs stay authorized; coordinator promptly CONTINUEs them while independent review proceeds. No new bootstrap or human GO. Max2activeauthors/1reviewer/READYqueue2.',
 'contentContract':'Personally read whole current card and full relevant source contexts. Frozen ID/topic/order/difficulty/integer correctIndex only; propose minimal necessary text corrections for source truth, unique MAIN, comparable options and absolute adult difficulty. Before network, inspect relevant full MAIN peers and sources so a duplicate/trivial original can be corrected before spending exact-claim attempts. Never route around an already exhausted claim or oldHOLD.',
 'required':'candidate.json/sourceproof.json/peer-snapshot.json standard entries[0], cycle0, sourceNativeId exact supported identity. fieldGroups dict6 canonical hashes; sourceproof.literalGroups exactly equal candidate prompt+ordered answer TEXTS+key, explanation and note0..3. Four fullPrompt/answer/note triples exactly equal candidate with canonical hashes and own grammar/plausibility/unique-key/note-truth/usefulness grounds. Correct-note additional fact concerns own answer option. Full relevant bilateral MAIN entity/relation/value/context and directreverse; self is not distinct peer. Machine inventory alone is not judgment.',
 'sourceBudget':x.get('canonicalSourceBudgetClarification','Saved full contexts first. For each uncovered exact claim, one primary attempt and one official alternative including discovery/preflight; no third request, retry, access bypass or history reset. Exhausted claim remains HOLD permanently. If it is MAIN or still asserted by the completed card, HOLD that ID; never replace MAIN to evade an exhausted MAIN claim. A discarded non-MAIN claim remains HOLD with its attempts and may be omitted while a distinct coherent fully source-backed row is completed. No old cardHOLD is reopened; no snippets/metadata/iframe as primary proof.'),
 'webToolUsage':'Use text(await tools.web__run(...)) or text(r) after the awaited call. Return may be string; do not assume r.content. Never slice/omit an original then refetch. Capture exact native original with existing helper once; reference path/hash/body locator. Prefer JSON raw wrappers to standalone source TXT; no whitespace cleanup of frozen raw. Necessary full context preserved, concise technical summaries sufficient; no exact-four/whole-output/manualjournal audits.',
 'readDiscipline':'Inventory helper stdout is only counts; never print entire inventory/topic/index/fence chain. Query exact relevant IDs/URLs internally, then personally read relevant whole bodies. Do not copy old author verdicts. Read each applicable policy once per revision, not each card.',
 'limits':'Writes only current assigned outputDirectory and descendants. You are not alone: preserve others. No catalog/planning/Git/index/claims/QA/runtime/build/deploy/newchats/subagents/model changes. First actualcompaction finish already-started current ID only, no nextcard; second preservationSTOP. Root identity is not author identity.',
 'stop':'One complete current-ID READY_FOR_INDEPENDENT_REVIEW or specific HOLD then end turn. READY/metadata/schema confer0credit. No next ID before same-batch operational CONTINUE.'}
task['inadmissibleRetainedSources']=x.get('inadmissibleRetainedSources',[])
task['editorialClarification']=x.get('authorEditorialClarification','')
task['recentRetainedSources']=x.setdefault('continuationRetainedSourceMetadata',task['recentRetainedSources'])
p=D/f'{key}-batch-task.json'
if p.exists():
 old=x.get('activeAuthorBatches',{}).get(key)
 if old:x.setdefault('completedAuthorBatchAssignments',[]).append(dict(old))
 p=D/f'{key}-batch{orders[0]}-{orders[-1]}-task.json'
assert not p.exists(), 'Preserve immutable prior batch assignment'
m.write(p,task)
x.setdefault('activeAuthorBatches',{})[key]={'orders':orders,'assignment':str(p),'currentOrder':orders[0],'status':'AWAITING_IDENTITY_START'}
x.setdefault('continuationRun',{'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'intakeCURRENT':x['CURRENT'],'processedOrders':[],'acceptedDelta':0,'holds':[]})
x['phase']='ACTIVE_FULL2000_CONTINUATION'
x['next']='Continue full2000 with existing authorized author roles and one independent reviewer; preserve all historical attempt and compaction fences.'
x['helpers'][Path(__file__).name]=str(Path(__file__))
m.write(D/'manifest.json',x)
print(m.savecode([p,D/'manifest.json',Path(__file__)],'Prepare bounded full2000 continuation author assignment'))
