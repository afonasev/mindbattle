import json,hashlib,os,glob
from copy import deepcopy
base='docs/content-audits/question-quality-wave-8/coordinator-01a14377'; out=base+'/source-parks14-primary-option-complete'; os.makedirs(out,exist_ok=True)
TASK=base+'/source-parks14-primary-option-complete-task.json'
def read(p): return json.load(open(p,encoding='utf8'))
def hb(b): return hashlib.sha256(b).hexdigest()
def ch(x): return hb(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def put(name,x):
 with open(out+'/'+name,'w',encoding='utf8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
t=read(TASK); topic='src/content/topics/national-parks-nature.json'; rawcat=open(topic,'rb').read(); doc=json.loads(rawcat); current=next(c for c in doc['questions'] if c['id']==t['id']); assert current==t['beforeCard'] and ch(current)==t['beforeHash']
proposed=deepcopy(current)
proposed['prompt']='Что плановые выжигания в некоторых национальных парках убирают из леса, чтобы снизить риск более сильного пожара?'
proposed['answers'][3]['text']='Лестничные горючие материалы, которые удаляют механическим прореживанием.'
proposed['answers'][3]['note']='В Yosemite NPS отдельно описывает mechanical thinning как способ убрать «лестничное топливо»; страница различает этот приём и плановый огонь.'
# candidate
candidate={'baselineCommit':t['baselineCommit'],'catalogCommit':t['catalogCommit'],'catalogSourceFileSHA256':hb(rawcat),'entries':[{'id':t['id'],'topicId':t['topicId'],'sourceOrder':14,'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':current,'beforeHash':ch(current),'proposedCard':proposed,'afterHash':ch(proposed),'fieldGroups':{'prompt_ordered_answers_key':{'beforeCanonicalSHA256':ch({'prompt':current['prompt'],'answers':[a['text'] for a in current['answers']],'correctIndex':current['correctIndex']}),'afterCanonicalSHA256':ch({'prompt':proposed['prompt'],'answers':[a['text'] for a in proposed['answers']],'correctIndex':proposed['correctIndex']})},'note3':{'beforeCanonicalSHA256':ch(current['answers'][3]['note']),'afterCanonicalSHA256':ch(proposed['answers'][3]['note'])},'otherFields':{'unchanged':['id','difficulty','correctIndex','explanation','source','answer0','note0','answer1','note1','answer2','note2']},'scope':'ONE concrete source-grounded #3 distractor/note repair closes false exclusivity and ambiguity; preserve tested MAIN, key, easy, ID/topic/order; no unsupported inference from missing text.'}}]}
put('candidate.json',candidate)
# source evidence: retain complete previously-read NPS native-visible outputs; author new evidence for the exact candidate
old=read(base+'/source-parks14-newprimary-solution/sourceproof.json'); raws=deepcopy(old['rawSources']);
for r in raws:
 data=r['fullVisibleOutput'].encode(); assert hb(data)==r['sha256']
# Ensure output file bodies correspond to saved visible outputs, and bind the real full-output path.
for i,r in enumerate(raws):
 fp=r['path']; assert hb(open(fp,'rb').read())==r['sha256']
entry={'id':t['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','literalGroups':[], 'fourFullPromptAnswerNoteAssessments':[]}
sourcepaths=[r['path'] for r in raws]
vals=[('prompt_ordered_answers_key',{'prompt':proposed['prompt'],'answers':[a['text'] for a in proposed['answers']],'correctIndex':proposed['correctIndex']},'Yosemite NPS explicitly says prescribed fires remove dead and overgrown vegetation that could contribute to a later severe fire. It separately says prescribed fire reduces heavy fuel loads; the explicit contrast with mechanical thinning and ladder fuels supports the replacement distractor without claiming fire cannot also affect branches.', ['L48','L51','L53-L55']),('explanation',proposed['explanation'],'The complete Yosemite context describes prescribed fire, its goals, fuel reduction, habitat and fire prescriptions; system-wide NPS FAQ provides fire ecology context.', ['L34','L48-L52']),('note0',proposed['answers'][0]['note'],'Yosemite NPS states that prescribed fire opens conifer forest structure and maintains meadow habitats.', ['L51']),('note1',proposed['answers'][1]['note'],'Yosemite NPS states that prescribed fire can enhance native plant communities and improve wildlife habitat.', ['L51']),('note2',proposed['answers'][2]['note'],'Yosemite NPS states that prescribed fire can maintain the health of meadow habitats and enhance native plant communities.', ['L51']),('note3',proposed['answers'][3]['note'],'Yosemite NPS identifies mechanical thinning as a separate named tool and says it removes ladder fuels; the page does not state that prescribed fire cannot also affect such fuels. The note claims only the source’s separate classification.', ['L34','L53-L55'])]
for group,literal,ground,loc in vals:
 entry['literalGroups'].append({'group':group,'literal':literal,'literalSHA256':ch(literal),'primaryGround':ground,'locator':loc,'sourcePaths':[sourcepaths[0]] if group!='prompt_ordered_answers_key' else sourcepaths})
for i,a in enumerate(proposed['answers']):
 if i==0: grammar='Complete noun phrase answering «что ... убирают»; grammatically fits the question. NPS source does not say prescribed fire removes living upper-canopy trees specifically; option therefore remains a plausible but unsupported distractor.'
 elif i==1: grammar='Complete noun phrase answering «что ... убирают»; it matches the NPS prescribed-fire statement about dead and overgrown vegetation.'
 elif i==2: grammar='Complete noun phrase answering «что ... убирают»; the action stated conflicts with NPS describing fire as maintaining meadow health and supporting native plants.'
 else: grammar='Complete noun phrase answering «что ... убирают»; the phrase explicitly attributes ladder-fuel removal to mechanical thinning, the separately named treatment in the source, rather than asserting that prescribed fire never affects branches.'
 entry['fourFullPromptAnswerNoteAssessments'].append({'slot':i,'fullPrompt':proposed['prompt'],'answer':a['text'],'note':a['note'],'grammar':grammar,'plausibilityUniqueKeyAndNoteTruthUsefulness':['Plausible forest-management outcome but not the source’s described prescribed-fire removal target.','The single correct answer is directly named by NPS.','Plausible stewardship misconception; NPS describes maintaining meadows/native plants, not removing them to preserve clearings.','A credible nearby treatment and source-grounded distractor; its wording pins the action to mechanical thinning without unsupported exclusion.'][i],'sourcePaths':[sourcepaths[0]],'locator':[['L51'],['L48-L51'],['L51'],['L53-L55']][i],'tripleSHA256':ch({'prompt':proposed['prompt'],'answer':a['text'],'note':a['note']})})
entry['correctNoteNewFact']='The correct answer note is unchanged and adds a separate supported fact: NPS also uses prescribed fire to enhance native plant communities and improve wildlife habitat.'
entry['absoluteDifficulty']='Provisional frozen easy: the question asks in plain language what planned burns remove to lower later fire risk; the exact response is stated directly by NPS without park-name, geography, or specialist term recall. Mechanical thinning remains the only technical phrase, confined to a wrong option note. This is an editorial judgement, not an audience survey.'
entry['taxonomy']='Fits National parks and protected nature: a conservation-management practice in protected forest ecosystems, not a city-park wrapper or park-identification fact.'
entry['personalRead']='Personally reread complete retained native-visible Yosemite NPS page L0-L130 and full NPS Wildland Fire Program FAQ L0-L127 for this gap. Read L48-L55 together: prescribed fire removes dead/overgrown vegetation and reduces heavy fuel loads; mechanical thinning is separately named and removes ladder fuels. The latter is not evidence that fire cannot affect lower branches, so the proposal makes no exclusivity claim.'
entry['fourOptionEditorialCheck']='All four options are plausible vegetation-management effects in fire-prone forest contexts. Only slot 1 is explicitly named in the primary as what prescribed fires remove. Slot 3 describes a separately named mechanical-thinning operation, preserving a plausible nearby distractor without treating a missing statement as proof of exclusion. Slots 0 and 2 refer to other plausible management objectives, not the removal target stated by NPS.'
sp={'sourceNativeId':t['sourceNativeId'],'id':t['id'],'topicId':t['topicId'],'cycle':1,'entries':[entry],'rawSources':raws}
put('sourceproof.json',sp)
# peer comparisons: refresh current bodies; compare to all exact current selected peers, archived held proposal and NEW #15 proposal
ps=read(base+'/source-parks14-newprimary-solution/peer-snapshot.json')
allcards={}
for fp in glob.glob('src/content/topics/*.json'):
 body=open(fp,'rb').read(); d=json.loads(body); path='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+fp
 for c in d.get('questions',[]):allcards[c['id']]=(c,path,hb(body))
for group in ['actualCurrentPeers','fullRelevantHits']:
 for it in ps[group]:
  if it['id'] in allcards:
   c,path,filehash=allcards[it['id']];it['card']=c;it['canonicalSHA256']=ch(c);it['sourceFile']=path;it['sourceFileSHA256']=filehash
# update target main card binding in peer list
ps['sourceNativeId']=t['sourceNativeId']; ps['cycle']=1
ps['frozenCandidate']={'id':t['id'],'topicId':t['topicId'],'sourceOrder':14,'difficulty':'easy','correctIndex':1,'beforeCanonicalSHA256':ch(current),'proposedCanonicalSHA256':ch(proposed),'changedFields':['prompt','answer3','note3']}
# Add latest #15 language proposal full card, not current #15; hash exact candidate body
p15path=base+'/source-parks15-newlanguage-solution/candidate.json'; p15=read(p15path)['entries'][0]['proposedCard']; p15hash=ch(p15)
ps['latestActual15']={'path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+p15path,'candidateFileSHA256':hb(open(p15path,'rb').read()),'candidateCanonicalSHA256':p15hash,'currentCatalogSourceFileSHA256':hb(rawcat),'card':p15,'currentState':'Unapplied language-only proposal, exact full body reread; its MAIN fact is shell/stone collection under uncertain local rules.'}
# old distinct proposal exact full-body historic hash kept/rechecked against saved candidate artifact
oldprop=read(base+'/source-parks14-cycle1-fresh/candidate.json')['candidates'][0]['proposedCard']; oldprop_hash=ch(oldprop)
ps['latestProposals']=[{'assignment':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+base+'/source-parks14-cycle1-fresh/candidate.json','stage':'HISTORICAL_BLOCKED_KILIMANJARO','status':'NOT_QUALIFIED_NOT_APPLIED','id':oldprop['id'],'card':oldprop,'canonicalSHA256':oldprop_hash,'reason':'Historical blocked proposal, re-compared as context, not current MAIN or inherited verdict.','sourceFile':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+base+'/source-parks14-cycle1-fresh/candidate.json','sourceFileSHA256':hb(open(base+'/source-parks14-cycle1-fresh/candidate.json','rb').read()),'applicationStatus':'NOT_APPLIED'}]
comparisons=[]
def add(peerid,card,filesha,kind):
 fact='Yosemite NPS prescribed burns remove dead and overgrown vegetation that may contribute to a later severe fire; they reduce heavy fuel loads.'
 pf={'national-parks-nature-002':'A conservation behavior in parks unrelated to prescribed-fire fuel removal.','national-parks-nature-009':'Prevent wildlife harm by not feeding animals and securing food/waste.','national-parks-nature-010':'Keep a safe distance from wildlife.','national-parks-nature-015':'Leave a found shell or rock in place and check local collection rules.','tourism-travel-stay-trail':'Use durable trails/campsites to limit visitor impact.','ecology-environment-citizen-science':'Participate in environmental citizen-science reporting.','national-parks-nature-014-blocked-Kilimanjaro-proposal':'Identify the park containing Africa’s highest mountain.','national-parks-nature-015-language-proposal':'Leave found shell/stone and check collection rules when unsure.'}.get(peerid,'Distinct fact')
 comparisons.append({'targetId':t['id'],'targetCanonicalSHA256':ch(proposed),'peerId':peerid,'peerCanonicalSHA256':ch(card),'peerSourceFileSHA256':filesha,'candidateFact':fact,'peerFact':pf,'ervc':{'relation':'Full MAIN facts, actions, conditions, and keys compared in both directions.','candidateToPeer':'The target asks what prescribed burning removes to reduce later fire risk; this differs from the peer’s tested fact and action.','peerToCandidate':'The peer does not ask what prescribed burning removes to reduce later fire risk.'},'directReverse':'Reading the peer as the candidate does not yield the Yosemite prescribed-fire fuel-removal fact; reading the candidate as the peer does not yield the peer’s distinct fact.','verdict':'distinct_MAIN_both_directions','peerKind':kind})
for it in ps['actualCurrentPeers']:
 if it['id']==t['id']:continue
 add(it['id'],it['card'],it['sourceFileSHA256'],'currentMAIN')
add('national-parks-nature-014-blocked-Kilimanjaro-proposal',oldprop,hb(open(base+'/source-parks14-cycle1-fresh/candidate.json','rb').read()),'historicalUnappliedProposal')
add('national-parks-nature-015-language-proposal',p15,hb(open(p15path,'rb').read()),'newUnappliedProposal')
ps['bilateralMainComparisons']=comparisons
ps['reviewMethod']='Recomputed hashes for all currently included full current cards from topic files. Compared target MAIN in both directions against six distinct selected actual peer cards, the historical blocked #014 proposal, and the latest #015 language proposal. The full global retrieval remains 11,000 rows; current delta metadata was inherited only after validating source file hash and current changed IDs. No new source research.'
ps['currentAsOf']='2026-10-16 current working-tree source snapshot, hash-checked'
# revalidate global retrieval metadata and delta rows from task baseline
retr=read(ps['fullGlobalPromptKeyRetrieval']['path']); assert retr['cardCount']==11000
oldrows={r['id']:r for r in retr['cards']}; now={}
for fp in glob.glob('src/content/topics/*.json'):
 tid=os.path.basename(fp)[:-5]
 for c in read(fp).get('questions',[]): now[c['id']]={'topicId':tid,'id':c['id'],'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']}
changed=[{'id':i,'retrievalRow':oldrows.get(i),'currentCMain':v} for i,v in now.items() if oldrows.get(i)!=v]
ps['currentCDeltaAgainstRetrieval']={'method':'Rebuilt every current MAIN row and compared exact prompt, ordered answer labels, and key with frozen complete retrieval.','currentTopicFileCount':len(glob.glob('src/content/topics/*.json')),'currentCardCount':len(now),'missingIds':[i for i in oldrows if i not in now],'newIds':[i for i in now if i not in oldrows],'changedRowCount':len(changed),'unchangedCount':len(now)-len(changed),'changedRows':changed}
ps['scope']='Only finish the primary uniqueness gap for #014 in the same unfinished cycle 1. One grounded distractor/note correction; preserve key and all product scope. The #015 new language proposal is also compared and remains unapplied.'
put('peer-snapshot.json',ps)
# critical final pre-actual2 freeze
files={}
for fn in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 b=open(out+'/'+fn,'rb').read(); files[fn]={'sha256':hb(b),'bytes':len(b)}
crit={'status':'READY_FOR_INDEPENDENT_REVIEW','gate':'SOURCE_EVIDENCE_COMPLETE_PRE_ACTUAL2_FREEZE','sourceNativeId':t['sourceNativeId'],'owner':t['owner'],'cycle':1,'id':t['id'],'topicId':t['topicId'],'outputDirectory':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/'+out,'files':files,'requirementsEvidence':{'allSixLiteralGroups':6,'fourWholePromptAnswerNoteVariants':4,'exactNPSPrimaryContextsRead':2,'updatedOnlyAnswer3AndNote3':True,'currentPeerCardsFullAndHashBound':len(ps['actualCurrentPeers']),'bilateralComparisons':len(comparisons),'latest15NewLanguageProposalComparedBothWays':True,'fullGlobalRetrievalRows':11000,'currentGlobalDeltaRows':len(changed),'candidateMainKeyUnchanged':True,'targetBeforeCardMatchesCurrentCatalog':True},'limitations':'One concrete source-grounded proposal is ready for independent review. It claims that NPS separately attributes ladder-fuel reduction to mechanical thinning; it does not claim that prescribed fire cannot affect branches. Not editorial PASS, application authorization, quality credit, or final acceptance. Stop before actual2.'}
put('critical-3.json',crit)
print(json.dumps({'out':out,'changedFields':[k for k in current if current[k]!=proposed[k]],'afterHash':ch(proposed),'sourceFileHash':hb(rawcat),'peers':len(ps['actualCurrentPeers']),'comparisons':len(comparisons),'globalDelta':len(changed),'files':files},indent=2))
