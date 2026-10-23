import copy, hashlib, json
from pathlib import Path

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a'
OUT = BASE / 'source-human-medicine39'
NATIVE = '01a16830-9c09-7220-93a6-dde8af9a1987'

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def groups(card):
    return {'prompt_ordered_answers_key': {'prompt': card['prompt'], 'answers': [a['text'] for a in card['answers']], 'correctIndex': card['correctIndex']}, 'explanation': card['explanation'], **{'note'+str(k): a['note'] for k,a in enumerate(card['answers'])}}
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

inv_path = OUT / 'fresh-inventory.json'
inv = json.loads(inv_path.read_text())
current = copy.deepcopy(next(p['card'] for p in inv['actualCurrentPeers'] if p['id'] == 'human-medicine-tonometer-purpose'))
assert canonical_sha(current) == '669699c96dfc5e37711fceb12f7b9a8a7e540832d39d98dec6e3da868607d614'
assert (current['difficulty'], current['correctIndex']) == ('easy', 2)
assert NATIVE == '01a16830-9c09-7220-93a6-dde8af9a1987'

proposed = copy.deepcopy(current)
proposed['answers'] = [
 {'text':'Термометром','note':'Термометр измеряет температуру; цифровой термометр показывает результат на дисплее.'},
 {'text':'Стетоскопом','note':'Врач выслушивает стетоскопом звуки сердца, например закрытие сердечных клапанов.'},
 {'text':'Манжетным аппаратом','note':'Манжету оборачивают вокруг плеча; она соединена с небольшим прибором, показывающим измеренное давление.'},
 {'text':'Глюкометром','note':'Глюкометр исследует каплю крови, обычно взятую из пальца, и показывает содержание глюкозы.'},
]
proposed['explanation'] = 'Артериальное давление измеряют манжетным аппаратом: на плечо надевают надувную манжету, соединённую с устройством, которое показывает результат. Результат записывают двумя числами: систолическим и диастолическим.'
proposed['source'] = {'title':'NHS: Blood pressure test','url':'https://www.nhs.uk/tests-and-treatments/blood-pressure-test/','verifiedAt':'2026-10-23'}

before_groups, after_groups = groups(current), groups(proposed)
field_groups = {k:{'beforeCanonicalSHA256':canonical_sha(before_groups[k]),'afterCanonicalSHA256':canonical_sha(after_groups[k])} for k in before_groups}
entry = {'id':proposed['id'],'topicId':'human-medicine','sourceOrder':39,'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':current,'beforeHash':canonical_sha(current),'proposedCard':proposed,'afterHash':canonical_sha(proposed),'fieldGroups':field_groups}
write('candidate.json', {'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'baselineCode':'15bdba652c4b8a5d766f9552bf3370b9068f8fdf','catalogCandidate':'15bdba652c4b8a5d766f9552bf3370b9068f8fdf','entries':[entry],'qualityCredit':0})

rawdir = OUT/'raw'
raw_specs = [
 ('nhs-blood-pressure-test.json','https://www.nhs.uk/tests-and-treatments/blood-pressure-test/','NHS blood-pressure-test page; its original URL redirected here. Full returned context saved in combined original call output.'),
 ('nhs-fever-in-adults.json','https://www.nhs.uk/symptoms/fever-in-adults/','NHS high-temperature page; original URL redirected here.'),
 ('royal-devon-stethoscope.pdf.json','https://www.royaldevon.nhs.uk/media/u0yftiyf/heart-murmurs-in-a-newborn-infant-077-v4.pdf','Royal Devon NHS and NIDDK pages share one combined original tool output and one retained raw file; the output contains both full page bodies.'),
 ('royal-devon-stethoscope.pdf.json','https://www.niddk.nih.gov/health-information/diabetes/overview/managing-diabetes/','NIDDK managing-diabetes page in the same combined original output as the Royal Devon NHS PDF; same raw path is intentional.'),
]
raw_sources=[]
for name,url,prov in raw_specs:
 p=rawdir/name
 raw=json.loads(p.read_text())
 assert raw['sourceNativeId']==NATIVE and url in raw['originalRecord']['payload']['output'][1]['text']
 raw_sources.append({'path':str(p.relative_to(ROOT)),'url':url,'sha256':file_sha(p),'captureReadProvenance':f'{prov} sourceNativeId={NATIVE}, native journal={raw["nativeJournal"]}, record line={raw["nativeRecordLine"]}, complete output pointer={raw["completeOutputPointer"]}, complete output SHA256={raw["completeOutputSHA256"]}. Personally read the complete returned page body and the cited locator.','completeOutputPointer':raw['completeOutputPointer'],'completeOutputSHA256':raw['completeOutputSHA256']})

all_paths=[x['path'] for x in raw_sources]
source_entries=[]
def add_group(name, ground, locator, paths=all_paths):
 source_entries.append({'group':name,'literal':after_groups[name],'literalSHA256':canonical_sha(after_groups[name]),'primaryGround':ground,'sourcePaths':paths,'locator':locator})
add_group('prompt_ordered_answers_key','NHS identifies blood-pressure testing as checking blood pressure and describes an inflatable upper-arm cuff connected to a machine that displays the measurement. The other three actual answer choices are established by official healthcare sources as temperature, heart-sound, and blood-glucose devices; only the cuffed machine measures blood pressure.','NHS blood-pressure-test L13-L18, L61-L65; NHS fever L27, L38-L49; Royal Devon NHS L4-L8, L23-L24; NIDDK L202-L205.')
add_group('explanation','NHS states the cuff wraps around the upper arm and connects to a small machine that shows blood-pressure measurements; it also defines the two reported numbers as systolic and diastolic.','NHS blood-pressure-test L61-L65 and L79-L85.',[raw_sources[0]['path']])
add_group('note0','The NHS page says a thermometer can show a temperature of 38C or above and gives digital thermometer instructions, including reading the temperature from the display.','NHS fever-in-adults L27 and L38-L49.',[raw_sources[1]['path']])
add_group('note1','The NHS Trust leaflet says a doctor listens to a baby’s heart with a stethoscope and can hear regular heart sounds such as valve closure.','Royal Devon NHS PDF L4-L8 and L23-L24.',[raw_sources[2]['path']])
add_group('note2','NHS describes the inflatable upper-arm cuff and linked machine showing the blood-pressure measurement; this adds the measuring setup beyond the correct answer alone.','NHS blood-pressure-test L61-L65.',[raw_sources[0]['path']])
add_group('note3','NIDDK says a blood-glucose meter tests a drop of blood, usually from a fingertip, and displays the glucose amount at that moment.','NIDDK Managing Diabetes L202-L205.',[raw_sources[3]['path']])

assessments=[]
variant_data=[
 ('NHS fever-in-adults L27 and L38-L49.','The instrumental answer form completes “Каким прибором измеряют…” naturally.','A thermometer is a genuine medical measuring device, so it is a plausible same-category distractor.','It measures temperature rather than arterial pressure.','Its note names a concrete use and says the digital reading appears on the display.'),
 ('Royal Devon NHS PDF L4-L8 and L23-L24.','The instrumental answer form completes the prompt grammatically.','A stethoscope is a familiar clinical instrument, making it a plausible device distractor.','It is used to listen to heart sounds; it does not give a blood-pressure reading as the cuffed machine does.','Its note identifies the heart sounds a clinician can hear with it.'),
 ('NHS blood-pressure-test L61-L65.','“Манжетным аппаратом” agrees with the instrumental prompt “Каким прибором…?”.','A cuffed apparatus is a plausible medical measuring instrument and matches the NHS description of the blood-pressure test.','This is the only choice the NHS page describes as displaying blood-pressure measurements.','The note adds the upper-arm cuff and its connection to a display machine beyond the requested purpose.'),
 ('NIDDK Managing Diabetes L202-L205.','The instrumental answer form completes the prompt grammatically.','A glucose meter is a genuine medical measuring device, so it is a plausible same-category distractor.','It measures glucose in a blood drop, not arterial pressure.','Its note names the sample and explains that the meter shows the glucose amount.'),
]
for slot,(locator,grammar,plaus,unique,useful) in enumerate(variant_data):
 a=proposed['answers'][slot]; triple={'prompt':proposed['prompt'],'answer':a['text'],'note':a['note']}
 p=[raw_sources[1]['path']] if slot==0 else [raw_sources[2]['path']] if slot==1 else [raw_sources[0]['path']] if slot==2 else [raw_sources[3]['path']]
 assessments.append({'slot':slot,'fullPrompt':proposed['prompt'],'answer':a['text'],'note':a['note'],'grammar':grammar,'plausibilityUniqueKeyAndNoteTruthUsefulness':f'{plaus} {unique} {useful}','sourcePaths':p,'locator':locator,'tripleSHA256':canonical_sha(triple)})

write('sourceproof.json',{
 'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'id':proposed['id'],'sourceOrder':39,'status':'READY_FOR_INDEPENDENT_REVIEW','qualityCredit':0,
 'sourceSelection':{'selection':'Use the exact NHS blood-pressure testing page for the key/explanation/correct note, NHS fever page for thermometer facts, Royal Devon NHS Trust leaflet for stethoscope facts, and NIDDK for glucometer facts. Read and retain original returned tool contexts; do not infer the word tonometer/sphygmomanometer because the selected NHS page names a cuff and machine instead.','selectedSourceURL':proposed['source']['url'],'retainedContextReviewed':all_paths,'sourceLimitation':'The NHS describes an upper-arm inflatable cuff connected to a small machine; it does not call the device a tonometer. Proposed answer uses the directly supported wording “манжетный аппарат”.'},
 'rawSources':raw_sources,
 'networkAttempts':[
  {'kind':'web.open','urls':['https://www.nhs.uk/conditions/blood-pressure-test/'],'result':'Page returned fully (102 lines), redirected to https://www.nhs.uk/tests-and-treatments/blood-pressure-test/. Read L13-L18, L61-L65, L79-L85.'},
  {'kind':'web.open','urls':['https://www.nhs.uk/conditions/fever-in-adults/','https://www.nhs.uk/conditions/heart-murmurs/','https://www.niddk.nih.gov/health-information/diabetes/overview/managing-diabetes/blood-glucose-monitoring'],'result':'Fever page returned fully (101 lines), redirected to https://www.nhs.uk/symptoms/fever-in-adults/, and was read at L27, L38-L49. Heart-murmurs and NIDDK blood-glucose-monitoring URLs each returned 404; no claims rely on those failed pages.'},
  {'kind':'web.search','queries':['site:nhs.uk stethoscope doctor listens heart sounds stethoscope','site:niddk.nih.gov blood glucose meter check blood glucose meter'],'result':'Discovery only, not used as proof. Results identified a Royal Devon NHS Trust leaflet and NIDDK Managing Diabetes.'},
  {'kind':'web.open','urls':['https://www.royaldevon.nhs.uk/media/u0yftiyf/heart-murmurs-in-a-newborn-infant-077-v4.pdf','https://www.niddk.nih.gov/health-information/diabetes/overview/managing-diabetes/'],'result':'Both official pages returned in full in one combined native tool output (83 lines for PDF, 333 total page lines for NIDDK). Personally read the full returned bodies and cited locations.'}
 ],
 'entries':[{'id':proposed['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','literalGroups':source_entries,'fourFullPromptAnswerNoteAssessments':assessments,'correctNoteNewFact':{'hasAdditionalFact':True,'fact':'The cuff is wrapped around the upper arm and connected to a small machine showing the measured pressure.','primaryLocator':'NHS blood-pressure-test L61-L65.','beyondPromptAndKey':True},'absoluteDifficulty':{'frozenLevel':'easy','assessment':'Broad adult-level recognition of the instrument for a familiar health measurement; this is a single-step device-purpose match. All distractors are real clinical instruments with identifiable uses rather than absurd choices.','locator':'NHS blood-pressure-test L61-L65; device functions in the four variant locators.'}}],
 'peerAssessmentScope':'Fresh inventory includes globalMAIN 11,000 rows and the full 100 current human-medicine cards. The only exact lexical catalog hit is this assigned card. Bilateral MAIN checks cover same-topic pulse and respiratory-pressure context, plus current and simultaneous proposals for source orders 37 and 38; self is not counted as a peer.',
 'sourceNetworkAccounting':{'actualWebCalls':4,'actualSourceOpens':6,'failedURLs':['https://www.nhs.uk/conditions/heart-murmurs/','https://www.niddk.nih.gov/health-information/diabetes/overview/managing-diabetes/blood-glucose-monitoring'],'recoveryCalls':0,'retriesOrRefetches':0,'extent':'Each opened page was read at the returned extent described above; no search result snippet was used as claim proof.'}
})

peer_by_id={x['id']:x for x in inv['actualCurrentPeers']}
relevant_ids=['human-medicine-diaphragm-inhalation','human-medicine-pulse-source']
relevant_peers=[copy.deepcopy(peer_by_id[i]) for i in relevant_ids]
s37=json.loads((OUT.parent/'source-human-medicine37/candidate.json').read_text())['entries'][0]
s38=json.loads((OUT.parent/'source-human-medicine38/candidate.json').read_text())['entries'][0]
pairs=[]
def addpair(label, card, status, a, b, rev):
 pairs.append({'candidateId':proposed['id'],'candidateCard':proposed,'candidateCanonicalSHA256':canonical_sha(proposed),'peerId':label,'peerCard':card,'peerCanonicalSHA256':canonical_sha(card),'peerStatus':status,'candidateToPeer':a,'peerToCandidate':b,'directReverseCheck':rev})
for peer_id in relevant_ids:
 q=peer_by_id[peer_id]
 if peer_id.endswith('diaphragm-inhalation'):
  left='The candidate asks which device measures systemic arterial pressure; the peer asks how intrapulmonary air pressure changes during inhalation. The entities, measurement target, and context differ.'
  right='The respiratory pressure change does not identify a blood-pressure instrument and cannot answer the candidate. This is a broad shared word “pressure,” not the same relation/value.'
 else:
  left='The candidate asks for an instrument to measure arterial pressure; the peer asks which organ generates the palpable pulse wave. Device-purpose and physiological-source are different relations.'
  right='Knowing the heart produces a pulse wave does not answer which device measures arterial pressure. They concern different entities and values.'
 addpair(peer_id,q['card'],'ACTUAL_CURRENT',left,right,'No direct reverse: neither prompt states the reverse of the other relation.')
for tag, e in [('source37-current',s37),('source37-simultaneous-proposal',s37),('source38-current',s38),('source38-simultaneous-proposal',s38)]:
 card=e['beforeCard'] if tag.endswith('current') else e['proposedCard']
 ident=e['id']+'-'+tag
 if '37' in tag:
  a='The card asks which direction blood flows in arteries of the systemic circuit. The candidate asks which instrument measures arterial pressure. Artery and pressure are related physiology vocabulary, but entity/relation/value/context differ.'
  b='The artery-flow direction does not identify the blood-pressure device; conversely, the device question says nothing about flow direction. No same MAIN.'
 else:
  a='The card asks the direction in which veins carry blood. The candidate asks which device measures arterial pressure. Blood-vessel route and measurement instrument are distinct facts.'
  b='The venous-flow direction cannot answer the device-purpose question, and the device purpose does not answer venous direction. No direct reverse.'
 addpair(ident,card,'HOLD_UNAPPLIED_PROPOSAL' if tag.endswith('proposal') else 'ACTUAL_CURRENT',a,b,'No direct reverse: the compared entities and relations are different (arterial flow direction or venous return vs device measurement).')
write('peer-snapshot.json',{
 'sourceNativeId':NATIVE,'topicId':'human-medicine','cycle':0,'inventory':{'path':str(inv_path),'fileSHA256':file_sha(inv_path)},
 'globalMAIN':inv['globalMAIN'],'sameTopicMAIN':inv['sameTopicMAIN'],'actualCurrentPeers':inv['actualCurrentPeers'],
 'relevantPeerIds':relevant_ids,'relevantPeers':relevant_peers,'relevantPairs':pairs,
 'simultaneousProposals':[{'id':s37['id'],'sourceOrder':37,'status':'HOLD_UNAPPLIED','currentCard':s37['beforeCard'],'currentCanonicalSHA256':canonical_sha(s37['beforeCard']),'proposedCard':s37['proposedCard'],'proposedCanonicalSHA256':canonical_sha(s37['proposedCard']),'beforeHash':s37['beforeHash'],'afterHash':s37['afterHash']},{'id':s38['id'],'sourceOrder':38,'status':'HOLD_UNAPPLIED','currentCard':s38['beforeCard'],'currentCanonicalSHA256':canonical_sha(s38['beforeCard']),'proposedCard':s38['proposedCard'],'proposedCanonicalSHA256':canonical_sha(s38['proposedCard']),'beforeHash':s38['beforeHash'],'afterHash':s38['afterHash']}],
 'qualityCredit':0
})
print(json.dumps({'status':'READY_FOR_INDEPENDENT_REVIEW','id':proposed['id'],'beforeHash':canonical_sha(current),'afterHash':canonical_sha(proposed),'inventoryFileSHA256':file_sha(inv_path),'globalMAINRows':len(inv['globalMAIN']['rows']),'topicPeers':len(inv['actualCurrentPeers']),'rawSourceUniquePaths':len(set(all_paths)),'rawSources':raw_sources,'outputs':['candidate.json','sourceproof.json','peer-snapshot.json'],'qualityCredit':0},ensure_ascii=False,indent=2))
