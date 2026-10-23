import copy, hashlib, json
from pathlib import Path

C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine75-cycle1'
OLD=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine75'
INV=json.loads((OUT/'fresh-inventory.json').read_text())
OLDPROOF_PATH=OLD/'sourceproof.json'
OLDPROOF=json.loads(OLDPROOF_PATH.read_text())
ID='human-medicine-ext-parathyroid-hormone'
NATIVE='01a16a57-4bd1-7132-9d5c-a9db16ce628e'
NATIVE_JOURNAL='/Users/eaafonasev/.codex/sessions/2026/10/24/rollout-2026-10-24T00-57-48-01a16a57-4bd1-7132-9d5c-a9db16ce628e.jsonl'
BEFORE_EXPECTED='fbbb4e116d0c709b8076890020dfa1d1bb37d8a4bd843a10e5db8c2ac3467502'

def canonical(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def rel(p): return str(Path(p).resolve().relative_to(C))
def groups(card):
 return {'prompt_ordered_answers_key':{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},'explanation':card['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}

def raw_source(path):
 x=next(s for s in OLDPROOF['rawSources'] if s['path']==path)
 return copy.deepcopy(x)

before=copy.deepcopy(next(x['card'] for x in INV['actualCurrentPeers'] if x['id']==ID))
assert canonical(before)==BEFORE_EXPECTED
assert (before['id'],before['difficulty'],before['correctIndex'])==(ID,'hard',3)
proposed=copy.deepcopy(before)
proposed['prompt']='Какой гормон одновременно усиливает высвобождение кальция из костной ткани и его реабсорбцию в почечных канальцах?'
proposed['answers'][3]['note']='Паратиреоидный гормон также увеличивает выведение фосфатов почками.'
assert (proposed['id'],proposed['difficulty'],proposed['correctIndex'])==(ID,'hard',3)
assert proposed['explanation']==before['explanation']

B=groups(before); A=groups(proposed)
fieldGroups={k:{'beforeCanonicalSHA256':canonical(B[k]),'afterCanonicalSHA256':canonical(A[k])} for k in B}
assert len(fieldGroups)==6
candidate={'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':1,'id':ID,'entries':[{'id':ID,'topicId':'human-medicine','sourceOrder':75,'status':'READY_FOR_SAME_READER_FINAL','beforeCard':before,'beforeHash':canonical(before),'proposedCard':proposed,'afterHash':canonical(proposed),'fieldGroups':fieldGroups}]}
write('candidate.json',candidate)

pth=rel(OLD/'raw-nlm-parathyroid.json'); epi=rel(OLD/'raw-nlm-epinephrine.json'); mel=rel(OLD/'raw-nlm-melatonin.json'); cort=rel(OLD/'raw-nlm-cortisol.json')
oldrel=rel(OLDPROOF_PATH)
unchanged=[
 {'fieldGroup':'explanation','priorAuthorJudgment':f'{oldrel}#/entries/0/literalGroups/1','reason':'Literal, note text and source context are unchanged; current prompt now asks for a subset of the positively grounded PTH mechanisms.'},
 {'fieldGroup':'note0','priorAuthorJudgment':f'{oldrel}#/entries/0/literalGroups/2 and /entries/0/fourFullPromptAnswerNoteAssessments/0/noteTruthUsefulness','reason':'Cortisol/hydrocortisone note is byte-identical and both NLM locators remain the same.'},
 {'fieldGroup':'note1','priorAuthorJudgment':f'{oldrel}#/entries/0/fourFullPromptAnswerNoteAssessments/1/noteTruthUsefulness','reason':'Adrenaline/epinephrine note is byte-identical. Cycle0 literalGroups/3 mistakenly pointed to the PTH-only raw file; cycle1 corrects this evidence binding to raw-nlm-epinephrine.json without changing the note.'},
 {'fieldGroup':'note2','priorAuthorJudgment':f'{oldrel}#/entries/0/literalGroups/4 and /entries/0/fourFullPromptAnswerNoteAssessments/2/noteTruthUsefulness','reason':'Melatonin note is byte-identical and its retained NLM MeSH page is unchanged.'}
]
rawSources=copy.deepcopy(OLDPROOF['rawSources'])
for s in rawSources:
 s['captureReadProvenance']=f'Reused immutable full source and original output pointer from {oldrel}; no network refetch or recapture in cycle1. '+s['captureReadProvenance']

entries=[]
source_data=[
 ('prompt_ordered_answers_key',A['prompt_ordered_answers_key'],
  'The exact question requires both bone calcium release and renal tubular calcium reabsorption. NLM MeSH Parathyroid Hormone L54 positively states both actions. The cortisol evidence links excess cortisol to osteoporosis, a pathological bone association, but does not establish this exact paired calcium-homeostatic action; osteoporosis alone is not equivalent to the pair. The question does not claim cortisol has no skeletal effect. Adrenaline and melatonin retain their independently sourced identities and notes.',
  'NLM MeSH Parathyroid Hormone L52-L54; Cushing Syndrome L52-L54; Adrenal Cortex Hormones L52-L54; Epinephrine L53-L55; Melatonin L52-L54.',[pth,cort,epi,mel]),
 ('explanation',A['explanation'],
  'Unchanged explanation explicitly names PTH, identifies secretion by parathyroid glands, and describes bone calcium release, renal calcium reabsorption and intestinal calcium absorption. The new prompt selects the first two directly stated PTH actions.',
  'NLM MeSH Parathyroid Hormone L54.',[pth]),
 ('note0',A['note0'],
  'Unchanged cortisol note is grounded by the exact immutable author judgment: hydrocortisone is another name for cortisol and is among major adrenal cortex hormones.',
  'Prior author proof '+oldrel+'#/entries/0/literalGroups/2; NLM MeSH Adrenal Cortex Hormones L54 and Cushing Syndrome L54.',[cort]),
 ('note1',A['note1'],
  'Unchanged adrenaline note is grounded by the exact immutable author judgment: NLM MeSH identifies epinephrine/adrenaline as an adrenal-medulla hormone that stimulates the heart.',
  'Prior author proof '+oldrel+'#/entries/0/literalGroups/3; NLM MeSH Epinephrine L53-L55 and L100-L101.',[epi]),
 ('note2',A['note2'],
  'Unchanged melatonin note is grounded by the exact immutable author judgment: NLM MeSH states secretion rises in darkness and decreases with light.',
  'Prior author proof '+oldrel+'#/entries/0/literalGroups/4; NLM MeSH Melatonin L52-L54.',[mel]),
 ('note3',A['note3'],
  'Changed correct-option note adds the distinct fact that PTH increases renal phosphate excretion; it is beyond the paired skeletal and renal calcium actions in the prompt and beyond the answer label.',
  'NLM MeSH Parathyroid Hormone L54.',[pth])
]
for k,literal,ground,loc,sps in source_data:
 entries.append({'group':k,'literal':literal,'literalSHA256':canonical(literal),'primaryGround':ground,'locator':loc,'sourcePaths':sps})

prompt=proposed['prompt']
variants=[]
variant_data=[
 (proposed['answers'][0], [pth,cort], 'Cortisol is a plausible endocrine distractor: its retained NLM source associates prolonged excess with osteoporosis, so I do not dismiss all skeletal effects. The asked relation is the specific paired calcium-homeostatic action of bone release plus renal tubular calcium reabsorption; NLM MeSH directly assigns that pair to PTH. The cortisol source describes an excess-related pathology and does not establish the same pair; osteoporosis alone does not establish it.', 'PTH: NLM MeSH Parathyroid Hormone L54. Cortisol context: Adrenal Cortex Hormones L54; Cushing Syndrome L54.'),
 (proposed['answers'][1], [pth,epi], 'Adrenaline is a real hormone and remains plausible in an endocrine question. Its NLM entry describes adrenal-medulla origin and cardiac stimulation, while the exact paired calcium-homeostatic action is directly stated for PTH in the retained NLM entry. The comparison makes no universal claim that adrenaline has no indirect skeletal effects.', 'NLM MeSH Parathyroid Hormone L54; Epinephrine L53-L55 and L100-L101.'),
 (proposed['answers'][2], [pth,mel], 'Melatonin is a real hormone with light-dependent secretion, a distinct endocrine role. The retained PTH entry positively grounds both requested calcium actions; the melatonin entry does not provide that paired physiological relation.', 'NLM MeSH Parathyroid Hormone L54; Melatonin L52-L54.'),
 (proposed['answers'][3], [pth], 'PTH is the only option positively grounded for the complete pair: NLM MeSH states that it promotes calcium release from bone and increases renal tubular calcium reabsorption. The note adds renal phosphate excretion as a separate PTH fact.', 'NLM MeSH Parathyroid Hormone L52-L54.')
]
for i,(ans,sps,why,loc) in enumerate(variant_data):
 triple={'prompt':prompt,'answer':ans['text'],'note':ans['note']}
 variants.append({'slot':i,'fullPrompt':prompt,'answer':ans['text'],'note':ans['note'],'tripleSHA256':canonical(triple),'grammar':'Read as a complete question with this masculine singular hormone name in nominative case. All four options are endocrine hormone names in the same syntactic form; none supplies a gland-name or answer-word clue.','plausibilityUniqueKeyAndNoteTruthUsefulness':why,'sourcePaths':sps,'locator':loc})

reader_receipt=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/independent-human-medicine75-initial/receipt.json'
reader_pointer=rel(reader_receipt)+'#/entries/0/defects/0'
reader_hash=file_sha(reader_receipt)
sourceproof={
 'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':1,'id':ID,
 'rawSources':rawSources,
 'reusedAttemptLedger':{'path':oldrel,'sha256':file_sha(OLDPROOF_PATH),'originalPacketFreeze':'e95c481f3d14c9769c552bdf4000491c8c18b3fc','networkCallsPointer':'/networkCalls','attemptAccountingPointer':'/attemptAccounting','calls':8,'cycle1NewNetworkCalls':0,'rule':'All failed/consumed URLs and returned extents remain in immutable cycle0 ledger. No URL was retried, relabeled or replaced in this directed cycle.'},
 'sessionBinding':{'nativeJournal':NATIVE_JOURNAL,'verifiedSessionMetaId':NATIVE,'preflightTopLevelCompactions':0,'preflightInputTokens':172445,'contextWindowTokens':258400,'preflightRemainingTokens':85955},
 'entries':[{'id':ID,'topicId':'human-medicine','sourceOrder':75,'status':'READY_FOR_SAME_READER_FINAL','literalGroups':entries,'fourFullPromptAnswerNoteAssessments':variants,
  'correctNoteNewFact':'PTH also increases renal phosphate excretion, distinct from the prompt’s paired calcium actions; NLM MeSH Parathyroid Hormone L54.',
  'absoluteDifficulty':'Hard remains absolute: answering requires specific knowledge of a coordinated two-part endocrine effect across skeletal and renal physiology. The paired action is not derivable from the wording, gland name, or any answer label; all four choices are real hormones.',
  'directedFixResponse':{'readerDefect':{'path':rel(reader_receipt),'sha256':reader_hash,'pointer':'/entries/0/defects/0','code':'UNIQUE_KEY_CORTISOL_NOT_EXCLUDED_BY_CURRENT_PROMPT'},'finding':'The broad bone-release prompt did not support excluding cortisol; osteoporosis association alone neither proves nor disproves the same calcium mechanism.','repair':'The prompt now asks for the specific conjunction of bone calcium release and renal tubular calcium reabsorption. The retained NLM PTH entry directly supports both in one calcium-homeostatic action. Cortisol’s cited osteoporosis association is acknowledged as a pathological bone effect, without claiming cortisol has no skeletal action or treating source silence as proof. The unchanged good explanation supplies the physiological context.'},
  'remainingDefects':[],
  'unchangedAuthorJudgments':unchanged,
  'frozen':{'id':ID,'topicId':'human-medicine','sourceOrder':75,'difficulty':'hard','correctIndex':3}}
 ],
 'qualityCredit':0
}
write('sourceproof.json',sourceproof)

same_ids=['human-medicine-large-intestine-water','human-medicine-ext-aldosterone','human-medicine-ext-calcitonin','human-medicine-ext-antidiuretic-hormone','human-medicine-ext-cortisol','human-medicine-ext-epinephrine','human-medicine-ext-melatonin','human-medicine-ext-growth-hormone']
actual={x['id']:x for x in INV['actualCurrentPeers']}
assess={
 'human-medicine-large-intestine-water':('75→42: paired PTH calcium actions remain distinct from intestinal water/salt absorption. “Calcium from bones” appears only as a wrong option in 42. 42→75: keyed fact is large-intestine absorption; it does not state the paired hormone mechanism. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-aldosterone':('75→72: candidate asks bone calcium release plus renal calcium reabsorption; 72 asks aldosterone-mediated renal sodium reabsorption. Shared organ, different hormone and ion. 72→75: PTH is only a distractor. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-calcitonin':('75→73: candidate asks the PTH paired calcium-homeostatic actions; 73 asks which thyroid hormone lowers osteoclast activity. These are related opposing regulation by different hormones, not the same claim. 73→75: keyed fact remains calcitonin’s osteoclast suppression. Not duplicate.','Direct reverse: checked; related opposing physiology but not a direct reverse question.'),
 'human-medicine-ext-antidiuretic-hormone':('75→74: candidate asks calcium actions on bone and renal calcium reabsorption; 74 asks ADH and water recovery in collecting ducts. 74→75: PTH is only a distractor, not its main fact. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-cortisol':('75→95: candidate asks a paired calcium-homeostatic mechanism; 95 asks cortisol’s glucocorticoid role in long-term stress. Shared option identity only. 95→75: its key and explanation remain about cortisol/stress, not the PTH pair. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-epinephrine':('75→96: candidate’s PTH pair differs from 96’s epinephrine fight-or-flight/heart-rate fact. 96→75: PTH is not the subject. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-melatonin':('75→97: candidate’s PTH pair differs from 97’s pineal melatonin and sleep-wake fact. 97→75: PTH is not the subject. Not duplicate.','Direct reverse: none.'),
 'human-medicine-ext-growth-hormone':('75→100: candidate asks PTH-mediated calcium regulation; 100 asks somatotropin-mediated tissue growth. Shared bone context has a different entity and relation. 100→75: PTH is not the subject. Not duplicate.','Direct reverse: none.')
}
pairs=[]
for pid in same_ids:
 cur=actual[pid]
 main,rev=assess[pid]
 pairs.append({'id':pid,'topicId':'human-medicine','sourceOrder':cur['sourceOrder'],'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'actualCurrentPeer':copy.deepcopy(cur['card']),'actualCurrentCanonicalSHA256':cur['sha256'],'bilateralMAINAssessment':main,'directReverseAssessment':rev,'priorSourceproofUsed':False})
chem=json.loads((C/'src/content/topics/chemistry.json').read_text())
chem_order=next(i for i,q in enumerate(chem['questions'],1) if q['id']=='chemistry-ext-calcium-bones')
chem_card=copy.deepcopy(chem['questions'][chem_order-1]); chem_peer={'id':chem_card['id'],'topicId':'chemistry','sourceOrder':chem_order,'card':chem_card,'sha256':canonical(chem_card)}
pairs.append({'id':chem_peer['id'],'topicId':'chemistry','sourceOrder':chem_order,'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'actualCurrentPeer':chem_card,'actualCurrentCanonicalSHA256':chem_peer['sha256'],'bilateralMAINAssessment':'75→chemistry calcium-bones: paired PTH calcium mobilization/reabsorption differs from chemistry’s calcium as a mineral element in bone and teeth. Chemistry→75: keyed fact is elemental composition, not hormonal transport or renal reabsorption. Not duplicate.','directReverseAssessment':'Direct reverse: none; element composition and hormone-mediated calcium regulation are distinct relations.','priorSourceproofUsed':False})
peer={'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':1,'id':ID,'globalMAIN':INV['globalMAIN'],'sameTopicMAIN':INV['sameTopicMAIN'],'actualCurrentPeers':INV['actualCurrentPeers'],'relevantCrossCatalogPeers':[chem_peer],'relevantProposedPairs':pairs,'selfPreimageBinding':{'id':ID,'sourceOrder':75,'actualCurrentCard':before,'actualCurrentCanonicalSHA256':canonical(before),'proposedCard':copy.deepcopy(proposed),'proposedCanonicalSHA256':canonical(proposed),'countsAsDistinctPeer':False},'certified73Reference':{'path':'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/certification-human-medicine73.json','acceptedId':'human-medicine-ext-calcitonin','acceptedCanonicalSHA256':'2a1fc58710350bd0b04edc22e34e296bda48c21dbecf9b70ddd6420efd6f0a32','usage':'The exact certified current73 full body is independently present in this fresh inventory and compared bilaterally.'},'peerFenceNote':'72 and 74 are included only as fresh exact CURRENT catalog bodies. Their prior HOLD proof is not adopted, fixed, or credited. Cycle0 peer inventory and judgments are not reused as fresh CURRENT evidence.','qualityCredit':0}
write('peer-snapshot.json',peer)
print(json.dumps({'candidate':str(OUT/'candidate.json'),'sourceproof':str(OUT/'sourceproof.json'),'peerSnapshot':str(OUT/'peer-snapshot.json'),'beforeHash':canonical(before),'afterHash':canonical(proposed),'fieldGroups':len(fieldGroups),'variants':len(variants),'currentPeers':len(INV['actualCurrentPeers']),'globalMAINRows':len(INV['globalMAIN']['rows']),'bilateralPairs':len(pairs),'newNetworkCalls':0,'credit':0},ensure_ascii=False))
