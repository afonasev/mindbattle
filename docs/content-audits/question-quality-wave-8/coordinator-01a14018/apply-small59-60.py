"""Normalize SOURCE small2; reconcile literal-identical first5 proposal promotion."""
import pathlib,importlib.util,copy,sys
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books51-70-01a14018/author/source-completion/remaining16/ready-first-small/qualification-completion2';B=D/'qualified-small59-60';B.mkdir(exist_ok=True)
candidate=m.read(A/'candidate.json');source=m.read(A/'sourceproof.json');peer=m.read(A/'peer-snapshot.json');prior={e['id']:e['proposedCard'] for e in m.read(A.parent/'candidate.json')['entries']};entries=[]
for e in candidate['entries']:
 assert e['status']=='READY';e['originalSourceStatus']='READY';e['status']='READY_FOR_INDEPENDENT_REVIEW';p=copy.deepcopy(prior[e['id']]);p['explanation']=e['proposedCard']['explanation'];assert p==e['proposedCard']
cards={e['id']:e for e in candidate['entries']}
for item in source['items']:
 c=cards[item['id']]['proposedCard'];assert m.sha(c)==item['proposedCardHash'];vs=item['fourFullPromptAnswerNoteAssessments'];assert len(vs)==4 and {v['slot'] for v in vs}==set(range(4))
 for v in vs:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and m.sha(tr)==v['variantTripleSHA256']
  v['grammar']=v['grammarAssessment'];v['plausibilityUniqueKeyAndNoteTruthUsefulness']='\n'.join(v[x] for x in ['answerTruthAndPlausibility','noteTruthAndUsefulness','uniqueKeyAssessment']);v['locator']=v['locators'];v['tripleSHA256']=v['variantTripleSHA256']
 groups=[]
 for original in item['literalGroups']:
  g=copy.deepcopy(original);assert m.sha(g['literal'])==g['sha256']==g['afterCanonicalSHA256'];g['literalSHA256']=g['afterCanonicalSHA256'];g['originalSourceReview']=g['review'];chosen=[next(v for v in vs if v['slot']==int(g['group'][4:]))] if g['group'].startswith('note') else vs
  g['primaryGround']='\n'.join(v['answerTruthAndPlausibility']+' '+v['noteTruthAndUsefulness']+' '+v['uniqueKeyAssessment'] for v in chosen);g['locator']=g['locators'];g['technicalComposition']='Verbatim existing corresponding SOURCE variant judgments resolve the SOURCE literal-group review reference, without new root factual grounds.'
  if g['group']=='explanation':g['sourceExplanationAssessment']=item['explanationAssessment']
  groups.append(g)
 entries.append({'id':item['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','literalGroups':groups,'fourFullPromptAnswerNoteAssessments':vs,'correctNoteNewFact':item['correctNoteNewFact'],'absoluteDifficulty':item['actualDifficulty']})
for s in source['rawSources']:assert m.raw(C/s['path'])==s['sha256'] and s['personallyRead'] and s['locators']
actual=[{'id':p['id'],'topicId':'books-publishing','sourceOrder':p['index']+1,'card':p['card'],'sha256':p['sha256']} for p in peer['actualCurrentTopic']['cards']]
for p in peer['globalActualRetrieval']['hits']:actual.append({'id':p['id'],'topicId':p['topicId'],'sourceOrder':p['index']+1,'card':p['card'],'sha256':p['sha256']})
cat={}
for t in {p['topicId'] for p in actual}:cat.update({q['id']:q for q in m.read(C/f'src/content/topics/{t}.json')['questions']})
latest={p['id']:p for p in peer['latestProposedMAIN']['items']};promoted=[]
for p in actual:
 assert m.sha(p['card'])==p['sha256']
 if p['card']!=cat[p['id']]:
  q=latest[p['id']];assert q['card']==cat[p['id']] and m.sha(q['card'])==q['hash'];promoted.append({'id':p['id'],'topicId':p['topicId'],'sourceOrder':p['sourceOrder'],'card':q['card'],'sha256':q['hash']})
assert len(promoted) in [0,5]
delta=D/'small59-60-peer-promotion-first5.json'
if promoted:m.write(delta,{'actualCurrentPeers':promoted,'meaning':'Exactly identical SOURCE-read first5 proposed cards are now applied CURRENT; only workflow state promoted, no new semantic claim or literal.','sourceProof':str((A/'peer-snapshot.json').relative_to(C)),'qualityCredit':0})
peer['actualCurrentPeers']=actual;peer['rootPromotionDelta']=str(delta.relative_to(C)) if promoted else None
m.write(B/'candidate.json',candidate);m.write(B/'sourceproof.json',{'rawSources':source['rawSources'],'entries':entries,'sourceOriginal':str((A/'sourceproof.json').relative_to(C)),'technicalComposition':'Only field/status aliases and existing SOURCE individual grounds; exact candidate text preserved.'});m.write(B/'peer-snapshot.json',peer)
same={'actualCurrentPeers':[p for p in actual if p['topicId']=='books-publishing']}
q=m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[59,60],None,None,None,qualifyOnly=True,peerSnapshot=same,peerAddendum=delta if promoted else None)
m.write(D/'qualification-small59-60.json',{'status':'SOURCE_QUALIFIED_NOT_YET_INDEPENDENT','sourceOriginal':str(A.relative_to(C)),'verified':{'cards':2,'literalGroups':12,'individualVariants':8,'actualPeers':len(actual),'sourceReadFirst5PromotionCount':len(promoted)},'qualification':q,'qualityCredit':0})
if '--apply' in sys.argv:
 m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[59,60],D/'apply-small59-60.json',D/'qa-first5-small2.json',pathlib.Path(__file__),peerSnapshot=same,peerAddendum=delta if promoted else None,concerns=['Only two originalremaining16 SOURCE-complete questions59/60; other14 remain unverified, no implicit HOLD completion.','SOURCE full primary book-parts/manual/CIEP ownnotes/extra/EASY and distinct individual8variant judgments; correctedexplanations two sentences/directkey. Reader independently assess factual scope/grammar/onekey/level/source/MAIN.','Same current100 withsource-read first5 proposal→CURRENT identicalliteral promotion only, full sourceconcurrent5 hashes preserved. No crossnoteban; MAIN entity/relation/value/context/directreverse.'])
