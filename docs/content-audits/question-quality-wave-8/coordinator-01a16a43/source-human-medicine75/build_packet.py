import copy, hashlib, json
from pathlib import Path

C = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine75'
INV = OUT / 'fresh-inventory.json'
ID = 'human-medicine-ext-parathyroid-hormone'
NATIVE = '01a16a57-4bd1-7132-9d5c-a9db16ce628e'
NATIVE_JOURNAL = '/Users/eaafonasev/.codex/sessions/2026/10/24/rollout-2026-10-24T00-57-48-01a16a57-4bd1-7132-9d5c-a9db16ce628e.jsonl'

def canonical(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def rel(path):
    return str(Path(path).resolve().relative_to(C))
def fulltext(path):
    d=json.loads(Path(path).read_text())
    return d['originalRecord']['payload']['output'][1]['text']

def groups(card):
    return {
        'prompt_ordered_answers_key': {'prompt': card['prompt'], 'answers': [a['text'] for a in card['answers']], 'correctIndex': card['correctIndex']},
        'explanation': card['explanation'],
        **{'note'+str(k): a['note'] for k,a in enumerate(card['answers'])}
    }

inventory=json.loads(INV.read_text())
before=copy.deepcopy(next(q['card'] for q in inventory['actualCurrentPeers'] if q['id']==ID))
assert canonical(before)=='53469a1a792898da62e355a08dfaa0e65084e215860c44f9c08c396fe0c443b4'
assert (before['id'], before['difficulty'], before['correctIndex']) == (ID, 'hard', 3)
peer=copy.deepcopy(before)
proposed=copy.deepcopy(before)
proposed['prompt']='Какой гормон усиливает высвобождение кальция из костной ткани?'
proposed['answers'][0]['note']='Кортизол (гидрокортизон) — один из главных гормонов коры надпочечников.'
proposed['answers'][1]['note']='Адреналин (эпинефрин) — гормон мозгового слоя надпочечников, стимулирующий сердце.'
proposed['answers'][2]['note']='Секреция мелатонина усиливается в темноте и снижается при освещении.'
proposed['answers'][3]['note']='Паратиреоидный гормон также усиливает реабсорбцию кальция в почечных канальцах.'
proposed['explanation']='Паратиреоидный гормон (ПТГ) выделяется околощитовидными железами и способствует высвобождению кальция из костной ткани. Он также усиливает реабсорбцию кальция в почках и его всасывание в кишечнике.'
proposed['source']={'title':'NLM MeSH: Parathyroid Hormone','url':'https://www.ncbi.nlm.nih.gov/mesh/68010281','verifiedAt':'2026-10-24'}
assert (proposed['id'],proposed['difficulty'],proposed['correctIndex']) == (ID,'hard',3)
assert len(proposed['answers'])==4 and len({a['text'] for a in proposed['answers']})==4
assert len(proposed['source']['url'])>0

gb,ga=groups(before),groups(proposed)
field_groups={k:{'beforeCanonicalSHA256':canonical(gb[k]),'afterCanonicalSHA256':canonical(ga[k])} for k in gb}
assert len(field_groups)==6

candidate={'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'id':ID,'entries':[{'id':ID,'topicId':'human-medicine','sourceOrder':75,'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':before,'beforeHash':canonical(before),'proposedCard':proposed,'afterHash':canonical(proposed),'fieldGroups':field_groups}]}
write('candidate.json',candidate)

pth_path=rel(OUT/'raw-nlm-parathyroid.json')
epi_path=rel(OUT/'raw-nlm-epinephrine.json')
mel_path=rel(OUT/'raw-nlm-melatonin.json')
cort_path=rel(OUT/'raw-nlm-cortisol.json')
raw_sources=[
 {'path':pth_path,'url':'https://www.ncbi.nlm.nih.gov/mesh/68010281','sha256':file_sha(OUT/'raw-nlm-parathyroid.json'),'captureReadProvenance':f'Captured complete original web.open response from author native {NATIVE}; personally read complete returned body. The initial response for the Epinephrine page was malformed and returned an internal error; the corrected exact URL was separately opened and saved in its own raw file.','completeOutputPointer':'/originalRecord/payload/output/1/text','completeOutputSHA256':hashlib.sha256(fulltext(OUT/'raw-nlm-parathyroid.json').encode()).hexdigest(),'locator':'Parathyroid Hormone page L52-L55, especially L54.'},
 {'path':epi_path,'url':'https://www.ncbi.nlm.nih.gov/mesh?Cmd=DetailsSearch&Db=mesh&Term=%22Epinephrine%22%5BMeSH+Terms%5D','sha256':file_sha(OUT/'raw-nlm-epinephrine.json'),'captureReadProvenance':f'Captured complete original corrected web.open response from author native {NATIVE}; personally read complete returned Epinephrine MeSH body.','completeOutputPointer':'/originalRecord/payload/output/1/text','completeOutputSHA256':hashlib.sha256(fulltext(OUT/'raw-nlm-epinephrine.json').encode()).hexdigest(),'locator':'Epinephrine page L53-L55, especially L55; source gives adrenal-medulla origin and cardiac stimulation.'},
 {'path':mel_path,'url':'https://www.ncbi.nlm.nih.gov/mesh/68008550','sha256':file_sha(OUT/'raw-nlm-melatonin.json'),'captureReadProvenance':f'Captured complete original web.open response from author native {NATIVE}; personally read complete returned Melatonin MeSH body. Same original response preserves recaptcha-only responses for two inaccessible NCBI Bookshelf URLs; those were not used as evidence.','completeOutputPointer':'/originalRecord/payload/output/1/text','completeOutputSHA256':hashlib.sha256(fulltext(OUT/'raw-nlm-melatonin.json').encode()).hexdigest(),'locator':'Melatonin page L52-L55, especially L54.'},
 {'path':cort_path,'url':'https://www.ncbi.nlm.nih.gov/mesh/68000305','sha256':file_sha(OUT/'raw-nlm-cortisol.json'),'captureReadProvenance':f'Captured complete original web.open response from author native {NATIVE}; personally read complete returned bodies for Adrenal Cortex Hormones and Cushing Syndrome.','completeOutputPointer':'/originalRecord/payload/output/1/text','completeOutputSHA256':hashlib.sha256(fulltext(OUT/'raw-nlm-cortisol.json').encode()).hexdigest(),'locator':'Adrenal Cortex Hormones page L52-L55, especially L54; Cushing Syndrome page https://www.ncbi.nlm.nih.gov/mesh/68003480 L52-L55, especially L54.'}
]

paths={
 'pth':pth_path,'epi':epi_path,'mel':mel_path,'cort':cort_path
}
source_loc={
 'pth':'NLM MeSH Parathyroid Hormone L52-L55; secretion by parathyroid glands, calcium release from bone, renal tubular calcium reabsorption.',
 'epi':'NLM MeSH Epinephrine L53-L55; hormone from adrenal medulla and stimulation of the heart.',
 'mel':'NLM MeSH Melatonin L52-L55; pineal production and secretion rises in darkness and falls with light.',
 'cort':'NLM MeSH Adrenal Cortex Hormones L52-L55; hydrocortisone among major adrenal cortex hormones. NLM MeSH Cushing Syndrome L52-L55 equates cortisol and hydrocortisone.'
}
sourceproof={
 'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'id':ID,'rawSources':raw_sources,
 'sessionBinding':{'nativeJournal':NATIVE_JOURNAL,'verifiedSessionMetaId':NATIVE,'topLevelCompactions':0},
 'networkCalls':[
  {'nativeCallLine':250,'nativeOutputLine':253,'kind':'open','urls':['https://openstax.org/books/anatomy-and-physiology-2e/pages/17-6-the-adrenal-glands','https://openstax.org/books/anatomy-and-physiology-2e/pages/17-7-the-pineal-gland'],'returnedExtents':[154,93],'outcome':'Bodies read, then excluded after page-level AI-use restriction; no OpenStax evidence is used.'},
  {'nativeCallLine':299,'nativeOutputLine':302,'kind':'search','queries':['site:ncbi.nlm.nih.gov/books parathyroid hormone increases blood calcium bone kidney physiology','site:ncbi.nlm.nih.gov/books epinephrine adrenal medulla acute stress hormone','site:ncbi.nlm.nih.gov/books melatonin pineal gland darkness secretion'],'outcome':'Search response truncated in displayed result; used only to locate official NLM pages, not as evidence.'},
  {'nativeCallLine':308,'nativeOutputLine':311,'kind':'search','queries':['site:ncbi.nlm.nih.gov/books epinephrine adrenal medulla physiology','site:ncbi.nlm.nih.gov/mesh Epinephrine adrenal medulla'],'outcome':'Search response truncated in displayed result; used only to locate official NLM page, not as evidence.'},
  {'nativeCallLine':315,'nativeOutputLine':318,'kind':'open','urls':['https://www.ncbi.nlm.nih.gov/books/NBK482510/','https://www.ncbi.nlm.nih.gov/books/NBK507716/','https://www.ncbi.nlm.nih.gov/mesh/68008550'],'returnedExtents':[3,3,134],'outcome':'Two Bookshelf requests returned reCAPTCHA challenge. Full Melatonin MeSH page was read and retained in raw-nlm-melatonin.json.'},
  {'nativeCallLine':322,'nativeOutputLine':325,'kind':'open','urls':['https://www.ncbi.nlm.nih.gov/mesh/68010281','https://www.ncbi.nlm.nih.gov/mesh?Cmd=DetailsSearch%26Db=mesh%26Term=%22Epinephrine%22%5BMeSH+Terms%5D'],'returnedExtents':[148,1],'outcome':'Full Parathyroid Hormone MeSH page was read and retained. Epinephrine URL encoding returned an internal error; no evidence taken from it.'},
  {'nativeCallLine':331,'nativeOutputLine':334,'kind':'open','urls':['https://www.ncbi.nlm.nih.gov/mesh?Cmd=DetailsSearch&Db=mesh&Term=%22Epinephrine%22%5BMeSH+Terms%5D'],'returnedExtents':[167],'outcome':'Corrected exact Epinephrine MeSH URL returned a full page, read and retained.'},
  {'nativeCallLine':346,'nativeOutputLine':349,'kind':'search','queries':['site:ncbi.nlm.nih.gov/mesh cortisol glucocorticoid adrenal cortex NLM MeSH'],'outcome':'Search response truncated in displayed result; used only to locate NLM pages, not as evidence.'},
  {'nativeCallLine':355,'nativeOutputLine':358,'kind':'open','urls':['https://www.ncbi.nlm.nih.gov/mesh/68000305','https://www.ncbi.nlm.nih.gov/mesh/68003480'],'returnedExtents':[140,143],'outcome':'Both complete NLM MeSH pages were read and are retained together in raw-nlm-cortisol.json.'}
 ],
 'attemptAccounting':[
  {'url':'https://openstax.org/books/anatomy-and-physiology-2e/pages/17-5-the-parathyroid-glands','outcome':'Retained earlier primary context was personally read, but its page states that AI use requires prior written permission; excluded from evidence.'},
  {'url':'https://openstax.org/books/anatomy-and-physiology-2e/pages/17-6-the-adrenal-glands','outcome':'Page disclosed AI-use restriction; excluded from evidence.'},
  {'url':'https://openstax.org/books/anatomy-and-physiology-2e/pages/17-7-the-pineal-gland','outcome':'Page disclosed AI-use restriction; excluded from evidence.'},
  {'url':'https://www.ncbi.nlm.nih.gov/books/NBK482510/','outcome':'Official NCBI Bookshelf request returned reCAPTCHA challenge; no page body used.'},
  {'url':'https://www.ncbi.nlm.nih.gov/books/NBK507716/','outcome':'Official NCBI Bookshelf request returned reCAPTCHA challenge; no page body used.'}
 ],
 'entries':[{'id':ID,'topicId':'human-medicine','sourceOrder':75,'status':'READY_FOR_INDEPENDENT_REVIEW',
  'literalGroups':[ 
   {'group':k,'literal':ga[k],'literalSHA256':canonical(ga[k]),'primaryGround':ground,'locator':loc,'sourcePaths':sps}
   for k,ground,loc,sps in [
    ('prompt_ordered_answers_key','The prompt now asks for the directly supported PTH action, calcium release from bone. Four choices are all hormones; only PTH is secreted by parathyroid glands and promotes bone calcium release. NLM entries independently ground cortisol/hydrocortisone, epinephrine/adrenaline, and melatonin as plausible hormone distractors.','NLM MeSH PTH L54; cortisol source pages L54; epinephrine L55; melatonin L54.',[pth_path,cort_path,epi_path,mel_path]),
    ('explanation','PTH is secreted by parathyroid glands; NLM MeSH states it promotes calcium release from bone and increases renal tubular reabsorption and intestinal calcium absorption.','NLM MeSH PTH L54.',[pth_path]),
    ('note0','Hydrocortisone is another name for cortisol; NLM MeSH lists hydrocortisone among major adrenal cortex hormones.','NLM MeSH Adrenal Cortex Hormones L54; Cushing Syndrome L54.',[cort_path]),
    ('note1','NLM MeSH identifies epinephrine (adrenaline) as a hormone from the adrenal medulla that stimulates the heart.','NLM MeSH Epinephrine L55.',[pth_path]),
    ('note2','NLM MeSH states that mammalian melatonin is produced by the pineal gland, increases in darkness, and decreases with light.','NLM MeSH Melatonin L54.',[mel_path]),
    ('note3','Renal tubular reabsorption of calcium is a distinct fact about PTH beyond the prompt’s bone-release relation and the answer label.','NLM MeSH PTH L54.',[pth_path])
   ]],
  'fourFullPromptAnswerNoteAssessments':[
   {'slot':i,'fullPrompt':proposed['prompt'],'answer':a['text'],'note':a['note'],'tripleSHA256':canonical({'prompt':proposed['prompt'],'answer':a['text'],'note':a['note']}),
    'grammar':'The completed question is grammatical with this masculine singular hormone name in nominative case; all four choices use the same syntactic form and category.','plausibilityUniqueKeyAndNoteTruthUsefulness':why,'sourcePaths':sps,'locator':loc}
   for i,(a,why,sps,loc) in enumerate([
    (proposed['answers'][0],'Cortisol is a real hormone from the adrenal cortex, but the source gives it no parathyroid or bone-calcium-release relation. Its note provides a useful synonym and gland fact.',[cort_path],source_loc['cort']),
    (proposed['answers'][1],'Adrenaline is a real hormone from adrenal medulla and stimulates the heart, but this does not match the parathyroid bone-calcium-release question. Its note gives a concrete organ-of-origin and effect fact.',[epi_path],source_loc['epi']),
    (proposed['answers'][2],'Melatonin is a real pineal hormone with light-dependent secretion, but it does not match the parathyroid bone-calcium-release relation. Its note gives a concrete regulatory fact.',[mel_path],source_loc['mel']),
    (proposed['answers'][3],'PTH is the only option identified as secreted by parathyroid glands and promoting calcium release from bone. The note adds its separate renal calcium-reabsorption action.',[pth_path],source_loc['pth'])
   ])],
  'correctNoteNewFact':'The correct note adds that PTH increases renal tubular calcium reabsorption, beyond the prompt’s bone-release claim and the answer label. NLM MeSH Parathyroid Hormone L54.',
  'absoluteDifficulty':'Hard is appropriate: the player must know the specific physiological effect of PTH on bone calcium mobilization. The choices are four real endocrine hormones and do not become absurd outside the topic.'
 }],
 'qualityCredit':0
}
write('sourceproof.json',sourceproof)

relevant_ids=['human-medicine-large-intestine-water','human-medicine-ext-aldosterone','human-medicine-ext-calcitonin','human-medicine-ext-antidiuretic-hormone','human-medicine-ext-cortisol','human-medicine-ext-epinephrine','human-medicine-ext-melatonin','human-medicine-ext-growth-hormone']
actual_by_id={x['id']:x for x in inventory['actualCurrentPeers']}
assessments={
 'human-medicine-large-intestine-water':('75→42: candidate asks about PTH-driven calcium release from bone; 42’s main fact is large-intestine absorption of water and salts. “Calcium from bones” is only an explicitly false distractor; the card does not teach PTH. 42→75: its keyed relation remains intestinal absorption, not calcium mobilization. Not duplicate.', 'Direct reverse checked: none; bone-calcium release does not reverse large-intestine water absorption.'),
 'human-medicine-ext-aldosterone':('75→72: distinct entity-relation-value-context. Candidate asks PTH-mediated bone calcium release; 72 asks aldosterone-mediated renal sodium reabsorption. 72→75: candidate PTH appears only as a distractor; 72’s main fact remains aldosterone and sodium. Not duplicate or direct reverse.', 'Direct reverse checked: none; sodium retention is not reversed by candidate calcium release.'),
 'human-medicine-ext-calcitonin':('75→73: distinct hormone and relation. Candidate asks PTH stimulating calcium release from bone; 73 asks calcitonin lowering osteoclast activity. 73→75: its main fact is calcitonin, thyroid origin and osteoclast inhibition; candidate does not ask that fact. They form related opposing physiology, not the same fact.', 'Direct reverse checked: candidate is directionally related but not a direct reverse. PTH and calcitonin have different origins and actions; candidate does not ask which hormone suppresses osteoclasts.'),
 'human-medicine-ext-antidiuretic-hormone':('75→74: candidate concerns PTH and bone calcium release; 74 concerns ADH and water reabsorption in collecting ducts. 74→75: PTH is only one distractor; 74’s main fact is ADH-mediated water retention. Not duplicate.', 'Direct reverse checked: none; calcium mobilization and water reabsorption are distinct.'),
 'human-medicine-ext-growth-hormone':('75→100: candidate asks about PTH-driven calcium release from bone; 100 asks which pituitary hormone promotes bone and soft-tissue growth. The shared bone context has a different entity and relation. 100→75: PTH is not its subject. Not duplicate.', 'Direct reverse checked: none; tissue growth is not the reverse of calcium release.'),
 'human-medicine-ext-cortisol':('75→95: candidate’s main fact is PTH and calcium release from bone; 95’s main fact is cortisol as a glucocorticoid in long-term stress. Cortisol is only a distractor in 75. 95→75: PTH is not the subject. Not duplicate.', 'Direct reverse checked: none.'),
 'human-medicine-ext-epinephrine':('75→96: candidate’s main fact is PTH and bone calcium; 96’s main fact is epinephrine from adrenal medulla and heart-rate response in fight-or-flight. Epinephrine is only a distractor in 75. 96→75: PTH is not the subject. Not duplicate.', 'Direct reverse checked: none.'),
 'human-medicine-ext-melatonin':('75→97: candidate’s main fact is PTH and bone calcium; 97’s main fact is pineal melatonin and sleep-wake cycle. Melatonin is only a distractor in 75. 97→75: PTH is not the subject. Not duplicate.', 'Direct reverse checked: none.')}
pairs=[]
for pid in relevant_ids:
    cur=actual_by_id[pid]
    main,rev=assessments[pid]
    pairs.append({'id':pid,'topicId':'human-medicine','sourceOrder':cur['sourceOrder'],'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'actualCurrentPeer':copy.deepcopy(cur['card']),'actualCurrentCanonicalSHA256':cur['sha256'],'bilateralMAINAssessment':main,'directReverseAssessment':rev,'priorSourceproofUsed':False})
chemistry=json.loads((C/'src/content/topics/chemistry.json').read_text())
chemistry_order=next(i for i,q in enumerate(chemistry['questions'],1) if q['id']=='chemistry-ext-calcium-bones')
chemistry_card=copy.deepcopy(chemistry['questions'][chemistry_order-1])
chemistry_peer={'id':chemistry_card['id'],'topicId':'chemistry','sourceOrder':chemistry_order,'card':chemistry_card,'sha256':canonical(chemistry_card)}
pairs.append({'id':chemistry_peer['id'],'topicId':'chemistry','sourceOrder':chemistry_order,'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'actualCurrentPeer':chemistry_card,'actualCurrentCanonicalSHA256':chemistry_peer['sha256'],'bilateralMAINAssessment':'75→chemistry calcium bones: candidate asks a hormone and the process of releasing calcium from bone; chemistry asks which element is part of bone and tooth mineral. Shared calcium/bone subject, but entity-relation differs. Chemistry→75: the keyed value is calcium as an element in mineral tissue; it does not describe hormonal release. Not duplicate.','directReverseAssessment':'Direct reverse checked: none; mineral composition and hormone-driven release are different relations.','priorSourceproofUsed':False})
peer_snapshot={
 'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'id':ID,
 'globalMAIN':inventory['globalMAIN'],
 'sameTopicMAIN':inventory['sameTopicMAIN'],
 'actualCurrentPeers':inventory['actualCurrentPeers'],
 'relevantCrossCatalogPeers':[chemistry_peer],
 'relevantProposedPairs':pairs,
 'selfPreimageBinding':{'id':ID,'sourceOrder':75,'actualCurrentCard':peer,'actualCurrentCanonicalSHA256':canonical(peer),'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'countsAsDistinctPeer':False},
 'certified73Reference':{'path':'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/certification-human-medicine73.json','acceptedId':'human-medicine-ext-calcitonin','acceptedCanonicalSHA256':'2a1fc58710350bd0b04edc22e34e296bda48c21dbecf9b70ddd6420efd6f0a32','usage':'Certification used to distinguish CURRENT73; the current full peer body is included above and compared directly.'},
 'peerFenceNote':'72 and 74 were compared only as their exact current catalog bodies; their historical unsupported proofs were not repaired, reused, or counted.',
 'qualityCredit':0
}
write('peer-snapshot.json',peer_snapshot)
print(json.dumps({'candidate':str(OUT/'candidate.json'),'sourceproof':str(OUT/'sourceproof.json'),'peerSnapshot':str(OUT/'peer-snapshot.json'),'beforeHash':canonical(before),'afterHash':canonical(proposed),'fieldGroups':6,'variants':4,'actualPeers':len(inventory['actualCurrentPeers']),'globalMainRows':len(inventory['globalMAIN']['rows']),'qualityCredit':0},ensure_ascii=False))
