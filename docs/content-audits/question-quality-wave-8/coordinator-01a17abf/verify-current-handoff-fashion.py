"""One deterministic closed-slice handoff check; no content review or QA rerun."""
from pathlib import Path
import importlib.util,json,subprocess,datetime
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(Path(x['canonicalCheckpoint']));n=len(cp['currentEligibleCompletedIds'])
assert n==x['CURRENT'] and x['remaining']==2000-n
assert cp['owner']==cp['activeCoordinator']==m.O
assert all(m.flow.get(c)[1]['owner']==m.O for c in x['claims'])
assert m.read(m.P/'.flow-leases.json')=={}
assert not any(a['stage'].startswith('START') for a in x['actors'].values())
selected={v['questionId']:v for v in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);left=set(cp['currentRemainingIds'])
assert len(selected)==len(cp['selectedCards'])==2000 and len(done)==n and len(left)==2000-n and not done&left and done|left==set(selected)
cat={};count=0
for tid in {v['topicId'] for v in selected.values()}:
 rel=f'src/content/topics/{tid}.json';a=m.read(m.C/rel);b=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':'+rel))
 assert [q['id'] for q in a['questions']]==[q['id'] for q in b['questions']]
 for q,z in zip(a['questions'],b['questions']):
  cat[q['id']]=q
  if q['id'] in selected:
   f=selected[q['id']];assert f['topicId']==tid and q['difficulty']==z['difficulty']==f['difficulty']
   assert type(q['correctIndex']) is int and q['correctIndex']==z['correctIndex']==f['correctIndex']
   assert m.sha(z)==f['baselineCanonicalSha256'];count+=1
assert count==2000 and len(cp['completedCardHashes'])==n
assert {v['questionId'] for v in cp['completedCardHashes']}==done
assert all(m.sha(cat[v['questionId']])==v['cardCanonicalSha256'] for v in cp['completedCardHashes'])
raw=[]
raw_proofs={}
for proof_path in D.glob('*-native-proof.json'):
 proof=m.read(proof_path)
 if 'packet' in proof and 'rawFileSHA256' in proof:
  if 'originalNetworkScannerDiagnostic' in proof:
   binding=proof['originalNetworkScannerDiagnostic'];original=m.read(binding['path'])
   assert m.raw(binding['path'])==binding['rawSHA256'] and proof['packet']==original['packet'] and proof['rawFileSHA256']==original['rawFileSHA256']
   continue  # Accounting-only derived proof preserves the unique original raw snapshot.
  assert proof['packet'] not in raw_proofs
  raw_proofs[proof['packet']]={'path':str(proof_path),'data':proof}
for order in x['ownedSourceOrders']:
 p=x[f'pendingFashion{order}']
 if p['qualityCredit']==1:
  assert p['id'] in done
  certificate=m.read(p['certification']);assert certificate['newQualityCredit']==1 and any(e['questionId']==p['id'] and e['cardCanonicalSha256']==m.sha(cat[p['id']]) for e in certificate['accepted'])
 else:
  assert 'HOLD' in p['status'] and p['id'] in left
  if p.get('applied'):assert m.sha(cat[p['id']])==p['appliedCurrentHash']
  else:assert m.sha(cat[p['id']])==p['beforeHash']
 pairs=[(Path(p.get('rawPacket',str(D/f'source-fashion{order}'))),p['rawFreeze'])]
 if p.get('cycle1RawFreeze'):pairs.append((Path(p.get('cycle1RawPacket',str(D/f'source-fashion{order}-cycle1'))),p['cycle1RawFreeze']))
 if p.get('originalRawFreeze'):pairs.append((D/f'source-fashion{order}',p['originalRawFreeze']))
 if p.get('originalUnsafeRawFreeze'):pairs.append((D/f'source-fashion{order}',p['originalUnsafeRawFreeze']))
 if p.get('cycle1RawSchemaFailure'):
  failed=p['cycle1RawSchemaFailure'];pairs.append((Path(failed['rawPacket']),failed['rawFreeze']))
 for packet,freeze in pairs:
  names=['hold.json'] if (packet/'hold.json').exists() and not (packet/'candidate.json').exists() else ['candidate.json','sourceproof.json','peer-snapshot.json']
  for name in names:
   f=packet/name;assert subprocess.check_output(['git','-C',str(m.C),'show',freeze+':'+str(f.relative_to(m.C))])==f.read_bytes()
  bound=raw_proofs.get(str(packet));assert bound, ('Missing original raw snapshot proof',str(packet))
  originals=bound['data']['rawFileSHA256']
  for name,digest in originals.items():
   f=packet/name;assert f.resolve().is_relative_to(packet.resolve()) and m.raw(f)==digest
   assert subprocess.check_output(['git','-C',str(m.C),'show',freeze+':'+str(f.relative_to(m.C))])==f.read_bytes()
  raw.append({'sourceOrder':order,'packet':str(packet),'freeze':freeze,'originalRawFilesByteExact':len(originals),'originalRawProof':bound['path']})
# The coordinator closed SOURCE100 before binding fashion; preserve that own raw too.
closed100=D/'source-cars-road-transport100';f100=m.read(D/'source100-raw-freeze.json')
assert set(f100['files'])=={str(p.relative_to(closed100)) for p in closed100.rglob('*') if p.is_file()}
for name,digest in f100['files'].items():
 p=closed100/name;assert m.raw(p)==digest
 assert subprocess.check_output(['git','-C',str(m.C),'show','a7586df46261f5968406bfaedfcd20279cc773b2:'+str(p.relative_to(m.C))])==p.read_bytes()
closed_manifest=m.read(D/'closed-cars-route-manifest.json');assert closed_manifest['pendingCarsRoadTransport100']['qualityCredit']==0
assert m.sha(m.read(m.C/'src/content/topics/cars-road-transport.json')['questions'][99])==closed_manifest['pendingCarsRoadTransport100']['beforeHash']
raw.append({'sourceOrder':100,'topicId':'cars-road-transport','packet':str(closed100),'freeze':'a7586df46261f5968406bfaedfcd20279cc773b2','originalRawFilesByteExact':len(f100['files']),'closedBeforeFashionRoute':True})
qa=x['ownAffectedRuns']
previous=m.read(Path(x['predecessorHandoff']).parent/'handoff-verification.json')
last_applicable=qa[-1] if qa else previous.get('lastApplicableQA',previous['ownQAReports'][-1] if previous.get('ownQAReports') else None)
assert last_applicable, 'No applicable exact catalog QA evidence'
for r in qa:
 q=m.read(r['path']);assert m.raw(r['path'])==r['rawSHA256']
 assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
last=last_applicable['testedCatalogCommit'];topics=list((m.C/'src/content/topics').glob('*.json'));assert len(topics)==110
for f in topics:assert subprocess.check_output(['git','-C',str(m.C),'show',last+':'+str(f.relative_to(m.C))])==f.read_bytes()
f=m.read(D/'own-consumed-source-fences.json');assert f['totalFences']==len(x['newAttemptFences'])==f['inheritedFenceCount']+len(f['ownClosedRecords'])
assert m.raw(f['inheritedPointer'])==f['inheritedRawSHA256']
assert x['newAttemptFences']==m.read(Path(x['predecessorHandoff']))['newAttemptFences']+f['ownClosedRecords']
r=m.read(D/'retained-reader-handoff.json');reader=x['actors']['reviewer']
assert r['readerOwnReceiptCount']==len(r['readerOwnReceipts'])==reader['ownReceiptCount']
for p,b in r['readerOwnReceipts'].items():assert m.raw(p)==b['rawSHA256']
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
report={'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'allCurrentAcceptedHashesExact':True,'all2000FrozenIdTopicOrderDifficultyNumericKey':True,'inheritedFencesByteExact':True,'totalFences':f['totalFences'],'ownRawFreezes':raw,'ownQAReports':qa,'lastApplicableQA':last_applicable,'all110TopicsSameAsLastQA':True,'retainedReaderNativeId':reader['threadId'],'retainedReaderOwnReceiptCount':r['readerOwnReceiptCount'],'noSemanticRereviewOrQARerun':True,'leaseEmpty':True,'foreignIndexesExact':True,'mainIntegrationPerformed':False,'fullUserGoal':x['fullUserGoal'],'unfinishedAuthorBatchOrders':x['unfinishedAuthorBatchOrders']}
out=D/'handoff-verification.json';m.write(out,report)
x['helpers'][Path(__file__).name]=str(Path(__file__));m.write(D/'manifest.json',x)
print(m.savecode([out,D/'manifest.json',Path(__file__)],'Verify exact closed SOURCE slice and full2000 handoff invariants once'))
print({'PASS':True,'CURRENT':n,'remaining':2000-n,'frozen':count,'rawFreezes':len(raw),'QA19Reports':len(qa),'readerOwn':reader['ownReceiptCount'],'fences':f['totalFences']})
