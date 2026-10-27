"""Owned exact-byte private saves; no quality credit."""
import pathlib,importlib.util,hashlib,json,datetime
C=pathlib.Path(__file__).resolve().parents[4]
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
D=pathlib.Path(__file__).parent
O='01a17b9e-f725-7421-a651-61846e5475fa'
def alias_source80_cycle1_single_peer_entry(candidate,sp,ps,R):
 """Expose identical containers from one SHA-bound own80 sole-cycle1 entry."""
 import copy
 R=pathlib.Path(R)
 if R!=D/'source-cars-road-transport80-cycle1':return
 ap=D/'source80-cycle1-single-peer-container-alias.json';a=read(ap)
 for name,digest in a['criticalRawSHA256'].items():assert raw(R/name)==digest
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==a['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']==a['cycle']==1
 assert len(ps['entries'])==1 and sha(ps['entries'][0])==a['entryCanonicalSHA256']
 e=ps['entries'][0];q=candidate['entries'][0]
 assert e['id']==q['id'] and e['sourceOrder']==q['sourceOrder']==80
 for key in a['exposedIdenticalContainers']:
  assert key in e and key not in ps;ps[key]=copy.deepcopy(e[key])
 ps['technicalOwn80Cycle1SingleEntryAlias']={'binding':str(ap),'bindingSHA256':raw(ap),'originalPointer':'/entries/0','originalKeyErrorUncured':True,'noSourceGroundLiteralOrJudgmentChange':True}
def alias_source26_cycle1_canonical_readiness(candidate,sp,ps,R):
 """Expose explicit same-author readiness/hash correction; exact body unchanged."""
 R=pathlib.Path(R)
 if R!=D/'source-cars-road-transport26-complete-cycle1':return
 import copy
 ap=D/'source26-cycle1-canonical-readiness-addendum/metadata.json';a=read(ap)
 assert a['sourceNativeId']==candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']=='01a176e9-3c5c-71a3-9841-924de8974519'
 assert a['cycle']==candidate['cycle']==sp['cycle']==ps['cycle']==1 and a['sourceOrder']==26
 assert a['topicId']==candidate['topicId']==sp['topicId']==ps['topicId']=='cars-road-transport'
 for b in a['originalRawFileSHA256BeforeAfter']:
  p=D/b['path'];assert p.parent==R and raw(p)==b['before']==b['after']
 e=candidate['entries'][0];old=read(D/'source-cars-road-transport26-cycle1/candidate.json')['entries'][0]
 assert e['sourceOrder']==26 and e['proposedCard']==old['proposedCard'] and a['fullValueProposedCardUnchangedFromSoleCycle1'] is True
 canonical=sha(e['proposedCard']);unsorted=hashlib.sha256(json.dumps(e['proposedCard'],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 assert e['afterHash']==old['afterHash']==unsorted==a['hashCorrection']['oldInsertionOrderCompactSHA256']
 assert canonical==a['hashCorrection']['correctSortedCanonicalSHA256']
 assert a['finalStatus']=='READY_FOR_SAME_READER_FINAL' and a['readinessJudgment']
 expected=copy.deepcopy(e);assert expected['status']=='HOLD';expected.update(status=a['finalStatus'],afterHash=canonical)
 assert a['amendedCandidateEntry']==expected
 se=copy.deepcopy(sp['entries'][0]);assert se['status']=='HOLD';se['status']=a['finalStatus']
 assert a['amendedSourceproofEntry']==se
 candidate['entries'][0]=copy.deepcopy(expected);sp['entries'][0]=se
 proof={'authorAddendum':str(ap),'addendumSHA256':raw(ap),'rawFreeze':a['originalRawFreeze'],'originalUnsortedHash':unsorted,'canonicalHash':canonical,'sameProposedCardValue':True,'originalTechnicalHOLDAndRootConstraintErrorUncured':True,'qualityCredit':0,'operation':'Only explicitly amended readiness and canonical card hash of identical body. All original raw, literal groups, variant judgments, source contexts and peers unchanged.'}
 candidate['technicalSource26ReadinessCorrection']=proof;sp['technicalSource26ReadinessCorrection']=proof;ps['technicalSource26ReadinessCorrection']=proof
def alias_source23_cycle1_self_preimage(candidate,sp,ps,R):
 """Exact same-author addendum for one redundant stale self row; raw untouched."""
 R=pathlib.Path(R)
 if R!=D/'source-cars-road-transport23-cycle1':return
 import copy
 ap=D/'source23-cycle1-self-binding-addendum/metadata.json';a=read(ap)
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==a['authorNativeId']=='01a176ac-c316-7733-991a-96988f6c4673'
 assert candidate['cycle']==sp['cycle']==ps['cycle']==a['cycle']==1
 for name,b in a['originalRawPacketFiles'].items():assert b['unchanged'] and raw(R/name)==b['sha256Before']==b['sha256After']
 e=candidate['entries'][0];uid=e['id'];old=a['authorizedSnapshotInterpretation']['substitution']['fromSnapshotCard'];new=e['beforeCard']
 assert e['sourceOrder']==a['sourceOrder']==23 and uid==a['id']==old['id']==new['id']
 assert a['exactCurrentBinding']['beforeCard']==new and a['exactCurrentBinding']['beforeCardCanonicalSHA256']==e['beforeHash']==sha(new)
 assert a['exactRevisedBinding']['afterCard']==e['proposedCard'] and a['exactRevisedBinding']['afterCardCanonicalSHA256']==e['afterHash']==sha(e['proposedCard'])
 assert a['authorizedSnapshotInterpretation']['substitution']['toAppliedINITIALBeforeCard']==new
 current=read(C/'src/content/topics/cars-road-transport.json');assert current['questions'][22]==new
 assert len(ps['sameTopicMAIN']['questions'])==len(ps['actualCurrentPeers'])==100
 assert ps['sameTopicMAIN']['questions'][22]==ps['actualCurrentPeers'][22]['card']==old
 assert ps['sameTopicMAIN']['questions'][:22]+ps['sameTopicMAIN']['questions'][23:]==current['questions'][:22]+current['questions'][23:]
 assert [p['card'] for p in ps['actualCurrentPeers']]==ps['sameTopicMAIN']['questions']
 g=ps['globalMAIN'];assert len(g['rows'])==11000 and sha(g['rows'])==g['rowsCanonicalSHA256']
 rows=[]
 for f in sorted((C/'src/content/topics').glob('*.json')):
  t=read(f);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 delta=[i for i,(before,after) in enumerate(zip(g['rows'],rows)) if before!=after]
 assert len(delta)==1 and g['rows'][delta[0]]['id']==uid==rows[delta[0]]['id']
 bindings=g['allCurrentFileByteBindings'];assert len(bindings)==110
 tp=C/'src/content/topics/cars-road-transport.json'
 for b in bindings:
  if C/b['path']!=tp:assert raw(C/b['path'])==b['sha256']
 ps['sameTopicMAIN']['questions']=copy.deepcopy(current['questions']);ps['sameTopicMAIN']['fileSHA256']=raw(tp)
 ps['actualCurrentPeers'][22].update(card=copy.deepcopy(new),sha256=sha(new))
 g['rows']=rows;g['rowsCanonicalSHA256']=sha(rows)
 next(b for b in bindings if C/b['path']==tp)['sha256']=raw(tp)
 proof={'authorAddendum':str(ap),'addendumSHA256':raw(ap),'rawFreeze':a['rawCycle1FreezeSHA1'],'selfOnly':uid,'allOther10999RowsExact':True,'originalFailureUncured':True,'qualityCredit':0,'operation':'Same-author explicit self-preimage binding. Only stale self23 replaced by exact applied INITIAL beforeCard; no raw, literal, source or semantic judgment changed.'}
 ps['technicalSource23Cycle1SelfPreimageAlias']=proof;sp['technicalSource23Cycle1SelfPreimageAlias']=proof
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('private_save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
flow=mod('owned_flow',C/'tools/flow.py').Flow(P)
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(p,v):
 p=pathlib.Path(p)
 if P in p.parents:
  assert read(P/'.flow-leases.json').get('planning',{}).get('owner')==O
  index=pathlib.Path(h.git(P,'rev-parse','--path-format=absolute','--git-path','index'))
  assert raw(index)==read(D/'manifest.json')['foreignIndexes']['planning']
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def alias_explicit_owned_packet_source_paths(candidate,sp,R):
 """Resolve explicit ownD-relative captures by exact native bytes; derived view only."""
 import copy
 R=pathlib.Path(R);assert R.parent==D
 aliases={};proof=[]
 for source in sp['rawSources']:
  declared=source['path'];p=pathlib.Path(declared)
  if p.is_absolute() or (C/p).exists():continue
  if not declared.startswith(R.name+'/'):continue
  resolved=(D/p).resolve();assert resolved.is_relative_to(R.resolve()) and resolved.is_file()
  assert raw(resolved)==source['sha256']
  cap=read(resolved);assert cap['sourceNativeId']==candidate['sourceNativeId'] and cap['url']==source['url']
  journal=pathlib.Path(cap['nativeJournal'])
  if not journal.exists():
   matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+cap['sourceNativeId']+'.jsonl'));assert len(matches)==1;journal=matches[0]
  original=[json.loads(line) for line in journal.open()][cap['nativeRecordLine']-1]
  assert original==cap['originalRecord']
  pointer=cap['completeOutputPointer'];body=cap
  for part in pointer.split('/')[1:]:
   part=part.replace('~1','/').replace('~0','~');body=body[int(part)] if isinstance(body,list) else body[part]
  assert isinstance(body,str) and source['url'] in body and hashlib.sha256(body.encode()).hexdigest()==cap['completeOutputSHA256']
  prior=copy.deepcopy(source);source.update(path=str(resolved),completeOutputPointer=source.get('completeOutputPointer',pointer),completeOutputSHA256=source.get('completeOutputSHA256',cap['completeOutputSHA256']))
  assert source['completeOutputPointer']==pointer and source['completeOutputSHA256']==cap['completeOutputSHA256']
  aliases[declared]=str(resolved);proof.append({'originalBinding':prior,'resolved':str(resolved),'rawFileSHA256':raw(resolved),'nativeId':cap['sourceNativeId'],'nativeLine':cap['nativeRecordLine'],'originalRecordExact':True,'completeBodySHA256':cap['completeOutputSHA256']})
 if not aliases:return
 def refs(v):
  if isinstance(v,dict):
   for k,w in v.items():
    if k=='sourcePaths' and isinstance(w,list):v[k]=[aliases.get(p,p) for p in w]
    else:refs(w)
  elif isinstance(v,list):
   for w in v:refs(w)
 refs(sp)
 sp['technicalExplicitOwnedPacketSourcePathAlias']={'rawSourceproof':str(R/'sourceproof.json'),'rawSHA256':raw(R/'sourceproof.json'),'bindings':proof,'operation':'Exact original ownD-relative capture paths plus SHA/native URL/body bindings exposed as absolute paths and already-declared capture pointers. No source/literal/ground/peer judgment/raw edit or quality credit. Original preservation failure uncured.'}
def alias_explicit_author_readiness_amendment(candidate,sp,ps,R):
 """Bind an explicit same-author readiness/date amendment; never reopen a terminal card."""
 import copy
 R=pathlib.Path(R);x=read(D/'manifest.json');e=candidate['entries'][0]
 pending=x.get('pendingVideoGameHistory'+str(e['sourceOrder']),{})
 if 'readinessAmendment' not in pending:return
 assert R.parent==D and e['sourceOrder'] in x['ownedSourceOrders']
 assert pending['status']=='AUTHOR_READINESS_CLARIFICATION_PENDING'
 assert not (D/f"independent-{e['topicId']}{e['sourceOrder']}-initial").exists()
 assert all(v['sourceOrder']!=e['sourceOrder'] for v in x['ownSourceCompletion'])
 p=pathlib.Path(pending['readinessAmendment']);assert p.parent==D/(R.name+'-metadata-amendment')
 amendment=read(p);uid=candidate['sourceNativeId']
 assert amendment['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 assert amendment['id']==e['id'] and amendment['topicId']==e['topicId'] and amendment['sourceOrder']==e['sourceOrder']
 assert amendment['cycle']==candidate['cycle']==sp['cycle']==ps['cycle']==0
 assert amendment['qualityCredit']==0 and amendment['noSixGroupOrFrozenOrPeerJudgmentOrSourceBodyChanges'] is True
 assert set(amendment['originalRawFileSHA256'])=={'candidate.json','sourceproof.json','peer-snapshot.json'}
 for name,digest in amendment['originalRawFileSHA256'].items():assert raw(R/name)==digest
 assert e['status']=='HOLD' and sp['entries'][0]['status']=='HOLD'
 amended=amendment['amendedCandidateEntry'];expected=copy.deepcopy(e)
 expected['status']='READY_FOR_INDEPENDENT_REVIEW'
 expected['proposedCard']['source']['verifiedAt']=pending['readinessAmendmentReviewDate']
 expected['afterHash']=sha(expected['proposedCard']);assert amended==expected
 old_entry=sp['entries'][0];new_entry=amendment['amendedSourceproofEntry']
 assert new_entry['resolution']['clarificationTurnId']==pending['readinessClarificationTurnId']
 assert all(isinstance(v,str) and v for v in new_entry['resolution'].values())
 expected_entry=copy.deepcopy(old_entry)
 expected_entry.update(status='READY_FOR_INDEPENDENT_REVIEW',holdReasons=[],originalHoldReasons=old_entry['holdReasons'],resolution=new_entry['resolution'])
 for field,value in [('beforeHash',amended['beforeHash']),('afterHash',amended['afterHash'])]:
  if field in expected_entry:expected_entry[field]=value
 assert new_entry==expected_entry
 proof={'path':str(p),'rawSHA256':raw(p),'originalRawFileSHA256':amendment['originalRawFileSHA256'],'originalHOLDCardHash':e['afterHash'],'amendedCardHash':amended['afterHash'],'sameNativeId':uid,'cycleUnchanged':0,'clarificationTurnId':pending['readinessClarificationTurnId'],'operation':'Explicit same-author correction of sole unsupported readiness restriction plus actual review-date metadata. Six literal groups/four variants, frozen fields, peer judgments and source bodies unchanged. Original HOLD remains immutable; no new source/content cycle, reset or quality credit.'}
 candidate['entries'][0]=copy.deepcopy(amended);sp['entries'][0]=copy.deepcopy(new_entry)
 if sp.get('status')=='HOLD':sp['status']='READY_FOR_INDEPENDENT_REVIEW'
 candidate['authorReadinessAmendment']=proof;sp['authorReadinessAmendment']=proof
def alias_source96_distinct99_preimage(candidate,sp,ps,R):
 """Exact original99 distinct bodies plus separately bound candidate self; no judgment."""
 R=pathlib.Path(R)
 if R.name!='source-human-medicine96' or candidate['sourceNativeId']!='01a16bab-b3d4-7be3-906c-3ed46a56bdb8':return
 import copy,subprocess
 assert R.parent==D and candidate['cycle']==sp['cycle']==ps['cycle']==0
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 expected={'candidate.json':'3261163c52d3b7139acc900ce63bca6a806eaf9c22c79071cafe4963ffa57454','sourceproof.json':'ff73d7a53384dc208b17e4bfe384951e7ed4eccfed18113e720675744815adb4','peer-snapshot.json':'3cfb5530bb43e28bf7d10a259d782080f2bbdb60a2b3ccebf30ebf8b8eda22e4'}
 for name,digest in expected.items():
  assert raw(R/name)==digest
  assert (R/name).read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(C),'show','2e29932dee0e85251b5b791c1e6c0689a10a0985:'+str((R/name).relative_to(C))])
 assert len(candidate['entries'])==len(sp['entries'])==1
 e=candidate['entries'][0];assert e['id']=='human-medicine-ext-epinephrine' and e['sourceOrder']==96 and e['topicId']=='human-medicine'
 assert sha(e['beforeCard'])==e['beforeHash'] and sha(e['proposedCard'])==e['afterHash']
 same=ps['sameTopicMAIN'];assert same=={'path':'src/content/topics/human-medicine.json','topicId':'human-medicine','fileSHA256':raw(C/'src/content/topics/human-medicine.json'),'questionCount':100}
 topic=read(C/same['path']);assert topic['questions'][95]==e['beforeCard']
 peers=ps['actualCurrentPeers'];assert len(peers)==99 and [v['sourceOrder'] for v in peers]==[i for i in range(1,101) if i!=96]
 assert all(v['topicId']=='human-medicine' and v['card']==topic['questions'][v['sourceOrder']-1] and v['id']==v['card']['id'] and v['sha256']==sha(v['card']) for v in peers)
 assert all(v['id']!=e['id'] for v in peers)
 self_binding={'id':e['id'],'topicId':e['topicId'],'sourceOrder':96,'card':copy.deepcopy(e['beforeCard']),'sha256':e['beforeHash'],'countedAsDistinctPeer':False}
 ps['originalDistinctCurrentPeers']=copy.deepcopy(peers)
 ps['actualCurrentPeers']=sorted([*peers,self_binding],key=lambda v:v['sourceOrder'])
 same['questions']=[copy.deepcopy(v['card']) for v in ps['actualCurrentPeers']]
 assert same['questions']==topic['questions']
 ps['technicalSource96Distinct99PreimageAlias']={'rawFreeze':'2e29932dee0e85251b5b791c1e6c0689a10a0985','rawCriticalSHA256':expected,'originalPeerPointer':'/actualCurrentPeers','originalSelfPointer':'candidate.json#/entries/0/beforeCard','distinctPeerCountUnchanged':99,'currentBindings':100,'originalFormatGapUncured':True,'operation':'Existing99 distinct full bodies plus exact candidate beforeCard/hash/order become100 technical bindings. Self countedAsDistinctPeer=false. No new body, source, peer assessment, semantic decision or raw edit.'}
def alias_explicit_inventory_file_digest(candidate,sp,ps,R):
 """Alias an explicit inventory file digest only after full live bindings."""
 g=ps.get('globalMAIN',{})
 if 'sourceInventoryFileSHA256' not in g or 'sourceInventorySHA256' in g:return
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0
 p=pathlib.Path(g['sourceInventoryPath']);p=p if p.is_absolute() else C/p
 assert p.is_relative_to(R) and raw(p)==g['sourceInventoryFileSHA256']
 inv=read(p);same=inv['sameTopicMAIN'];full=inv['globalMAIN'];e=candidate['entries'][0]
 topic=read(C/same['path']);peers=ps['actualCurrentPeers']
 assert same['topicId']==topic['id']==e['topicId']
 assert len(peers)==same['questionCount']==len(topic['questions'])==100
 assert [v['sourceOrder'] for v in peers]==list(range(1,101))
 assert [v['card'] for v in peers]==same['questions']==topic['questions']
 assert all(v['id']==v['card']['id'] and v['topicId']==topic['id'] and v['sha256']==sha(v['card']) for v in peers)
 assert same['fileSHA256']==raw(C/same['path'])
 assert full['questionCount']==g['questionCount']==11000 and full['topicFileCount']==g['topicFileCount']==110
 assert full['rowsCanonicalSHA256']==g['rowsCanonicalSHA256']
 assert full['allCurrentFileByteBindings']==g['allCurrentFileByteBindings'] and len(full['allCurrentFileByteBindings'])==110
 rows=[]
 for b in full['allCurrentFileByteBindings']:
  assert raw(C/b['path'])==b['sha256'];t=read(C/b['path'])
  rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==g['rowsCanonicalSHA256']
 if 'rows' in g:assert g['rows']==rows
 assert 'sameTopicMAIN' not in ps and 'sourceInventoryPath' not in sp
 proof={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPath':g['sourceInventoryPath'],'originalFileSHA256':g['sourceInventoryFileSHA256'],'operation':'Exact explicit path/fileSHA and original ordered100 full bodies,110 live file digests,11000 MAIN digest verified. Redundant digest/container names and absolute path only; raw, literals, grounds and judgments unchanged.'}
 g.update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['sameTopicMAIN']={**same,'sourceInventoryPath':str(p),'sourceInventorySHA256':raw(p)}
 sp.update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['technicalExplicitInventoryFileDigestAlias']=proof
def alias_explicit_fresh_inventory_context(candidate,sp,ps,R):
 """Expose an explicit SHA/pointer-bound full snapshot; keep assessed peers distinct."""
 if 'sameTopicMAIN' in ps or 'freshInventory' not in ps:return
 import copy
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0 and len(candidate['entries'])==1
 e=candidate['entries'][0];b=ps['freshInventory'];p=pathlib.Path(b['path']);p=p if p.is_absolute() else C/p
 compact_binding='fileSHA256' not in b
 original_compact_binding=copy.deepcopy(b)
 if compact_binding:
  assert set(b)=={'path','sha256'} and p.is_relative_to(R) and raw(p)==b['sha256']
  b.update(fileSHA256=b['sha256'],globalMAINPointer='/globalMAIN',sameTopicMAINPointer='/sameTopicMAIN',actualCurrentPeersPointer='/actualCurrentPeers')
 assert p.is_relative_to(R) and raw(p)==b['fileSHA256']
 assert b['globalMAINPointer']=='/globalMAIN' and b['sameTopicMAINPointer']=='/sameTopicMAIN' and b['actualCurrentPeersPointer']=='/actualCurrentPeers'
 inv=read(p);g=inv['globalMAIN'];same=inv['sameTopicMAIN'];full=inv['actualCurrentPeers'];topic=read(C/same['path'])
 if compact_binding:
  assert set(g)=={'rows','rowsCanonicalSHA256','topicFileCount','questionCount','allCurrentFileByteBindings'}
  assert set(g)-{'rows'}<=set(ps['globalMAIN'])
  assert all(ps['globalMAIN'][k]==v for k,v in g.items() if k in ps['globalMAIN'])
  assert len(g['rows'])==11000 and sha(g['rows'])==g['rowsCanonicalSHA256']
  ps['globalMAIN']['rows']=copy.deepcopy(g['rows'])
  ps['technicalCompactFreshInventoryBinding']={'originalBinding':original_compact_binding,'inventoryPath':str(p),'inventorySHA256':raw(p),'operation':'Exact explicit whole-file path/SHA binds standard generated globalMAIN/sameTopicMAIN/actualCurrentPeers containers. Only redundant digest/pointer names and already SHA-bound machine rows exposed. Original eight/relevant peer judgments and extra query metadata retained; no raw or semantic change.'}
 else:assert g==ps['globalMAIN']
 assert g['topicFileCount']==110 and g['questionCount']==11000
 assert same['topicId']==topic['id']==e['topicId'] and same['questionCount']==len(full)==100
 assert same['fileSHA256']==raw(C/same['path']) and same['questions']==topic['questions']
 assert [v['sourceOrder'] for v in full]==list(range(1,101)) and [v['card'] for v in full]==topic['questions']
 assert all(v['id']==v['card']['id'] and v['topicId']==e['topicId'] and v['sha256']==sha(v['card']) for v in full)
 mapping={v['id']:v for v in full};assessed=ps['actualCurrentPeers'];assert assessed and isinstance(assessed,list)
 for v in assessed:
  bound=mapping[v['id']]
  assert v['topicId']==bound['topicId'] and v['sourceOrder']==bound['sourceOrder'] and v['card']==bound['card'] and v['sha256']==bound['sha256']
 assert len(g['allCurrentFileByteBindings'])==110
 for v in g['allCurrentFileByteBindings']:assert raw(C/v['path'])==v['sha256']
 assert 'sourceInventoryPath' not in sp and 'sourceInventoryPath' not in ps['globalMAIN']
 ps['sameTopicMAIN']=copy.deepcopy(same)
 ps['sameTopicMAIN'].update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['globalMAIN'].update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 sp.update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['technicalExplicitFreshInventoryContextAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPointer':'/freshInventory','inventoryPath':str(p),'inventorySHA256':raw(p),'assessedPeerCountUnchanged':len(assessed),'fullSnapshotCards':100,'operation':'Original explicit path/fileSHA and three pointers bind the full100 machine snapshot and identical110/11000 global bindings. Original assessed peers unchanged; no invented peer judgment or raw edit. Original preservation assertion remains uncured.'}
def alias_explicit_cross_topic_peers(candidate,sp,ps,R):
 """Keep explicit foreign-topic peer bodies in the validator's peer container."""
 if 'crossCatalogClosestFullBodies' in ps:return
 containers=[k for k in ['actualRelevantCrossTopicPeers','relevantCrossTopicPeers','crossTopicCurrentPeers','relevantCrossTopicCurrentPeers'] if k in ps]
 if not containers:return
 assert len(containers)==1
 container=containers[0]
 import copy
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 peers=copy.deepcopy(ps[container]);position_aliases=[]
 for peer in peers:
  if 'sha256' not in peer:
   assert peer['canonicalSHA256']==sha(peer['card'])
   peer['sha256']=peer['canonicalSHA256']
   peer['technicalExplicitCanonicalDigestNameAlias']='Identical declared full-card canonical digest exposed under redundant sha256 name; original raw/ground unchanged. Original KeyError bf45bf uncured.'
  t=read(C/('src/content/topics/'+peer['topicId']+'.json'))
  if 'sourceOrder' not in peer:
   matches=[(i,q) for i,q in enumerate(t['questions'],1) if q['id']==peer['id']]
   assert len(matches)==1
   position,q=matches[0]
   assert peer['card']==q and peer['sha256']==sha(q)
   peer['sourceOrder']=position
   position_aliases.append({'id':peer['id'],'topicId':peer['topicId'],'sourceOrder':position,'originalCardAndHashExact':True})
  q=t['questions'][peer['sourceOrder']-1]
  assert peer['id']==q['id'] and peer['card']==q and peer['sha256']==sha(q)
 ps['crossCatalogClosestFullBodies']=peers
 if position_aliases:ps['technicalExactCrossTopicPositionAlias']={'bindings':position_aliases,'operation':'Position derived only from unique exact original ID plus full body/hash in CURRENT. Original container/raw and semantic assessments unchanged; original root KeyError uncured.'}
 ps['technicalCrossTopicContainerAlias']={'rawPeerSnapshot':str(pathlib.Path(R)/'peer-snapshot.json'),'rawPeerSHA256':raw(pathlib.Path(R)/'peer-snapshot.json'),'originalPointer':'/'+container,'operation':'Exact original explicit foreign-topic full bodies and hashes verified against CURRENT, redundant container name only; raw and bilateral assessments unchanged.'}
def alias_explicit_inventory_binding(candidate,sp,ps,R):
 """Expose only the author's explicit SHA-bound inventory; raw stays immutable."""
 if 'sameTopicMAIN' in ps or 'inventoryBinding' not in ps:return
 import copy
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 cycle=candidate['cycle'];assert cycle==sp['cycle']==ps['cycle'] and cycle in [0,1]
 if cycle==1:
  assert R.name.endswith('-cycle1')
  prior=read(R.with_name(R.name.removesuffix('-cycle1'))/'candidate.json')
  current=candidate['entries'][0];original=prior['entries'][0]
  assert prior['cycle']==0 and prior['sourceNativeId']==candidate['sourceNativeId']
  assert current['id']==original['id'] and current['beforeCard']==original['proposedCard']
  assert current['beforeHash']==original['afterHash']==sha(current['beforeCard'])
  initial=read(D/f"independent-{current['topicId']}{current['sourceOrder']}-initial/receipt.json")['entries'][0]
  assert initial['status']=='FIX' and initial['currentCard']==current['beforeCard']
 e=candidate['entries'][0];b=ps['inventoryBinding'];p=pathlib.Path(b['path'])
 if not p.is_absolute():
  original_path=b['path'];p=C/p
  assert p.is_relative_to(R) and p.is_file() and raw(p)==b.get('fileSHA256',b.get('sha256'))
  b['path']=str(p)
  ps['technicalExplicitInventoryPathAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPath':original_path,'absolutePath':str(p),'operation':'Exact declared repository-relative inventory path resolved within owned raw packet; original digest and all live inventory assertions retained. Raw bytes and grounds unchanged.'}
 if 'sha256' not in b and 'fileSHA256' in b:
  assert p.is_relative_to(R) and raw(p)==b['fileSHA256']
  inv=read(p);same=inv['sameTopicMAIN'];g=inv['globalMAIN']
  peers=ps['actualCurrentPeers'];topic=read(C/same['path'])
  assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101))
  assert [v['card'] for v in peers]==same['questions']==topic['questions']
  assert all(v['topicId']==topic['id'] and v['id']==v['card']['id'] and v['sha256']==sha(v['card']) for v in peers)
  assert same['topicId']==e['topicId']==topic['id'] and same['fileSHA256']==raw(C/same['path'])
  assert g['questionCount']==11000 and g['topicFileCount']==110
  assert g['rowsCanonicalSHA256']==ps['globalMAIN']['rowsCanonicalSHA256']
  assert g['allCurrentFileByteBindings']==ps['globalMAIN']['allCurrentFileByteBindings']
  ps['originalExplicitFileSHA256InventoryBinding']=copy.deepcopy(b)
  b={**b,'sha256':b['fileSHA256'],'topicCards':100,'globalMAINRows':11000,'globalTopicFiles':110,'topicFileSHA256':same['fileSHA256']}
  ps['inventoryBinding']=b
  ps['technicalExplicitFileSHA256InventoryBindingAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'originalPointer':'/inventoryBinding','operation':'Exact explicit fileSHA256-bound inventory plus original ordered100 full peers and live topic bytes; redundant names/count projections only. Original binding retained, no raw or judgment edit.'}
 assert p.is_relative_to(R) and raw(p)==b['sha256']
 inv=read(p);same=inv['sameTopicMAIN'];g=inv['globalMAIN'];topic=read(C/same['path'])
 assert same['topicId']==e['topicId']==topic['id']
 assert same['questions']==topic['questions'] and same['questionCount']==b['topicCards']==100
 assert same['fileSHA256']==b['topicFileSHA256']==raw(C/same['path'])
 assert g['questionCount']==b['globalMAINRows']==11000 and g['topicFileCount']==b['globalTopicFiles']==110
 assert g['rowsCanonicalSHA256']==ps['globalMAIN']['rowsCanonicalSHA256']
 assert g['allCurrentFileByteBindings']==ps['globalMAIN']['allCurrentFileByteBindings']
 rows=[]
 for f in g['allCurrentFileByteBindings']:
  assert raw(C/f['path'])==f['sha256'];t=read(C/f['path'])
  rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==g['rowsCanonicalSHA256']
 assert 'rows' not in ps['globalMAIN'] or ps['globalMAIN']['rows']==rows
 ps['sameTopicMAIN']=copy.deepcopy(same)
 sp.update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['globalMAIN'].update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 if 'crossTopicCurrentPeers' in ps:
  assert 'crossCatalogClosestFullBodies' not in ps
  ps['crossCatalogClosestFullBodies']=copy.deepcopy(ps['crossTopicCurrentPeers'])
 ps['technicalExplicitInventoryBindingAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPointer':'/inventoryBinding','inventoryPath':str(p),'inventorySHA256':raw(p),'operation':'Exact original path/SHA and full100/110/11000 live bindings expose redundant container names only. Original peers, cross-topic bodies, assessments and raw remain unchanged; no new ground or quality credit.'}
def alias_explicit_root_candidate(candidate,sp,ps,R):
 """Expose an explicit own single-card root as entries[0]; raw stays immutable."""
 if 'entries' in candidate:return
 import copy
 R=pathlib.Path(R);x=read(D/'manifest.json');uid=candidate['sourceNativeId']
 assert R.parent==D and uid in x['createdNativeThreadsCurrentOwner']
 assert candidate['sourceOrder'] in x['ownedSourceOrders']
 assert uid==sp['sourceNativeId']==ps['sourceNativeId']
 cycle=candidate['cycle'];assert cycle==sp['cycle']==ps['cycle']
 if cycle==1:
  # Only this exact preserved directed98 raw triple may use the root-field alias.
  assert R.name=='source-human-medicine98-cycle1' and uid=='01a16bce-a09e-7252-975d-487bfcf95800'
  expected={'candidate.json':'b19c4348595fbd7096bdaa0d1e4e121950bc424f57eb1a570f3fffc1dd993de7','sourceproof.json':'b73046af4cde0ca8d266712b1a899fbeb07dfd36f532eda51c913cc7cb757376','peer-snapshot.json':'f14554d7c89975d837ffe5df7ae3450efbec5df16aa5d6c5731fea2b959955f5'}
  import subprocess
  for name,digest in expected.items():
   assert raw(R/name)==digest
   assert (R/name).read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(C),'show','8dd60f49c2e7ed5a99d3352e56c54daba612748f:'+str((R/name).relative_to(C))])
  initial=read(D/'independent-human-medicine98-initial/receipt.json')['entries'][0]
  prior=read(D/'qualified-source-human-medicine98/candidate.json')['entries'][0]
  assert initial['stage']=='INITIAL' and initial['status']=='FIX' and initial['defects']
  assert candidate['id']==initial['id']==prior['id']=='human-medicine-ext-prolactin'
  assert candidate['beforeCard']==initial['currentCard']==prior['proposedCard']
  assert candidate['beforeHash']==initial['currentCardCanonicalSHA256']==prior['afterHash']==sha(candidate['beforeCard'])
  candidate['technicalExact98Cycle1RootAliasGuard']={'rawFreeze':'8dd60f49c2e7ed5a99d3352e56c54daba612748f','rawCriticalSHA256':expected,'originalFormatGapUncured':True,'operation':'Only exact same-author solecycle1 with beforeCard bound to its own INITIAL FIX and prior proposal. Existing root-field alias below, no new literal, source or judgment.'}
 else:assert cycle==0
 assert len(sp['entries'])==1
 keys=['id','topicId','sourceOrder','status','beforeCard','beforeHash','proposedCard','afterHash','fieldGroups']
 e={k:copy.deepcopy(candidate[k]) for k in keys};q=e['proposedCard'];b=e['beforeCard']
 if 'id' not in ps:
  own_peers=[(i,p) for i,p in enumerate(ps['actualCurrentPeers']) if p['id']==e['id']]
  assert len(own_peers)==1
  peer_index,peer=own_peers[0]
  assert peer['card']==b and peer['sha256']==e['beforeHash']==sha(b) and peer['topicId']==e['topicId'] and peer['sourceOrder']==e['sourceOrder']
  ps['id']=peer['id']
  ps['technicalExplicitRootIdAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalRootIdAbsent':True,'originalSelfPreimagePointer':'/actualCurrentPeers/'+str(peer_index),'operation':'Expose the identical ID from the unique explicit full-before-body/hash/topic/order-bound peer. Existing root ID assertion retained; no guessed identity, raw change or new judgment.'}
 assert e['id']==b['id']==q['id']==sp['entries'][0]['id']==ps['id']
 assert e['topicId']==sp['topicId']==ps['topicId']
 if 'sourceOrder' not in ps:
  own_peers=[(i,p) for i,p in enumerate(ps['actualCurrentPeers']) if p['id']==e['id']]
  assert len(own_peers)==1
  peer_index,peer=own_peers[0]
  assert peer['card']==b and peer['sha256']==e['beforeHash']==sha(b) and peer['topicId']==e['topicId'] and peer['sourceOrder']==e['sourceOrder']
  ps['sourceOrder']=peer['sourceOrder']
  ps['technicalExplicitRootOrderAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalRootOrderAbsent':True,'originalSelfPreimagePointer':'/actualCurrentPeers/'+str(peer_index),'operation':'Expose the identical sourceOrder from the unique explicit ID/full-before-body/hash/topic-bound peer. Existing root order assertion retained; no guessed identity, raw change or new judgment.'}
 if 'sourceOrder' not in sp:
  declared=sp['entries'];assert len(declared)==1
  se=declared[0]
  assert se['id']==sp['id']==e['id'] and se['topicId']==sp['topicId']==e['topicId']
  assert se['sourceOrder']==e['sourceOrder'] and se['status']==sp['status']==e['status']
  assert len(se['literalGroups'])==6 and len(se['fourFullPromptAnswerNoteAssessments'])==4
  sp['sourceOrder']=se['sourceOrder']
  sp['technicalExplicitEntryOrderAlias']={'rawSourceproof':str(R/'sourceproof.json'),'rawSHA256':raw(R/'sourceproof.json'),'originalPointer':'/entries/0/sourceOrder','originalRootOrderAbsent':True,'operation':'Exact sole entry ID/topic/order/status agrees with candidate and native identity; redundant root order name only. Original raw, groups and judgments unchanged; original KeyError uncured.'}
 assert e['sourceOrder']==sp['sourceOrder']==ps['sourceOrder']
 assert e['status']==sp['entries'][0]['status']
 assert sha(b)==e['beforeHash'] and sha(q)==e['afterHash']
 assert len(e['fieldGroups'])==6 and len(sp['entries'][0]['literalGroups'])==6
 assert len(sp['entries'][0]['fourFullPromptAnswerNoteAssessments'])==4
 candidate['entries']=[e]
 candidate['technicalExplicitRootCandidateAlias']={'rawPath':str(R/'candidate.json'),'rawSHA256':raw(R/'candidate.json'),'originalRootFields':keys,'operation':'Exact explicit root single-card fields deep-copied to entries[0]; original root retained. No new literal, hash, source, judgment or status. Original format deviation remains uncured.'}
def save(root,ref,files,message):
 paths=sorted(set(str(pathlib.Path(p).relative_to(root)) for p in files));idx=root/h.git(root,'rev-parse','--git-path','index');expected=read(D/'manifest.json')['foreignIndexes']['planning' if root==P else 'code'];assert raw(idx)==expected, 'Foreign index differs from exact task boundary';return h.save(root,ref,paths,message,expected)
def savecode(files,message):return save(C,'refs/heads/codex/question-quality-wave-6',files,message)
def alias_explicit_global_inventory_file(candidate,sp,ps,R):
 """Expose an already explicit global inventory file binding; raw stays immutable."""
 g=ps.get('globalMAIN',{})
 if 'inventoryPath' not in g or 'inventoryFileSHA256' not in g:return
 if 'questions' in ps.get('sameTopicMAIN',{}):return
 import copy
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']
 e=candidate['entries'][0];p=pathlib.Path(g['inventoryPath']);p=p if p.is_absolute() else C/p
 assert p.is_relative_to(R) and raw(p)==g['inventoryFileSHA256']
 inv=read(p);full=inv['globalMAIN'];same=inv['sameTopicMAIN'];peers=inv['actualCurrentPeers']
 assert same['topicId']==e['topicId'] and same['questionCount']==100
 topic=read(C/same['path']);assert topic['id']==e['topicId']
 assert same['fileSHA256']==raw(C/same['path']) and same['questions']==topic['questions']
 assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101))
 assert [v['card'] for v in peers]==topic['questions']
 assert all(v['topicId']==e['topicId'] and v['id']==v['card']['id'] and v['sha256']==sha(v['card']) for v in peers)
 assert full['topicFileCount']==g['topicFileCount']==110 and full['questionCount']==g['questionCount']==11000
 assert full['rowsCanonicalSHA256']==g['rowsCanonicalSHA256']
 assert full['allCurrentFileByteBindings']==g['allCurrentFileByteBindings']
 rows=[]
 for b in full['allCurrentFileByteBindings']:
  assert raw(C/b['path'])==b['sha256'];t=read(C/b['path'])
  rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==full['rowsCanonicalSHA256'] and full['rows']==rows
 byid={v['id']:v for v in peers};assessed=copy.deepcopy(ps['actualCurrentPeers'])
 foreign=[]
 for v in assessed:
  if v['topicId']==e['topicId']:
   b=byid[v['id']];assert all(v[k]==b[k] for k in ['id','topicId','sourceOrder','card','sha256'])
  else:
   t=read(C/('src/content/topics/'+v['topicId']+'.json'));q=t['questions'][v['sourceOrder']-1]
   assert v['id']==q['id'] and v['card']==q and v['sha256']==sha(q)
   foreign.append(copy.deepcopy(v))
 if foreign:
  existing=ps.setdefault('crossCatalogClosestFullBodies',[])
  for v in foreign:
   matches=[p for p in existing if p['id']==v['id']]
   if matches:assert len(matches)==1 and matches[0]['card']==v['card'] and matches[0]['sha256']==v['sha256']
   else:existing.append(v)
 assert ps['sameTopicMAIN']['questionCount']==100
 original_same=copy.deepcopy(ps['sameTopicMAIN'])
 for k in ['path','topicId','fileSHA256','questionCount']:
  if k in original_same:assert original_same[k]==same[k]
 for k,value in [('inventoryPath',str(p)),('inventoryFileSHA256',raw(p))]:
  if k in original_same:assert original_same[k]==value
 if original_same.get('rowsCanonicalSHA256') is not None:
  projected=[{'topicId':e['topicId'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in same['questions']]
  assert original_same['rowsCanonicalSHA256'] in [sha(same['questions']),sha(projected)]
 for k in ['sourceInventoryPath','sourceInventorySHA256']:assert k not in sp
 ps['originalRelevantCurrentPeers']=assessed
 ps['actualCurrentPeers']=copy.deepcopy(peers)
 ps['sameTopicMAIN']={**copy.deepcopy(same),'sourceInventoryPath':str(p),'sourceInventorySHA256':raw(p)}
 g.update(rows=copy.deepcopy(rows),sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 sp.update(sourceInventoryPath=str(p),sourceInventorySHA256=raw(p))
 ps['technicalExplicitGlobalInventoryFileAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalGlobalPathPointer':'/globalMAIN/inventoryPath','originalGlobalDigestPointer':'/globalMAIN/inventoryFileSHA256','inventoryPath':str(p),'inventoryFileSHA256':raw(p),'originalSameTopicContainer':original_same,'assessedPeerCountUnchanged':len(assessed),'machineBindings':100,'operation':'Exact original explicit path/file digest binds generated full100/110/11000 inventory. Full machine bodies exposed separately from unchanged assessed peers. No new body, hash hydration, source, semantic judgment, raw edit or quality credit.'}
def saveplan(files,message):
 with flow.locked():flow.lease('acquire','planning',O)
 try:return save(P,'refs/heads/codex/question-revision-resume-20261014',files,message)
 finally:
  with flow.locked():flow.lease('release','planning',O)

def alias_full_prompt_answer_concatenation(candidate,sp):
 e=candidate['entries'][0];q=e['proposedCard'];entry=sp['entries'][0]
 variants=entry['fourFullPromptAnswerNoteAssessments']
 if all(v['fullPrompt']==q['prompt'] for v in variants):return
 assert len(variants)==4 and {v['slot'] for v in variants}==set(range(4))
 assert sha(q)==e['afterHash']
 group={'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 assert e['fieldGroups']['prompt_ordered_answers_key']['afterCanonicalSHA256']==sha(group)
 literal=next(g for g in entry['literalGroups'] if g['group']=='prompt_ordered_answers_key')
 assert literal['literal']==group and literal['literalSHA256']==sha(group)
 for v in variants:
  a=q['answers'][v['slot']]
  assert v['answer']==a['text'] and v['note']==a['note']
  triple={'prompt':q['prompt'],'answer':a['text'],'note':a['note']}
  assert v['tripleSHA256']==sha(triple)
  assert v['fullPrompt']==q['prompt']+' '+a['text']
  v['originalPromptAnswerConcatenationLiteral']=v['fullPrompt']
  v['technicalRedundantPromptAnswerDecomposition']={'originalCanonicalSHA256':sha(v['fullPrompt']),'candidatePromptCanonicalSHA256':sha(q['prompt']),'alreadyDeclaredTripleSHA256':v['tripleSHA256'],'operation':'Exact prompt + one ASCII space + exact separately bound answer; invertible redundant serialization decomposition only. Original literal retained; no answer, note, hash, primary ground or assessment changed.'}
  v['fullPrompt']=q['prompt']

def alias_explicit_nested_inventory(candidate,sp,ps,R):
 """Lossless derived view of explicit SHA-bound inventory and original100 peers."""
 if 'globalMAIN' in ps or 'globalMAINRetrieval' not in ps:return
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']
 g=ps['globalMAINRetrieval'];b=sp['freshInventoryBinding'];i=ps['immutableInventoryRaw']
 assert g['path']==b['path']==i['path'] and g['inventoryFileSHA256']==b['sha256']==i['sha256']
 path=pathlib.Path(g['path']);path=path if path.is_absolute() else C/path
 assert path.is_relative_to(R) and raw(path)==i['sha256']
 inv=read(path);full=inv['globalMAIN'];same=ps['sameTopicMAIN'];retained=same['actualCurrentPeers']
 assert g['topicFileCount']==full['topicFileCount']==110 and g['questionCount']==full['questionCount']==11000
 assert g['rowsCanonicalSHA256']==full['rowsCanonicalSHA256']==b['globalRowsCanonicalSHA256']
 assert len(full['allCurrentFileByteBindings'])==110
 rows=[]
 for f in full['allCurrentFileByteBindings']:
  assert raw(C/f['path'])==f['sha256']
  t=read(C/f['path']);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==full['rowsCanonicalSHA256']
 topic=read(C/same['path']);assert len(retained)==same['questionCount']==100
 assert [e['sourceOrder'] for e in retained]==list(range(1,101))
 assert [e['card'] for e in retained]==inv['sameTopicMAIN']['questions']==topic['questions']
 assert all(e['topicId']==topic['id'] and e['id']==e['card']['id'] and sha(e['card'])==e['sha256'] for e in retained)
 assert same['fileSHA256']==inv['sameTopicMAIN']['fileSHA256']==b['sameTopicFileSHA256']==raw(C/same['path'])
 ps['globalMAIN']={**full,'sourceInventoryPath':str(path),'sourceInventorySHA256':raw(path)}
 ps['actualCurrentPeers']=retained
 same.update(questions=[e['card'] for e in retained],sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 sp.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 ps['technicalExplicitNestedInventoryAlias']={'originalPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'inventoryPath':str(path),'inventorySHA256':raw(path),'operation':'Exact explicit three-way path/SHA and live110/11000/100 bindings; nested original full peers aliased only, no new semantic assessment. Original relevantPairs retained.'}

def alias_single_sourceproof_entry(candidate,sp):
 """Alias a native-bound singular entry without changing author raw or grounds."""
 if 'entries' in sp:return
 if 'entry' not in sp:return
 assert len(candidate['entries'])==1 and isinstance(sp['entry'],dict)
 assert candidate['sourceNativeId']==sp['sourceNativeId'] and candidate['cycle']==sp['cycle']
 c=candidate['entries'][0];e=sp['entry'];q=c['proposedCard']
 assert e['id']==c['id']==q['id'] and e['topicId']==c['topicId']==sp['topicId']==candidate['topicId']
 assert e['sourceOrder']==c['sourceOrder'] and e['status']==c['status']
 assert len(e['literalGroups'])==6 and len(e['fourFullPromptAnswerNoteAssessments'])==4
 assert {v['slot'] for v in e['fourFullPromptAnswerNoteAssessments']}==set(range(4))
 for v in e['fourFullPromptAnswerNoteAssessments']:
  a=q['answers'][v['slot']];assert v['fullPrompt']==q['prompt'] and v['answer']==a['text'] and v['note']==a['note']
 sp['entries']=[json.loads(json.dumps(e,ensure_ascii=False))]
 assert sp['entries'][0]==e
 sp['technicalSingleEntryContainerAlias']={'originalKey':'entry','originalEntryCanonicalSHA256':sha(e),'sourceNativeId':sp['sourceNativeId'],'cycle':sp['cycle'],'operation':'Exact native/cycle/ID/topic/order/status and original six/four literals bound to candidate; singular original entry retained unchanged, deep-copied as entries[0]. No hydration, new ground, or raw edit.'}

def alias_serialized_prompt_group(candidate,sp):
 """Decode only exact canonical JSON serializations of the six bound literals."""
 alias_single_sourceproof_entry(candidate,sp)
 e=candidate['entries'][0];q=e['proposedCard'];expected={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in sp['entries'][0].get('literalGroups',[]):
  target=expected[g['group']]
  if g['literal']==target or not isinstance(g['literal'],str) or not g['literal'].startswith(('{','"')):continue
  original=g['literal'];assert json.loads(original)==target
  assert original==json.dumps(target,ensure_ascii=False,sort_keys=True,separators=(',',':'))
  assert hashlib.sha256(original.encode()).hexdigest()==g['literalSHA256']==e['fieldGroups'][g['group']]['afterCanonicalSHA256']==sha(target)
  g.update(originalSerializedLiteral=original,originalSerializedLiteralSHA256=g['literalSHA256'],literal=target,literalSHA256=sha(target),technicalSerializedGroupAlias='Canonical JSON serialization of exact bound literal decoded to identical object/string; raw immutable, all values/grounds unchanged.')

def alias_full_body_wrapper_digests(ps,R):
 same=ps.get('sameTopicMAIN',{});wrappers=same.get('questions',[])
 if len(wrappers)!=100 or not all(isinstance(w,dict) and 'card' in w for w in wrappers):return
 if all('sha256' in w for w in wrappers):return
 path=C/same['path'];topic=read(path)
 assert same['questionCount']==100 and same['fileSHA256']==raw(path)
 assert [w['sourceOrder'] for w in wrappers]==list(range(1,101))
 assert [w['card'] for w in wrappers]==topic['questions']
 assert all(w['id']==w['card']['id'] and w['topicId']==topic['id'] for w in wrappers)
 for w in wrappers:
  if 'sha256' in w:assert w['sha256']==sha(w['card'])
  else:w.update(sha256=sha(w['card']),technicalDerivedBodyDigest='Exact original full card body, id, sourceOrder, topic path and fileSHA verified against live entire100; digest computed, raw untouched.')
 ps['technicalFullBodyWrapperDigestAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'topicFileSHA256':raw(path),'orderedFullBodiesVerified':100,'operation':'Deterministic digest of explicit unchanged full bodies; no new peer assessment or unbound hydration.'}

def alias_explicit_peer_inventory_projection(candidate,sp,ps,R):
 """Recover only explicit SHA-bound full bodies behind author MAIN projections."""
 if not isinstance(ps.get('actualCurrentPeers'),int):return
 if not all(k in ps for k in ['freshInventoryPath','freshInventorySHA256','fullClosestCurrentPeers']):return
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 e=candidate['entries'][0];same=ps['sameTopicMAIN'];global_audit=ps['globalMAIN']
 path=pathlib.Path(ps['freshInventoryPath']);path=path if path.is_absolute() else C/path
 assert path.is_relative_to(R) and raw(path)==ps['freshInventorySHA256']
 inv=read(path);full=inv['sameTopicMAIN']['questions'];topic=read(C/same['path'])
 assert inv['sameTopicMAIN']['topicId']==same['topicId']==e['topicId']==topic['id']
 assert ps['actualCurrentPeers']==same['questionCount']==len(full)==len(topic['questions'])==100
 assert full==topic['questions']
 assert same['fileSHA256']==inv['sameTopicMAIN']['fileSHA256']==raw(C/same['path'])
 def projection(q):return {'topicId':topic['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 assert same['questions']==[projection(q) for q in full]
 assert global_audit['topicFileCount']==inv['globalMAIN']['topicFileCount']==110
 assert global_audit['questionCount']==inv['globalMAIN']['questionCount']==11000
 assert global_audit['rowsCanonicalSHA256']==inv['globalMAIN']['rowsCanonicalSHA256']
 assert global_audit['allCurrentFileByteBindings']==inv['globalMAIN']['allCurrentFileByteBindings']
 assert len(global_audit['allCurrentFileByteBindings'])==110
 for f in global_audit['allCurrentFileByteBindings']:assert raw(C/f['path'])==f['sha256']
 mapping={q['id']:q for q in full};relevant=ps['fullClosestCurrentPeers'];assert relevant
 for peer in relevant:
  assert peer['topicId']==topic['id'] and peer['card']==mapping[peer['id']]
  assert peer['card']==full[peer['sourceOrder']-1] and sha(peer['card'])==peer['sha256']
 same['originalMAINProjectionQuestions']=same['questions'];same['questions']=json.loads(json.dumps(full,ensure_ascii=False))
 ps['originalActualCurrentPeerInventoryCount']=ps['actualCurrentPeers'];ps['actualCurrentPeers']=json.loads(json.dumps(relevant,ensure_ascii=False))
 global_audit.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 same.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 sp.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 ps['technicalExplicitProjectedTopicSnapshotAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'inventoryPath':str(path),'inventorySHA256':raw(path),'operation':'Exact original top-level path/SHA,100MAIN projections,110filebindings,11000rowdigest and same-topic fileSHA bind the full100 bodies already retained by this author. Inventory count100 is not assessed-peer credit; only original fullClosestCurrentPeers are substantive peers. No unbound hydration, new peer assessment, literal or source ground.'}


def alias_source83_clarified_literals(candidate,sp,ps,R):
 """Bind two author-clarified literal copies; original raw and grounds stay intact."""
 if candidate['entries'][0]['topicId']!='history-russia':return
 if candidate['entries'][0]['sourceOrder']!=83 or candidate.get('cycle')!=0:return
 R=pathlib.Path(R);assert R==D/'source-history-russia83'
 uid='01a1627c-8cb4-7b52-b8b1-7f6752217e7f'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 cp=R/'literal-binding-clarification.json';clar=read(cp)
 assert clar['sourceNativeId']==uid and clar['networkCalls']==clar['cycle']==clar['qualityCredit']==0
 freeze='463701e1cb541566022b1f042f32981a6153b761'
 for name,proof in clar['originalPacketFiles'].items():
  p=R/name;assert raw(p)==proof['sha256']
  assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
 e=candidate['entries'][0];assert sha(e['proposedCard'])==e['afterHash']==clar['originalPacketFiles']['candidate.json']['afterHash']
 if isinstance(e['fieldGroups'],list):
  original=e['fieldGroups'];assert len(original)==6 and {g['group'] for g in original}=={'prompt_ordered_answers_key','explanation','note0','note1','note2','note3'}
  assert all(set(g)=={'group','beforeCanonicalSHA256','afterCanonicalSHA256'} for g in original)
  e['originalFieldGroupsList']=original
  e['fieldGroups']={g['group']:{k:v for k,v in g.items() if k!='group'} for g in original}
  e['technicalFieldGroupsListAlias']='Six explicit distinct named before/after hash entries projected to dictionary; original ordered list retained unchanged.'
 def pointer(value,path):
  for key in path.split('/')[1:]:value=value[int(key)] if isinstance(value,list) else value[key]
  return value
 assert {v['group'] for v in clar['bindings']}=={'explanation','note2'} and len(clar['bindings'])==2
 for b in clar['bindings']:
  g=pointer(sp,b['originalSourceproofPointer']);literal=pointer(candidate,b['existingCandidatePointer'])
  assert g['group']==b['group'] and g['literal']==b['originalLiteral'] and g['literalSHA256']==b['originalLiteralSHA256']==sha(g['literal'])
  assert g['primaryGround']==b['unchangedPrimaryGround'] and g['sourcePaths']==b['unchangedSourcePaths'] and g['locator']==b['unchangedLocator']
  assert literal==b['intendedLiteral'] and sha(literal)==b['intendedLiteralSHA256']==e['fieldGroups'][b['group']]['afterCanonicalSHA256']
  if b['group']=='note2':
   assert pointer(sp,b['existingVariantPointer'])['note']==literal
   assert pointer(sp,b['existingCorrectNoteNewFactPointer'])['newFact']==literal
  g['originalLiteralBindingBeforeClarification']={'literal':g['literal'],'literalSHA256':g['literalSHA256']}
  g.update(literal=literal,literalSHA256=sha(literal))
 sp['technicalAuthorClarifiedLiteralBinding']={'path':str(cp),'rawSHA256':raw(cp),'originalPacketFreeze':freeze,'temporalBoundary':clar['temporalBoundary'],'operation':'Two stale literal copies bound to already-emitted exact candidate and explicit author clarification. Original raw, all grounds/locators/source paths and judgments retained; no new source claim or quality credit.'}

def alias_source83_cycle1_redundant_snapshot(candidate,sp,ps,R):
 """Reconcile exact known shared apply; preserve historical full snapshot."""
 if candidate['entries'][0]['topicId']!='history-russia':return
 if candidate['entries'][0]['sourceOrder']!=83 or candidate.get('cycle')!=1:return
 R=pathlib.Path(R);assert R==D/'source-history-russia83-cycle1'
 uid='01a1627c-8cb4-7b52-b8b1-7f6752217e7f'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 freeze='f2941aeffbcbc0757507313f92b0ff8bcc57599c'
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=R/name;assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
 topic_path=C/'src/content/topics/history-russia.json';topic=read(topic_path);live=topic['questions']
 full=ps['actualCurrentPeers'];assert len(full)==6 and [v['sourceOrder'] for v in full]==[50,64,70,74,85,96]
 assert all(v['card']==live[v['sourceOrder']-1] for v in full)
 assert all(v['topicId']=='history-russia' and v['id']==v['card']['id'] and sha(v['card'])==v['sha256'] for v in full)
 assert len(ps['fullClosestCurrentPeers'])==6 and all(v['card']==next(q for q in live if q['id']==v['id']) for v in ps['fullClosestCurrentPeers'])
 batch=read(D/'source83-84-shared-apply.json')
 oldbytes=__import__('subprocess').check_output(['git','-C',str(C),'show',batch['baseline']+':src/content/topics/history-russia.json'])
 old=json.loads(oldbytes)['questions'];assert ps['sameTopicMAIN']['questions']==old
 assert ps['sameTopicMAIN']['fileSHA256']==hashlib.sha256(oldbytes).hexdigest()
 assert [i for i,(a,b) in enumerate(zip(old,live),1) if a!=b]==[83,84]
 derived=__import__('copy').deepcopy(old);applied_bindings=[]
 for order in [83,84]:
  app=read(D/f'qualified-source-history-russia{order}-apply.json')['applied'][0]
  assert old[order-1]==app['beforeCard'] and live[order-1]==app['proposedCard']
  derived[order-1]=app['proposedCard']
  applied_bindings.append({'path':str(D/f'qualified-source-history-russia{order}-apply.json'),'rawSHA256':raw(D/f'qualified-source-history-russia{order}-apply.json'),'beforeCanonicalSHA256':sha(app['beforeCard']),'afterCanonicalSHA256':sha(app['proposedCard'])})
 assert derived==live
 e=candidate['entries'][0];assert e['beforeCard']==live[82] and e['beforeHash']==sha(live[82])
 assert ps['candidate']['beforeCard']==live[82] and ps['candidate']['proposedCard']==e['proposedCard']
 bindings=ps['globalMAIN']['allCurrentFileByteBindings'];files=sorted((C/'src/content/topics').glob('*.json'));assert len(bindings)==len(files)==110
 assert [b['path'] for b in bindings]==[str(f.relative_to(C)) for f in files]
 rows=[]
 for b,f in zip(bindings,files):
  if f==topic_path:assert b['sha256']==hashlib.sha256(oldbytes).hexdigest()
  else:assert b['sha256']==raw(f)
  t=read(f);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
 proof={'originalRaw':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'rawFreeze':freeze,'historicalQuestionsPointer':'/sameTopicMAIN/questions','originalQuestionsCanonicalSHA256':sha(old),'explicitFreshRelevantPeersPointer':'/actualCurrentPeers','explicitFreshRelevantPeersCount':6,'currentQuestionsCanonicalSHA256':sha(derived),'oldTopicFileSHA256':hashlib.sha256(oldbytes).hexdigest(),'currentTopicFileSHA256':raw(topic_path),'knownSharedApply':str(D/'source83-84-shared-apply.json'),'exactAppliedBodyBindings':applied_bindings,'changedOrders':[83,84],'preapplicationOnly':True,'inventoryFileHydration':False,'operation':'Original cycle1 retains historical100 full bodies plus6 unchanged fresh relevant peers. Project only exact known applied83/84 before-to-after bodies into the historical full snapshot. All other98 bodies and110 file bindings proven unchanged. Original raw,6 relevant peer bodies and semantic comparisons/grounds remain unchanged. Original full100 is explicitly historical, not called fresh.'}
 ps['sameTopicMAIN']['questions']=derived
 ps['sameTopicMAIN']['fileSHA256']=raw(topic_path)
 next(b for b in bindings if b['path']=='src/content/topics/history-russia.json')['sha256']=raw(topic_path)
 ps['technicalRedundantSnapshotStageBinding']=proof;sp['technicalRedundantSnapshotStageBinding']=proof

def alias_source84_cycle1_variant_names(candidate,sp,ps,R):
 """Expose exact existing prompt and SHA-bound locator lists under contract names."""
 if candidate['entries'][0]['topicId']!='history-russia':return
 if candidate['entries'][0]['sourceOrder']!=84 or candidate.get('cycle')!=1:return
 R=pathlib.Path(R);assert R==D/'source-history-russia84-cycle1'
 uid='01a16282-713c-7aa3-b66b-ca02fb99d0e1'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=R/name;assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show','d0baf3be7a148345b6dca8f9363b706338353c88:'+str(p.relative_to(C))])
 q=candidate['entries'][0]['proposedCard'];sources={}
 for source in sp['rawSources']:
  p=pathlib.Path(source['path']);p=p if p.is_absolute() else C/p
  assert raw(p)==source['sha256'];sources[str(p)]=source['sha256']
 for v in sp['entries'][0]['fourFullPromptAnswerNoteAssessments']:
  a=q['answers'][v['slot']];assert v['prompt']==q['prompt'] and v['answer']==a['text'] and v['note']==a['note']
  assert v['tripleSHA256']==sha({'prompt':v['prompt'],'answer':v['answer'],'note':v['note']})
  assert 'fullPrompt' not in v and 'sourcePaths' not in v and 'locator' not in v
  paths=[];locators=[]
  for loc in v['sourcesLocators']:
   p=pathlib.Path(loc['path']);p=p if p.is_absolute() else C/p
   assert sources[str(p)]==loc['fileSHA256']==raw(p)
   paths.append(loc['path']);locators.append(loc['locator'])
  assert paths
  v.update(fullPrompt=v['prompt'],sourcePaths=list(dict.fromkeys(paths)),locator=' | '.join(locators))
 sp['technicalVariantFieldNameAlias']={'rawSourceproof':str(R/'sourceproof.json'),'rawSHA256':raw(R/'sourceproof.json'),'operation':'Exact existing prompt literal and explicit original SHA-bound source locator paths exposed as fullPrompt/sourcePaths/locator. Original prompt/sourcesLocators and every judgment retained unchanged. Unchanged INITIAL reader judgments remain attributed to original reader, not claimed as new independent author review.'}

def alias_source77_own_prior_application(candidate,sp,ps,R):
 """Exact own77 preapplication bookkeeping delta; no inventory-file hydration."""
 if candidate['entries'][0]['topicId']!='history-russia':return
 if candidate.get('cycle')!=1 or candidate['entries'][0]['sourceOrder']!=77:return
 R=pathlib.Path(R);assert R.parent==D and R.name=='source-history-russia77-cycle1'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId'] and sp['cycle']==ps['cycle']==1
 import copy
 files=sorted((C/'src/content/topics').glob('*.json'));assert len(files)==110
 live={};live_rows=[]
 def project(t,q):return {'topicId':t,'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 for f in files:
  t=read(f);live[t['id']]=t;live_rows.extend(project(t['id'],q) for q in t['questions'])
 assert len(live_rows)==11000
 if ps['globalMAIN']['rowsCanonicalSHA256']==sha(live_rows):return
 I=R.with_name('source-history-russia77');initial=read(I/'candidate.json');oldps=read(I/'peer-snapshot.json');e0=initial['entries'][0];e=candidate['entries'][0]
 assert initial['sourceNativeId']==candidate['sourceNativeId'] and initial['cycle']==0
 assert e['id']==e0['id']=='history-russia-constitution-1993-method' and e['beforeCard']==e0['proposedCard'] and sha(e['beforeCard'])==e0['afterHash']
 only=copy.deepcopy(e['proposedCard']);assert only['answers'][2]['text']=='Всенародным голосованием';only['answers'][2]['text']='Всенародное голосование';assert only==e['beforeCard']
 assert ps['candidate']['beforeCard']==e['beforeCard'] and ps['candidate']['proposedCard']==e['proposedCard']
 assert ps['globalMAIN']==oldps['globalMAIN'] and ps['sameTopicMAIN']==oldps['sameTopicMAIN'] and ps['actualCurrentPeers']==oldps['actualCurrentPeers'] and ps['fullClosestCurrentPeers']==oldps['fullClosestCurrentPeers'] and ps['currentGuardRows']==oldps['currentGuardRows']
 oldtask=read(D/'source-history-russia77-task.json');oldbytes=__import__('subprocess').check_output(['git','--no-optional-locks','-C',str(C),'show',oldtask['baselineCode']+':src/content/topics/history-russia.json']);oldtopic=json.loads(oldbytes);now=live['history-russia']
 assert oldtopic['questions'][76]==e0['beforeCard'] and now['questions'][76]==e0['proposedCard']
 assert [i for i,(a,b) in enumerate(zip(oldtopic['questions'],now['questions']),1) if a!=b]==[77]
 prior=read(D/'qualified-source-history-russia77-apply.json');assert prior['author']==candidate['sourceNativeId'] and prior['applied'][0]['beforeCard']==e0['beforeCard'] and prior['applied'][0]['proposedCard']==e['beforeCard']
 binding=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(binding)==110 and [v['path'] for v in binding]==[str(f.relative_to(C)) for f in files]
 old_rows=[];history_field=None
 for b,f in zip(binding,files):
  key=next(k for k in ['sha256','fileSHA256','fileSha256','rawSHA256'] if k in b)
  if f.name=='history-russia.json':assert b[key]==hashlib.sha256(oldbytes).hexdigest();t=oldtopic;history_field=key
  else:assert b[key]==raw(f);t=live[f.stem]
  old_rows.extend(project(t['id'],q) for q in t['questions'])
 assert len(old_rows)==11000 and sha(old_rows)==ps['globalMAIN']['rowsCanonicalSHA256']
 assert ps['sameTopicMAIN']['questions']==oldtopic['questions'] and ps['sameTopicMAIN']['fileSHA256']==hashlib.sha256(oldbytes).hexdigest()
 peers=ps['actualCurrentPeers'];assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101)) and [v['card'] for v in peers]==oldtopic['questions']
 for v in peers:assert v['id']==v['card']['id'] and v['topicId']=='history-russia' and v['sha256']==sha(v['card'])
 assert all(v['id']!=e['id'] for v in ps['fullClosestCurrentPeers'])
 guard=ps['currentGuardRows']['currentTargetBeforeCard'];assert guard['card']==e0['beforeCard'] and guard['sha256']==e0['beforeHash']
 proof={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'ownInitialCandidatePath':str(I/'candidate.json'),'ownInitialCandidateSHA256':raw(I/'candidate.json'),'ownInitialPeerPath':str(I/'peer-snapshot.json'),'ownInitialPeerSHA256':raw(I/'peer-snapshot.json'),'originalCatalogCommit':oldtask['baselineCode'],'oldGlobalRowSHA256':sha(old_rows),'currentGlobalRowSHA256':sha(live_rows),'oldSelfHash':e0['beforeHash'],'currentSelfHash':e['beforeHash'],'newGrammarProposalHash':e['afterHash'],'allOtherCardsAnd110FileBindingsProven':True,'inventoryFileHydration':False,'selfIsDistinctPeer':False,'operation':'Only exact own prior77 application replaces historical self-preimage in full100/110/11000 bookkeeping. Original raw unchanged; no literal, primaryGround or distinct-peer assessment changed.'}
 ps['globalMAIN']['rowsCanonicalSHA256']=sha(live_rows)
 for b in binding:
  if b['path']=='src/content/topics/history-russia.json':b[history_field]=raw(C/b['path'])
 ps['sameTopicMAIN']['questions']=copy.deepcopy(now['questions']);ps['sameTopicMAIN']['fileSHA256']=raw(C/'src/content/topics/history-russia.json')
 for v in peers:
  if v['id']==e['id']:v.update(card=copy.deepcopy(e['beforeCard']),sha256=e['beforeHash'])
 guard.update(card=copy.deepcopy(e['beforeCard']),sha256=e['beforeHash'])
 ps['technicalOwnPrior77SelfPreimageAlias']=proof;sp['technicalOwnPrior77SelfPreimageAlias']=proof


def alias_source31_root_entry_identity(candidate, sp, R):
 """Exact already-declared source31 root identity; derived view only, raw immutable."""
 if R.name != 'source-human-medicine31' or candidate['sourceNativeId'] != '01a16731-2baf-76e3-a052-31ab747f1ff8':return
 assert raw(R/'sourceproof.json') == '776b63fca4c3223ee4d7477c86dc56427f27b55cdc6e46b375212b2e3ea4f122'
 assert candidate['cycle'] == sp['cycle'] == 0 and candidate['sourceNativeId'] == sp['sourceNativeId']
 assert len(candidate['entries']) == len(sp['entries']) == 1
 c = candidate['entries'][0];e = sp['entries'][0]
 assert candidate['id'] == sp['id'] == c['id'] == 'human-medicine-brain-protection'
 assert candidate['topicId'] == sp['topicId'] == c['topicId'] == 'human-medicine'
 assert sp['sourceOrder'] == c['sourceOrder'] == 31 and sp['status'] == c['status'] == 'READY_FOR_INDEPENDENT_REVIEW'
 q = c['proposedCard'];assert sha(q) == c['afterHash']
 groups = {'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 assert len(e['literalGroups']) == 6 and len(e['fourFullPromptAnswerNoteAssessments']) == 4
 for g in e['literalGroups']:assert g['literal'] == groups[g['group']] and g['literalSHA256'] == sha(g['literal'])
 for v in e['fourFullPromptAnswerNoteAssessments']:
  a=q['answers'][v['slot']];tr={'prompt':q['prompt'],'answer':a['text'],'note':a['note']}
  assert tr == {'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']} and sha(tr) == v['tripleSHA256']
 for k in ['id','topicId','sourceOrder','status']:
  assert k not in e or e[k] == sp[k]
  e[k] = sp[k]
 e['technicalRootIdentityContainerAlias'] = {'originalSourceproofSHA256':raw(R/'sourceproof.json'),'originalPointers':['/id','/topicId','/sourceOrder','/status'],'operation':'Already explicit root identity aliased into sole entry; candidate, six literals, four triples, original assessments and raw unchanged. Original KeyError remains uncured.'}

def alias_same_topic_current_peer_container(candidate,sp,ps,R):
 """Expose exact original nested100 peers; no new body or judgment."""
 if 'actualCurrentPeers' in ps:return
 same=ps.get('sameTopicMAIN',{})
 if 'actualCurrentPeers' not in same:return
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']
 assert len(candidate['entries'])==1
 e=candidate['entries'][0];tid=e['topicId']
 assert candidate['topicId']==sp['topicId']==ps['topicId']==same['topicId']==tid
 rel='src/content/topics/'+tid+'.json';assert same['path']==rel and same['questionCount']==100
 topic=read(C/rel);peers=same['actualCurrentPeers']
 assert topic['id']==tid and raw(C/rel)==same['fileSHA256']
 if len(peers)==99 and 'selfPreimageBinding' in same:
  self_binding=same['selfPreimageBinding']
  assert self_binding['countedAsDistinctPeer'] is False
  assert self_binding['id']==e['id'] and self_binding['sourceOrder']==e['sourceOrder']
  assert self_binding['card']==e['beforeCard']==topic['questions'][e['sourceOrder']-1] and self_binding['sha256']==e['beforeHash']==sha(e['beforeCard'])
  assert all(p['id']!=self_binding['id'] for p in peers)
  peers=sorted([*peers,{**self_binding,'topicId':tid}],key=lambda p:p['sourceOrder'])
  ps['technicalExplicitSelfPreimagePeerAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPeerPointer':'/sameTopicMAIN/actualCurrentPeers','originalSelfPointer':'/sameTopicMAIN/selfPreimageBinding','operation':'Exact99 full original peers plus explicitly separate full self preimage exposed as100 ordered current bindings. Self remains countedAsDistinctPeer=false; topicId comes from the same explicit verified topic. All live body/hash/order assertions retained; raw and judgments unchanged.'}
 assert len(peers)==100 and [p['sourceOrder'] for p in peers]==list(range(1,101))
 assert [p['card'] for p in peers]==topic['questions']
 assert all(p['topicId']==tid and p['id']==p['card']['id'] and sha(p['card'])==p.get('sha256',p.get('canonicalSHA256')) for p in peers)
 bindings=ps['globalMAIN']['allCurrentFileByteBindings']
 b=next(b for b in bindings if b['path']==rel)
 assert b.get('sha256',b.get('fileSHA256',b.get('fileSha256')))==same['fileSHA256']
 ps['actualCurrentPeers']=peers
 original_questions_absent='questions' not in same
 if original_questions_absent:same['questions']=[peer['card'] for peer in peers]
 ps['technicalExplicitNestedSameTopicPeerAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalPointer':'/sameTopicMAIN/actualCurrentPeers','originalTopLevelAbsent':True,'originalSameTopicQuestionsAbsent':original_questions_absent,'operation':'Exact100 original ordered full peer bodies, identity, digests and topic file binding verified; redundant container name only. Raw and judgments unchanged; original format gap uncured.'}

def alias_exact_videogame2_distinct_peers(candidate,sp,ps,R):
 """Exact native raw99 distinct plus explicit candidate self; no new judgment."""
 R=pathlib.Path(R)
 if R.name not in ['source-video-game-history2','source-video-game-history2-cycle1'] or candidate['sourceNativeId']!='01a16c14-487b-7060-8311-a40288bb963b':return
 import copy,subprocess
 cycle=1 if R.name.endswith('-cycle1') else 0
 assert R.parent==D and candidate['cycle']==sp['cycle']==ps['cycle']==cycle
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 expected={'candidate.json':'e480b2d671e1259299d14a9964e9342b4aaacc27219bd12369fa65f8d1b86382','sourceproof.json':'916891162ee0d59c5d171634aeed74a86bb453397c5aea4581fda96e7e8eff96','peer-snapshot.json':'31553faa80c1a6228a0eca3e059280af87828d0e3173491ec38c683ac47d2312'}
 freeze='08efc06fa1ff87f7210a435a0e0e57071bb621c2'
 if cycle==1:
  expected={'candidate.json':'6012c41bb4e953334a7ee73387e57be85c0bbbd8cdfed9ab92308981e7b432ff','sourceproof.json':'54128e0505c2b1e445a9eee9282a76d0b78bcdeffcba8227cf4839d8284365ec','peer-snapshot.json':'30d70aadad7dd41ef647f5937b3c71000fb3acd910e66b958d72af5aa960090a'}
  freeze='80dfe074d5cab9984519491634d09affb5d65f45'
  prior=read(R.with_name('source-video-game-history2')/'candidate.json')['entries'][0]
  initial=read(D/'independent-video-game-history2-initial/receipt.json')['entries'][0]
  current=candidate['entries'][0]
  assert initial['stage']=='INITIAL' and initial['status']=='FIX' and initial['defects']
  assert current['beforeCard']==initial['currentCard']==prior['proposedCard']
  assert current['beforeHash']==initial['currentCardCanonicalSHA256']==prior['afterHash']==sha(current['beforeCard'])

 for name,digest in expected.items():
  assert raw(R/name)==digest
  assert (R/name).read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str((R/name).relative_to(C))])
 e=candidate['entries'][0];assert e['id']=='video-game-history-tetris-creator' and e['sourceOrder']==2 and e['topicId']=='video-game-history'
 b=ps['inventoryBinding'];p=pathlib.Path(b['path']);assert p.is_relative_to(R) and raw(p)==b['fileSHA256']
 assert b['selfPreimageIsCandidateBeforeCard'] is True and b['sameTopicActualCurrentPeersCount']==99
 inv=read(p);same=inv['sameTopicMAIN'];g=inv['globalMAIN'];topic=read(C/'src/content/topics/video-game-history.json');peers=ps['actualCurrentPeers']
 assert same['questions']==topic['questions'] and same['questionCount']==b['sameTopicCardCount']==100
 assert same['fileSHA256']==b['sameTopicFileSHA256']==raw(C/b['sameTopicFile'])
 assert g==ps['globalMAIN'] and g['topicFileCount']==b['globalTopicFileCount']==110 and g['questionCount']==b['globalMAINRowCount']==11000 and g['rowsCanonicalSHA256']==b['globalMAINRowsCanonicalSHA256']
 assert len(peers)==99 and [v['sourceOrder'] for v in peers]==[i for i in range(1,101) if i!=2]
 assert all(v['card']==topic['questions'][v['sourceOrder']-1] and v['id']==v['card']['id'] and v['topicId']==e['topicId'] and v['sha256']==sha(v['card']) for v in peers)
 assert topic['questions'][1]==e['beforeCard'] and sha(e['beforeCard'])==e['beforeHash']
 ps['originalDistinctCurrentPeers']=copy.deepcopy(peers)
 ps['actualCurrentPeers']=sorted([*peers,{'id':e['id'],'topicId':e['topicId'],'sourceOrder':2,'card':copy.deepcopy(e['beforeCard']),'sha256':e['beforeHash'],'countedAsDistinctPeer':False}],key=lambda v:v['sourceOrder'])
 ps['originalExplicitInventoryBinding']=copy.deepcopy(b)
 b.update(sha256=b['fileSHA256'],topicCards=b['sameTopicCardCount'],globalMAINRows=b['globalMAINRowCount'],globalTopicFiles=b['globalTopicFileCount'],topicFileSHA256=b['sameTopicFileSHA256'])
 ps['technicalExactVideoGame2PeerBindingAlias']={'rawFreeze':freeze,'rawCriticalSHA256':expected,'originalPeerPointer':'/actualCurrentPeers','selfPointer':'candidate.json#/entries/0/beforeCard','distinctPeerCountUnchanged':99,'technicalCurrentBindings':100,'operation':'Exact declared99 distinct full bodies plus separately declared candidate self preimage and SHA-bound100 inventory. Inventory redundant names only; no new source/body/peer judgment/raw edit/quality credit.'}

def alias_explicit_complete_inventory_paths(candidate,sp,ps,R):
 """Expose original completeCardsPath/completeRowsPath SHA-bound full inventory only."""
 same=ps.get('sameTopicMAIN',{});g=ps.get('globalMAIN',{})
 if 'completeCardsPath' not in same or 'completeRowsPath' not in g:return
 import copy
 R=pathlib.Path(R);assert R.parent==D
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 e=candidate['entries'][0]
 if 'cycle' not in ps:
  task=read(R.with_name(R.name+'-task.json'))
  assert task['cycle']==candidate['cycle']==sp['cycle']==0 and task['owner']==O
  assert task['id']==e['id']==sp['id'] and task['sourceOrder']==e['sourceOrder']==ps['sourceOrder']
  assert task['authorNativeId']==candidate['sourceNativeId'] and task['beforeHash']==e['beforeHash']==sha(e['beforeCard'])
  assert R.name=='source-'+e['topicId']+str(e['sourceOrder']) and not (D/('independent-'+e['topicId']+str(e['sourceOrder'])+'-initial/receipt.json')).exists()
  ps['cycle']=task['cycle']
  ps['technicalExactInitialCycleAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalCycleAbsent':True,'task':str(R.with_name(R.name+'-task.json')),'taskSHA256':raw(R.with_name(R.name+'-task.json')),'operation':'Expose identical cycle0 from own exact native initial task and unchanged candidate/sourceproof, with exact ID/topic/order/preimage and no prior INITIAL. Original omission and root KeyError remain uncured.'}
 assert candidate['cycle']==sp['cycle']==ps['cycle']
 declared=sp['sourceInventoryPath'];assert declared==same['completeCardsPath']==g['completeRowsPath']
 p=pathlib.Path(declared);p=p if p.is_absolute() else C/p
 assert p.is_relative_to(R) and raw(p)==sp['sourceInventorySHA256']==g['completeInventoryFileSHA256']
 inv=read(p);full=inv['sameTopicMAIN'];glob=inv['globalMAIN'];peers=inv['actualCurrentPeers'];e=candidate['entries'][0]
 topic=read(C/full['path']);assert topic['id']==full['topicId']==same['topicId']==e['topicId']
 assert full['path']==same['path'] and full['fileSHA256']==same['fileSHA256']==raw(C/full['path'])
 assert full['questionCount']==same['questionCount']==len(peers)==100
 assert full['questions']==topic['questions']==[v['card'] for v in peers]
 assert [v['sourceOrder'] for v in peers]==list(range(1,101))
 assert all(v['id']==v['card']['id'] and v['topicId']==topic['id'] and v['sha256']==sha(v['card']) for v in peers)
 original=ps['actualCurrentPeers'];byid={v['id']:v for v in peers}
 assert all(v['id'] in byid and v['card']==byid[v['id']]['card'] and v.get('sha256',v.get('canonicalSHA256'))==byid[v['id']]['sha256'] for v in original)
 assert glob['questionCount']==g['questionCount']==11000 and glob['topicFileCount']==g['topicFileCount']==110
 assert glob['rowsCanonicalSHA256']==g['rowsCanonicalSHA256'] and glob['allCurrentFileByteBindings']==g['allCurrentFileByteBindings']
 rows=[]
 for b in glob['allCurrentFileByteBindings']:
  assert raw(C/b['path'])==b['sha256'];t=read(C/b['path'])
  rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==glob['rowsCanonicalSHA256'] and glob['rows']==rows
 ps['originalRelevantCurrentPeers']=copy.deepcopy(original)
 ps['actualCurrentPeers']=copy.deepcopy(peers);same['questions']=copy.deepcopy(full['questions'])
 ps['globalMAIN']['rows']=copy.deepcopy(glob['rows'])
 ps['technicalExplicitCompleteInventoryPathsAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalCompleteCardsPointer':'/sameTopicMAIN/completeCardsPath','originalCompleteRowsPointer':'/globalMAIN/completeRowsPath','inventoryPath':str(p),'inventorySHA256':raw(p),'operation':'Exact original author sameTopic/global complete path and sourceproof SHA references expose existing full100 bodies/11000 rows. Original ten relevant peer bodies and all judgments retained separately. No new judgment or quality credit; raw unchanged.'}

def alias_source74_cycle1_own_global_metadata(candidate,sp,ps,R):
 """Exact already-applied own74 delta in copied global bookkeeping; raw untouched."""
 R=pathlib.Path(R)
 if R.name!='source-video-game-history74-cycle1':return
 assert R.parent==D and candidate['cycle']==sp['cycle']==ps['cycle']==1
 e=candidate['entries'][0];uid=candidate['sourceNativeId'];assert uid==sp['sourceNativeId']==ps['sourceNativeId']=='01a174d0-7f1a-7dd0-9624-56c9f75aa321'
 x=read(D/'manifest.json');I=D/'source-video-game-history74';initial=read(I/'candidate.json');ie=initial['entries'][0];oldps=read(I/'peer-snapshot.json')
 assert e['id']==ie['id'] and e['beforeCard']==ie['proposedCard'] and e['beforeHash']==ie['afterHash']==sha(e['beforeCard'])
 tp=C/'src/content/topics/video-game-history.json';live=read(tp);oldbytes=__import__('subprocess').check_output(['git','-C',str(C),'show',x['pendingVideoGameHistory74']['qualifiedFreeze']+':'+str(tp.relative_to(C))]);old=json.loads(oldbytes)
 assert [i for i,(a,b) in enumerate(zip(old['questions'],live['questions']),1) if a!=b]==[74]
 assert old['questions'][73]==ie['beforeCard'] and live['questions'][73]==e['beforeCard']
 peers=ps['actualCurrentPeers'];assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101)) and [v['card'] for v in peers]==live['questions']
 assert all(v['id']==v['card']['id'] and v['topicId']=='video-game-history' and v['sha256']==sha(v['card']) for v in peers)
 assert ps['globalMAIN']==oldps['globalMAIN'];bindings=ps['globalMAIN']['currentFileByteBindings'];files=sorted((C/'src/content/topics').glob('*.json'));assert len(bindings)==len(files)==110
 oldrows=[];nowrows=[]
 def projection(t,q):return {'topicId':t,'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']}
 for b,f in zip(bindings,files):
  assert b['path']==str(f.relative_to(C));now=read(f);before=old if f==tp else now
  assert b['sha256']==(__import__('hashlib').sha256(oldbytes).hexdigest() if f==tp else raw(f))
  oldrows.extend(projection(before['id'],q) for q in before['questions']);nowrows.extend(projection(now['id'],q) for q in now['questions'])
 assert len(oldrows)==len(nowrows)==11000 and ps['globalMAIN']['rowsCanonicalSHA256']==sha(oldrows)
 proof={'rawPeer':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'originalGlobalPointer':'/globalMAIN','initialRawPeer':str(I/'peer-snapshot.json'),'initialRawPeerSHA256':raw(I/'peer-snapshot.json'),'ownInitialApplication':str(D/'qualified-source-video-game-history74-apply.json'),'oldGlobalRowsSHA256':sha(oldrows),'currentGlobalRowsSHA256':sha(nowrows),'onlyAppliedDelta':74,'all100CurrentFullPeersAlreadyExact':True,'allOther109FilesExact':True,'rawAndSemanticGroundsUnchanged':True,'originalMetadataFailureUncured':True,'operation':'Copied initial global machine bookkeeping updated for its exact already-applied own74 only. No source, literal, peer judgment, budget or cycle change.'}
 ps['globalMAIN']['rowsCanonicalSHA256']=sha(nowrows)
 next(v for v in bindings if v['path']==str(tp.relative_to(C)))['sha256']=raw(tp)
 if 'rows' in ps['globalMAIN']:
  assert ps['globalMAIN']['rows']==oldrows;ps['globalMAIN']['rows']=nowrows
 if 'sameTopicFile' in ps:
  assert ps['sameTopicFile']['path']==str(tp.relative_to(C)) and ps['sameTopicFile']['fileSHA256'] in [raw(tp),__import__('hashlib').sha256(oldbytes).hexdigest()]
  ps['sameTopicFile']['fileSHA256']=raw(tp)
 ps['technicalOwnApplied74GlobalMetadataAlias']=proof;sp['technicalOwnApplied74GlobalMetadataAlias']=proof

def alias_source78_concurrent74_snapshot(candidate,sp,ps,R):
 """Bind the preserved author's separate updated peer to its exact single74 delta."""
 R=pathlib.Path(R)
 if R.name!='source-video-game-history78':return
 assert R.parent==D and candidate['cycle']==sp['cycle']==ps['cycle']==0
 e=candidate['entries'][0];uid=candidate['sourceNativeId'];assert uid==sp['sourceNativeId']==ps['sourceNativeId']=='01a174e7-c642-73e2-9ead-64c396c2bafc'
 recovery=D/'source78-ready-peer-recovery.json';rec=read(recovery);assert raw(R/'peer-snapshot.json')==rec['reconstructedOriginalPeerSHA256']
 cp=pathlib.Path(rec['newAuthorPeer']);cur=read(cp);assert raw(cp)==rec['newAuthorPeerSHA256'] and cur['sourceNativeId']==uid and cur['proposedCard']==e['proposedCard']
 proof=read(D/'video-game-history78-native-proof.json');tp=C/'src/content/topics/video-game-history.json';baseline=proof['preservedCatalogBaseline'];oldbytes=__import__('subprocess').check_output(['git','-C',str(C),'show',baseline+':'+str(tp.relative_to(C))]);old=json.loads(oldbytes);live=read(tp)
 assert [i for i,(a,b) in enumerate(zip(old['questions'],live['questions']),1) if a!=b]==[74]
 app=read(D/'qualified-source-video-game-history74-cycle1-apply.json')['applied'][0];assert app['beforeCard']==old['questions'][73] and app['proposedCard']==live['questions'][73]
 assert live['questions'][77]==e['beforeCard'] and sha(e['beforeCard'])==e['beforeHash'] and sha(e['proposedCard'])==e['afterHash']
 assert [v['card'] for v in ps['actualCurrentPeers']]==old['questions'] and [v['card'] for v in cur['actualCurrentPeers']]==live['questions']
 for peers in [ps['actualCurrentPeers'],cur['actualCurrentPeers']]:
  assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101)) and all(v['id']==v['card']['id'] and v['topicId']=='video-game-history' and sha(v['card'])==v['sha256'] for v in peers)
 rows=[];nowrows=[];oldbindings=ps['globalMAIN']['allCurrentFileByteBindings'];newbindings=cur['globalMAIN']['allCurrentFileByteBindings'];assert len(oldbindings)==len(newbindings)==110
 for b,n in zip(oldbindings,newbindings):
  assert b['path']==n['path'] and raw(C/n['path'])==n['sha256'];now=read(C/n['path']);before=old if C/n['path']==tp else now
  assert b['sha256']==(__import__('hashlib').sha256(oldbytes).hexdigest() if C/n['path']==tp else n['sha256'])
  rows.extend({'topicId':before['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in before['questions'])
  nowrows.extend({'topicId':now['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in now['questions'])
 assert len(rows)==len(nowrows)==11000 and ps['globalMAIN']['rows']==rows and ps['globalMAIN']['rowsCanonicalSHA256']==sha(rows)
 assert cur['globalMAIN']['rows']==nowrows and cur['globalMAIN']['rowsCanonicalSHA256']==sha(nowrows)
 ip=C/cur['inventoryPath'];assert raw(ip)==cur['inventoryFileSHA256'];inv=read(ip);assert inv['globalMAIN']==cur['globalMAIN'] and inv['actualCurrentPeers']==cur['actualCurrentPeers']
 cmp=next(v for v in cur['mainComparisons'] if v.get('sourceOrder')==74);assert cmp['peerCardSHA256']==sha(live['questions'][73]) and all(cmp['bilateralComparison'][k] for k in ['proposedToPeer','peerToProposed'])
 binding={'rawOriginalPeer':str(R/'peer-snapshot.json'),'rawOriginalPeerSHA256':raw(R/'peer-snapshot.json'),'newAuthorPeer':str(cp),'newAuthorPeerSHA256':raw(cp),'recovery':str(recovery),'recoverySHA256':raw(recovery),'knownSingleAppliedDelta':74,'allOtherCardsAnd109FilesExact':True,'rawMutationHistoricallyUncured':True,'noRootSemanticDecision':True,'qualityCredit':0}
 ps.clear();ps.update(cur);ps['technicalConcurrent74DependencyOverlay']=binding;sp['technicalConcurrent74DependencyOverlay']=binding

def assert_retained_source_admissibility(sp):
 """Enforce explicit existing capture exclusions; preserve unsafe originals separately."""
 exclusions=read(D/'manifest.json').get('inadmissibleRetainedSources',[])
 for ex in exclusions:
  forbidden=pathlib.Path(ex['path']).resolve();assert raw(forbidden)==ex['rawSHA256']
  bad=read(forbidden);origin=(bad.get('sourceNativeId'),bad.get('nativeRecordLine'))
  for source in sp.get('rawSources',[]):
   path=pathlib.Path(source['path']);path=path if path.is_absolute() else C/path
   assert path.resolve()!=forbidden and raw(path)!=ex['rawSHA256'], ('EXPLICIT_INADMISSIBLE_CAPTURE',str(path),ex['reason'])
   if path.suffix=='.json':
    cap=read(path)
    if isinstance(cap,dict) and all(origin):assert (cap.get('sourceNativeId'),cap.get('nativeRecordLine'))!=origin, ('RENAMED_INADMISSIBLE_NATIVE_CAPTURE',str(path),origin)


def alias_source83_cycle1_copied_same_topic(candidate,sp,ps,R):
 """Exact own83cycle1 redundant copied container; preserve original and judgments."""
 R=pathlib.Path(R)
 if R!=D/'source-video-game-history83-cycle1':return
 import copy,subprocess
 expected={'candidate.json':'c424b0f2e7e9023eec4c538bf8af2ecae93803fe8d58249e1f828dad92e4df14','sourceproof.json':'9b9142b15314146b53cc36a1f04be906855619a4d254cf767c6771a30c24d223','peer-snapshot.json':'1fd8134e58dbb2ece83dd1584805142189d3be2d43fb514260106adfae5d468a'}
 for name,digest in expected.items():
  assert raw(R/name)==digest
  assert (R/name).read_bytes()==subprocess.check_output(['git','-C',str(C),'show','9baeed109306552e8aef588f9b6e3340e0d7ead2:'+str((R/name).relative_to(C))])
 assert candidate['cycle']==sp['cycle']==ps['cycle']==1
 uid='01a17544-0206-7353-af92-26b8e9323ed9';assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 e=candidate['entries'][0];live=read(C/'src/content/topics/video-game-history.json');initial=read(D/'independent-video-game-history83-initial/receipt.json')['entries'][0]
 assert e['sourceOrder']==83 and e['beforeCard']==initial['currentCard']==live['questions'][82] and e['beforeHash']==initial['currentCardCanonicalSHA256']==sha(e['beforeCard']) and initial['status']=='FIX'
 original=copy.deepcopy(ps['sameTopicMAIN']);old=read(D/'qualified-source-video-game-history83-initial-complete/peer-snapshot.json')['sameTopicMAIN'];assert original==old
 peers=ps['actualCurrentPeers'];assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101))
 assert [v['card'] for v in peers]==live['questions'] and all(v['id']==v['card']['id'] and v['topicId']=='video-game-history' and v['sha256']==sha(v['card']) for v in peers)
 g=ps['globalMAIN'];rows=[];assert len(g['allCurrentFileByteBindings'])==110
 for b in g['allCurrentFileByteBindings']:
  p=C/b['path'];assert raw(p)==b['sha256'];t=read(p);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and rows==g['rows'] and sha(rows)==g['rowsCanonicalSHA256']
 ps['sameTopicMAIN']={**original,'questions':copy.deepcopy(live['questions']),'fileSHA256':raw(C/'src/content/topics/video-game-history.json')}
 proof={'rawFreeze':'9baeed109306552e8aef588f9b6e3340e0d7ead2','rawCriticalSHA256':expected,'originalCopiedSameTopicMAIN':original,'freshActual100AndGlobal11000Exact':True,'originalFailureUncured':True,'operation':'Only exact same-author83 solecycle1 already contains full ordered current100 peers and current110 file bindings/11000rows. Expose identical existing current bodies under redundant sameTopicMAIN copied from own initialqualified container. All raw, content, sources and author semantic assessments unchanged.'}
 ps['technicalSource83Cycle1RedundantSnapshotAlias']=proof;sp['technicalSource83Cycle1RedundantSnapshotAlias']=proof


def alias_source86_single_peer_entry(candidate,sp,ps,R):
 """Only exact own86 nested single entry; no new data or judgments."""
 R=pathlib.Path(R)
 if R!=D/'source-video-game-history86' or 'globalMAIN' in ps:return
 import copy,subprocess
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  assert (R/name).read_bytes()==subprocess.check_output(['git','-C',str(C),'show','859b464044b09a32c3e26f26aa7c98962c2774cd:'+str((R/name).relative_to(C))])
 uid='01a17560-9396-7bc0-8d8c-b899b68d34cf';assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0 and len(candidate['entries'])==len(sp['entries'])==len(ps['entries'])==1
 e=ps['entries'][0];q=candidate['entries'][0];assert e['id']==q['id']==sp['entries'][0]['id'] and q['sourceOrder']==86
 for key in ['globalMAIN','sameTopicMAIN','actualCurrentPeers','relevantProposedPairs','crossCatalogDirectReverseSearch','sourceInventory']:
  assert key in e and key not in ps;ps[key]=copy.deepcopy(e[key])
 ps['technicalSingleOwnPeerEntryContainerAlias']={'rawFreeze':'859b464044b09a32c3e26f26aa7c98962c2774cd','originalPointer':'/entries/0','originalEntrySHA256':sha(e),'originalKeyErrorUncured':True,'operation':'Exact same author/cycle/ID single peer entry already contains all data. Expose identical original containers at root; preserve raw, original entry, semantic assessments and all normal full100/110/11000 assertions.'}


def alias_source9_global_field_names(candidate,sp,ps,R):
 """Exact own9 global field-name alias; never mutate the frozen author packet."""
 R=pathlib.Path(R)
 if R!=D/'source-cars-road-transport9':return
 frozen=read(D/'source9-raw-freeze.json')
 for name,digest in frozen['files'].items():assert raw(R/name)==digest
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']=='01a17644-1369-7d63-858a-f3a32f8e8a92'
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0
 g=ps['globalMAIN'];assert g['topicFiles']==110 and g['rowCount']==11000
 assert len(g['fileBindings'])==110 and all(raw(C/b['path'])==b['sha256'] for b in g['fileBindings'])
 ip=pathlib.Path(ps['inventoryPath']);assert ip.is_relative_to(R) and raw(ip)==ps['inventorySHA256']
 inv=read(ip);assert inv['globalMAIN']['allCurrentFileByteBindings']==g['fileBindings'] and inv['globalMAIN']['rowsCanonicalSHA256']==g['rowsCanonicalSHA256']
 assert inv['globalMAIN']['topicFileCount']==g['topicFiles'] and inv['globalMAIN']['questionCount']==g['rowCount']
 g.update(allCurrentFileByteBindings=g['fileBindings'],topicFileCount=g['topicFiles'],questionCount=g['rowCount'])
 ps['technicalOwn9GlobalFieldNamesAlias']={'rawPeer':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'originalFields':['fileBindings','topicFiles','rowCount'],'inventory':str(ip),'inventorySHA256':raw(ip),'operation':'Only exact immutable author field names exposed under standard names; all110 live file bindings and existing inventory digest/counts match. Raw, source bodies and semantic judgments unchanged; original helper failures uncured.'}


def alias_source22_peer_header(candidate,sp,ps,R):
 """Same author's explicit missing raw22 header addendum; raw unchanged."""
 R=pathlib.Path(R)
 if R!=D/'source-cars-road-transport22':return
 frozen=read(D/'source22-raw-freeze.json');ap=D/'source22-peer-header-addendum/metadata.json';a=read(ap)
 assert a['rawFileSHA256Before']==a['rawFileSHA256After']==frozen['files'] and not a['rawBytesChanged'] and not a['sourceBodiesOrGroundsChanged']
 for name,digest in frozen['files'].items():assert raw(R/name)==digest
 assert candidate['sourceNativeId']==sp['sourceNativeId']==a['sourceNativeId']==read(D/'source-cars-road-transport22-task.json')['authorNativeId']
 assert candidate['cycle']==sp['cycle']==a['cycle']==0 and candidate['topicId']==sp['topicId']==a['topicId']==ps['sameTopicMAIN']['topicId']=='cars-road-transport'
 assert a['sourceOrder']==candidate['entries'][0]['sourceOrder']==22 and a['samePacketBinding']
 for kind,name in [('peerSnapshot','peer-snapshot.json'),('candidate','candidate.json'),('sourceproof','sourceproof.json')]:assert a[kind+'Path']==str(R/name) and a[kind+'SHA256']==raw(R/name)
 missing=[]
 for key in ['sourceNativeId','topicId','cycle']:
  if key in ps:assert ps[key]==a[key]
  else:missing.append(key);ps[key]=a[key]
 assert missing==a['originalMissingHeaderFields']
 ps['technicalOwn22HeaderAddendum']={'authorAddendum':str(ap),'addendumSHA256':raw(ap),'rawPeer':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'originalMissingHeaderFields':missing,'originalFailureUncured':True,'operation':'Expose exact same-author explicit UID/topic/cycle declaration and SHA-bound immutable peer packet at standard header names. No raw, body, source, ground or identity invention.'}


def alias_fashion7_cycle1_redundant_global(candidate,sp,ps,R):
 """Exact frozen own7 current full bodies bind its redundant stale self MAIN row."""
 R=pathlib.Path(R)
 if R!=D/'source-fashion7-cycle1':return
 import copy,subprocess
 frozen=read(D/'fashion7-cycle1-raw-freeze-unqualified.json')
 for name,digest in frozen['rawFileSHA256'].items():
  assert raw(R/name)==digest
  assert (R/name).read_bytes()==subprocess.check_output(['git','-C',str(C),'show','17c6678fd4c6b3034782a86de0e8bac7823c2bc7:'+str((R/name).relative_to(C))])
 uid='01a17b43-34b1-74b3-af1f-19887807fe35'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 assert candidate['cycle']==sp['cycle']==ps['cycle']==1
 e=candidate['entries'][0];assert e['id']=='fashion-raincoat-water' and e['sourceOrder']==7
 live=read(C/'src/content/topics/fashion.json');full=ps['actualCurrentPeers']
 assert len(full)==100 and [v['sourceOrder'] for v in full]==list(range(1,101))
 assert [v['card'] for v in full]==ps['sameTopicMAIN']['questions']==live['questions']
 assert all(v['id']==v['card']['id'] and v['sha256']==sha(v['card']) for v in full)
 assert e['beforeCard']==live['questions'][6] and e['beforeHash']==sha(e['beforeCard'])
 old=read(D/'source-fashion7/candidate.json')['entries'][0]['beforeCard']
 g=ps['globalMAIN'];assert len(g['rows'])==11000 and sha(g['rows'])==g['rowsCanonicalSHA256']
 rows=[];bindings=[]
 for p in sorted((C/'src/content/topics').glob('*.json')):
  t=read(p);bindings.append({'path':str(p.relative_to(C)),'sha256':raw(p)})
  rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 differences=[i for i,(a,b) in enumerate(zip(g['rows'],rows)) if a!=b]
 assert len(differences)==1 and rows[differences[0]]['id']==e['id']
 oldrow={'topicId':'fashion','id':old['id'],'prompt':old['prompt'],'answers':[a['text'] for a in old['answers']],'correctIndex':old['correctIndex']}
 assert g['rows'][differences[0]]==oldrow
 prior=copy.deepcopy(g);assert len(g['allCurrentFileByteBindings'])==110
 for before,now in zip(g['allCurrentFileByteBindings'],bindings):
  assert before['path']==now['path']
  if now['path']!='src/content/topics/fashion.json':assert before['sha256']==now['sha256']
 g.update(rows=rows,rowsCanonicalSHA256=sha(rows),allCurrentFileByteBindings=bindings)
 proof={'rawFreeze':'17c6678fd4c6b3034782a86de0e8bac7823c2bc7','rawFileSHA256':frozen['rawFileSHA256'],'originalGlobalMAIN':prior,'full100CurrentBodiesAlreadyExact':True,'onlyChangedMAINRow':e['id'],'originalFailuresUncured':['7c8a66','6e3046','7e4932'],'qualityCredit':0,'operation':'Expose identical already-saved full CURRENT own self body in redundant global projection only. All other10999 rows and109files exact. No raw, literal, source, ground, peer judgment or cycle change.'}
 ps['technicalFashion7Cycle1RedundantGlobalAlias']=proof;sp['technicalFashion7Cycle1RedundantGlobalAlias']=proof
