"""Lossless aliases for existing independent polar14 INITIAL proof; no semantic invention."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=OLD/'independent-polar14-initial';F=D/'bound-independent-polar14-initial';F.mkdir(exist_ok=True)
original='2c3c98363672a29ca40ca141e2b43c9f07533ece'
import subprocess
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};r=docs['receipt.json'];e=r['entries'][0];assert e['status']=='PASS' and not e['defects'];q=e['currentCard'];h=m.sha(q);assert h==e['currentCardCanonicalSHA256'];ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};target=ps['candidate'];assert target['card']==q and target['sha256']==h
assert q['id'] not in actual;ps['actualCurrentPeers'].append(target);actual[q['id']]=target
prior=m.read(OLD/'bound-independent-polar12-cycle1-final/peers.json')['latestProposalSnapshots'];props={};snapshots=[]
for p in ps['relevantProposedPairs']:
 digest=p['canonicalSHA256'];assert m.sha(p['card'])==digest
 priorbinding=next(x for x in prior if x['proposal']['id']==p['proposalId'] and x['proposal']['sha256']==digest)
 path=priorbinding['sourcePath'];raw=priorbinding['sourceRawSHA256'];assert m.raw(C/path)==raw
 sd=m.read(C/path);source=next(x for x in sd.get('entries',sd.get('candidates',[sd] if 'proposedCard' in sd else [])) if x['id']==p['proposalId']);assert source['proposedCard']==p['card'] and source['afterHash']==digest
 p={**p,'id':p['proposalId'],'sha256':digest};props[p['id'],digest]=p;snapshots.append({'sourcePath':path,'sourceRawSHA256':raw,'proposal':p})
ps['latestProposalSnapshots']=snapshots;ps['bilateralMainComparisons']=[]
for row in ps['bilateralMainAssessments']:
 assert row['candidateId']==q['id'] and row['candidateSHA256']==h
 key=(row['peerId'],row['peerSHA256']);isproposal=key in props;peer=props[key] if isproposal else actual[row['peerId']];assert peer['sha256']==row['peerSHA256'];assert row['candidateMAIN']['prompt']==q['prompt'] and row['candidateMAIN']['key']==q['answers'][q['correctIndex']]['text'];assert row['peerMAIN']['prompt']==peer['card']['prompt'] and row['peerMAIN']['key']==peer['card']['answers'][peer['card']['correctIndex']]['text']
 for direction in ['candidateToPeer','peerToCandidate']:assert row[direction]['duplicate'] is False and row[direction]['directReverse'] is False and row[direction]['ground']
 state=('UNAPPLIED_'+row['peerState']) if isproposal else row['peerState']
 ps['bilateralMainComparisons'].append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['candidateMAIN']['ERVC'],'key':row['candidateMAIN']['key']},'right':{**peer,'state':state,'MAIN':row['peerMAIN']['ERVC'],'key':row['peerMAIN']['key']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalAssessment':row})
v=docs['verification.json'];assert v['rawTestedSHA256']==v['rawReaderSHA256']==v['rawLiveReadSHA256'];v['catalogRawSHA256']=v['rawReaderSHA256'];v['existingQA19']={'path':v['QA19Path'],'rawSHA256':v['QA19RawSHA256']}
for p in docs['sources.json']['sources']:assert p['personalReadEvidence'];p['locator']=p['personalReadEvidence']
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only existing body/digest/path/schema aliases; target copied from candidate; SOURCE13 path proven by prior raw binding and exact original proposal bytes. All semantic judgments remain verbatim.'};m.write(F/name,doc)
print('BOUND',len(ps['actualCurrentPeers']),len(ps['bilateralMainComparisons']))
