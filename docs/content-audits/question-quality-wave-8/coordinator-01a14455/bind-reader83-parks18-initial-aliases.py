"""Bind freshOTHER83 parks18 INITIAL without inventing judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-parks18-initial';F=D/'bound-independent-parks18-initial';F.mkdir(exist_ok=True);original='18b287398860724c1dc788ef066948b5ef0ba7b7'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};pairs=[]
for row in ps['bilateralMAINComparisons']:
 left=actual[row['targetId']];right=actual[row['peerId']];assert left['sha256']==row['targetSHA256'] and right['sha256']==row['peerSHA256'];assert row['directReverse'] is False and row['duplicate'] is False
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['targetERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['targetToPeer'],'rightToLeft':row['peerToTarget'],'originalAssessment':row})
ps['latestProposalSnapshots']=[];path=D/'source-parks18-20-original/candidate.json';source=m.read(path)
held=ps['held19_20'];assert held['promoted'] is False and held['mainComparison'];target=actual[docs['receipt.json']['entries'][0]['id']]
for p in held['proposalCards']:
 entry=next(e for e in source['entries'] if e['id']==p['id']);assert entry['proposedCard']==p['card'] and entry['afterHash']==p['sha256']==m.sha(p['card'])
 prop={**p,'state':'UNAPPLIED_SOURCE_HOLD_NOT_QUALITY'};ps['latestProposalSnapshots'].append({'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path),'proposal':prop})
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT'},'right':prop,'leftToRight':held['mainComparison'],'rightToLeft':held['mainComparison'],'originalJointBothDirectionAssessment':held['mainComparison']})
ps['bilateralMainComparisons']=pairs;src=docs['sources.json'];src['sources']=src['rawSources']
for source in src['sources']:source['personalReadEvidence']=source['readEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['qa19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only schema/path/body/hash aliases and verbatim existing bilateral/ERVC grounds. Held19/20 joint prose explicitly contains bothdirections; copiedverbatim toboth fields. StatusPASS18 andHOLDnotpromoted unchanged.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
