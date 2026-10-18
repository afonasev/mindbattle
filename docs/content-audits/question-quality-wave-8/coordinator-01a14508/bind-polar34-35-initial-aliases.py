"""Lossless independent receipt/wholebody/source aliases only; no new judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar34-35-initial';F=D/'bound-independent-polar34-35-initial';F.mkdir(exist_ok=True);freeze='c1c46c107437cc4cff9f8b15c7227b7c41ed22e7'
for p in R.glob('*.json'):assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:dict(p) for p in ps['fullClosestActualPeers']}
for e in docs['receipt.json']['entries']:
 assert m.sha(e['currentCard'])==e['currentCardCanonicalSHA256']
 if e['id'] in actual:assert actual[e['id']]['card']==e['currentCard']
 actual[e['id']]={'id':e['id'],'topicId':'polar-regions','card':e['currentCard'],'sha256':e['currentCardCanonicalSHA256']}
pairs=[]
for row in ps['bilateralCurrentPairs']:
 left=actual[row['candidateId']];right=actual[row['peerId']];assert left['card']==row['candidateCard'] and left['sha256']==row['candidateFullCardSHA256'];assert right['card']==row['peerCard'] and right['sha256']==row['peerFullCardSHA256'];assert row['directReverse'] and row['verdict']=='DISTINCT'
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalIndependentAssessment':row})
proposals={};propPairs=[]
for row in ps['genuineProposalPairs']:
 left=actual[row['candidateId']];assert left['card']==row['candidateCard'] and left['sha256']==row['candidateFullCardSHA256'];path=pathlib.Path(row['proposalPath']);assert m.raw(path)==row['proposalSourceFileRawSHA256'];data=m.read(path);version=(row['proposalId'],row['proposalFullCardSHA256']);assert m.sha(row['proposalCard'])==row['proposalFullCardSHA256']
 if 'scope' in data:
  scope=data['scope'];assert scope['id']==row['proposalId'] and scope['proposedCard']==row['proposalCard'] and scope['afterHash']==row['proposalFullCardSHA256'];assert path.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','1e40f8549f22dd42b937179c581696260edad0fe:'+str(path.relative_to(C))]);alias=F/'proposal27-source-scope-alias.json';m.write(alias,{'entries':[scope],'technicalSchemaProvenance':{'originalPath':str(path.relative_to(C)),'originalRawSHA256':m.raw(path),'originalFreeze':'1e40f8549f22dd42b937179c581696260edad0fe','operation':'Exact originalscope object wrapped asentries only. NoSOURCEqualification/qualityapproval or newsemanticjudgment.'}});bindingPath=alias
 else:
  e=next(e for e in data['entries'] if e['id']==row['proposalId']);assert e['proposedCard']==row['proposalCard'] and e['afterHash']==row['proposalFullCardSHA256'];bindingPath=path
 right={'id':row['proposalId'],'topicId':'national-parks-nature' if row['proposalId'].startswith('national-parks') else 'polar-regions','card':row['proposalCard'],'sha256':row['proposalFullCardSHA256'],'state':'UNAPPLIED_GENUINE_PROPOSAL' if row['proposalId'].startswith('national-parks') else 'HISTORICAL_PROPOSAL_NOW_ACTUAL'}
 snap={'proposal':right,'sourcePath':str(bindingPath.relative_to(C)),'sourceRawSHA256':m.raw(bindingPath),'originalSourcePath':str(path.relative_to(C)),'originalSourceRawSHA256':row['proposalSourceFileRawSHA256']}
 if version in proposals:assert proposals[version]==snap
 else:proposals[version]=snap
 assert row['directReverse'] and row['verdict']=='DISTINCT';propPairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'MAIN':row['proposalERVC']},'leftToRight':row['candidateToProposal'],'rightToLeft':row['proposalToCandidate'],'originalIndependentAssessment':row})
ps['actualCurrentPeers']=list(actual.values());ps['bilateralMainComparisons']=pairs;ps['proposedBilateralMAINComparisons']=propPairs;ps['latestProposalSnapshots']=list(proposals.values())
for source in docs['sources.json']['sources']:
 source['personalReadEvidence']=source['readEvidence'];source['locator']=source.get('locator') or source.get('scientificClaimRange') or source['fullRangeRead'];assert source['personalReadEvidence'] and source['locator']
v=docs['verification.json'];assert m.raw(pathlib.Path(v['task']))==v['taskRawSHA256'];task=m.read(pathlib.Path(v['task']));assert m.raw(C/task['QA19'])==task['QA19RawSHA256'];v['catalogRawSHA256']=v['currentCatalog']['rawSHA256'];v['existingQA19']={'rawSHA256':task['QA19RawSHA256'],'binding':'Exact reader task rawSHA verified, referencesROOT existingQA19 report; no reader execution/qualityclaim added.'}
for n,x in docs.items():
 x['technicalBindingProvenance']={'originalPath':str((R/n).relative_to(C)),'originalRawSHA256':m.raw(R/n),'originalCommit':freeze,'operation':'Exact 12groups/8variants unchanged. Full30actual peer bodies/hashes andbothfoci linkedbyexistingrowIDs/hashes. All58current+4genuine paired directions/4ERVC/directreverse verdict preserved. Exactscope-only SOURCE27 wrapper adapter linkedtoraworiginal1e40; no qualification or SOURCEjudgment added. Existing3primaryreadEvidence/scientificClaimRange aliased. Exactreader taskQAraw pointer validatedwithoutreaderclaimedexecution. Corevalidator unchanged.'};m.write(F/n,x)
print('BOUND',len(actual),len(pairs),len(propPairs),len(proposals))
