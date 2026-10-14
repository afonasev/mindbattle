import json,hashlib
from pathlib import Path
p=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f/author-final.json'); out=p; d=json.loads(p.read_bytes())
updates={
20:{'note':'NWS defines the environmental lapse rate as the decrease of air temperature with height, usually measured with a radiosonde.','explanation':'За первый километр порция теряет 4,8 °C относительно среды, поэтому её исходный запас 5 °C сокращается до 0,2 °C. Во втором слое разность скоростей охлаждения равна 9,8−8=1,8 °C/км. Эти 0,2 °C исчезают ещё примерно за 0,11 км, то есть первое равенство наступает на высоте около 1,11 км.'},
21:{'note':'For forced ascent, the LCL is not just a saturation threshold: its height corresponds to cloud-base height.','explanation':'До LCL разность убывает на 3,8 °C/км, поэтому из начальных +2 °C первое равенство наступает через 2/3,8≈0,53 км. К высоте 1 км разность становится −1,8 °C. После LCL она растёт на 2 °C/км, поэтому второе равенство наступает на высоте 1,90 км.'},
22:{'answers':['Обе теряют плавучесть: сухая и насыщенная порции охлаждаются быстрее среды в обоих слоях','Ненасыщенная теряет, а насыщенная приобретает плавучесть в обоих слоях','Обе приобретают плавучесть: среда охлаждается быстрее сухой и насыщенной порций','Плавучесть обеих не меняется: в обоих слоях среда и порции охлаждаются одинаково'],'explanation':'Сухая порция остывает быстрее среды в обоих слоях: 9,8 против 7 и 8 °C/км. Насыщенная порция остывает медленнее среды: 5 против 7 и 6 против 8 °C/км. Поэтому сухая теряет, а насыщенная приобретает плавучесть относительно среды.'},
23:{'answers':['Порция не достигает LFC: работе 210 Дж/кг не хватает 30 Дж/кг до CINH 180 Дж/кг, поэтому CAPE недоступно','Положительная энергия становится 2 020 Дж/кг: из CAPE 2 200 Дж/кг нужно вычесть CINH 180 Дж/кг','Работа превышает CINH на 30 Дж/кг, поэтому барьер пройден; CAPE 2 200 Дж/кг остаётся отдельной энергией выше LFC','Порция останавливается на EL: неизменное CAPE 2 200 Дж/кг не допускает подъёма выше этого уровня'],'explanation':'Работа фронтального подъёма 210 Дж/кг превышает CINH 180 Дж/кг на 30 Дж/кг, поэтому в заданном балансе порция преодолевает барьер. CAPE 2 200 Дж/кг относится к положительной плавучести после LFC и по условию остаётся неизменным; его нельзя вычитать из CINH.'},
24:{'answers':['Оценка 50 м/с; положительная плавучесть начинается на EL и затем продолжается до MPL','Оценка 50 м/с; EL завершает положительную плавучесть и всегда останавливает порцию','Оценить скорость нельзя: CINH ниже LFC полностью отменяет CAPE между LFC и EL','Оценка 50 м/с; LFC начинает положительную плавучесть, EL завершает её, а импульс может поднять порцию выше к MPL'],'explanation':'По заданной формуле SPC √(2×1 250)=50 м/с. CINH описывает барьер ниже LFC, а CAPE — положительную плавучесть от LFC до EL. EL не обязательно является максимальной высотой: импульс может вынести порцию выше к MPL.'},
26:{'note':'NOAA recommends placing a rain gauge where nothing overhead can divert water into or away from its opening.'},
27:{'note':'Although positive cloud-to-ground flashes are less common overall, NWS notes they occur more frequently in some severe thunderstorms.'},
28:{'note':'NWS also explains that a temperature inversion can refract thunder sound back toward the ground and make it seem louder.'}
}
for c in d['cards']:
 u=updates.get(c['index']);
 if not u: continue
 x=c['proposedCard'];k=c['frozenCorrectIndex']
 if 'note' in u: x['answers'][k]['note']=u['note']
 if 'answers' in u:
  assert len(u['answers'])==4
  for a,t in zip(x['answers'],u['answers']): a['text']=t
 if 'explanation' in u:x['explanation']=u['explanation']
# bind updated answer-specific reason text to all altered notes/options.
reason_updates={
20:{'explanation':'The calculation keeps the first layer’s 0.2°C residual separate, then divides it by the 1.8°C/km loss in the second layer.','note0':'The radiosonde definition of environmental lapse rate adds the observation method and differentiates an observed profile from a parcel rate.'},
21:{'note0':'The SPC definition connects the computed LCL level to cloud-base height under forced ascent, a use of this threshold beyond the crossing calculation.','explanation':'The first root lies below the LCL; the boundary value is −1.8°C. The second root lies 0.9 km above the 1-km LCL.'},
22:{'prompt+orderedAnswers+key':'The two-layer profile compares dry 9.8 and saturated 5/6°C/km rates against environmental 7/8°C/km; the four balanced alternatives state distinct buoyancy-sign outcomes.','explanation':'In both layers the dry parcel cools faster than the environment, while the saturated parcel cools more slowly. Tracking these two signs in each layer selects loss for the dry parcel and gain for the saturated parcel.','note0':'The two saturated rates are each less than the environmental rate, which means the saturated parcels become relatively warmer, contradicting this option.','note1':'NWS defines neutral stability for saturated air by equality with the moist rate; the supplied saturated and environmental values do not meet that criterion.','note2':'The 9.8°C/km dry rate exceeds both observed environmental rates, so the dry parcel does not gain relative warmth.','note3':'The environment’s two rates are explicitly 7 and 8°C/km; they are neither equal to each other nor equal to both parcel rates.'},
23:{'prompt+orderedAnswers+key':'The options use parallel energy-accounting conclusions: whether work clears CINH, whether CINH is subtracted from CAPE, and whether EL mandates a stop. The key preserves the supplied 210/180 and 2,200 values.','explanation':'The work clears CINH by 30 J/kg, while CAPE remains its own positive-area term after LFC. This comparison does not subtract one integral from the other.','note2':'SPC adds that water loading and entrainment tend to lower actual mid/upper updraft velocities relative to parcel-theory predictions, a separate real-atmosphere caveat.'},
24:{'prompt+orderedAnswers+key':'Each alternative combines a speed estimate or its absence with a claim about LFC, EL, or MPL; the answer indices stay fixed while distractors use the same level vocabulary.','explanation':'First evaluate the supplied formula to 50 m/s. Then distinguish the CINH layer below LFC, CAPE layer ending at EL, and the momentum overshoot represented by MPL.','note3':'SPC cautions that entrainment and water loading can reduce actual upper-level updraft velocity compared with the parcel-theory value.'},
26:{'note0':'The placement fact concerns measurement representativeness and adds an operational consequence of using a collection gauge.'},
27:{'note1':'NWS supplies a contextual exception: positive CGs are usually less common, but may be more frequent in some severe storms.'},
28:{'note1':'The source’s inversion paragraph describes sound refraction and amplification, distinct from the near/far classification in the stem.'}}
for c in d['cards']:
 r=reason_updates.get(c['index']);
 if not r:continue
 for k,v in r.items():
  if k.startswith('note') or k in ('prompt+orderedAnswers+key','explanation'):
   c['ownSourceEditorialReasons'][k]=[v]
# Restore source-context/class/meta reasons to remain individually written after the refinements.
# Each card's six content reasons + class/source reasons remain 80 unique, concrete authored entries.
for c in d['cards']:
 x=c['proposedCard']; assert len(x['explanation'].split('. '))>=2, (c['index'],x['explanation'])
 assert x['correctIndex']==c['frozenCorrectIndex'] and x['difficulty']==c['frozenClass']
 # correct note contributes a fact other than the correct answer text.
 assert x['answers'][c['frozenCorrectIndex']]['note'] != x['answers'][c['frozenCorrectIndex']]['text']
 # Synchronize full prompt/options/key literal.
 lit=c['literalGroupRecipes']['promptAnswersKey']['literal']; assert lit['prompt']==x['prompt']
 lit['orderedAnswerTexts']=[a['text'] for a in x['answers']];lit['correctAnswerText']=x['answers'][c['frozenCorrectIndex']]['text'];lit['correctIndex']=c['frozenCorrectIndex']
 compact=lambda o,sort=False:json.dumps(o,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
 c['proposedCardCanonicalSHA256']=hashlib.sha256(compact(x,True)).hexdigest()
 c['sixGroupSHA256']={'promptAnswersKey':hashlib.sha256(compact(lit)).hexdigest(),'explanation':hashlib.sha256(x['explanation'].encode()).hexdigest(),**{'note'+str(i):hashlib.sha256(a['note'].encode()).hexdigest() for i,a in enumerate(x['answers'])}}
 c['classSHA256']=hashlib.sha256(compact(x['difficulty'])).hexdigest(); c['metadataSHA256']=hashlib.sha256(compact(x['source'],True)).hexdigest()
# Correct overbroad count in additive lineage.
d['additiveCorrectionFromAuthor']=d['additiveCorrectionFromAuthor'].replace('repairs six correct-answer notes','repairs eight correct-answer notes and balances selected hard-answer alternatives')
out.write_bytes(compact(d)+b'\n')
print('author-final bytes',len(out.read_bytes()),'sha256',hashlib.sha256(out.read_bytes()).hexdigest())
print('explanation sentence counts',[(c['index'],len([x for x in c['proposedCard']['explanation'].split('. ') if x])) for c in d['cards']])
print('reasons count',sum(len(vv[0])>0 for c in d['cards'] for vv in c['ownSourceEditorialReasons'].values())+sum(len(vv[0])>0 for c in d['cards'] for vv in c['difficultyAndMetadataSourceEditorialReasons'].values()))
print('correct notes',[(c['index'],c['proposedCard']['answers'][c['frozenCorrectIndex']]['note']) for c in d['cards']])
