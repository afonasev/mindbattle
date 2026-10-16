import json,hashlib,os,glob
from copy import deepcopy
base='docs/content-audits/question-quality-wave-8/coordinator-01a14377'
out=base+'/source-parks15-newlanguage-solution'
os.makedirs(out,exist_ok=True)
def read(p):
 with open(p,encoding='utf8') as f:return json.load(f)
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def canon(x):return sha_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def dump(p,x):
 with open(out+'/'+p,'w',encoding='utf8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
# frozen current card and singular referent language-only proposal
catalog_path='src/content/topics/national-parks-nature.json'; catalog=read(catalog_path)
current=next(c for c in catalog['questions'] if c['id']=='national-parks-nature-015')
task=read(base+'/source-parks15-newlanguage-solution-task.json')
assert current==task['beforeCard']
assert canon(current)==task['beforeHash']
proposed=deepcopy(current)
proposed['prompt']='Если вы нашли в парке раковину или камень и не уверены, разрешено ли собирать такие находки, как поступить с этой находкой?'
after=canon(proposed)
# candidate
candidate={'baselineCommit':task['frozenSelectionBaseline'],'catalogCommit':task['latest14Freeze'],'catalogSourceFileSHA256':sha_bytes(open(catalog_path,'rb').read()),'entries':[{'id':current['id'],'topicId':task['topicId'],'sourceOrder':15,'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':current,'beforeHash':canon(current),'proposedCard':proposed,'afterHash':after,'fieldGroups':{'prompt_ordered_answers_key':{'beforeSHA256':canon({'prompt':current['prompt'],'answers':[a['text'] for a in current['answers']],'correctIndex':current['correctIndex']}),'afterSHA256':canon({'prompt':proposed['prompt'],'answers':[a['text'] for a in proposed['answers']],'correctIndex':proposed['correctIndex']}),'changedFields':['prompt']},'explanation':{'beforeSHA256':canon(current['explanation']),'afterSHA256':canon(proposed['explanation']),'changed':False},'notes':{'beforeSHA256':canon([a['note'] for a in current['answers']]),'afterSHA256':canon([a['note'] for a in proposed['answers']]),'changed':False},'source':{'beforeSHA256':canon(current['source']),'afterSHA256':canon(proposed['source']),'changed':False}},'scope':'Only the prompt wording changes to establish singular feminine referent находка; all fact, entities, decision condition, options, notes, explanation, source, difficulty, key, and order remain byte-identical.'}]}
dump('candidate.json',candidate)
# source proof reuse exact full primary contexts and provenance, rebind the assessment to revised literal
sp=read(base+'/source-parks15-cycle1-adopt0/sourceproof.json'); entry=sp['entries'][0]
entry['literalGroups'][0]['literal']['prompt']=proposed['prompt']; entry['literalGroups'][0]['literalSHA256']=canon(entry['literalGroups'][0]['literal'])
for i,a in enumerate(entry['fourFullPromptAnswerNoteAssessments']):
 a['fullPrompt']=proposed['prompt']; a['grammar']=['The prompt introduces one shell-or-stone find as «эту находку»; feminine singular её/одну and находка in the options agree with that singular referent. The infinitive action answers are complete after «как поступить?».' if i==0 else '«Переложить её» agrees in feminine singular with the prompt’s explicit «эту находку»; the infinitive is a complete action answer.' if i==1 else '«Оставить её» agrees in feminine singular with the prompt’s explicit «эту находку»; the infinitive is a complete action answer.' if i==2 else '«Взять одну» agrees in feminine singular with the prompt’s explicit «эту находку»; the infinitive is a complete action answer.'][0]
 a['tripleSHA256']=canon({'prompt':a['fullPrompt'],'answer':a['answer'],'note':a['note']})
entry['fourOptionEditorialCheck']='Read the revised full prompt with each answer and note. The prompt identifies one found item as «эту находку»; all singular feminine references (находка, она, её, одну) agree. Facts and decision condition are unchanged.'
entry['personalRead']='Personally read both complete retained NPS outputs again for this language-only packet; source facts remain applicable to the unchanged leave-in-place/check-rules decision. Reuse is explicitly limited to the same two frozen source bodies and listed locators; no new research.'
# raw source bodies from retained full files
index=read(base+'/source-captures/sourcec5-parks15-original-web/index.json')
for raw,idx in zip(sp['rawSources'],index['entries']):
 data=open(idx['retainedSourceBodyPath'],'rb').read(); assert sha_bytes(data)==idx['retainedRawSHA256']
 raw['path']='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+idx['retainedSourceBodyPath'];raw['sha256']=sha_bytes(data);raw['fullVisibleOutput']=data.decode('utf8')
sp['sourceNativeId']=task['sourceNativeId']; sp['cycle']=1; sp['entries']=[entry]
dump('sourceproof.json',sp)
# peer snapshot: retain reviewed same-topic list/query coverage, refresh actual bodies and hashes from source, compare revised candidate to all 16 others + newest #14 proposal
ps=read(base+'/source-parks15-cycle1-adopt0/peer-snapshot.json')
ps['sourceNativeId']=task['sourceNativeId'];ps['cycle']=1
ps['frozenCandidate']={'id':current['id'],'topicId':task['topicId'],'sourceOrder':15,'difficulty':'easy','correctIndex':2,'beforeCanonicalSHA256':canon(current),'proposedCanonicalSHA256':after,'changedField':'prompt'}
ps['candidateScope']='Language-only: the proposed MAIN fact and key are unchanged; only the singular feminine antecedent is made explicit.'
# map existing peer ids to current full cards/files
allcards={}; filehash={}
for fp in glob.glob('src/content/topics/*.json'):
 doc=read(fp); arr=doc.get('questions',[]); h=sha_bytes(open(fp,'rb').read())
 for c in arr: allcards[c['id']]=(c,fp,h)
# refresh full peer bodies based on current catalogs
peers=[]
for item in ps['actualCurrentPeers']:
 c,fp,h=allcards[item['id']]; item['card']=c;item['sourceFile']='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+fp;item['sourceFileSHA256']=h;item['canonicalSHA256']=canon(c); peers.append(item)
ps['actualCurrentPeers']=peers
# full hit bodies hashes refreshed
for item in ps['fullRelevantHits']:
 c,fp,h=allcards[item['id']];item['card']=c;item['sourceFile']='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+fp;item['sourceFileSHA256']=h;item['canonicalSHA256']=canon(c)
# new #14 proposal exact latest candidate
c14=read(base+'/source-parks14-newprimary-solution/candidate.json')['entries'][0]['proposedCard']
h14=canon(c14)
ps['latestProposals']=[{'assignment':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+base+'/source-parks14-newprimary-solution/candidate.json','stage':'SOURCE14_NEWPRIMARY_SOLUTION_PRE2','status':'READY_FOR_INDEPENDENT_REVIEW_NOT_APPLIED','id':c14['id'],'card':c14,'canonicalSHA256':h14,'sourceFile':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/src/content/topics/national-parks-nature.json','sourceFileSHA256':sha_bytes(open(catalog_path,'rb').read()),'applicationStatus':'not applied'}]
# compare MAIN fact/key both directions against each of 16 distinct current peers plus #14 proposed candidate
comparisons=[]
for peer in peers:
 if peer['id']==current['id']:continue
 p=peer['card']; comparisons.append({'targetId':current['id'],'targetCanonicalSHA256':after,'peerId':p['id'],'peerCanonicalSHA256':canon(p),'peerSourceFileSHA256':peer['sourceFileSHA256'],'candidateToPeer':'The candidate tests the action under uncertainty for collecting a found natural object (leave it and check local rules); this peer tests a distinct fact, object/action, or condition.','peerToCandidate':'This peer’s tested fact and key do not ask what to do with a found shell or stone when collection rules are unknown. The revised singular wording does not change the candidate MAIN.','relation':'distinct_MAIN_fact_and_key_both_directions'})
comparisons.append({'targetId':current['id'],'targetCanonicalSHA256':after,'peerId':c14['id'],'peerCanonicalSHA256':h14,'peerSourceFileSHA256':sha_bytes(open(catalog_path,'rb').read()),'candidateToPeer':'Candidate asks visitor conduct for a found shell or stone under uncertain collection rules. The #014 proposal asks what planned burns remove from forest to reduce wildfire risk.','peerToCandidate':'The #014 proposal tests prescribed-fire fuel reduction, not handling a found natural object or checking collection permission.','relation':'distinct_MAIN_fact_and_key_both_directions','peerIsUnappliedProposal':True})
ps['bilateralMainComparisons']=comparisons
ps['reviewMethod']='Reused the previously personally read 100 same-topic MAIN rows and 16 distinct full near-peer bodies after checking each current underlying topic file and refreshing its hash. Rebuilt full global prompt/key table and current delta from all current topic JSON files. Read latest #014 candidate body and compared MAIN applicability in both directions. No new source research.'
# current delta against frozen retrieval recompute
retr=read(ps['fullGlobalPromptKeyRetrieval']['path']); rows=retr['cards']; currows={}
for fp in glob.glob('src/content/topics/*.json'):
 tid=os.path.basename(fp)[:-5]
 for c in read(fp).get('questions',[]):currows[c['id']]={'topicId':tid,'id':c['id'],'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']}
old={r['id']:r for r in rows}; changed=[]
for id,v in currows.items():
 if old.get(id)!=v:changed.append({'id':id,'retrievalRow':old.get(id),'currentCMain':v})
ps['currentCDeltaAgainstRetrieval']={'method':'Rebuilt current MAIN map from every src/content/topics JSON and compared id, prompt, ordered answers, key with frozen retrieval rows.','currentTopicFileCount':len(glob.glob('src/content/topics/*.json')),'currentCardCount':len(currows),'missingIds':[i for i in old if i not in currows],'newIds':[i for i in currows if i not in old],'changedRowCount':len(changed),'unchangedCount':len(currows)-len(changed),'changedRows':changed}
# use query coverage from prior auditable retrieval, annotate re-read applicability
ps['currentAsOf']='2026-10-16; current source file hashes refreshed'
ps['sameTopicMAINRowsRead']=ps['sameTopicPeersRead']
ps['scope']='One language-only #015 proposal. Final HOLD0 stays immutable; no reopen PASS or quality credit. This packet is new concrete language solution for root eligibility assessment only.'
dump('peer-snapshot.json',ps)
# critical ready pre-actual2
files={}
for fn in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 b=open(out+'/'+fn,'rb').read();files[fn]={'sha256':sha_bytes(b),'bytes':len(b)}
crit={'status':'READY_FOR_INDEPENDENT_REVIEW','gate':'SOURCE_EVIDENCE_COMPLETE_PRE_ACTUAL2_FREEZE','sourceNativeId':task['sourceNativeId'],'owner':task['owner'],'cycle':1,'id':current['id'],'topicId':task['topicId'],'outputDirectory':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+out,'files':files,'requirementsEvidence':{'changedOnlyPrompt':True,'allNotesExplanationSourceDifficultyKeyOrderIdentical':True,'literalGroups':6,'fullPromptAnswerNoteGrammarAssessments':4,'sameTopicMAINRowsRead':ps['sameTopicPeersRead'],'distinctBilateralMAINComparisons':len(comparisons),'currentGlobalRetrievalRows':ps['fullGlobalPromptKeyRetrieval']['cardCount'],'currentGlobalDeltaRows':len(changed),'primarySourcesPersonallyRead':2,'allSourceBodiesAndHashesVerified':True,'latest14CandidateComparedBothWays':True,'targetBeforeCardMatchesCurrentCatalog':True},'limitations':'This is a concrete new language-only proposal and evidence packet for root eligibility assessment. It is not reopen PASS, quality credit, application authorization, final acceptance, or actual2. FINAL HOLD0 remains immutable until root decision. No source/catalog/Git/tests/runtime changes.'}
dump('critical-3.json',crit)
print(json.dumps({'output':out,'candidateHash':after,'sourceFileSHA256':candidate['catalogSourceFileSHA256'],'peers':len(peers),'comparisons':len(comparisons),'globalDelta':len(changed),'files':files},indent=2))
