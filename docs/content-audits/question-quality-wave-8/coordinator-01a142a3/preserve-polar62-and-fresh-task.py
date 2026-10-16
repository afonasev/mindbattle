"""Preserve terminal SOURCE and prepare exact fresh successor intake; no credit."""
import pathlib, importlib.util, json, subprocess, datetime
D = pathlib.Path(__file__).parent.resolve()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py')
B=m.C/'docs/content-audits/question-quality-wave-8/process-v2-polar-first10-01a142a3/author/source-next2-10'
u='01a14262-85b3-7bd3-be22-0c76b96bbc5a'
fs=[]
for base in ['sessions','archived_sessions']:
 fs += list((pathlib.Path('/Users/eaafonasev/.codex')/base).rglob('*'+u+'.jsonl'))
assert len(fs)==1
bounds=[e['timestamp'] for line in fs[0].open() if (e:=json.loads(line)).get('type')=='compacted']
assert len(bounds)==2
out=D/'source62-polar-terminal-preservation.json'
m.write(out,{'actor':u,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actualCompactions':2,'boundaries':bounds,'STOP':True,'noOrdinaryReuse':True,'preservedIncomplete':str(B.relative_to(m.C)),'noCritical3For2_10':True,'qualityCredit':0,'validEarlierSourceFreezes':['6c54ac64a204e20c43e6910e864a9b012364eef5','2bef5f44be23ca7cc304a5767717f094140a8bbd'],'next':'Fresh native SOURCE personally reads retained raw2-10 and exact absolute contract; no inherited SOURCE/PASS','ownedRuntimeProcesses':[],'archiveOrderingIncident':'First preservation command failed parsing. Old native chat archived and fresh actor created before task save; no source files deleted. This script corrects durable preservation before further work.'})
print('preservation',m.savecode([p for p in B.rglob('*') if p.is_file()]+[out,pathlib.Path(__file__)],'Preserve SOURCE62 terminalactual2 incomplete polar9 rawcontexts and archiveordering incident; credit0'))
topic=m.read(m.C/'src/content/topics/polar-regions.json')
cards=[{'sourceOrder':i+1,'id':q['id'],'card':q,'sha256':m.sha(q)} for i,q in enumerate(topic['questions']) if 2<=i+1<=10]
ids=[e['id'] for e in cards]
args=['rg','-l','--glob','receipt.json','-F']
for id in ids:args += ['-e',id]
args += ['docs/content-audits']
r=subprocess.run(args,cwd=m.C,capture_output=True,text=True)
assert r.returncode in [0,1]
matches=[]
for file in r.stdout.splitlines():
 for e in m.read(m.C/file).get('entries',[]):
  if isinstance(e,dict) and e.get('id',e.get('questionId')) in ids:
   matches.append({'path':file,'id':e.get('id',e.get('questionId')),'stage':e.get('stage'),'status':e.get('status')})
assert not matches
intake=D/'polar2-10-fresh-intake.json'
m.write(intake,{'topicId':'polar-regions','CURRENT':832,'stage':'INITIAL','cards':cards,'canonicalReceiptMatches':matches,'matchingCanonicalFilesExamined':len(r.stdout.splitlines()),'catalogCommit':'b493eea5475fef35c9e7916f5fc0a7c3a99d0900','completed1Immutable':True,'priorSOURCEIncompleteRaw':str(B.relative_to(m.C)),'noQualityCredit':True})
contract=D.parent/'coordinator-01a13f31/packet-contract.json'
assert contract.is_file()
t={
 'coordinator':m.O,'actor':'01a142d0-3ae4-7d93-a1f3-ad8038c4254d','C':str(m.C),'CURRENT':832,'remaining':1168,'fullGoal':2000,
 'scope':'Fresh SOURCE polar-regions orders2-10 exact9 INITIAL; finish original incomplete slice personally, no inherited judgments',
 'intake':str(intake),'contract':str(contract),
 'pinnedProcessCommand':'git -C '+str(m.C)+' show 12e5581b:.agents/references/question-revision.md',
 'sourceIndex':str(B/'checkpoint.json'),'sourceDirectory':str(B/'sources'),
 'card1FullPrimary':str(m.C/'docs/content-audits/question-quality-wave-8/process-v2-polar-first10-01a142a3/author/source-completion2'),
 'output':str(m.C/'docs/content-audits/question-quality-wave-8/process-v2-polar2-10-fresh-01a142a3/author'),
 'frozen':'Exact ID/topic/order/difficulty/correctIndex from fresh intake. All text mutable only sourced within topic and honest frozen absolute grade. Certified1 untouched.',
 'primary':'Read existing complete relevant original NOAA/NASA/NSIDC/USGS/AAP contexts once. Prior23 outputs are material, not your personal proof. Inspect every complete relevant context and all claims/ownnotes. ErrorPDF/challenge/snippet/paraphrase is inadmissible. No retry known failedPDF/403 bypass; one normal official HTML alternative then concrete HOLD. Save newly opened full body once with URL/SHA/precise locator; reuse actual existing raw.',
 'MAIN':'Actual11000 prompt+correctkey targeted retrieval across relevant polar/geography/oceans/maps/climate/physics peers; full actual closest cards byID/topic/hash, substantive both ERVC directions/directreverse and all mutual proposed versions. No generic topic/answerclass/tautology proof. Retain compared relevant cards rather than blind100carddump.',
 'outputContract':'Standard candidate/sourceproof/peer-snapshot. Exact actualbeforeCard/beforeHash, proposedCard/afterHash,6 literal canonical groups with JSONstringquotes,4 whole prompt-answer-ownnote variants with grammar/plausibility/uniquekey/truth/usefulness and primary locators. Correct ownnote adds fact beyond prompt/key. Namekey explanation2 sentences. EASY broadadult; MEDIUM thematic; HARD expertise or substantive multistep. Frozenkey position not proof key. Actual question/answer category consistency required.',
 'ownership':'Only NEW output. No Git/index/refs/claims/planning/catalog/statusrefresh/tests/runtime/build/deploy/chats/subagents. Read-only gitshow pinned allowed. Actual nativeID; maxSOURCE2/OTHER1/readyQueue2. Atactual1 checkpoint; actual2 only atomicpreserveSTOP. READY first fullycompleted portion promptly ENDturn, then waitrootfreeze/queueACK before further portion. All9 stay scope; HOLD0 isnotcompletion.'
}
m.write(D/'source-polar2-10-fresh-task.json',t)
print('task',m.savecode([intake,D/'source-polar2-10-fresh-task.json'],'Save fresh native SOURCEpolar9 exact contract and retained raw index after terminalactor2 STOP'))
