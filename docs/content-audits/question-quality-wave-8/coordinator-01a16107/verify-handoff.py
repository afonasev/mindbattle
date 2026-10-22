"""One fresh deterministic closing slice; no quality review, QA replay or old intake replay."""
import pathlib,json,hashlib,subprocess,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=x['CURRENT']
assert x['ownIntakeCURRENT']==975 and x['fullGoal']==2000 and x['remaining']==2000-n
assert cp['owner']==m.O and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
sel={q['questionId'] for q in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds'])
assert len(sel)==2000 and len(done)==n and len(remaining)==2000-n and not done&remaining and done|remaining==sel
cat={};bytopic={}
for p in (m.C/'src/content/topics').glob('*.json'):
 bytopic[p.stem]=m.read(p)['questions'];cat.update({q['id']:q for q in bytopic[p.stem]})
assert len(cat)==11000 and len(bytopic)==110
assert len(cp['completedCardHashes'])==n and {v['questionId'] for v in cp['completedCardHashes']}==done
assert all(m.sha(cat[v['questionId']])==v['cardCanonicalSha256'] for v in cp['completedCardHashes'])
baseline={t:json.loads(subprocess.check_output(['git','-C',str(m.C),'show',cp['baselineSHA']+':src/content/topics/'+t+'.json']))['questions'] for t in {v['topicId'] for v in cp['selectedCards']}}
for v in cp['selectedCards']:
 old=next(q for q in baseline[v['topicId']] if q['id']==v['questionId']);q=cat[v['questionId']]
 assert m.sha(old)==v['baselineCanonicalSha256'] and q['difficulty']==old['difficulty']==v['difficulty'] and q['correctIndex']==old['correctIndex']==v['correctIndex']
 assert [q['id'] for q in bytopic[v['topicId']]]==[q['id'] for q in baseline[v['topicId']]]
frozen=[]
for order in range(71,79):
 p=x['pendingHistoryRussia'+str(order)];a=x['actors']['author'+str(order)];assert a['archived'] and not a['stage'].startswith('START')
 for suffix in ['', '-cycle1']:
  if suffix and 'cycle1RawFreeze' not in p:continue
  for qualified in [False,True]:
   key=('cycle1QualifiedFreeze' if qualified else 'cycle1RawFreeze') if suffix else ('qualifiedFreeze' if qualified else 'rawFreeze')
   if key not in p:continue
   packet=D/(('qualified-' if qualified else '')+'source-history-russia'+str(order)+suffix)
   for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
    f=packet/name;assert subprocess.check_output(['git','-C',str(m.C),'show',p[key]+':'+str(f.relative_to(m.C))])==f.read_bytes();frozen.append({'path':str(f),'freeze':p[key],'rawSHA256':m.raw(f)})
   for raw in m.read(packet/'sourceproof.json')['rawSources']:assert m.raw(m.C/raw['path'])==raw['sha256']
 assert p['id']==bytopic['history-russia'][order-1]['id']
 if order==76:assert p['qualityCredit']==0 and not p['applied'] and m.sha(cat[p['id']])==p['beforeHash'] and p['id'] in remaining
 else:
  assert p['qualityCredit']==1 and p['id'] in done
  cert=m.read(pathlib.Path(p['certification']));assert len(cert['accepted'])==cert['newQualityCredit']==1 and cert['accepted'][0]['cardCanonicalSha256']==m.sha(cat[p['id']])
assert n==982 and len(x['ownProgress']['accepted'])==n-975==7 and len(x['coordinatorSlicesToPreserve'])==38
assert not x['sourceActorKeys'] and not x.get('pendingFinal77Reviewer') and not any(a['stage'].startswith('START') for a in x['actors'].values())
qa=[]
for path in x['ownAffectedRuns']:
 q=m.read(path);assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0;qa.append({'path':path,'rawSHA256':m.raw(path),'PASS':19,'FAIL':0})
assert len(qa)==5
native={}
for key,a in [('root',x['rootNativeAudit'])]+list(x['actors'].items()):
 uid=a['threadId'];ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(ps)==1
 rr=[json.loads(l) for l in ps[0].open()];assert next(r['payload']['id'] for r in rr if r['type']=='session_meta')==uid
 tokens=[r['payload']['info'] for r in rr if r.get('type')=='event_msg' and r['payload'].get('type')=='token_count']
 native[key]={'threadId':uid,'currentNativeJournal':str(ps[0]),'actualCompactions':sum(r['type']=='compacted' for r in rr),'lastInput':tokens[-1]['last_token_usage']['input_tokens'] if tokens else None,'window':tokens[-1].get('model_context_window') if tokens else None}
 if key=='root':rootrows=rr
assert native['root']['actualCompactions']==1 and native['reviewer']['actualCompactions']==0
assert 475000-native['reviewer']['lastInput']>=80000
assert all(native['author'+str(i)]['actualCompactions']==(1 if i==77 else 0) for i in range(71,79))
archive=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('archived') is True and v.get('threadId'):archive.append(v['threadId'])
  for z in v.values():walk(z)
 elif isinstance(v,list):
  for z in v:walk(z)
 elif isinstance(v,str):
  try:p=json.loads(v)
  except:return
  if p!=v:walk(p)
for r in rootrows:
 if r.get('payload',{}).get('type')=='custom_tool_call_output':walk(r['payload'].get('output'))
assert all(x['actors']['author'+str(i)]['threadId'] in archive for i in range(71,79))
remote=m.flow.get(x['claims'][0])[1]['evidence']['remote_push'];assert all(m.flow.get(cid)[1]['evidence']['remote_push']==remote for cid in x['claims']) and remote['CURRENT']==n and remote['remaining']==2000-n and remote['readbackVerified']
assert m.h.git(m.C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0]==remote['commit']
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mainids=[]
available=subprocess.run(['git','-C',str(m.C),'cat-file','-e',main+'^{commit}'],capture_output=True).returncode==0
if available:
 for t in {v['topicId'] for v in cp['selectedCards']}:
  body=json.loads(subprocess.check_output(['git','-C',str(m.C),'show',main+':src/content/topics/'+t+'.json']))
  mainids.extend(q['id'] for q in body['questions'] if q['id'] in done and m.sha(q)==m.sha(cat[q['id']]))
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines()
assert tracked and all((m.C/p).read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show','HEAD:'+p]) for p in tracked)
report={'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':975,'ownCredit':7,'HOLD76Credit':0,'frozenPartition2000AndMetadataExact':True,'currentAcceptedHashBindings':n,'preservedCoordinatorSlices':38,'immutablePacketFiles':frozen,'existingAffectedQAOnly':qa,'nativeAudit':native,'archiveConfirmedOwnAuthors':8,'claimsOwner':m.O,'foreignIndexes':x['foreignIndexes'],'lease':{},'remotePushAll3':remote,'freshMainSHA':main,'mainObjectAvailable':available,'acceptedCurrentHashesPresentOnMain':len(mainids) if available else None,'integrationMeaning':'Exact hash presence checked separately; no main merge performed. No claim that all feature work integrated.','uncuredDeviationsRemain':['SOURCE61','SOURCE69outside-output','SOURCE70outside-output','SOURCE73duplicate','SOURCE78duplicate'],'noActiveSourceReviewOrPendingFINAL':True,'trackedOwnFilesByteExact':len(tracked),'QAReplayed':False,'nextUntouchedMetadataOnly':x['nextUntouched']}
p=D/'handoff-verification.json';m.write(p,report);print('verificationCommit',m.savecode([p,pathlib.Path(__file__)],'Preserve fresh exact982 handoff verification without QA replay'))
print(json.dumps({'CURRENT':n,'remaining':2000-n,'packetFilesFrozen':len(frozen),'acceptedHashBindings':n,'ownCredit':7,'QAReports':len(qa),'rootCompactions':1,'readerCompactions':0,'source77Compactions':1,'mainSHA':main,'mainExactCurrentHashes':len(mainids) if available else None,'lease':{},'foreignIndexesPreserved':True}))
