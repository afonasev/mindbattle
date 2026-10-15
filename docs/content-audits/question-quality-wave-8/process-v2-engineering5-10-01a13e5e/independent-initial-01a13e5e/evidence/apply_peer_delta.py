import json,hashlib,subprocess
from pathlib import Path
P=Path('docs/content-audits/question-quality-wave-8/process-v2-engineering5-10-01a13e5e');O=P/'independent-initial-01a13e5e';E=O/'evidence'
def enc(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(enc(x)).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=json.loads((O/'receipt.json').read_text());assert old['status']=='FIX'
history=E/'receipt-initial-before-peer-delta.json';assert not history.exists();history.write_bytes((O/'receipt.json').read_bytes())
q=json.loads(Path('src/content/topics/engineering-machines.json').read_text())['questions'];by={c['id']:c for c in q}
apply=json.loads((P/'apply-initial5-6.json').read_text());assert len(apply['applied'])==2
committed=json.loads(subprocess.check_output(['git','show','0490354c8cd8ce8d0753274e3a87c6fcaa1383a7:src/content/topics/engineering-machines.json'],text=True));cb={c['id']:c for c in committed['questions']}
peerIds=['engineering-machines-bolt-fastener','engineering-machines-screw-fastener']
for p in apply['applied']:
 assert by[p['id']]==p['proposedCard']==cb[p['id']]
 assert sha(by[p['id']])==p['proposedSHA256']
for c in old['cards']:assert sha(by[c['id']])==c['canonicalSHA256']
prev=json.loads((E/'current-peers-full.json').read_text());before={c['id']:c for c in prev['fullRelevantCards']}
comparisons=[]
for c in old['cards']:
 t=by[c['id']];isNut=c['id'].endswith('nut-fastener');label='Гайка' if isNut else 'Заклёпка'
 for pid in peerIds:
  p=by[pid];an=next(a for a in p['answers'] if a['text']==label)
  rev=next(a for a in t['answers'] if a['text']==('Болт' if pid.endswith('bolt-fastener') else 'Винт'))
  comparisons.append({'targetId':t['id'],'targetFullCardCanonicalSHA256':sha(t),'peerId':pid,'peerFullCardCanonicalSHA256':sha(p),'status':'PASS','directions':[{'from':pid,'to':t['id'],'fromPromptQuote':p['prompt'],'fromAnswerNoteQuote':an['note'],'fromExplanationQuote':p['explanation'],'targetPromptQuote':t['prompt'],'status':'PASS','grounds':('The new peer note labels a specific nylon locknut and explains insert compression. It no longer states the female receiving thread screwed onto a bolt. Its stem/explanation instead identifies shear-bolt loading or self-tapping-screw operation; neither supplies the nut target relationship.' if isNut else 'The new peer rivet note states permanent installation and drilling removal. It no longer states insertion plus formation of a second/closing head. The replacement peer stem/explanation concerns shear loading or self-tapped threads, not the target rivet-setting discriminator. Removal is an adjacent practical fact, not the answer-defining operation.')},{'from':t['id'],'to':pid,'fromPromptQuote':t['prompt'],'fromNoteQuote':rev['note'],'fromExplanationQuote':t['explanation'],'targetPromptQuote':p['prompt'],'status':'PASS','grounds':('The unchanged target gives generic bolt materials and generic bolt/nut pairing or rivet setting. It says nothing about shear-bolt loading versus tension, nor half torque; it does not teach the new peer5 answer.' if pid.endswith('bolt-fastener') else 'The unchanged target warns of screw/bolt terminology overlap but says nothing about self-cutting mating threads in an unthreaded undersize hole. Its stem/explanation also lacks that operation; it does not teach the new peer6 answer.')}],'previousFinding':'CURRENT-PEER-ANSWER-LEAKAGE resolved for this exact actual peer snapshot only; not an approval of peer5/6 quality.'})
unchanged={k:old[k] for k in ['rootBindingCanonicalSHA256','rootBindingPath','groups12RootCanonicalSHA256','scope','nylonJudgement','rivetCorrectNoteJudgement']}
delta={'stage':'INITIALCURRENT2 narrow actual-CURRENT peer delta','triggerCommit':'0490354c8cd8ce8d0753274e3a87c6fcaa1383a7','priorReceiptPath':str(history),'priorReceiptRawSHA256':raw(history),'scope':'Only changed current peer5/6 and their bidirectional dependency with unchanged targets7/8. No new INITIAL or source/grammar/difficulty approval of 5/6.','unchanged7and8':unchanged,'retainedIndependentConclusions':'All 12 groups, eight full triples, source/nylon/extra-correct-note/easy/frozen conclusions retained from independent initial reading without rereading unchanged content. Final7/8 self-pair unchanged; other full peers unchanged.','peerChangeBindings':[{'id':pid,'beforeFullCard':before[pid]['fullCard'],'beforeFullCardCanonicalSHA256':before[pid]['canonicalSHA256'],'currentFullCard':by[pid],'currentFullCardCanonicalSHA256':sha(by[pid]),'exactApplyAndCommitMatch':True} for pid in peerIds],'comparisons':comparisons,'judgement':'PASS for 7/8 CURRENT context after removal of the defining old peer notes. New peer facts concern materials, locking/removal, load subtype and self-tapping operation. They do not supply the 7/8 internal-bolt-receiving or formed-head discriminators.','historicalFinding':{'id':'CURRENT-PEER-ANSWER-LEAKAGE','previousStatus':'FIX','currentStatus':'RESOLVED_FOR_EXACT_CURRENT_PEERS','retainedEvidence':str(E/'current-peers-full.json')},'qualityCredit':0,'peer5and6InitialQuality':'NOT_REVIEWED: known category/grammar cue concern is outside this peer-only delta; remains coordinator separate review.','sourceDelta':'No 7/8 source-claim change. No NASA reread/refetch or FAA source review needed for detecting/removing lexical/semantic answer leakage.','testsRuntimeBuild':'Not run, explicitly excluded.'}
save(E/'current-peer-delta.json',delta)
root={'unchangedInitialRoot':json.loads((E/'root-binding.json').read_text()),'peerDeltaCanonicalSHA256':sha(delta),'peerDeltaPath':str(E/'current-peer-delta.json'),'currentPeers':[{'id':pid,'canonicalSHA256':sha(by[pid])} for pid in peerIds],'effectiveStatuses':[{'id':c['id'],'canonicalSHA256':c['canonicalSHA256'],'status':'PASS'} for c in old['cards']]}
save(E/'current-root-binding.json',root)
new=dict(old);new['status']='PASS';new['stage']='INITIALCURRENT2 with narrow actual-CURRENT peer delta';new['observedHEAD']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();new['previousReceiptPath']=str(history);new['previousReceiptRawSHA256']=raw(history);new['rootBindingPath']=str(E/'current-root-binding.json');new['rootBindingCanonicalSHA256']=sha(root);new['peerDeltaPath']=str(E/'current-peer-delta.json');new['peerDeltaCanonicalSHA256']=sha(delta)
new['cards']=[{**c,'status':'PASS','defects':[],'catalogContextStatus':'PASS','reason':'Old 5/6 defining notes replaced in exact CURRENT; narrow bidirectional delta completed.'} for c in old['cards']]
new['findings']=[{**f,'status':'RESOLVED_FOR_EXACT_CURRENT_PEERS','resolutionEvidence':str(E/'current-peer-delta.json')} for f in old['findings']]
new['qualityCredit']=0
new['independence']=old['independence']+' Subsequently personally read full actual changed 5/6 cards and their exact apply bindings; checked only affected bidirectional semantic leakage for unchanged7/8. Historical FIX remains in preserved receipt.'
new['checks']={**old['checks'],'narrowPeerDeltaExactCommit':'0490354c8cd8ce8d0753274e3a87c6fcaa1383a7','changedPeerFullCardsMatchApplyAndCommit':True,'unchangedTargetHashesVerified':True,'snapshotDriftOnly7and8':'Historical initial condition; new current differs by peer5/6 as explicitly bound in delta.'}
new['preservation']={**old['preservation'],'nextAction':'Coordinator adjudicates the current PASS of 7/8 and saves receipt plus all evidence/history in Git before archiving; separately reviews initial5/6. No tests/build/claim/index mutations performed.'}
new['evidenceManifest']=[{'path':str(f),'rawSHA256':raw(f),'bytes':f.stat().st_size} for f in sorted(E.iterdir()) if f.is_file()]
save(O/'receipt.json',new)
print(json.dumps({'status':new['status'],'cards':new['cards'],'root':new['rootBindingCanonicalSHA256'],'peerHashes':root['currentPeers']},ensure_ascii=False))
