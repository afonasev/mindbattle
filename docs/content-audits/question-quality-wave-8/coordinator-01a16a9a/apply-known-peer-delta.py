"""Apply an unchanged qualified READY after one author-bound changed peer.

Keep both original raw and qualified snapshots immutable. The existing standard
apply API validates every original peer with an explicit exact peer addendum.
"""
import pathlib,json,hashlib,importlib.util,subprocess,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order,changed=map(int,sys.argv[1:3]);original_qualified,raw_freeze=sys.argv[3:5]
clar_name=sys.argv[5];assert pathlib.Path(clar_name).name==clar_name
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId']
assert not x['actors']['reviewer']['stage'].startswith('START')
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
R=D/f'source-{topic}{order}';B=D/f'qualified-source-{topic}{order}'
clar_path=R/clar_name;clar=m.read(clar_path);candidate=m.read(B/'candidate.json');e=candidate['entries'][0]
uid=candidate['sourceNativeId'];assert clar['sourceNativeId']==uid==x['actors'][f'author{order}']['threadId']
assert candidate['cycle']==clar['cycle']==0 and e['status']=='READY_FOR_INDEPENDENT_REVIEW'
def at(ref,p):return subprocess.check_output(['git','-C',str(m.C),'show',ref+':'+str(p.relative_to(m.C))])
original_bindings={}
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=B/name;assert p.read_bytes()==at(original_qualified,p);original_bindings[name]=m.raw(p)
native_proof=m.read(D/f'{topic}{order}-native-proof.json')
for name,digest in native_proof['rawFileSHA256'].items():
 p=R/name;assert m.raw(p)==digest and p.read_bytes()==at(raw_freeze,p)
for name,digest in clar['originalInputsBeforeDependencyRefresh'].items():assert m.raw(name)==digest
rows=[json.loads(l) for l in pathlib.Path(native_proof['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[uid]
assert sum(r.get('type')=='compacted' for r in rows)<2
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
timing=clar['readAndAssessmentTiming'];report_read=timing[f'actual{changed}ReportRead'];report_path=pathlib.Path(report_read['path'])
assert report_path.parent==D and m.raw(report_path)==report_read['sha256']
app=m.read(report_path)['applied'][0];old,new=app['beforeCard'],app['proposedCard'];assert app['sourceOrder']==changed
assert clar[f'actual{changed}']['card']==new and clar[f'actual{changed}']['canonicalSHA256']==m.sha(new)
unchanged=clar[f'source{order}Unchanged'];assert unchanged['proposedCard']==e['proposedCard'] and unchanged['proposedSHA256']==e['afterHash']==m.sha(e['proposedCard'])
assert unchanged['preimageSHA256']==e['beforeHash']
assessment=clar['bilateralMAINComparison'];assert len(assessment['results'])==2
assert {r['direction'] for r in assessment['results']}=={f'{changed} to {order}',f'{order} to {changed}'}
assert all(all(r[k] for k in ['entity','relation','value','context','assessment']) and isinstance(r['directReverse'],bool) for r in assessment['results'])
def native_pair(cid):
 calls=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call' and r['payload'].get('call_id')==cid]
 outs=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==cid]
 assert len(calls)==len(outs)==1;return calls[0],outs[0]
read_call,read_out=native_pair(report_read['callId']);assess_call,assess_out=native_pair(timing['dependencyAssessment']['nativeCallId'])
assert report_path.name in read_call[1]['payload']['input'] and read_out[0]<assess_call[0]
assert read_call[1]['timestamp']==report_read['callTimestampUTC'] and read_out[1]['timestamp']==report_read['outputTimestampUTC']
assert assess_call[1]['timestamp']==timing['dependencyAssessment']['callTimestampUTC'] and assess_out[1]['timestamp']==timing['dependencyAssessment']['outputTimestampUTC']
ps=m.read(R/'peer-snapshot.json');old_peers=ps['actualCurrentPeers'];assert len(old_peers)==100 and [p['sourceOrder'] for p in old_peers]==list(range(1,101))
old_cards=[p['card'] for p in old_peers];assert all(p['id']==p['card']['id'] and p['sha256']==m.sha(p['card']) and p['topicId']==topic for p in old_peers)
tp=m.C/f'src/content/topics/{topic}.json';live=m.read(tp);assert old_cards[changed-1]==old and live['questions'][changed-1]==new
derived=json.loads(json.dumps(old_cards));derived[changed-1]=new;assert derived==live['questions']
assert live['questions'][order-1]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
old_catalog=x[f'pendingHumanMedicine{changed}']['testedCatalogCommit'];old_bytes=at(old_catalog,tp);assert json.loads(old_bytes)['questions']==old_cards
inventory_path=pathlib.Path(clar['inventory']['path']);assert inventory_path.parent==R and m.raw(inventory_path)==clar['inventory']['fileSHA256']
inventory=m.read(inventory_path);assert inventory['sameTopicMAIN']['questions']==derived and inventory['sameTopicMAIN']['fileSHA256']==m.raw(tp)
files=sorted((m.C/'src/content/topics').glob('*.json'));bindings=ps['globalMAIN']['allCurrentFileByteBindings'];fresh=inventory['globalMAIN']['allCurrentFileByteBindings']
assert len(files)==len(bindings)==len(fresh)==110
assert [b['path'] for b in bindings]==[b['path'] for b in fresh]==[str(p.relative_to(m.C)) for p in files]
old_rows=[];current_rows=[]
def project(t,q):return {'topicId':t,'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
for p,b,f in zip(files,bindings,fresh):
 now=m.read(p);before=json.loads(old_bytes) if p==tp else now
 assert b['sha256']==(hashlib.sha256(old_bytes).hexdigest() if p==tp else m.raw(p)) and f['sha256']==m.raw(p)
 old_rows.extend(project(before['id'],q) for q in before['questions']);current_rows.extend(project(now['id'],q) for q in now['questions'])
assert len(old_rows)==len(current_rows)==11000 and ps['globalMAIN']['rows']==old_rows and ps['globalMAIN']['rowsCanonicalSHA256']==m.sha(old_rows)
assert inventory['globalMAIN']['rows']==current_rows and inventory['globalMAIN']['rowsCanonicalSHA256']==m.sha(current_rows)
assert [i for i,(a,b) in enumerate(zip(old_rows,current_rows)) if a!=b]==[i for i,q in enumerate(old_rows) if q['id']==new['id']]
binding=D/f'source{order}-concurrent{changed}-dependency-binding.json';delta=D/f'source{order}-current-peer-addendum.json'
assert not binding.exists() and not delta.exists()
same_set=set(a['text'] for a in new['answers'])==set(a['text'] for a in e['proposedCard']['answers'])
same_order=[a['text'] for a in new['answers']]==[a['text'] for a in e['proposedCard']['answers']]
m.write(binding,{'owner':m.O,'targetOrder':order,'changedOrder':changed,'rawOriginalFreeze':raw_freeze,'originalQualifiedFreeze':original_qualified,'qualifiedFileSHA256':original_bindings,'authorClarification':str(clar_path),'authorClarificationSHA256':m.raw(clar_path),'authorNativeId':uid,'authorReadCallLine':read_call[0],'authorReadResultLine':read_out[0],'authorAssessmentCallLine':assess_call[0],'authorAssessmentResultLine':assess_out[0],'knownApplyReport':str(report_path),'knownApplyReportSHA256':m.raw(report_path),'oldSnapshotCatalogCommit':old_catalog,'oldGlobalRowsCanonicalSHA256':m.sha(old_rows),'currentGlobalRowsCanonicalSHA256':m.sha(current_rows),'freshInventory':str(inventory_path),'freshInventorySHA256':m.raw(inventory_path),'all100And110And11000Exact':True,'allOtherCardsAnd109FilesUnchanged':True,'originalQualifiedSnapshotExplicitlyHistorical':True,'noRawOrQualifiedOrTargetLiteralEdit':True,'deterministicOptionProperties':{'sameAnswerSet':same_set,'sameAnswerOrder':same_order,'authorSharedOrderProseIsDataNotAdopted':True},'operation':'Existing standard apply peerAddendum API; only exact already-applied dependency is overlaid after same-author full-body bilateral clarification. No new SOURCE cycle, source claim, root semantic judgment or quality credit.'})
m.write(delta,{'actualCurrentPeers':[{'id':new['id'],'topicId':topic,'sourceOrder':changed,'card':new,'sha256':m.sha(new)}],'dependencyBinding':str(binding),'dependencyBindingSHA256':m.raw(binding),'authorClarification':str(clar_path),'authorClarificationSHA256':m.raw(clar_path)})
freeze=m.savecode([binding,delta,clar_path,inventory_path,pathlib.Path(__file__)],f'Bind exact changed peer{changed} for unchanged READY{order}; preserve original snapshots')
print('criticalBindingFreeze',freeze)
s=importlib.util.spec_from_file_location('apply',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
a.apply(B,uid,[order],D/(B.name+'-apply.json'),D/('qa-'+B.name+'.json'),pathlib.Path(__file__),peerAddendum=delta,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']==topic]})
