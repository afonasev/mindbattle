"""Lossless aliases for OTHER50 existing grounded verdicts; no semantic authoring."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/sys.argv[1];F=D/sys.argv[2];F.mkdir();original=m.savecode([p for p in R.iterdir() if p.is_file()],'Preserve OTHER50 original exactCURRENT receipt '+R.name);assert len(original)==40
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];entries=docs['receipt.json']['entries'];assert all(e['status']=='PASS' and not e['defects'] for e in entries);assert len(entries)==1
actual={p['id']:p for p in ps['actualCurrentPeers']};proposed={p['id']:p for p in ps['relevantProposedPairs']};target=entries[0];q=target['currentCard'];assert m.sha(q)==target['currentCardCanonicalSHA256'];assert target['id'] in actual and actual[target['id']]['card']==q
ps['latestProposalSnapshots']=[{'sourcePath':p['origin'],'sourceRawSHA256':p['originRawSHA256'],'proposal':p} for p in proposed.values()];ps['bilateralMainComparisons']=[]
for p in ps['bilateralMainAssessments']:
 assert p['targetId']==target['id'] and p['targetSHA256']==m.sha(q) and p['targetToPeer'] and p['peerToTarget'] and p['directReverse'] and p['verdict']=='DISTINCT_MAIN';peer=proposed[p['peerId']] if p['peerState'].startswith(('UNAPPLIED_','HISTORICAL_')) else actual[p['peerId']];assert p['peerSHA256']==peer['sha256'];ps['bilateralMainComparisons'].append({'left':{'id':q['id'],'state':'ACTUAL_CURRENT','card':q,'sha256':m.sha(q)},'right':peer,'leftToRight':p['targetToPeer'],'rightToLeft':p['peerToTarget'],'directReverseCheck':p['directReverse'],'result':p['verdict'],'originalAssessment':p})
v=docs['verification.json'];v['catalogRawSHA256']=v['rawReaderSHA256'];v['existingQA19']={'path':v['QA19Path'],'rawSHA256':v['QA19RawSHA256']};assert v['rawTestedSHA256']==v['rawReaderSHA256']==v['rawLiveReadSHA256']
for n,d in docs.items():
 d['technicalBindingProvenance']={'originalPath':str((R/n).relative_to(C)),'originalRawSHA256':m.raw(R/n),'originalCommit':original,'operation':'Existing reader field aliases/fullbody bindings only; original semanticgrounds unchanged, no missing judgments invented.'};m.write(F/n,d)
print(original)
