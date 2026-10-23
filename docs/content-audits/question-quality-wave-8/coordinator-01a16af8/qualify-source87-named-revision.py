"""Exact named revision intake, preserving every original; no semantic decisions."""
import pathlib,json,importlib.util,subprocess,re,copy,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'source-human-medicine87';B=D/'qualified-source-human-medicine87';x=m.read(D/'manifest.json')
assert not B.exists() and x['owner']==m.O and x['ownedSourceOrders']==[86,87]
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
freeze='7f57c20970883ebf2bc6d4bf137c931fa888b8b2'
raw_freeze=sys.argv[1]
assert m.h.git(m.C,'rev-parse','--verify',raw_freeze+'^{commit}')==raw_freeze
names={'candidate.json':'candidate-revision-03.json','sourceproof.json':'sourceproof-revision-03.json','peer-snapshot.json':'peer-snapshot-revision-03.json'}
for p in R.rglob('*'):
 if p.is_file():
  assert p.read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',raw_freeze+':'+str(p.relative_to(m.C))])
  if p.name!='source86-proposed-dependency-addendum.json':assert p.read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
ca,sp,ps=[m.read(R/names[n]) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]
uid=x['actors']['author87']['threadId'];e=ca['entries'][0]
assert ca['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
assert ca['cycle']==sp['cycle']==ps['cycle']==0 and ca['topicId']==sp['topicId']==ps['topicId']=='human-medicine'
assert e['sourceOrder']==87 and e['status']=='READY_FOR_INDEPENDENT_REVIEW' and e['id']=='human-medicine-ext-cell-eating'
assert m.sha(e['beforeCard'])==e['beforeHash'] and m.sha(e['proposedCard'])==e['afterHash']=='1d6a1504958ff2dc7ae1a7a062758b574bee01ec5aee2d23f34be127fded3cb2'
live=m.read(m.C/'src/content/topics/human-medicine.json');assert live['questions'][86]==e['beforeCard']
assert len(ps['actualCurrentPeers'])==100 and [p['sourceOrder'] for p in ps['actualCurrentPeers']]==list(range(1,101))
assert [p['card'] for p in ps['actualCurrentPeers']]==live['questions']
assert all(p['id']==p['card']['id'] and p['topicId']=='human-medicine' and p['sha256']==m.sha(p['card']) for p in ps['actualCurrentPeers'])
rows=[];files=sorted((m.C/'src/content/topics').glob('*.json'));bindings=ps['globalMAIN']['allCurrentFileByteBindings']
assert len(files)==len(bindings)==110
for p,b in zip(files,bindings):
 assert str(p.relative_to(m.C))==b['path'] and m.raw(p)==b['sha256'];t=m.read(p)
 rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
assert len(rows)==11000 and rows==ps['globalMAIN']['rows'] and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
ip=pathlib.Path(ps['inventoryPath']);assert ip.is_relative_to(R) and m.raw(ip)==ps['inventorySHA256'];inv=m.read(ip)
assert inv['sameTopicMAIN']['questions']==live['questions'] and inv['globalMAIN']['rowsCanonicalSHA256']==m.sha(rows)
ps['sameTopicMAIN']=copy.deepcopy(inv['sameTopicMAIN'])
cross=ps['relevantCrossTopicActualPeers'];assert len(cross)==9
for p in cross:
 t=m.read(m.C/('src/content/topics/'+p['topicId']+'.json'));matches=[(i,q) for i,q in enumerate(t['questions'],1) if q['id']==p['id']];assert len(matches)==1
 order,q=matches[0]
 if 'sourceOrder' in p:assert p['sourceOrder']==order
 assert p['card']==q and p['id']==q['id'] and p['sha256']==m.sha(q)
ps['crossCatalogClosestFullBodies']=copy.deepcopy(cross)
assert len(ps['relevantBilateralMAINComparisons'])==14
native=pathlib.Path(x['actors']['author87']['nativeJournal']);nr=[json.loads(l) for l in native.open()]
assert [v['payload']['id'] for v in nr if v.get('type')=='session_meta']==[uid]
assert sum(v.get('type')=='compacted' for v in nr)==0
assert next(v['payload']['type'] for v in reversed(nr) if v.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
paths={}
for src in sp['rawSources']:
 p=pathlib.Path(src['path']);assert p.is_relative_to(R) and m.raw(p)==src['sha256'];cap=m.read(p)
 assert nr[cap['nativeRecordLine']-1]==cap['originalRecord'] and cap['sourceNativeId']==uid
 body=cap
 for k in src['completeOutputPointer'].split('/')[1:]:body=body[int(k)] if isinstance(body,list) else body[k]
 assert isinstance(body,str) and __import__('hashlib').sha256(body.encode()).hexdigest()==src['completeOutputSHA256']
 rel=str(p.relative_to(m.C));paths[src['path']]=rel;src['originalSourceBinding']=copy.deepcopy(src);src['path']=rel
def aliases(v):
 if isinstance(v,dict):
  for k,z in v.items():
   if k=='sourcePaths':v[k]=[paths.get(p,p) for p in z]
   else:aliases(z)
 elif isinstance(v,list):
  for z in v:aliases(z)
aliases(sp)
selection={'owner':m.O,'rawDirectory':str(R),'firstAndNamedOriginalsFreeze':freeze,'selectedNamedFiles':{k:{'file':v,'rawSHA256':m.raw(R/v)} for k,v in names.items()},'allOriginalFilesUnchanged':True,'operation':'Exact author-declared final revision03 selected under standard container filenames. Absolute source paths become equivalent repository paths; same-topic inventory and cross-topic containers exposed losslessly. No literal, source ground, judgment, cycle or identity changes.','qualityCredit':0}
for v in [ca,sp,ps]:v['mechanicalNamedRevisionIntake']=selection
B.mkdir()
for n,v in zip(['candidate.json','sourceproof.json','peer-snapshot.json'],[ca,sp,ps]):m.write(B/n,v)
s=importlib.util.spec_from_file_location('standard',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
report=a.apply(B,uid,[87],D/'source-human-medicine87-apply.json',D/'qa-qualified-source-human-medicine87.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']})
report.update(rawPacket=str(R.relative_to(m.C)),cycle=0,globalMAIN=m.sha(rows),status='MECHANICAL_INTAKE_PASS_PENDING_INDEPENDENT_REVIEW',qualityCredit=0,namedRevisionIntake=selection)
starts=[i for i,v in enumerate(nr,1) if v.get('type')=='event_msg' and v.get('payload',{}).get('type')=='task_started'];assert len(starts)==3
network=[]
for i,v in enumerate(nr,1):
 p=v.get('payload',{})
 if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())):
  matches=[j for j,z in enumerate(nr,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']];assert len(matches)==1;network.append({'callLine':i,'call':p['input'],'resultLine':matches[0]})
assert len(network)==1 and starts[1]<network[0]['callLine']<starts[2]
info=next(v['payload']['info'] for v in reversed(nr) if v.get('payload',{}).get('type')=='token_count')
proof={'owner':m.O,'sourceNativeId':uid,'nativeJournal':str(native),'actualCompactions':0,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':e['status'],'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'sixGroups':6,'fourVariants':4,'qualityCredit':0,'networkCalls':network,'priorTaskNetworkCalls':[],'currentTaskStartLine':starts[1],'namedRevisionSelection':selection,'latestClarificationTaskStartLine':starts[2]}
x['pendingHumanMedicine87']={'id':e['id'],'topicId':'human-medicine','sourceOrder':87,'status':'SOURCE_READY_QUALIFIED_NAMED_REVISION03','qualityCredit':0,'applied':False,'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'rawFreeze':raw_freeze,'firstRawFreeze':freeze,'sourceActualCompactions':0,'actualWebCalls':1,'selectedNamedFiles':selection['selectedNamedFiles']}
x['actors']['author87'].update(stage='IDLE_AFTER_SOURCE87_READY_AND_DEPENDENCY_CLARIFICATION',actualCompactions=0,lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],lastTaskEvent='task_complete',nativePreflightVerifiedBy=m.O)
rp=D/'source-human-medicine87-intake.json';np=D/'human-medicine87-native-proof.json';selp=D/'source87-named-revision-selection.json'
for p,v in [(rp,report),(np,proof),(selp,selection),(D/'manifest.json',x)]:m.write(p,v)
print(m.savecode([*B.glob('*.json'),rp,np,selp,D/'manifest.json',pathlib.Path(__file__)],'Qualify exact author named SOURCE87 revision03 without raw or content changes'))
print({'sourceOrder':87,'six':6,'four':4,'sameTopic':100,'globalRows':11000,'crossPeers':9,'originalsUnchanged':True,'qualityCredit':0})
