"""Parent's deterministic audit of exact native readonly ACK and full successful document reads."""
import pathlib,json,importlib.util,hashlib
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');S=x['successorThreadId'];native=pathlib.Path(x['successorNativeJournal']);rows=[json.loads(l) for l in native.open()]
assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==S
assert sum(r['type']=='compacted' for r in rows)==0
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
def command_results(v):
 if isinstance(v,dict):
  if 'exit_code' in v and 'output' in v:
   yield v
   return  # stdout/diagnostic source JSON is data, not a new command result.
  for a in v.values():yield from command_results(a)
 elif isinstance(v,list):
  for a in v:yield from command_results(a)
 elif isinstance(v,str):
  try:a=json.loads(v)
  except (ValueError,TypeError):return
  if a!=v:yield from command_results(a)
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
success=[];bad=[];bodies=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{})
 if p.get('type')!='custom_tool_call_output':continue
 results=list(command_results(p.get('output')))
 if not results:continue
 line,call=calls[p['call_id']];entry={'callLine':line,'call':call,'resultLine':i,'result':r}
 if any(v['exit_code'] not in [None,0] for v in results):bad.append(entry);continue
 if not all(v['exit_code']==0 for v in results):continue
 success.append(entry)
 for v in results:
  if 'Warning: truncated output' not in v['output'] and 'Output exceeded available model context' not in v['output']:bodies.append((p['call_id'],v['output']))
docs=[m.C/'docs/content-audits/question-quality-wave-8'/p for p in ['coordinator-01a14377/pinned-question-revision-12e5581b.md','coordinator-01a13f31/packet-contract.json','coordinator-01a1593a/method-pilot.md','coordinator-01a1593a/packet-format.md']]
reads=[]
for p in docs:
 content=p.read_text().strip();expected="text(await tools.exec_command({cmd:'cat "+str(p)+"',max_output_tokens:12000}));";matches=[cid for cid,b in bodies if b==p.read_text() and calls[cid][1]['payload'].get('input','').strip()==expected];assert matches,('No complete successful untruncated read',str(p));reads.append({'path':str(p),'rawSHA256':m.raw(p),'exactSuccessfulCallIds':matches})
assert len({v['exactSuccessfulCallIds'][0] for v in reads})==4, 'Four separate full structured successful read calls required'
first_actual=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type') in ['custom_tool_call','function_call']][:4]
assert len(first_actual)==4
for (_,r),p in zip(first_actual,docs):
 assert r['payload'].get('type')=='custom_tool_call'
 assert r['payload'].get('input','').strip()=="text(await tools.exec_command({cmd:'cat "+str(p)+"',max_output_tokens:12000}));"
primary=pathlib.Path('/Users/eaafonasev/Projects/mindbattle')
mandatory=[primary/'AGENTS.md',m.C/'AGENTS.md',
 *[primary/'.agents/references'/name for name in ['execution-policy.md','context-efficiency.md','coordination.md','project-policy/planning.md','flow/lifecycle.md','flow/efficiency.md','model-routing.md','delivery-workflow.md']],
 *[pathlib.Path('/Users/eaafonasev/.codex/references')/name for name in ['session-efficiency.md','game-execution.md','task-cleanup.md']],
 primary/'.agents/skills/flow-coordinate/SKILL.md',
 primary/'.agents/skills/flow-coordinate/references/project.md',
 primary/'.agents/skills/flow-coordinate/references/control.md',
 m.C/'docs/content-audits/question-authoring-guide-2026-09-02.md',
 D/'native-bootstrap-identity-readonly.py',D/'route-frontier.json',D/'successor-readonly-check.py']
mandatory_reads=[]
for p in mandatory:
 matches=[cid for cid,b in bodies if b==p.read_text() and str(p) in calls[cid][1]['payload'].get('input','')]
 assert matches,('Missing whole successful mandatory policy/reference read',str(p))
 mandatory_reads.append({'path':str(p),'rawSHA256':m.raw(p),'exactSuccessfulCallIds':matches})
section_reads=[]
for p,start,end in [(m.P/'docs/GAME_SPEC.md',135,285),(m.P/'openspec/specs/question-catalog/spec.md',21,33)]:
 section='\n'.join(p.read_text().splitlines()[start-1:end]).strip()
 matches=[cid for cid,b in bodies if b.strip()==section and str(p) in calls[cid][1]['payload'].get('input','')]
 assert matches,('Missing complete canonical policy section',str(p),start,end)
 section_reads.append({'path':str(p),'lines':[start,end],'wholeFileSHA256':m.raw(p),'exactSuccessfulCallIds':matches})
creation=m.read(D/'successor-create-native-proof.json');parent_rows=[json.loads(l) for l in pathlib.Path(creation['parentNative']).open()]
identity=[]
for cid,b in bodies:
 if '/native-bootstrap-identity-readonly.py' not in calls[cid][1]['payload'].get('input',''):continue
 try:z=json.loads(b)
 except (ValueError,TypeError):continue
 if not isinstance(z,dict) or z.get('verifiedSessionMetaId')!=S:continue
 assert z['nativeJournal']==str(native) and z['actualCompactions']==0
 assert z['originalCreateCallLine']==creation['createCallLine'] and z['originalCreateOutputLine']==creation['exactOriginalResultLine']
 assert z['originalCreateCall']==parent_rows[z['originalCreateCallLine']-1]
 assert z['originalCreateOutput']==parent_rows[z['originalCreateOutputLine']-1]
 identity.append({'call_id':cid,'wholeOriginalCreateCallAndOutputObserved':True,'nativeJournal':str(native),'actualCompactions':0,'decodeErrorsPreserved':z['decodeErrorsPreserved']})
assert identity, 'Successor must personally observe full original identity call and output'
checker_launches=[{'callLine':line,'call_id':cid} for cid,(line,r) in calls.items()
 if 'python3 -B '+str(D/'successor-readonly-check.py') in r['payload'].get('input','')]
assert checker_launches, 'Actual pure readonly checker execution required'
barriers=[]
for cid,b in bodies:
 try:z=json.loads(b)
 except (ValueError,TypeError):continue
 if not isinstance(z,dict) or z.get('READONLY_BARRIER')!='PASS':continue
 assert z['CURRENT']==x['CURRENT'] and z['remaining']==x['remaining'] and z['successorRegistered']==S
 assert z['HEAD']==z['freshOriginFeature']
 if z['HEAD']!=m.h.git(m.C,'rev-parse','HEAD'):continue  # Historical original PASS retained in success; latest HEAD needs its own PASS.
 barriers.append({'actualCompletionCallLine':calls[cid][0],'call_id':cid,'exitCode':0,'boundedOriginalPASS':z})
assert barriers, 'Actual exit0 checker completion required; async launch is not completion'
finals=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='message' and r['payload'].get('role')=='assistant' and r['payload'].get('phase')=='final_answer']
assert finals
last=finals[-1];text='\n'.join(a.get('text','') for a in last[1]['payload']['content'] if isinstance(a,dict))
stop_alias='STOP' not in text and 'Останавливаюсь до явного parent ACTIVATE.' in text
assert 'ACK' in text and str(x['CURRENT']) in text and str(x['remaining']) in text and text.rstrip().splitlines()[-1]=='STOP'
alias_path=D/'successor-ack-stop-declaration-alias.json'
if stop_alias:
 m.write(alias_path,{'owner':m.O,'successor':S,'nativeJournal':str(native),'originalFinalACKLine':last[0],'originalFinalACKCanonicalSHA256':m.sha(last[1]),'originalLiteralSTOPAbsent':True,'exactOriginalStopDeclaration':'Останавливаюсь до явного parent ACTIVATE.','actualOriginalTaskCompleteVerified':True,'operation':'Exact explicit Russian stop-until-ACTIVATE declaration is the barrier equivalent of STOP; original ACK unchanged, formatting gap remains uncured. No new authorization, writes, or quality credit.'})
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
report={'successor':S,'native':str(native),'rootPersonallyVerifiedExactNativeACK':True,'exactNativeVerificationCallsAndResults':success,'diagnosticFailuresPreservedSeparately':bad,'fullFourDocumentsSuccessfulUntruncatedReads':reads,'actualCompactions':0,'exactFinalACKLine':last[0],'exactFinalACKRecord':last[1],'CURRENT':x['CURRENT'],'remaining':x['remaining'],'claimsOwnerBeforeRelease':m.O,'leaseEmpty':True,'foreignIndexes':x['foreignIndexes'],'noQualityReplay':True}
report.update(fullMandatoryPolicyReads=mandatory_reads,canonicalSectionReads=section_reads,wholeOriginalIdentityObservations=identity)
report.update(firstFourActualToolCallLines=[i for i,r in first_actual],firstFourActualToolsExactlyRequiredLiterals=True,
              originalReadonlyCheckerLaunches=checker_launches,actualReadonlyCheckerExit0Completions=barriers)
if stop_alias:report['exactOriginalStopDeclarationAlias']={'path':str(alias_path),'rawSHA256':m.raw(alias_path),'originalACKUnchanged':True}
m.write(D/'successor-ack.json',report)
print(m.savecode([pathlib.Path(__file__),D/'successor-ack.json',*([alias_path] if stop_alias else [])],'Preserve personally audited exact native readonly successor ACK'))
print({'successor':S,'actualCompactions':0,'successfulVerificationCalls':len(success),'diagnosticFailedCalls':len(bad),'fullDocuments':len(reads),'finalACK':text})
