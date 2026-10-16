"""Technical SOURCE proof shape normalization; preserve every candidate literal and SOURCE judgment."""
import pathlib,importlib.util,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py')
S=C/'docs/content-audits/question-quality-wave-8/process-v2-parks6-15-fresh-01a142a3/author/proof-completion'
Old=S.parent
B=D/'qualified-parks6-8-cycle1-sourced8';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'}
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');original=m.read(Old/'sourceproof.json')
proposed={e['id']:e['proposedCard'] for e in a['entries']}
for e in sp['entries']:
 assert 'fourFullPromptAnswerNoteAssessments' not in e
 e['fourFullPromptAnswerNoteAssessments']=e.pop('fourFullPromptAnswerNoteVariants')
 for v in e['fourFullPromptAnswerNoteAssessments']:
  assert 'plausibilityUniqueKeyAndNoteTruthUsefulness' not in v
  v['plausibilityUniqueKeyAndNoteTruthUsefulness']={k:v[k] for k in ['plausibility','truthUniqueKey','noteTruthUsefulness']}
  v['locator']='; '.join(v['sourcesLocators'])
# SOURCE's explicitly compared global peers are distinct from its retained full-topic snapshot.
ps['sourceFullTopicSnapshot']=ps['actualCurrentPeers']
closest=ps['globalMainRetrieval']['closestCurrentCards']
by={p['id']:p for p in closest}
for pair in ps['globalMainRetrieval']['bilateralMainComparisons']:
 p=pair['actualCurrentPeer'];by[p['id']]=p
 c=pair['candidate'];assert c['card']==proposed[c['id']]and m.sha(c['card'])==c['sha256']
 assert c['assessment']and pair['reverseAssessmentFromPeer']
ps['actualCurrentPeers']=list(by.values())
for p in ps['sourceFullTopicSnapshot']+ps['actualCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions']if q['id']==p['id'])
 assert p['card']==q and m.sha(q)==p['sha256']
# Retain the same author's original concrete mutual ERVC prose. Only source metadata changed.
def MAIN(card):
 return {'prompt':card['prompt'],'answers':[x['text']for x in card['answers']],'correctIndex':card['correctIndex']}
latestPairs={frozenset([r['left']['id'],r['right']['id']]):r for r in ps['proposedMutualPairs']}
mutual=[]
for old in original['mutualERVC']:
 pair=copy.deepcopy(latestPairs[frozenset([old['left']['id'],old['right']['id']])])
 for side in ['left','right']:
  previous=old[side];current=pair[side];assert previous['id']==current['id']
  assert current['card']==proposed[current['id']]and m.sha(current['card'])==current['sha256']
  assert MAIN(previous['card'])==MAIN(current['card'])and previous['assessment']
 pair['leftToRight']=old['left']['assessment'];pair['rightToLeft']=old['right']['assessment']
 pair['SOURCEAssessmentLineage']='Concrete prior same-author MAIN judgment, unchanged prompt/ordered-answer/key; current fullcard/hash explicitly supplied again by SOURCE in its completed latest mutual pair. Older non-MAIN source/explanation snapshots are not promoted.'
 mutual.append(pair)
ps['relevantProposedPairs']=mutual
for obj in [a,sp,ps]:
 obj['rootNormalization']={'coordinator':m.O,'actualSourceNativeId':'01a142d8-32ad-7621-83d1-4865c76c51f5','sourceOriginal':str(S.relative_to(C)),'sourceOriginalFreeze':'d4d41d12c52c4c57fe639872499fe3e7017ce07c','earlierSourceMutualProof':str((Old/'sourceproof.json').relative_to(C)),'earlierSourceFreeze':'5926bccc0cd5591f1083414283396007f06cc99e','transformations':['fourFullPromptAnswerNoteVariants field exposed under standard Assessments name','Existing SOURCE plausibility/unique-key/truth/usefulness judgments grouped without prose change; sourcesLocators joined as locator','Explicitly compared global full peers promoted from existing SOURCE closest/pair records; complete100 topic snapshot retained separately','Original same-author concrete mutual MAIN prose attached to fullcard/hash explicitly supplied in latest SOURCE mutual pair; MAIN prompt/ordered-answer/key byteidentical, older non-MAIN source/explanation snapshots retained only as lineage'],'wordingOrJudgmentChangedByRoot':False,'qualityCredit':0}
for name,obj in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/name,obj)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
r=app.apply(B,'01a142d8-32ad-7621-83d1-4865c76c51f5',[6,7,8],D/'apply-parks6-8-cycle1.json',D/'qa-parks6-8-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']})
m.write(D/'qualification-parks6-8-cycle1.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'relevantGlobalPeers':len(ps['actualCurrentPeers']),'sourceMutualPairs':len(mutual),'qualityCredit':0})
print('sourceFreeze',m.savecode([pathlib.Path(__file__),D/'qualification-parks6-8-cycle1.json']+list(B.iterdir()),'Freeze exact SOURCEanimal6-8 gradecycle1 technical shapes and original meaningfulSOURCE comparisons; no credit'))
