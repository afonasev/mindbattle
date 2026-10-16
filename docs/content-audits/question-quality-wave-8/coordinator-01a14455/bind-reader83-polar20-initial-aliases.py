"""Bind freshOTHER83 polar20 INITIAL without inventing judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar20-initial';F=D/'bound-independent-polar20-initial';F.mkdir(exist_ok=True);original='a8fbd0d9b3a676291c3d251fd2a3d256eec3d3c3'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};pairs=[]
for row in ps['bilateralMAINComparisons']:
 left=actual[row['targetId']];right=actual[row['peerId']];assert left['sha256']==row['targetSHA256'] and right['sha256']==row['peerSHA256'];assert row['directReverse'] is False and row['duplicate'] is False
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['targetERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['targetToPeer'],'rightToLeft':row['peerToTarget'],'originalAssessment':row})
ps['latestProposalSnapshots']=[]
for hist in ps['relevantGenuineProposals']:
 assert hist['card']==actual[hist['id']]['card'] and hist['sha256']==actual[hist['id']]['sha256']
ps['bilateralMainComparisons']=pairs;src=docs['sources.json'];src['sources']=src['rawSources']
for source in src['sources']:assert source['personalReadEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only schema/path/body/hash aliases and verbatim existing bilateral/ERVC grounds. Samebody16/17proposalhistory equals actualCURRENT exactly, notactivealternate orindependentduplicate. All statuses/verbatimjudgments unchanged.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
