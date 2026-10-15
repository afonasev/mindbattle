import pathlib,json,hashlib,subprocess,importlib.util,datetime,shutil
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');O='01a13e5e-e7e9-7f33-8165-57a15db42e1c'
def rd(p):return json.loads(p.read_text())
def wr(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');g=h.git
A=C/'docs/content-audits/question-quality-wave-8/process-v2-engineering21-40-01a13e5e';G=C/'docs/content-audits/question-quality-wave-8/process-v2-engineering11-20-01a13e5e';D=pathlib.Path(__file__).parent
# Only preserve already-returned PUBLIC web tool output text blocks; never reasoning/messages or tool input.
sess=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/15').glob('*01a13f00-5942-77a2-a3f5-25b5e3d617e6.jsonl'));refs=rd(A/'author/source-completed/terminal-closure.json')['publicSourceOutputRecoveryRefsOnly'];captures=[]
for n,line in enumerate(sess.open(),1):
 x=json.loads(line).get('payload',{})
 if x.get('type')!='custom_tool_call_output':continue
 output=x.get('output',[])
 if not isinstance(output,list):continue
 for k,b in enumerate(output):
  t=b.get('text','') if isinstance(b,dict) else ''
  hits=[r for r in refs if r in t]
  if hits and ('Source: open(' in t or '[wordlim:' in t):
   p=A/f'author/source-completed/source-native-preserved/public-web-{n}-{k}.txt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t);captures.append({'path':str(p.relative_to(C)),'rawSHA256':raw(p),'nativeEventLine':n,'refs':hits,'qualityCredit':0,'meaning':'public returned source output; may be partial/failed/search; fresh author must assess source completeness'})
wr(A/'author/source-completed/source-native-preserved/manifest.json',{'sourceActor':sess.stem,'privateReasoningExported':False,'captures':captures,'missingRefs':[r for r in refs if not any(r in v['refs'] for v in captures)]})
cp=rd(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');cards={};frozen=True
for topic in {x['topicId'] for x in cp['selectedCards']}:
 current=rd(C/f'src/content/topics/{topic}.json')['questions'];base=json.loads(subprocess.check_output(['git','-C',str(C),'show',cp['baselineSHA']+f':src/content/topics/{topic}.json']))['questions'];assert [q['id'] for q in current]==[q['id'] for q in base]
 cards.update({q['id']:q for q in current})
for e in cp['selectedCards']:assert cards[e['questionId']]['difficulty']==e['difficulty'] and cards[e['questionId']]['correctIndex']==e['correctIndex']
done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds']);assert len(done)==707 and len(remaining)==1293 and not done&remaining and done|remaining=={x['questionId'] for x in cp['selectedCards']}
for e in cp['completedCardHashes']:assert sha(cards[e['questionId']])==e['cardCanonicalSha256']
assert len(cp['completedCardHashes'])==707
qa=rd(A/'qa-initial-material-grounded4.json');assert qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0 and qa['success']
for t in ['maps-cartography','engineering-machines']:assert (C/f'src/content/topics/{t}.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','6a3098e64d34bd9c6dd24f14b9f3b01ea67e0130'+f':src/content/topics/{t}.json'])
audit=[]
for owner in [O,'01a13f00-5942-77a2-a3f5-25b5e3d617e6','01a13efc-07e2-7a51-95ca-0e90fde03f38']:
 p=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/15').glob('*'+owner+'.jsonl'));events=[{'line':n,'timestamp':d.get('timestamp')} for n,l in enumerate(p.open(),1) if (d:=json.loads(l)).get('type')=='compacted'];audit.append({'thread':owner,'actualCompactions':len(events),'events':events})
assert audit[0]['actualCompactions']>=2
indices={str(r):raw(r/g(r,'rev-parse','--git-path','index')) for r in [C,P]}
report={'owner':O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen2000MetadataAndTopicOrder':True,'all707CURRENTCanonicalHashes':True,'uniqueDisjointPartition':[707,1293],'waveCURRENT':[w['currentSourceEditorialCards'] for w in cp['waves']],'QA':{'passed':19,'failed':0,'pending':0,'catalogUnchangedSinceApply':'6a3098e64d34bd9c6dd24f14b9f3b01ea67e0130','path':str((A/'qa-initial-material-grounded4.json').relative_to(C))},'actualCompactionAudit':audit,'sharedIndexSHA256':indices,'mainIntegrated':False,'fullGoalNotComplete':True,'noRootRuntimeBuildServer':True,'diskAvailableBytes':shutil.disk_usage(C).free}
wr(D/'current-verification707-handoff.json',report)
# Explicit owned evidence directories only. Compare raw bytes to owned ref; no shared index changes.
owned=[D,A,G];files=[];head=g(C,'rev-parse','refs/heads/codex/question-quality-wave-6')
for root in owned:
 for p in root.rglob('*'):
  if not p.is_file() or '__pycache__' in p.parts:continue
  rel=str(p.relative_to(C))
  old=subprocess.run(['git','-C',str(C),'show',head+':'+rel],capture_output=True)
  if old.returncode or old.stdout!=p.read_bytes():files.append(rel)
assert files
commit=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Preserve current707 verification QA19 and terminal author drafts for second-compaction handoff',indices[str(C)])
print(json.dumps({'codeCommit':commit,'filesSaved':len(files),'audit':audit,'captures':len(captures),'indexSHA':indices},ensure_ascii=False))
