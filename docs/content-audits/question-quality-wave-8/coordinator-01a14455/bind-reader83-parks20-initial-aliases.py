"""Bind freshOTHER83 polar18 INITIAL without inventing judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-parks20-initial';F=D/'bound-independent-parks20-initial';F.mkdir(exist_ok=True);original='c8e319539dc9fd8db09c127b4dd5561b505149de'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};pairs=[]
for row in ps['bilateralMAINComparisons']:
 left=actual[row['targetId']];right=actual[row['peerId']];assert left['sha256']==row['targetSHA256'] and right['sha256']==row['peerSHA256'];assert row['directReverse'] is False and row['duplicate'] is False
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['targetERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['targetToPeer'],'rightToLeft':row['peerToTarget'],'originalAssessment':row})
ps['latestProposalSnapshots']=[]
for hist in ps['relevantHistoricalAndCurrentProposals']:
 if hist['sha256']==actual[hist['id']]['sha256']:
  assert hist['card']==actual[hist['id']]['card'];continue
 path=D/'source-parks18-20-original/candidate.json';entry=next(e for e in m.read(path)['entries'] if e['id']==hist['id']);assert entry['proposedCard']==hist['card'] and entry['afterHash']==hist['sha256']==m.sha(hist['card'])
 prop={**hist,'sha256':hist['sha256'],'state':'HISTORICAL_'+hist['state']};ps['latestProposalSnapshots'].append({'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path),'proposal':prop});target=actual[docs['receipt.json']['entries'][0]['id']]
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT'},'right':prop,'leftToRight':hist['current20ToProposal'],'rightToLeft':hist['proposalToCurrent20'],'originalAssessment':hist})
ps['bilateralMainComparisons']=pairs;src=docs['sources.json'];src['sources']=src['rawSources']
for source in src['sources']:assert source['personalReadEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only schema/path/body/hash aliases and verbatim existing bilateral/ERVC grounds. Current17/18bodyhistory equals actualCURRENT; rejected16 historicalproposal directlybound to originalsourcefullbody/hash andexistingexplicitbothdirectionjudgments. All statuses/verbatimjudgments unchanged.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
