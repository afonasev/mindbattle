import pathlib,importlib.util
D=pathlib.Path(__file__).parent;s=importlib.util.spec_from_file_location('cert',D/'certification-common.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);C,P=m.C,m.P;read,sha,raw=m.read,m.sha,m.raw;B=C/'docs/content-audits/question-quality-wave-8/process-v2-engineering-new-wheel-pulley2-01a13e5e/independent-initial-01a13e5e';R=B/'receipt.json';r=read(R);E=B/'evidence';cards=read(E/'full-current-six-groups-four-variants.json');current={q['id']:q for q in read(C/'src/content/topics/engineering-machines.json')['questions']};oldB=C/'docs/content-audits/question-quality-wave-8/process-v2-engineering1-10-01a13e5e/author-cycle1-01a13e5e';oldAuth={e['id']:e for e in read(oldB/'candidate.json')['entries']};newB=B.parent/'author/final';newAuth={e['id']:e for e in read(newB/'candidate.json')['entries']};newProof={e['id']:e for e in read(newB/'sourceproof.json')['entries']};assert len(r['entries'])==2 and all(e['status']=='PASS' for e in r['entries'])
source=read(E/'source-review.json')
for src in source['rawSources']:assert raw(C/src['path'])==src['rawSHA256']
for p in read(E/'actual-peer-snapshot-and-bidirectional-pair.json')['peers']:assert p['fullCURRENT']==current[p['id']] and sha(p['fullCURRENT'])==p['canonicalSHA256']
accepted=[]
for e in cards:
 i=e['id'];c=current[i];assert e['status']=='PASS' and c==e['fullCURRENT'] and sha(c)==e['canonicalSHA256'];gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(e['sixLiteralGroups'])==6
 for g in e['sixLiteralGroups']:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['canonicalSHA256'] and g['status']=='PASS'
 vs=e['fourFullPromptAnswerNoteAssessments'];assert len(vs)==4 and {v['slot'] for v in vs}==set(range(4))
 for v in vs:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert all(v[k]==tr[k] for k in tr) and sha(tr)==v['tripleCanonicalSHA256'] and v['status']=='PASS'
 if e['sourceOrder']==2:
  assert c==oldAuth[i]['proposedCard'] and sha(c)==oldAuth[i]['proposedCanonicalSHA256']
  for g in oldAuth[i]['sixLiteralGroups']:assert g['after']==gs[g['group']] and sha(g['after'])==g['afterCanonicalSHA256']
  oldV=next(x for x in read(oldB/'proof-variants-addendum.json')['entries'] if x['id']==i);assert oldV['proposedFullCardCanonicalSHA256']==sha(c)
  for v in oldV['slots']:
   k=v['slot'];assert v['fullPrompt']==c['prompt'] and v['fullAnswer']==c['answers'][k]['text'] and v['fullNote']==c['answers'][k]['note']
  author='01a13ec5-dca5-7db3-b6b7-b1303219898c';authorReceipt=oldB/'proof-variants-addendum.json';basis='Exact same author fullCURRENT2/source6groups4variants retained; earlier FINALHOLD was only changedpeer named-example leak. NEW4premise eliminates that dependency and freshOTHER independently rereadall2/source, no inheritedPASS.'
 else:
  assert e['sourceOrder']==4 and c==newAuth[i]['proposedCard'] and sha(c)==newAuth[i]['afterHash']
  for g in newProof[i]['sixLiteralGroups']:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['literalSHA256']
  author='01a13ee9-8cf3-7d22-bd57-1360441f9001';authorReceipt=newB/'sourceproof.json';basis='ConcreteNEW4construction premise, actualnamedexamples absent fromprompt. Existingacceptednote/explanation preservedexactly; independentlyverifiednewcompletecard/group/variant/primary/actualpeers.'
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':author,'authorReceipt':str(authorReceipt.relative_to(C)),'readerNativeId':'01a13f07-9d8e-70f1-932f-3c4c1379bb00','independentReceipt':str(R.relative_to(C)),'readerReceiptRawSHA256':raw(R),'coordinatorDecision':basis+' Originaloldterminal receipts preserved0; thissource/editorialcredit belongs only actualNEWpair context.'})
q=read(D/'qa-NEW-wheel4-cycle1-fasteners56.json');assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0;out=D/'certification-NEW-wheel-pulley.json';report={'verified':{'authorOld2New4FullcardAnd6groups':True,'freshOTHER12groups8variants':True,'fullPrimarySourceBytes':True,'actualPeersAndBidirectionalNewPair':True},'sourceProvenanceCorrection':r['evidenceCorrection'],'primaryProvenance':source['provenanceCorrection'],'oldTerminalHistory':r['oldTerminalHistory'],'QA':{'commit':'51d65ba1f5c2834cae4da5759fbb8f88b3eae576','passed':19,'failed':0,'pending':0,'sourceBytesUnchanged':True}};files=[p for p in E.rglob('*') if p.is_file()]+[R,pathlib.Path(__file__).resolve()];m.certify(accepted,report,703,8,out,files,'51d65ba1f5c2834cae4da5759fbb8f88b3eae576')
