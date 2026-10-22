import json,hashlib,copy,pathlib
ROOT=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE=ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a16329'
OUT=BASE/'source-history-russia91-cycle1'
NATIVE='01a164f2-bdf7-78b1-a2b1-803a3d34a4f0'
OWNER='01a16329-04c9-75f0-806f-091bcec4b169'
TOPIC='history-russia'
def canon(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def fields(c): return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(c['answers'])}}
task=json.load(open(BASE/'source-history-russia91-cycle1-task.json'))
inv=json.load(open(OUT/'fresh-inventory.json'))
current=next(q for q in inv['sameTopicMAIN']['questions'] if q['id']==task['id'])
before=copy.deepcopy(current)
assert canon(before)==task['beforeHash']
after=copy.deepcopy(before)
after['prompt']='Какое из этих событий произошло в марте 1921 года?'
assert all(before[k]==after[k] for k in ['id','difficulty','correctIndex','explanation','source'])
assert all(before['answers'][i]==after['answers'][i] for i in range(4))
bg,ag=fields(before),fields(after)
fieldGroups={k:{'beforeCanonicalSHA256':canon(bg[k]),'afterCanonicalSHA256':canon(ag[k])} for k in bg}
BH,AH=canon(before),canon(after)
meta={'owner':OWNER,'sourceNativeId':NATIVE,'stage':'SOURCE_CYCLE1','cycle':1,'qualityCredit':0}
frozen={'id':task['id'],'topicId':TOPIC,'sourceOrder':91,'difficulty':'medium','correctIndex':3}
candidate={**meta,'scope':{'baselineCode':task['catalogCommit'],'catalogCandidate':task['catalogCommit'],'frozen':frozen,'cycle0QualifiedAfterHash':task['beforeHash']},'history':{'decision':'READY_FOR_SAME_READER_FINAL','cycle1Fix':'Prompt-only neutralization of the political qualifier that made all three distractors trivially rejectable. Notes, all labels, explanation, source metadata, and frozen fields are preserved.','initialReceipt':task['initialReceipt'],'initialReceiptSHA256':task['initialReceiptSHA256']},'entries':[{'id':task['id'],'topicId':TOPIC,'sourceOrder':91,'status':'READY_FOR_SAME_READER_FINAL','beforeCard':before,'beforeHash':BH,'proposedCard':after,'afterHash':AH,'fieldGroups':fieldGroups,'proposedCardCanonicalSHA256':AH}]}
# Use actual retained source rows from the qualified cycle0 packet, but declare each cycle1 field reference directly.
priorSP=json.load(open(BASE/'qualified-source-history-russia91/sourceproof.json'))
raw=copy.deepcopy(priorSP['rawSources'])
path_by_url={x['url']:x['path'] for x in raw}
url_k='https://www.prlib.ru/node/619247';url_bs='https://www.prlib.ru/history/618968';url_dec='https://www.prlib.ru/history/619844';url_feb='https://www.prlib.ru/history/619088'
paths={'kron':[path_by_url[url_k]],'bloody':[path_by_url[url_bs]],'dec':[path_by_url[url_dec]],'feb':[path_by_url[url_feb]],'all':[path_by_url[u] for u in [url_k,url_bs,url_dec,url_feb]]}
loc={'kron':'turn4view0 L63-L64','bloody':'turn4view0 L48-L50','dec':'turn3view0 L40-L45','feb':'turn1view0 L53-L60'}
source_text={
'prompt_ordered_answers_key':('The neutral prompt asks which of four historical events occurred in March 1921. The primary Kronstadt context directly identifies that event. Each alternative is a real event with its own official primary context, so none is made categorically absurd by a political qualifier.',paths['all'],'; '.join([loc['kron'],loc['bloody'],loc['dec'],loc['feb']])),
'explanation':('The retained primary page states that the Kronstadt uprising began in March 1921 and was soon suppressed. The explanation follows those exact claims.',paths['kron'],loc['kron']),
'note0':('The retained Presidential Library context documents the workers procession and 9 (22) January 1905 firing, grounding the Bloody Sunday date and event.',paths['bloody'],loc['bloody']),
'note1':('The retained Presidential Library context dates the Decembrist armed uprising to 14 (26) December 1825 in St Petersburg.',paths['dec'],loc['dec']),
'note2':('The retained Presidential Library context links the February Revolution to the overthrow of autocracy in 1917, grounding the monarchy-fall fact.',paths['feb'],loc['feb']),
'note3':('The retained Presidential Library context names the Kronstadt garrison and crews of some Baltic Fleet ships and dates their uprising against the Bolsheviks to March 1921.',paths['kron'],loc['kron'])}
literalGroups=[]
for group,literal in ag.items():
 ground,sp,locator=source_text[group]
 literalGroups.append({'group':group,'literal':literal,'literalSHA256':canon(literal),'primaryGround':ground,'sourcePaths':sp,'locator':locator})
oldslots=priorSP['entries'][0]['fourFullPromptAnswerNoteAssessments']
slot_assessments=[]
plausibility=[
'This names a genuine mass protest event, so it fits the neutral category of a historical event. It occurred in 1905, not March 1921; the option is now plausible without the previous regime-based giveaway. Its note is accurate and gives the procession’s context.',
'This is a genuine political uprising and fits the neutral event category. Its 1825 date makes it a plausible chronology distractor; knowing only that it is pre-Soviet no longer rejects it by a qualifier. Its note is accurate and useful.',
'This is a genuine revolution and fits the neutral category of historical events. The 1917 date makes it a plausible chronology distractor, rather than an obviously wrong political side. Its note is accurate and gives its consequence.',
'This is the only event matching March 1921. The date-to-event association requires Russian-history familiarity; the question no longer hands out a political-side test. The note adds the specific garrison and Baltic Fleet participants, supported by the retained primary page.'
]
for i,(a,old) in enumerate(zip(after['answers'],oldslots)):
 sourcepath=old['sourcePaths'][0]
 slot_assessments.append({'slot':i,'fullPrompt':after['prompt'],'answer':a['text'],'note':a['note'],'tripleSHA256':canon({'prompt':after['prompt'],'answer':a['text'],'note':a['note']}),'grammar':'Neutral «Какое из этих событий» fits each standalone event name without a case mismatch; labels and notes are unchanged.','plausibilityUniqueKeyAndNoteTruthUsefulness':plausibility[i],'sourcePaths':[sourcepath],'locator':old['locator']})
sourceproof={**meta,'rawSources':raw,'sourceIndex':{'cycle1SourceReuse':'Exact saved primary contexts reused from original SOURCE91 raw evidence. No network calls or new captures. Every field below binds direct actual sourcePaths and exact locators; no cycle0 technical alias is replayed.','promptAndRow':'The newly neutral prompt presents all four as events and asks for the month/year link. The retained official contexts verify each named event/date; see fourFullPromptAnswerAssessments.','absoluteDifficulty':'MEDIUM is supported by thematic recognition of the less widely known 1921 event among genuine Russian-history events; the row now relies on event/date knowledge rather than an easy political-era elimination.','cycle0IndependentInitial':'Initial reviewer identified only ANTI_BOLSHEVIK_QUALIFIER_ELIMINATES_ALL_DISTRACTORS. The prompt change directly removes that defect; no other text changed.'},'entries':[{'id':task['id'],'status':'READY_FOR_SAME_READER_FINAL','beforeHash':BH,'literalGroups':literalGroups,'fourFullPromptAnswerNoteAssessments':slot_assessments,'correctNoteNewFact':priorSP['entries'][0]['correctNoteNewFact'],'absoluteDifficulty':'Frozen MEDIUM remains appropriate: Russian-history familiarity helps identify the specific March 1921 event; outside that theme the date-event association is materially less familiar. The neutral wording no longer makes all distractors rejectable by political era alone. All four options are real historical events, with dates spanning 1825, 1905, 1917, and 1921.'}],'limitations':['All evidence is limited to retained original source bodies and locators.','No new network calls, source captures, QA, or independent review in this author cycle.','Quality credit remains zero pending same-reader FINAL and coordinator binding.'],'immutableFullOriginalToolOutputs':copy.deepcopy(priorSP['immutableFullOriginalToolOutputs']),'mechanicalIntake':{'cycle0QualifiedSourceproofPath':str(BASE/'qualified-source-history-russia91/sourceproof.json'),'cycle0QualifiedSourceproofSHA256':hashlib.sha256((BASE/'qualified-source-history-russia91/sourceproof.json').read_bytes()).hexdigest(),'cycle0OriginalRawPath':str(BASE/'source-history-russia91/sourceproof.json'),'cycle0OriginalRawUnmodified':True,'currentInventory':'fresh-inventory.json','currentInventorySHA256':hashlib.sha256((OUT/'fresh-inventory.json').read_bytes()).hexdigest(),'operation':'Direct cycle1 source bindings and hashes; no copied source bodies; no source-index alias normalization.'}}
# Current selected peer inventory: 14 reviewed cards including target; exclude self for 13 bilateral pairs.
oldPeers=json.load(open(BASE/'independent-history-russia91-initial/peers.json'))
old_selected=oldPeers['actualCurrentPeers']
current_by_id={x['id']:x for x in inv['actualCurrentPeers']}
# Cross-topic peer is read from its current source file and rehashed; same-topic peers are taken from fresh inventory.
selected=[]
for prior in old_selected:
 if prior['id']==task['id']:
  card=after
  info={'id':task['id'],'topicId':TOPIC,'sourceOrder':91,'card':card,'canonicalSHA256':canon(card),'sourcePath':inv['sameTopicMAIN']['path'],'fileSHA256':inv['sameTopicMAIN']['fileSHA256']}
 else:
  if prior['topicId']==TOPIC:
   q=current_by_id[prior['id']]['card']
   file_path=inv['sameTopicMAIN']['path']; file_hash=inv['sameTopicMAIN']['fileSHA256']
  else:
   f=ROOT/prior['sourcePath']; catalog=json.load(open(f)); q=next(z for z in catalog['questions'] if z['id']==prior['id']); file_path=prior['sourcePath']; file_hash=hashlib.sha256(f.read_bytes()).hexdigest()
  assert canon(q)==prior['canonicalSHA256'], prior['id']+' peer drift'
  info={'id':prior['id'],'topicId':prior['topicId'],'sourceOrder':prior['sourceOrder'],'card':copy.deepcopy(q),'canonicalSHA256':canon(q),'sourcePath':file_path,'fileSHA256':file_hash}
 selected.append(info)
assert len(selected)==14 and len([x for x in selected if x['id']!=task['id']])==13
# Every current topic card is retained as a whole current body; target updated to proposed postimage only in proposed candidate field.
actual_current=copy.deepcopy(inv['actualCurrentPeers'])
# Replace own target copy in actualCurrentPeers with current preimage (not the proposed card).
for x in actual_current:
 if x['id']==task['id']:
  x['card']=copy.deepcopy(before); x['sha256']=canon(before)
# Bilateral ERVC comparisons, re-evaluated against the neutral cycle1 prompt.
peer_notes={
'history-russia-revolution-1917-month':('October Revolution 1917','named as the October Revolution','Bolshevik seizure of power in autumn 1917','Russian Revolution','This peer identifies an event in 1917; the candidate identifies the event in March 1921. Different date and event.','The candidate does not name or identify the October Revolution; the peer does not ask which event occurred in March 1921.'),
'history-russia-civil-war-colors':('main forces of Russian Civil War','called','Reds and Whites','Russian Civil War 1918–1921','The peer asks for names of Civil War camps; the candidate asks for an event on a date. Different entity and relation.','Neither answer supplies the other card’s requested classification or event.'),
'history-russia-decembrist-year':('Decembrist uprising','dated by year','1825','Russian Empire','This peer dates a distinct uprising in 1825; candidate asks for a different event in 1921.','The candidate does not ask for the Decembrist year, and the peer does not identify the 1921 event.'),
'history-russia-nep-introduction':('New Economic Policy','introduced instead of War Communism','1921','Soviet Russia','Both cards touch 1921, but this peer asks for an economic policy introduced during that year; the candidate identifies an event that occurred in March. Entity and relation differ.','The candidate asks for an event, not a policy; the peer’s answer does not identify the Kronstadt uprising.'),
'history-russia-dual-power-1917':('dual-power institutions','two centers of authority','Provisional Government and Petrograd Soviet','Russia 1917','The peer asks for the institutions after the February Revolution in 1917; candidate asks for a dated 1921 event.','The candidate does not ask for 1917 institutions and cannot answer the peer’s question.'),
'history-russia-monarchy-ended':('February Revolution','caused abdication and monarchy fall','1917','Russian Empire','The peer asks what brought down the monarchy in 1917; candidate asks which event occurred in March 1921.','Different historical event, date, and relation.'),
'history-russia-decembrists-square':('Decembrist uprising','occurred at','Senate Square, December 1825','St Petersburg','The peer asks for the location of an 1825 event; candidate asks for a 1921 event.','The candidate does not ask for a location; the peer does not identify the March 1921 event.'),
'history-russia-bloody-sunday-event':('Bloody Sunday','named as','9 (22) January 1905 workers-procession shooting','St Petersburg, 1905','This peer names a 1905 event; the candidate asks for a separate March 1921 event. The Kronstadt phrase appears only among the peer’s distractors/notes, not its MAIN.','The candidate does not name the 1905 event or explain its procession; the peer does not ask for the March 1921 event.'),
'history-russia-abdication-emperor':('Nicholas II','abdicated','March 1917','Russian Empire','The peer identifies the emperor and abdication in 1917; candidate asks for an event in March 1921. Shared month wording does not mean shared event.','Neither card asks for the other’s entity or relation.'),
'history-russia-pugachev-rebellion':('Pugachev Rebellion','led by','Yemelyan Pugachev, 1773–1775','Catherine II era','Both are uprisings in Russian history, but these are distinct events separated by more than a century and with different actors.','The candidate does not ask about Pugachev or the 18th century; peer does not identify Kronstadt.'),
'history-russia-port-arthur-war':('defense of Port Arthur','occurred during','Russo-Japanese War 1904–1905','Russian Far East','The peer asks which war included Port Arthur’s defense in 1904–1905; candidate asks for an event in March 1921.','The candidate does not ask about a war involving Port Arthur; peer does not identify Kronstadt.'),
'history-russia-june-third-coup':('dissolution of Second Duma and electoral-law change','called','Third of June Coup, 1907','Russia','The peer asks for the name of a 1907 political event; candidate asks which event occurred in March 1921.','No direct or reverse restatement: event and year differ.'),
'history-united-kingdom-sample-04':('Manchester reform-meeting attack','named as','Peterloo, 16 August 1819','Britain','The peer asks for a 1819 Manchester event; candidate asks for a Russian event in March 1921. A Bloody Sunday distractor within the peer is the 1887 British event, not this candidate’s Russian episode.','Different country, entity, relation, and date; no reverse duplicate.')}
comparisons=[]
for p in selected:
 if p['id']==task['id']: continue
 ent,rel,val,ctx,c2p,p2c=peer_notes[p['id']]
 comparisons.append({'kind':'current-main-semantic-neighbor','peerId':p['id'],'peerFullCardSHA256':p['canonicalSHA256'],'candidateERVC':'entity=Kronstadt uprising; relation=occurred in; value=March 1921; context=Russian history','peerERVC':f'entity={ent}; relation={rel}; value={val}; context={ctx}','candidateToPeer':c2p,'peerToCandidate':p2c,'isDuplicate':False})
assert len(comparisons)==13
# The source90 cycle1 proposed edit changes only one Port Arthur note; it does not create a shared MAIN relation.
source90=json.load(open(BASE/'source-history-russia90-cycle1/candidate.json'))['entries'][0]
proposal={'sourceId':'history-russia-port-arthur-war','topicId':TOPIC,'id':source90['id'],'status':source90['status'],'proposedCard':source90['proposedCard'],'comparison':'This separate saved proposal changes only the Port Arthur answer note from defense to fall. Its MAIN remains the Russo-Japanese War/Port Arthur relation, distinct from the March 1921 Kronstadt event; not a relevant semantic peer pair. It is un-applied, so the current snapshot remains the unchanged card.'}
# Exact query hits remain retrieval only and never establish duplication.
terms=['Кронштадтское восстание','Восстание декабристов','Кровавое воскресенье','Февральская революция']
hits=[];seen=set()
for row in inv['globalMAIN']['rows']:
 text=row['prompt']+' '+' '.join(row['answers'])
 matched=[t for t in terms if t.casefold() in text.casefold()]
 if matched and row['id']!=task['id'] and row['id'] not in seen:
  seen.add(row['id']); item=current_by_id.get(row['id'])
  card=item['card'] if item else row
  hits.append({'topicId':row['topicId'],'id':row['id'],'card':card,'cardCanonicalSHA256':canon(card),'sourceFilePath':inv['sameTopicMAIN']['path'] if item else 'fresh global MAIN row projection','matchedTerms':matched})
peer_snapshot={'owner':OWNER,'sourceNativeId':NATIVE,'stage':'SOURCE_CYCLE1','cycle':1,'qualityCredit':0,'candidate':{'id':task['id'],'topicId':TOPIC,'sourceOrder':91,'beforeCard':before,'beforeCardCanonicalSHA256':BH,'proposedCard':after,'proposedCardCanonicalSHA256':AH,'frozen':frozen,'semanticEntity':'Kronstadt uprising','semanticRelation':'occurred in','semanticValue':'March 1921'},'globalMAIN':copy.deepcopy(inv['globalMAIN']),'sameTopicMAIN':copy.deepcopy(inv['sameTopicMAIN']),'fullClosestCurrentPeers':[x for x in selected if x['id']!=task['id']],'currentGuardRows':{'currentTargetBeforeCard':{'id':before['id'],'topicId':TOPIC,'sourceOrder':91,'card':before,'cardCanonicalSHA256':BH},'readerInitialPeerSetCount':len(selected),'readerInitialPeerSet':[{'id':x['id'],'topicId':x['topicId'],'sourceOrder':x['sourceOrder'],'cardCanonicalSHA256':x['canonicalSHA256']} for x in selected],'sameTopicFilePath':inv['sameTopicMAIN']['path'],'sameTopicFileSHA256':inv['sameTopicMAIN']['fileSHA256'],'allCurrentFileByteBindings':inv['globalMAIN']['allCurrentFileByteBindings']},'bilateralCurrentComparisons':comparisons,'globalLiteralRetrievalOnlyHits':hits,'genuineProposalPairs':[],'observedNonmatchingProposals':[proposal],'proposalSearchLimitations':'Source90 cycle1 proposal is saved but unapplied. It was read and assessed as a nonmatching proposal; no candidate 91 MAIN overlap, so it is not included among the 13 current bilateral pairs. No other proposals supplied.','limitations':['Current source90 card remains pre-cycle1; its proposed note3 edit is separately bound as un-applied.','Current card and peer set were refreshed from inventory; all 14 selected INITIAL peer hashes were rechecked against current files.','No independent FINAL, QA, application, or quality credit in this author result.'],'actualCurrentPeers':actual_current}
for name,obj in [('candidate.json',candidate),('sourceproof.json',sourceproof),('peer-snapshot.json',peer_snapshot)]: (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'READY_FOR_SAME_READER_FINAL','beforeHash':BH,'afterHash':AH,'changedGroups':[k for k in bg if bg[k]!=ag[k]],'independentPeerCards':len(selected),'bilateralPairs':len(comparisons),'sameTopicCurrentPeers':len(actual_current),'globalRows':peer_snapshot['globalMAIN']['questionCount'],'rawSources':len(raw)}))
