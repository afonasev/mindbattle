"""Only lossless schema/body/hash/locator aliases from native83 polar25 raw proof."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar25-initial';F=D/'bound-independent-polar25-initial';F.mkdir(exist_ok=True);freeze='a814d95c6d974e853b760fe46664a56f4aa43a8b'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:{**p,'sha256':p['canonicalSHA256']} for p in ps['actualCurrentPeers']};focus=docs['receipt.json']['entries'][0];assert m.sha(focus['currentCard'])==focus['currentCardCanonicalSHA256'];actual[focus['id']]={'id':focus['id'],'topicId':focus['topicId'],'card':focus['currentCard'],'sha256':focus['currentCardCanonicalSHA256']};
for hist in ps['relevantGenuineProposals']:
 live=next(q for q in m.read(C/'src/content/topics/polar-regions.json')['questions'] if q['id']==hist['id'])
 if hist['card']==live and m.sha(live)==hist['canonicalSHA256']:
  actual[hist['id']]={'id':hist['id'],'topicId':'polar-regions','card':hist['card'],'sha256':hist['canonicalSHA256']}
ps['actualCurrentPeers']=list(actual.values());target=actual[focus['id']];pairs=[]
for row in ps['bilateralMAINComparisons']:
 peer=actual[row['peerId']];assert peer['sha256']==row['peerCanonicalSHA256'] and row['status']=='DISTINCT_MAIN' and row['directReverseAssessment'].startswith('No ')
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['currentERVC']},'right':{**peer,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['currentToPeer'],'rightToLeft':row['peerToCurrent'],'originalAssessment':row})
ps['latestProposalSnapshots']=[]
for hist in ps['relevantGenuineProposals']:
 assert m.sha(hist['card'])==hist['canonicalSHA256']
 if hist['id'] in actual and hist['canonicalSHA256']==actual[hist['id']]['sha256']:
  assert hist['card']==actual[hist['id']]['card'];continue
 path=C/hist['sourcePath'];entry=next(e for e in m.read(path)['entries'] if e['id']==hist['id']);assert entry['proposedCard']==hist['card'] and entry['afterHash']==hist['canonicalSHA256'] and entry['status']=='READY_FOR_INDEPENDENT_REVIEW'
 prop={**hist,'sha256':hist['canonicalSHA256'],'state':hist['state'] if hist['state'].startswith('UNAPPLIED_') else 'UNAPPLIED_'+hist['state']};ps['latestProposalSnapshots'].append({'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path),'proposal':prop})
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT'},'right':prop,'leftToRight':hist['bothDirections'],'rightToLeft':hist['bothDirections'],'originalJointBothDirectionAssessment':hist['bothDirections']})
ps['bilateralMainComparisons']=pairs
for entry in docs['receipt.json']['entries']:
 entry['fourFullPromptAnswerNoteVariants']=entry['fourFullPromptAnswerNoteAssessments']
 for variant in entry['fourFullPromptAnswerNoteVariants']:
  noteGroup=next(g for g in entry['sixLiteralCanonicalGroups'] if g['group']=='note'+str(variant['slot']));assert noteGroup['literal']==variant['note'] and variant['status']=='PASS'
  variant['tripleCanonicalSHA256']=variant['tripleSHA256'];variant['plausibility']=variant['individualGround'];variant['truthUniqueKey']=variant['individualGround'];variant['noteTruthUsefulness']=noteGroup['individualGround']
src=docs['sources.json'];src['sources']=src['rawSources']
for source in src['sources']:
 source['personalReadEvidence']=source.get('personalReadEvidence',source.get('readEvidence'));loc=[]
 for entry in docs['receipt.json']['entries']:
  for group in entry['sixLiteralCanonicalGroups']:
   for ref in group['sourcesLocators']:
    if ref.get('path',ref.get('source'))==source['path'] and ref['locator'] not in loc:loc.append(ref['locator'])
 source['locators']=loc;assert loc
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':freeze,'operation':'Only canonicalSHA256→sha256 and structuredpair field aliases; focus currentCard/fullhash from exact reader receipt linked as actual focus body for pair references; existingverbatimdirections/ERVC/reverseassessment retained. Whole4Assessments→Variants; tripleSHAalias; existingjointvariantground copiedverbatim to plausibility/truthUniqueKey, noteTruthUsefulness uses SAMEslot literalgroup individualground verifiedequalnote. ExistingpersonalReadEvidence preserved andlocators takenverbatimfromexactreceiptgroupreferencessamepath. Already-current full personallyread proposalhistory bodies equalactual freshlyverified; theirmissingrowaliases linked fromsame reader wholebody/hash (no newquality);26fullunapplied55ca body/hash boundtoverbatimreaderprovidedSOURCEcycle1path READYrawcfcd, distinctfromactual26cf49/no26acceptance.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
