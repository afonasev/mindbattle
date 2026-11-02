"""Apply an unchanged qualified READY after one author-bound changed peer.

Keep both original raw and qualified snapshots immutable. The existing standard
apply API validates every original peer with an explicit exact peer addendum.
"""
import pathlib,json,hashlib,importlib.util,subprocess,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order,changed=map(int,sys.argv[1:3]);original_qualified,raw_freeze=sys.argv[3:5]
clar_name=sys.argv[5]
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId']
assert not x['actors']['reviewer']['stage'].startswith('START')
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
R=D/f'source-{topic}{order}';B=D/f'qualified-source-{topic}{order}'
clar_path=pathlib.Path(clar_name);clar_path=clar_path if clar_path.is_absolute() else R/clar_path;assert clar_path.is_relative_to(D) and clar_path.is_file();clar=m.read(clar_path);candidate=m.read(B/'candidate.json');e=candidate['entries'][0]
uid=candidate['sourceNativeId'];author_keys=[k for k,a in x['actors'].items() if k.startswith('author') and a['threadId']==uid];assert len(author_keys)==1 and clar['sourceNativeId']==uid
assert candidate['cycle']==clar['cycle']==0 and e['status']=='READY_FOR_INDEPENDENT_REVIEW'
def at(ref,p):return subprocess.check_output(['git','-C',str(m.C),'show',ref+':'+str(p.relative_to(m.C))])
original_bindings={}
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=B/name;assert p.read_bytes()==at(original_qualified,p);original_bindings[name]=m.raw(p)
native_proof=m.read(D/f'{topic}{order}-native-proof.json')
for name,digest in native_proof['rawFileSHA256'].items():
 p=R/name;assert m.raw(p)==digest and p.read_bytes()==at(raw_freeze,p)
for name,digest in clar['originalInputsBeforeDependencyRefresh'].items():assert m.raw(name)==(digest['sha256'] if isinstance(digest,dict) and set(digest)=={'sha256'} else digest)
rows=[json.loads(l) for l in pathlib.Path(native_proof['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[uid]
assert sum(r.get('type')=='compacted' for r in rows)<2
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
report_read=clar[f'actual{changed}Report'];report_path=pathlib.Path(report_read['path'])
assert report_path.parent==D and m.raw(report_path)==report_read['sha256']
app=m.read(report_path)['applied'][0];old,new=app['beforeCard'],app['proposedCard'];assert app['sourceOrder']==changed
assert clar[f'actual{changed}']['card']==new and clar[f'actual{changed}']['canonicalSHA256']==m.sha(new)
unchanged=clar[f'source{order}Unchanged'];assert unchanged['proposedCard']==e['proposedCard'] and unchanged['proposedSHA256']==e['afterHash']==m.sha(e['proposedCard'])
assert unchanged['preimageSHA256']==e['beforeHash']
assessment=clar['bilateralMAINComparison'];assert len(assessment['results'])==2
assert {r['direction'] for r in assessment['results']}=={f'{changed} to {order}',f'{order} to {changed}'}
for r in assessment['results']:
 assert r['assessment'] and isinstance(r['directReverse'],bool)
 if 'from' in r and 'to' in r:
  assert all(all(r[side][k] for k in ['id','entity','relation','value','context']) for side in ['from','to'])
  expected_ids=[new['id'],e['id']] if r['direction']==f'{changed} to {order}' else [e['id'],new['id']]
  assert [r[side]['id'] for side in ['from','to']]==expected_ids
 else:assert all(r[k] for k in ['entity','relation','value','context'])
# Revision2026-10-25 removes manual native-call ordering as a gate.
# Same-native declaration, original SHA bindings and exact whole-card dependencies remain required.
assert clar['dependencyConclusion']
ps=m.read(R/'peer-snapshot.json');old_peers=ps['actualCurrentPeers'];assert len(old_peers)==100 and [p['sourceOrder'] for p in old_peers]==list(range(1,101))
old_cards=[p['card'] for p in old_peers];assert all(p['id']==p['card']['id'] and p['sha256']==m.sha(p['card']) and p['topicId']==topic for p in old_peers)
tp=m.C/f'src/content/topics/{topic}.json';live=m.read(tp);assert old_cards[changed-1]==old and live['questions'][changed-1]==new
derived=json.loads(json.dumps(old_cards));derived[changed-1]=new;assert derived==live['questions']
assert live['questions'][order-1]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
old_catalog=m.read(D/f'source-{topic}{order}-task.json')['catalogCandidate'];old_bytes=at(old_catalog,tp);assert json.loads(old_bytes)['questions']==old_cards
inventory_path=pathlib.Path(clar['inventory']['path']);assert inventory_path.parent==clar_path.parent and m.raw(inventory_path)==clar['inventory']['fileSHA256']
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
if 'rows' not in ps['globalMAIN']:
 ip=pathlib.Path(ps['freshInventoryPath']);ip=ip if ip.is_absolute() else m.C/ip
 assert ip.is_relative_to(R) and m.raw(ip)==ps['freshInventorySHA256']==native_proof['rawFileSHA256'][str(ip.relative_to(R))]
 assert at(raw_freeze,ip)==ip.read_bytes()
 retained_inventory=m.read(ip)
 assert retained_inventory['actualCurrentPeers']==old_peers
 assert all(ps['globalMAIN'][k]==v for k,v in retained_inventory['globalMAIN'].items() if k in ps['globalMAIN'])
 assert retained_inventory['globalMAIN']['rows']==old_rows
 ps['globalMAIN']['rows']=retained_inventory['globalMAIN']['rows']
assert len(old_rows)==len(current_rows)==11000 and ps['globalMAIN']['rows']==old_rows and ps['globalMAIN']['rowsCanonicalSHA256']==m.sha(old_rows)
assert inventory['globalMAIN']['rows']==current_rows and inventory['globalMAIN']['rowsCanonicalSHA256']==m.sha(current_rows)
expected_delta=[i for i,q in enumerate(old_rows) if q['id']==new['id']] if project(topic,old)!=project(topic,new) else []
assert [i for i,(a,b) in enumerate(zip(old_rows,current_rows)) if a!=b]==expected_delta
binding=D/f'source{order}-concurrent{changed}-dependency-binding.json';delta=D/f'source{order}-current-peer-addendum.json'
assert not binding.exists() and not delta.exists()
same_set=set(a['text'] for a in new['answers'])==set(a['text'] for a in e['proposedCard']['answers'])
same_order=[a['text'] for a in new['answers']]==[a['text'] for a in e['proposedCard']['answers']]
m.write(binding,{'owner':m.O,'targetOrder':order,'changedOrder':changed,'rawOriginalFreeze':raw_freeze,'originalQualifiedFreeze':original_qualified,'qualifiedFileSHA256':original_bindings,'authorClarification':str(clar_path),'authorClarificationSHA256':m.raw(clar_path),'authorNativeId':uid,'processRevision':'2026-10-25','manualNativeCallOrderingAudit':False,'knownApplyReport':str(report_path),'knownApplyReportSHA256':m.raw(report_path),'oldSnapshotCatalogCommit':old_catalog,'oldGlobalRowsCanonicalSHA256':m.sha(old_rows),'currentGlobalRowsCanonicalSHA256':m.sha(current_rows),'freshInventory':str(inventory_path),'freshInventorySHA256':m.raw(inventory_path),'all100And110And11000Exact':True,'allOtherCardsAnd109FilesUnchanged':True,'originalQualifiedSnapshotExplicitlyHistorical':True,'noRawOrQualifiedOrTargetLiteralEdit':True,'deterministicOptionProperties':{'sameAnswerSet':same_set,'sameAnswerOrder':same_order,'authorSharedOrderProseIsDataNotAdopted':True},'operation':'Existing standard apply peerAddendum API; only exact already-applied dependency is overlaid after same-author full-body bilateral clarification. No new SOURCE cycle, source claim, root semantic judgment or quality credit.'})
m.write(delta,{'actualCurrentPeers':[{'id':new['id'],'topicId':topic,'sourceOrder':changed,'card':new,'sha256':m.sha(new)}],'dependencyBinding':str(binding),'dependencyBindingSHA256':m.raw(binding),'authorClarification':str(clar_path),'authorClarificationSHA256':m.raw(clar_path)})
freeze=m.savecode([binding,delta,clar_path,inventory_path,pathlib.Path(__file__)],f'Bind exact changed peer{changed} for unchanged READY{order}; preserve original snapshots')
print('criticalBindingFreeze',freeze)
