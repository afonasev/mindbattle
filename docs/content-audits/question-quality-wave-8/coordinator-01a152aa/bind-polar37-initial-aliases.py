"""Lossless adapters of original independent37 proof; no new editorial judgments."""
import pathlib, importlib.util, subprocess
D=pathlib.Path(__file__).parent; C=D.parents[3]; OLD=D.parent/'coordinator-01a14508'
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar37-initial';F=D/'bound-independent-polar37-initial';F.mkdir(exist_ok=True)
freeze='27947ac45d1ba6b1374382f924df1181669eeb57'
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']}
for n in docs:assert (R/n).read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str((R/n).relative_to(C))])
ps=docs['peers.json']; actual={p['id']:{**p,'topicId':'polar-regions'} for p in ps['fullClosestActualPeers']}
for e in docs['receipt.json']['entries']:
 assert m.sha(e['currentCard'])==e['currentCardCanonicalSHA256']
 actual[e['id']]={'id':e['id'],'topicId':e['topicId'],'card':e['currentCard'],'sha256':e['currentCardCanonicalSHA256']}
pairs=[]
for row in ps['bilateralCurrentPairs']:
 left=actual[row['candidateId']];right=actual[row['peerId']]
 assert left['card']==row['candidateCard'] and left['sha256']==row.get('candidateFullCardSHA256',row.get('candidateCanonicalSHA256'))
 assert right['card']==row['peerCard'] and right['sha256']==row.get('peerFullCardSHA256',row.get('peerCanonicalSHA256'))
 assert row['directReverse'] and row['verdict']=='DISTINCT'
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalIndependentAssessment':row})
proposals=[];propPairs=[]
for row in ps['latePresentGenuineProposalPairs']:
 left=actual[row['candidateId']];path=pathlib.Path(row['peerSourcePath']);assert m.raw(path)==row['peerSourceRawSHA256']
 data=m.read(path);e=next(e for e in data['entries'] if e['id']==row['peerId'])
 assert e['proposedCard']==row['peerCard'] and e['afterHash']==row.get('peerFullCardSHA256',row.get('peerCanonicalSHA256'))==m.sha(row['peerCard'])
 assert left['card']==row['candidateCard'] and left['sha256']==row.get('candidateFullCardSHA256',row.get('candidateCanonicalSHA256'))
 right={'id':row['peerId'],'topicId':'national-parks-nature' if row['peerId'].startswith('national-parks') else 'polar-regions','card':row['peerCard'],'sha256':row.get('peerFullCardSHA256',row.get('peerCanonicalSHA256')),'state':'UNAPPLIED_GENUINE_PROPOSAL' if row['peerId'].startswith('national-parks') else 'HISTORICAL_PROPOSAL_NOW_ACTUAL'}
 proposals.append({'proposal':right,'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path)})
 assert row['directReverse'] and row['verdict']=='DISTINCT'
 propPairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'MAIN':row['peerERVC']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalIndependentAssessment':row})
ps.update(actualCurrentPeers=list(actual.values()),bilateralMainComparisons=pairs,proposedBilateralMAINComparisons=propPairs,latestProposalSnapshots=proposals)
# Refresh bytes only by proving the independent fresh scan still matches every file.
rows=[]
for source in ps['globalMAIN']['sourceFiles']:
 path=pathlib.Path(source['path']);assert m.raw(path)==source['rawSHA256']
 for q in m.read(path)['questions']:
  rows.append({'topicId':source['topicId'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']})
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['canonicalRowsSHA256']
for source in docs['sources.json']['sources']:
 source['personalReadEvidence']={'ownPreviousFullReadReuse':source['fullPersonalContextReadReuse'],'currentScientificContext':source['scientificContextAndClaimGrounds']} if 'fullPersonalContextReadReuse' in source else source['personalFullRead']
 source['locator']=source.get('scientificContextAndClaimGrounds',source.get('personalFullRead'));assert source['personalReadEvidence']
v=docs['verification.json'];assert m.raw(pathlib.Path(v['task']))==v['taskRawSHA256'];task=m.read(pathlib.Path(v['task']))
assert m.raw(C/task['QA19'])==task['QA19RawSHA256']
v['catalogRawSHA256']=v['current']['rawSHA256'];v['existingQA19']={'rawSHA256':task['QA19RawSHA256'],'binding':'Exact original task QA pointer; no independent reader execution claim.'}
for n,x in docs.items():
 x['technicalBindingProvenance']={'originalPath':str((R/n).relative_to(C)),'originalRawSHA256':m.raw(R/n),'originalCommit':freeze,'operation':'Unchanged6literal/4wholevariant judgments. Existing full11closest+focus bodies linked via original hashes; existing11actual+1lateSOURCE38 bilateralERVC/directreverse assessments preserved. Existing ownfullreadreuse3+freshfullNSIDC scientific locators and exactQA task pointer aliased. Original lateSOURCE38 fullbody/hash/path and bothdirections preserved without38approval. HistoricalNSIDCjournal exactpath recheckNotRun retained; preservedwhole212labelsuccessfulresponse personallyread/hashverified, notfailedBritannica output. All110 current file bytes/global11000 rows verified unchanged.'}
 m.write(F/n,x)
print('BOUND',len(actual),len(pairs),len(propPairs),len(proposals))
