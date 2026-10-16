"""Lossless binding of OTHER15 full semantic judgments and three historical14 versions."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar12-cycle1-final';F=D/'bound-independent-polar12-cycle1-final';F.mkdir(exist_ok=True)
original=m.savecode([p for p in R.iterdir() if p.is_file()],'Preserve OTHER12solecycle1 FINALPASS exactCURRENT rawreceipt')
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};r=docs['receipt.json'];assert len(r['entries'])==1;e=r['entries'][0];assert e['status']=='PASS' and not e['defects'];q=e['currentCard'];h=m.sha(q);assert h==e['currentCardCanonicalSHA256'];ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']}
assert q['id'] not in actual;target={'id':q['id'],'topicId':'polar-regions','sourceOrder':12,'card':q,'sha256':h};ps['actualCurrentPeers'].append(target);actual[q['id']]=target
props={};snapshots=[]
for p in ps['relevantProposedPairs']:
 digest=p.get('sha256',p.get('canonicalSHA256',p.get('cardSHA256')));assert digest and m.sha(p['card'])==digest
 if 'sourcePath' in p:path=p['sourcePath'];raw=p.get('sourceRawSHA256',m.raw(C/path))
 elif 'sourceFile' in p:path=p['sourceFile'];raw=p['sourceFileSHA256']
 else:binding=next(x for x in p['sourcePacketBindings'] if x['path'].endswith('/candidate.json'));path=binding['path'];raw=binding['rawSHA256']
 assert m.raw(C/path)==raw;sd=m.read(C/path);source=next(x for x in sd.get('entries',sd.get('candidates',[sd] if 'proposedCard' in sd else [])) if x['id']==p['id']);assert source['proposedCard']==p['card'] and source['afterHash']==digest
 key=(p['id'],digest);assert key not in props;props[key]={**p,'sha256':digest};snapshots.append({'sourcePath':path,'sourceRawSHA256':raw,'proposal':props[key]})
ps['latestProposalSnapshots']=snapshots;ps['bilateralMainComparisons']=[]
for row in ps['bilateralMainAssessments']:
 assert row['candidateId']==q['id'] and row['candidateSHA256']==h
 key=(row['peerId'],row['peerSHA256']);isproposal=key in props;peer=props[key] if isproposal else actual[row['peerId']];assert peer['sha256']==row['peerSHA256'];assert row['candidateMAIN']['prompt']==q['prompt'] and row['candidateMAIN']['key']==q['answers'][q['correctIndex']]['text'];assert row['peerMAIN']['prompt']==peer['card']['prompt'] and row['peerMAIN']['key']==peer['card']['answers'][peer['card']['correctIndex']]['text']
 for direction in ['candidateToPeer','peerToCandidate']:assert row[direction]['duplicate'] is False and row[direction]['directReverse'] is False and row[direction]['ground']
 state=row['peerState']
 if isproposal:
  state=state if state.startswith(('HISTORICAL_','UNAPPLIED_')) else ('HISTORICAL_' if 'HISTORY' in state else 'UNAPPLIED_')+state
 else:assert state.startswith('ACTUAL_CURRENT')
 ps['bilateralMainComparisons'].append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['candidateMAIN']['ERVC'],'key':row['candidateMAIN']['key']},'right':{**peer,'state':state,'MAIN':row['peerMAIN']['ERVC'],'key':row['peerMAIN']['key']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalAssessment':row})
v=docs['verification.json'];assert v['rawTestedSHA256']==v['rawReaderSHA256']==v['rawLiveReadSHA256'];v['catalogRawSHA256']=v['rawReaderSHA256'];v['existingQA19']={'path':v['QA19Path'],'rawSHA256':v['QA19RawSHA256']}
for p in docs['sources.json']['sources']:assert p['personalReadEvidence'];p['locator']=p['personalReadEvidence']
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only existing fullbody/digest/path/version aliases; semantic ERVC/directions/locator prose unchanged. SOURCE13 historical proposal stays distinct from actual13 by ID+canonicalSHA; actualpeer freshness stillstrict. Source fullread scope string copied verbatim aslocator, preciseclaimlocators remainin6groups.'};m.write(F/name,doc)
print(original)
