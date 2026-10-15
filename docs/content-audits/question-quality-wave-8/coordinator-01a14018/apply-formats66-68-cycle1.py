"""Compose verbatim SOURCE cycle1 judgments into standard packet and apply two."""
import pathlib,importlib.util,copy,json
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books66-68-cycle1-01a14018/author';B=D/'qualified-formats66-68-cycle1';B.mkdir(exist_ok=True)
candidate=m.read(A/'candidate.json');source=m.read(A/'sourceproof.json');peer=m.read(A/'peer-snapshot.json');manifest=m.read(A/'manifest.json');assert manifest['cycle']==1 and len(candidate['entries'])==2
cards={e['id']:e for e in candidate['entries']};entries=[]
for e in candidate['entries']:
 assert e['status']=='READY';e['originalAuthorStatus']=e['status'];e['status']='READY_FOR_INDEPENDENT_REVIEW'
 if e['sourceOrder']==68:
  expected=copy.deepcopy(e['beforeCard']);expected['answers'][1]['note']=e['proposedCard']['answers'][1]['note'];assert expected==e['proposedCard']
for item in source['items']:
 c=cards[item['id']]['proposedCard'];vs=item['variantAssessments'];assert len(vs)==4 and {v['slot'] for v in vs}==set(range(4));assert m.sha(c)==item['afterHash']
 for v in vs:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and m.sha(tr)==v['variantTripleSHA256'] and v['isKey']==(k==c['correctIndex'])
  v['grammar']=v['grammarAssessment'];v['plausibilityUniqueKeyAndNoteTruthUsefulness']=v['plausibilityAndUniqueKey']+'\n'+v['noteTruthAndUsefulness'];v['tripleSHA256']=v['variantTripleSHA256']
 groups=[]
 for original in item['literalGroups']:
  g=copy.deepcopy(original);assert m.sha(g['literal'])==g['afterCanonicalSHA256'];g['literalSHA256']=g['afterCanonicalSHA256'];g['originalSourceAssessment']=g['assessment']
  chosen=[next(v for v in vs if v['slot']==int(g['group'][4:]))] if g['group'].startswith('note') else vs
  g['primaryGround']='\n'.join(v['plausibilityAndUniqueKey']+' '+v['noteTruthAndUsefulness'] for v in chosen)
  if g['group']=='explanation':g['explicitSourceExplanationReference']=item['explanationPrimaryGround']
  g['technicalComposition']='Resolved SOURCE explicit see-variant reference by copying existing corresponding individual SOURCE judgments verbatim; no new root factual ground.'
  groups.append(g)
 entries.append({'id':item['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','literalGroups':groups,'fourFullPromptAnswerNoteAssessments':vs,'correctNoteNewFact':item['correctNoteNewFact'],'absoluteDifficulty':item['actualDifficulty'],'originalSourceItem':item})
for s in source['rawSources']:
 assert m.raw(C/s['path'])==s['sha256'] and s['personallyRead'] and s['locators']
 if s.get('readPath'):assert m.raw(pathlib.Path(s['readPath']))==s['readTextSHA256']
actual=[{'id':p['id'],'topicId':'books-publishing','sourceOrder':p['index']+1,'card':p['card'],'sha256':p['sha256']} for p in peer['actualCurrentTopic']['cards']]
# Existing full cross-catalog captures remain exact; preserve source-selected extra context.
prior=m.read(D/'qualified-formats4/peer-snapshot.json')
actual += [p for p in prior['actualCurrentPeers'] if p['topicId']!='books-publishing']
cat={}
for t in {p['topicId'] for p in actual}:cat.update({q['id']:q for q in m.read(C/f'src/content/topics/{t}.json')['questions']})
for p in actual:assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
for p in peer['proposedCards']:assert p['card']==cards[p['id']]['proposedCard'] and m.sha(p['card'])==p['afterHash']
for p in peer['protectedMainChecks']:assert m.sha(cat[p['id']])==p['hash']
first5={e['id']:e['proposedCard'] for e in m.read(C/'docs/content-audits/question-quality-wave-8/process-v2-books31-50-01a14018/author/source-completion/qualified-first5/candidate.json')['entries']}
for p in peer['latestProposedMAIN']['cards']:assert p['card']==first5[p['id']] and m.sha(p['card'])==p['hash']
peer['actualCurrentPeers']=actual;peer['retainedPriorCrossRetrieval']='qualified-formats4 includes exact9 current fullcrosshits; original SOURCE already compared Adobe-origin PDF relation; extra incidental hits remain incidental.'
proof={'rawSources':source['rawSources'],'entries':entries,'sourceOriginal':str((A/'sourceproof.json').relative_to(C)),'technicalComposition':'Mechanical field/status aliases; individual existing SOURCE grounds resolved into literal groups and variants; no new root semantic proof.'}
m.write(B/'candidate.json',candidate);m.write(B/'sourceproof.json',proof);m.write(B/'peer-snapshot.json',peer)
same={'actualCurrentPeers':[p for p in actual if p['topicId']=='books-publishing']}
q=m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[66,68],None,None,None,qualifyOnly=True,peerSnapshot=same)
m.write(D/'qualification-formats66-68-cycle1.json',{'status':'SOURCE_CYCLE1_QUALIFIED_PENDING_CURRENT_FINAL','sourceOriginal':str(A.relative_to(C)),'verified':{'cards':2,'literalGroups':12,'individualVariants':8,'actualPeers':len(actual),'protectedCertified65_67Unchanged':True,'only68Note1Changed':True,'first5ProposedBindings':5},'qualification':q,'finalAttention':['66 actualMEDIUM print-production boundary distinction, onekey and concrete ownextra (TrimBox default CropBox).','Fresh FULL MAIN comparisons include current trim-process37 and physical page53 versus proposed PDF box66; SOURCE full100 stored, prior crossAdobe-origin relation preserved; reader personally adjudicates each relevant relation.','68 exact page-tree wording only; SOURCE singular Kindle§8.2 explanation reference and extracted75 corrected; no unchanged secondcycle.'],'qualityCredit':0})
m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[66,68],D/'apply-formats66-68-cycle1.json',D/'qa-formats66-68-cycle1.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['SOLE directed substantivecycle1 after INITIALFIX66level/68wording. ExactSOURCE2 complete12/8 withprimaryTable30/page-tree/Kindle75; originalSOURCE alternate schema composed verbatim tostandard, no invented root grounds.','Do not touch protected certified65/67 or pendingfirst5. FINAL unresolvedHOLD0; no automatic secondcycle.','66 newMAIN page-print TrimBox physical finished-size distinction must independently pass actualMEDIUM, not cosmetictechnicalwords. Preserve inherited/default conditions and onekey. 68 onlyPDFnote1changed.','FINAL must personally judge relevant trimming-process37/physical-page53/currentAdobe-origin crosspeer and actual/proposedfirst5; canonicalwrongnote factpool allowed.'])
