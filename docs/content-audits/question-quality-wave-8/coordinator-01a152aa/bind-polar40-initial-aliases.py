"""Lossless SOURCE40 reader receipt adapters; all original judgments preserved."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar40-initial';F=D/'bound-independent-polar40-initial';F.mkdir(exist_ok=True);freeze='84caac8a60e532d4392d24ca5595908013da1ecd'
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']}
for n in docs:assert (R/n).read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str((R/n).relative_to(C))])
ps=docs['peers.json'];actual={p['id']:dict(p) for p in ps['fullClosestActualPeers']}
for e in docs['receipt.json']['entries']:
 assert m.sha(e['currentCard'])==e['currentCardCanonicalSHA256']
 actual[e['id']]={'id':e['id'],'topicId':e['topicId'],'card':e['currentCard'],'sha256':e['currentCardCanonicalSHA256']}
pairs=[]
for row in ps['bilateralCurrentPairs']:
 left=actual[row['candidateId']];right=actual[row['peer']['id']]
 assert left['card']==row['candidateCard'] and left['sha256']==row['candidateCanonicalSHA256'];assert right['card']==row['peer']['card'] and right['sha256']==row['peer']['sha256']
 assert row['candidateToPeer']['status']==row['peerToCandidate']['status']=='DISTINCT' and row['directReverse']['status']=='NONE'
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['candidateToPeer'],'rightToLeft':row['peerToCandidate'],'originalIndependentAssessment':row})
proposals=[];pp=[];focus=docs['receipt.json']['entries'][0];left=actual[focus['id']]
for row in ps['genuineProposalPairs']:
 path=pathlib.Path(row['packetPath']);assert m.raw(path)==row['packetRawSHA256'];data=m.read(path);entry=next(e for e in data['entries'] if e['id']==row['proposalId'])
 assert entry['proposedCard']==row['proposalCard'] and entry['afterHash']==row['proposalCanonicalSHA256']==m.sha(row['proposalCard'])
 right={'id':row['proposalId'],'topicId':'national-parks-nature' if row['proposalId'].startswith('national-parks') else 'polar-regions','card':row['proposalCard'],'sha256':row['proposalCanonicalSHA256'],'state':'HISTORICAL_OR_UNAPPLIED_INPUT_PROPOSAL_NO_QUALITY_APPROVAL'}
 proposals.append({'proposal':right,'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path)})
 assert row['candidateToProposal'] and row['proposalToCandidate'] and row['directReverseAssessment']
 pp.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['candidateERVC']},'right':{**right,'MAIN':row['proposalERVC']},'leftToRight':row['candidateToProposal'],'rightToLeft':row['proposalToCandidate'],'originalIndependentAssessment':row})
ps.update(actualCurrentPeers=list(actual.values()),bilateralMainComparisons=pairs,proposedBilateralMAINComparisons=pp,latestProposalSnapshots=proposals)
rows=[]
for sf in ps['globalMAIN']['fileByteBindings']:
 path=pathlib.Path(sf['path']);assert m.raw(path)==sf['rawSHA256'];topic=m.read(path)
 for q in topic['questions']:rows.append({'topicId':topic['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']})
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
src=docs['sources.json'];src['sources']=[]
for source in src['rawSources']:
 assert source['readerNativeId']==docs['receipt.json']['readerNativeId'] and source['personallyReadFullRetainedBodyThisINITIAL'] and source['noSOURCEPersonalReadOrGradeInherited']
 src['sources'].append({**source,'rawReadSHA256':source['rawSHA256'],'personalReadEvidence':{'actualWholeReadCoverage':source['actualWholeReadCoverage'],'jsonPointer':source['jsonPointer'],'capturedTextSHA256':source['capturedTextSHA256'],'capturedTextUTF8Bytes':source['capturedTextUTF8Bytes'],'captureProvenanceAsSOURCEIndex':source['captureProvenanceAsSOURCEIndex'],'noSOURCEPersonalReadOrGradeInherited':source['noSOURCEPersonalReadOrGradeInherited']},'locator':source['specificLocators']})
v=docs['verification.json'];assert m.raw(pathlib.Path(v['task']))==v['taskRawSHA256'];task=m.read(pathlib.Path(v['task']));assert m.raw(C/task['QA19'])==task['QA19RawSHA256'];v['catalogRawSHA256']=v['current']['rawSHA256'];v['existingQA19']={'rawSHA256':task['QA19RawSHA256'],'binding':'Exact task QA pointer only; reader execution not claimed.'}
for n,x in docs.items():
 x['technicalBindingProvenance']={'originalPath':str((R/n).relative_to(C)),'originalRawSHA256':m.raw(R/n),'originalCommit':freeze,'operation':'Lossless aliases only. Original6literal/4WHOLEvariants fourindependentjudgments preserved. Full8actualclosest+focus and8bilateraldirections bindbody/hash, including additionalPutorana protectedplateau/reindeerherdmigration relation; same100polar/all100animalMAIN scans retained. Actualold31proposal94de wholebody/path/hash/bothdirections retainedINPUTonly, noSOURCE31quality. Fourwholeofficialbody readcoverages Wapusk187/Jasper143/Banff140/NOAA258 andexactFILEsha/JSONpointer/bodysha/provenance preserved; unsupportedLatinclaim remainshistoricalnotcurrentproof. All110currentfilebytes/11000MAIN verified. No ROOTsemanticjudgment or additionalreaderexecution invented.'}
 m.write(F/n,x)
print('BOUND',len(actual),len(pairs),len(pp),len(proposals))
