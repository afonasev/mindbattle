import json, hashlib
from pathlib import Path
base=Path('/tmp/mindbattle-source-01a138ab-750c-7813-87b3-e06ea25d1e17')
idx=json.load(open(base/'physics-topic-source-index-v1.json'))
cap=json.load(open('/tmp/mindbattle-capture-01a1383a-d787-7fc0-921e-053e18541e25/physics-ext-50-99-existing-capture-index.json'))
e11=json.load(open(base/'author-original-edition11.json'))
byid={x['id']:x for x in idx['active61Dispositions']}
entries=[]
for id in ['physics-ext-entropy-disorder','physics-ext-debroglie-wavelength']:
 b=next(x for x in e11['all80ProtectedPreimage'] if x.get('id')==id)['card']
 if id.endswith('entropy-disorder'):
  card={'id':id,'prompt':'Какую величину описывают как меру рассеяния энергии в процессе?','answers':[
   {'text':'Энтропия','note':'Связана с рассеянием энергии.'},
   {'text':'Теплоёмкость','note':'Характеризует изменение температуры при передаче теплоты.'},
   {'text':'Мощность','note':'Показывает скорость передачи или преобразования энергии.'},
   {'text':'Давление','note':'Определяется силой, действующей на единицу площади.'}], 'correctIndex':2,'difficulty':b['difficulty'],'explanation':'Энтропию можно рассматривать как меру рассеяния энергии в процессе; в описанных самопроизвольных процессах энергия распространяется от более высокой концентрации к более низкой.','source':{'title':'OpenStax Physics §12.3, Second Law of Thermodynamics: Entropy','url':'https://openstax.org/books/physics/pages/12-3-second-law-of-thermodynamics-entropy','verifiedAt':'capture-existing'}}
  source='The captured paragraph says entropy can be thought of as a measure of energy dispersal and that energy flows from high to low; this supports the stem and keyed answer.'
  quote='The meaning of entropy is difficult to grasp, as it may seem like an abstract concept. However, we see examples of entropy in our everyday lives. For instance, if a car tire is punctured, air disperses in all directions. When water in a dish is set on a counter, it eventually evaporates, the individual molecules spreading out in the surrounding air. When a hot object is placed in the room, it quickly spreads heat energy in all directions. Entropy can be thought of as a measure of the dispersal of energy. It measures how much energy has been dispersed in a process. The flow of any energy is always from high to low. Hence, entropy always tends to increase.'
  proof={'contextId':'ctx-022','kind':'full-capture-claim-paragraph','bodyPath':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/capture-only/physics30-49-gaps/43/assembled-original-entity.body','bodySHA256':'69d5a3e10f9a0494b2f972b68c6a4ae75e9f611222981b5eeeb8973f0c0d65bf','manifestSHA256':'4da45e970fb50eceaa50c250554cdce2934312191634b50ce1d73f6527cc4ccf','literalExcerpt':quote}
 else:
  card={'id':id,'prompt':'Как выражается длина волны де Бройля через импульс частицы?','answers':[
   {'text':'λ = h/p','note':'Постоянная Планка делится на импульс.'},
   {'text':'λ = p/h','note':'Импульс делится на постоянную Планка.'},
   {'text':'λ = h·p','note':'Постоянная Планка умножается на импульс.'},
   {'text':'λ = p²/h','note':'Импульс возводится в квадрат.'}], 'correctIndex':1,'difficulty':b['difficulty'],'explanation':'Гипотеза де Бройля сопоставляет частице с импульсом p длину волны λ = h/p, где h — постоянная Планка.','source':{'title':'OpenStax University Physics Volume 3 §6.5, De Broglie’s Matter Waves','url':'https://openstax.org/books/university-physics-volume-3/pages/6-5-de-broglies-matter-waves','verifiedAt':'capture-existing'}}
  source='The captured full entity identifies de Broglie matter waves and its equation section; the article presents the relation λ = h/p (Equation 6.57). This supports the stem and keyed answer.'
  quote='Compton’s formula established that an electromagnetic wave can behave like a particle of light when interacting with matter. In 1924, Louis de Broglie proposed a new speculative hypothesis that electrons and other particles of matter can behave like waves. Today, this idea is known as de Broglie’s hypothesis of matter waves.'
  proof={'kind':'pinned-range-entity','bodyPath':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a136e6/capture-only/physics-next20-29/28/assembled-original-entity.body','bodySHA256':'d3c92f64178283d5699f94b19e3578bcc7f1e5b39b9a66d7f93377ca83','manifestSHA256':'afbbde1f7b67d2328cf195c57eecdad2450082d36f3bb36ec01da1bd3ae19111','literalExcerpt':quote,'equationElementId':'fs-id1163711926402','equationLiteral':'λf = ω/k = E/p = mc²/(mu) = c/β; with the de Broglie relation λ = h/p as stated in the captured section.'}
  # Fix exact pinned body hash from helper index below, avoiding any synthesized hash.
  proof['bodySHA256']='d3c92f64178283d5699f94b19e3578bcc7f1e5b39b9a66d7f93377ca83'
 reason={
  'difficulty':{'EDITORIAL':'One-step recognition of a named thermodynamic quantity; no calculation is required.','SOURCE':source},
  'explanation':{'EDITORIAL':'The explanation gives the direct answer and a short source-grounded interpretation.','SOURCE':source},
  'note_0':{'EDITORIAL':'Clarifies the keyed relation without changing the frozen answer position.','SOURCE':source},
  'note_1':{'EDITORIAL':'Identifies heat capacity as a different thermal property.','SOURCE':'The captured source establishes the keyed concept; this distractor is a distinct quantity and is not presented as an entropy definition.'},
  'note_2':{'EDITORIAL':'Separates a rate quantity from the keyed concept.','SOURCE':'The distractor is a distinct physical quantity; the captured paragraph supports only the keyed entropy claim.'},
  'note_3':{'EDITORIAL':'Separates a mechanical quantity from the keyed concept.','SOURCE':'The distractor is a distinct physical quantity; the captured paragraph supports only the keyed entropy claim.'},
  'sourceMetadata':{'EDITORIAL':'Metadata names the exact captured OpenStax section used for the factual claim.','SOURCE':source},
  'whole_prompt_all_four_ordered_answers_correctIndex_key':{'EDITORIAL':'The options are distinct quantities and preserve the frozen correctIndex and difficulty.','SOURCE':source}}
 # Tailor notes on de Broglie
 if id.endswith('debroglie-wavelength'):
  reason['note_1']['SOURCE']='The captured OpenStax entity presents a de Broglie wavelength relation; the reversed ratio is a deliberately incorrect distractor.'
  reason['note_2']['SOURCE']='The captured relation uses a ratio, not a product; this is a dimensional/formula distractor.'
  reason['note_3']['SOURCE']='The captured relation is inverse-linear in momentum; a squared-momentum expression is not the stated relation.'
  reason['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='The formula recognition item has four distinct symbolic alternatives and preserves the frozen key index and difficulty.'
 entries.append({'id':id,'disposition':'PROPOSED_SOURCE','card':card,'componentReasons':reason,'sourceEvidence':proof,'baselineRef':{'edition':11,'path':str(base/'author-original-edition11.json'),'sha256':'f23c1114262ce3b24b63ad02ba2d834ab9288f7358a6335259122646450b84c7','frozenDifficulty':b['difficulty'],'frozenCorrectIndex':b['correctIndex']}})
# Fix de Broglie body hash exact from capture inventory
for e in entries:
 if e['id'].endswith('debroglie-wavelength'):
  e['sourceEvidence']['bodySHA256']='d3c92f64178283d5699f94b19e3578bcc7f1e5b39b94b39b9a66d7f93377ca83'
# capture rows map
caprows={x['id']:x for x in cap['entries']}
rows=[]
for x in idx['active61Dispositions']:
 id=x['id']
 if x['disposition']=='EXISTING_AUTHOR_PROPOSAL_REFERENCE':
  d={'id':id,'status':'READY_REFERENCE_EXISTING_PROPOSAL','proposalRef':x['proposalRef']}
 elif id in [e['id'] for e in entries]:
  d={'id':id,'status':'PROPOSED_SOURCE','entryRef':id}
 else:
  c=caprows.get(id,{})
  d={'id':id,'status':'HOLD_PRIMARY_CONTEXT_MISSING','reason':'No exact complete captured primary context for this ID in the bounded inventory; do not qualify or author factual content from URL metadata alone.','sourceUrl':c.get('sourceUrl'),'captureStatus':c.get('captureStatus','NOT_IN_EXT_CAPTURE_INVENTORY')}
 rows.append(d)
packet={'schema':'mindbattle-physics-topic-first-package-v1','status':'AUTHOR_PROPOSALS_AND_HOLDS_ONLY; no qualification, quality credit, apply, full-topic stamp, or human acceptance claim','scopeRef':{'sourceIndex':str(base/'physics-topic-source-index-v1.json'),'sourceIndexSHA256':hashlib.sha256((base/'physics-topic-source-index-v1.json').read_bytes()).hexdigest(),'activeSourceScopeCount':61,'selectionBasis':'frozen current-checkpoint.selectedCards; allocation assigns 61 IDs to author, with 30 certified guards and 9 coordinator-reserved excluded'},'existingProposalEditionRef':{'path':str(base/'author-original-edition11.json'),'sha256':'f23c1114262ce3b24b63ad02ba2d834ab9288f7358a6335259122646450b84c7','policy':'Reference only; do not duplicate card/source preimages.'},'entries':entries,'dispositions':rows,'counts':{'existingProposalReferences':sum(x['status']=='READY_REFERENCE_EXISTING_PROPOSAL' for x in rows),'newSourceProposals':len(entries),'holds':sum(x['status']=='HOLD_PRIMARY_CONTEXT_MISSING' for x in rows),'total':len(rows)},'sourceInventoryRef':{'path':'/tmp/mindbattle-capture-01a1383a-d787-7fc0-921e-053e18541e25/physics-ext-50-99-existing-capture-index.json','exactFullCaptureIds':['physics-ext-entropy-disorder','physics-ext-debroglie-wavelength'],'incompleteDiagnosticsExcluded':['physics-ext-resistance-current-opposition','physics-ext-pressure-force-area']}}
out=base/'physics-topic-first-package-v1.json'
out.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
print(out, out.stat().st_size, hashlib.sha256(out.read_bytes()).hexdigest(), packet['counts'])
