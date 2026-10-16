"""Lossless bindings for fresh OTHER83 pair INITIAL; statuses and judgments unchanged."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar16-17-fresh-initial';F=D/'bound-independent-polar16-17-fresh-initial';F.mkdir(exist_ok=True);original='e1ee9f043c6515077ce462583b79924f5d6d3098'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',original+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:p for p in ps['actualCurrentPeers']};pairs=[]
for row in ps['bilateralMAINComparisons']:
 left=actual[row['targetId']];right=actual[row['peerId']];assert left['sha256']==row['targetSHA256'] and right['sha256']==row['peerSHA256'];assert row['directReverse'] is False and row['duplicate'] is False
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['targetERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['targetToPeer'],'rightToLeft':row['peerToTarget'],'originalAssessment':row})
r=ps['mutualCurrent16x17'];left=actual[r['leftId']];right=actual[r['rightId']];assert left['sha256']==r['leftSHA256'] and right['sha256']==r['rightSHA256'];pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':r['leftERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':r['rightERVC']},'leftToRight':r['leftToRight'],'rightToLeft':r['rightToLeft'],'originalAssessment':r})
ps['latestProposalSnapshots']=[]
paths={'rejected16SeaIceProposal':D/'source-polar16-original/candidate.json','priorInputOnlyProposal':D/'source-polar17-original/candidate.json'}
for hist in ps['relatedHistoricalProposals']:
 path=paths[hist['kind']];body=hist['card'];h=hist['canonicalSHA256'];assert m.sha(body)==h;entry=next(e for e in m.read(path)['entries'] if e['id']==body['id']);assert entry['proposedCard']==body and entry['afterHash']==h
 prop={'id':body['id'],'topicId':'polar-regions','card':body,'sha256':h,'state':'HISTORICAL_'+hist['state']};ps['latestProposalSnapshots'].append({'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path),'proposal':prop})
 for row in hist['bilateralAssessments']:
  left=actual[row['currentId']];assert left['sha256']==row['currentSHA256'];assert row['directReverse'] is False and row['independentCatalogDuplicate'] is False
  pairs.append({'left':{**left,'state':'ACTUAL_CURRENT'},'right':prop,'leftToRight':row['currentToProposal'],'rightToLeft':row['proposalToCurrent'],'originalAssessment':row})
ps['bilateralMainComparisons']=pairs;src=docs['sources.json'];src['sources']=src['rawSources'];v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['qa19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':original,'operation':'Only schema/path/body/hash aliases and verbatim existing directional/ERVC grounds; original16FIX and17PASS unchanged. Historical same-version17 not independent duplicate. Supplement fulloriginal capture retained embedded; no semantic invention.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
