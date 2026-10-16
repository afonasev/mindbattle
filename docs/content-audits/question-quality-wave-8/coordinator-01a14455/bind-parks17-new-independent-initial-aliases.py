"""Lossless aliases for existing independent parks17 NEW INITIAL proof; no semantic invention."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-parks17-new-independent-initial';F=D/'bound-independent-parks17-new-independent-initial';F.mkdir(exist_ok=True)
original='956712694ef7e7da88348e6f00dd59f7dd1eedf8'
import subprocess
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};r=docs['receipt.json'];e=r['entries'][0];assert e['status']=='PASS' and not e['defects'];q=e['currentCard'];h=m.sha(q);assert h==e['currentCardCanonicalSHA256'];ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};target=ps['candidate'];assert target['card']==q and target['sha256']==h
assert q['id'] not in actual;ps['actualCurrentPeers'].append(target);actual[q['id']]=target
props={};snapshots=[]
for p in ps['relevantProposedPairs']:
 digest=p['canonicalSHA256'];assert m.sha(p['card'])==digest
 pid=p['id'];path=p['path'];raw=p['sourceFileSHA256'];assert m.raw(C/path)==raw
 sd=m.read(C/path);source=next(e for e in sd['entries'] if e['id']==pid);assert source['proposedCard']==p['card'] and source['afterHash']==digest
 p={**p,'sha256':digest};props[pid,digest]=p;snapshots.append({'sourcePath':path,'sourceRawSHA256':raw,'proposal':p})
ps['latestProposalSnapshots']=snapshots;ps['bilateralMainComparisons']=[]
for row in ps['bilateralMainAssessments']:
 assert row['candidateId']==q['id'] and row['candidateSHA256']==h
 key=(row['peerId'],row['peerSHA256']);isproposal=key in props;peer=props[key] if isproposal else actual[row['peerId']];assert peer['sha256']==row['peerSHA256'];assert row['candidateMAIN']['prompt']==q['prompt'] and row['candidateMAIN']['key']==q['answers'][q['correctIndex']]['text'];assert row['peerMAIN']['prompt']==peer['card']['prompt'] and row['peerMAIN']['key']==peer['card']['answers'][peer['card']['correctIndex']]['text']
 for direction in ['candidateToPeer','peerToCandidate']:assert row[direction]['duplicate'] is False and row[direction]['directReverse'] is False and row[direction]['ground']
 state=row['peerState']
 if isproposal and not state.startswith(('UNAPPLIED_','HISTORICAL_')):state='HISTORICAL_'+state
 ps['bilateralMainComparisons'].append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['candidateMAIN']['ERVC'],'key':row['candidateMAIN']['key']},'right':{**peer,'state':state,'MAIN':row['peerMAIN']['ERVC'],'key':row['peerMAIN']['key']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalAssessment':row})
v=docs['verification.json'];assert v['rawTestedSHA256']==v['rawReaderSHA256']==v['rawLiveReadSHA256'];v['catalogRawSHA256']=v['rawReaderSHA256'];v['existingQA19']={'path':v['QA19Path'],'rawSHA256':v['QA19RawSHA256']}
for p in docs['sources.json']['sources']:assert p['personalReadEvidence'];p['locator']=p['personalReadEvidence']
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only existing body/digest/path/schema aliases; target copied from candidate; Historical17 path proven directly by original reader raw source binding and exact original proposal body/hash. All semantic judgments remain verbatim.'};m.write(F/name,doc)
print('BOUND',len(ps['actualCurrentPeers']),len(ps['bilateralMainComparisons']))
