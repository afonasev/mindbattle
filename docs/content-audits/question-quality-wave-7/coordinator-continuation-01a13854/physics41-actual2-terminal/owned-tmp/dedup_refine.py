import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
P=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original-edition2.json');d=json.loads(P.read_bytes());by={e['index']:e for e in d['entries']}
def card(i):return by[i]['card']
def update(i,prompt,answers,explanation):
 c=card(i);c['prompt']=prompt;c['answers']=[{'text':t,'note':n} for t,n in answers];c['explanation']=explanation
# #39: keep all four angle choices parallel and avoid a length cue.
update(39,'При отражении света от плоского зеркала как связаны углы падения и отражения?',[
('Угол отражения больше и отсчитывается от нормали','Закон отражения задаёт равные углы, оба от нормали.'),
('Они равны и отсчитываются от нормали','Для плоского зеркала изображение виртуально и равноудалено от поверхности.'),
('Угол падения от нормали, а отражения от поверхности','Оба угла измеряются от линии, перпендикулярной зеркалу.'),
('Угол отражения всегда прямой','Нормаль перпендикулярна зеркалу, но отражённый луч не обязан идти вдоль неё.')],
'Закон отражения приравнивает углы падения и отражения, отсчитываемые от нормали. Для плоского зеркала изображение виртуальное и находится на таком же расстоянии за зеркалом, как предмет перед ним.')
# #38: make the last distractor a factual overgeneralization rather than unsupported pole switching.
c=card(38);c['answers'][3]={'text':'Всегда притягиваются независимо от полюсов','note':'Северный и южный полюса притягиваются, но два одинаковых полюса отталкиваются.'}
# #44: avoid repeating the neighbouring boiling/freezing threshold; ask about the distinct triple point.
update(44,'Какие фазы воды одновременно существуют в тройной точке?',[
('Жидкая и газовая','При температуре кипения жидкая и газовая фазы воды могут сосуществовать в закрытом сосуде.'),
('Твёрдая и жидкая','При 1 atm лёд и вода находятся на границе плавления около 0 °C.'),
('Твёрдая, жидкая и газовая','Тройная точка воды — более точная калибровочная температура, чем плавление при 1 atm.'),
('Твёрдая и газовая','При достаточно низком давлении вода может переходить между льдом и паром без жидкой фазы.')],
'Тройная точка — единственная комбинация температуры и давления, при которой вещество существует во всех трёх фазах. Для воды она соответствует 273.16 K, или 0.01 °C.')
# #46: change the circuit/open-circuit inverse predicate to the independently supported electron-drift direction.
update(46,'В каком направлении относительно электрического поля движутся свободные электроны в металлическом проводнике?',[
('По направлению поля','Так двигался бы положительный заряд; свободные электроны в металле заряжены отрицательно.'),
('Перпендикулярно полю','Электрическое поле задаёт силу вдоль себя, а не поперёк поля.'),
('У электронов нет средней скорости','Хаотическое движение не отменяет дрейфовой скорости, возникающей под действием поля.'),
('Против направления поля','Условный ток направлен по полю, противоположно дрейфу электронов.')],
'Свободные электроны отрицательно заряжены, поэтому их средняя дрейфовая скорость противоположна электрическому полю. Условный ток задают как направление движения положительного заряда, поэтому в металле он направлен противоположно дрейфу электронов.')
# Nonrepetitive key notes requested by the review.
c=card(45);c['answers'][3]['note']='В отличие от механических волн, свет распространяется через вакуум.'
c=card(35);c['answers'][1]['note']='Международный символ джоуля — J.'
c=card(31);c['answers'][0]['note']='Одна секунда равна 9 192 631 770 периодам излучения перехода цезия-133.'
c=card(48);c['answers'][3]['note']='В идеальном рычаге выигрыш в силе компенсируется большим перемещением точки её приложения.'
# #47 choices retain source-faithful consequences while reducing length differences and note duplication.
c=card(47);c['answers']=[
 {'text':'Остаётся у электронов; столкновения не передают её решётке','note':'Свободные электроны сталкиваются с атомами проводника, поэтому энергия передаётся решётке.'},
 {'text':'Полностью возвращается источнику; ввод энергии не нужен','note':'Для устойчивого тока в обычном проводнике требуется постоянный ввод энергии; сверхпроводник — исключение.'},
 {'text':'Охлаждает решётку при столкновениях электронов','note':'Столкновения передают энергию атомам и могут повышать температуру проводника.'},
 {'text':'Передаётся атомам решётки, нагревая проводник','note':'Дрейф электронов медленный, хотя их хаотическое движение намного быстрее.'},
]
# Tailor source/editorial arguments to revised #39/#44/#46/#47/#48/#45.
profiles={
39:('OpenStax §16.1 states that reflected and incident angles are equal when both are measured from the normal; it also describes virtual images and equal object/image distance.','The revised prompt tests only the reflection law. Its alternatives probe normal-versus-surface measurement, unequal angles and the mistaken fixed-right-angle rule.'),
44:('OpenStax College Physics 2e §13.5 defines the water triple point as simultaneous solid/liquid/gas equilibrium and gives 273.16 K (0.01 °C).','This replaces the adjacent boiling/freezing threshold with a distinct phase-diagram fact. The four choices compare different coexisting phases and the fixed key remains at index 2.'),
46:('OpenStax College Physics 2e §20.1 figure caption says electron drift velocity is opposite the electric field and conventional current; electrons carry metal current.','The new question asks carrier direction rather than a circuit-open/closed condition, so it avoids the inverse overlap with protected #16. Its four direction choices remain parallel.'),
47:('OpenStax College Physics 2e §20.1 says free-electron collisions transfer energy to atoms, warming the conductor; continuous input sustains an ordinary current.','The card now asks about collision energy, distinct from protected #5’s “which particles carry current?” The four alternatives contrast transfer, storage, loss and cooling.'),
48:('OpenStax Physics §9.3 defines a lever as pivoting around a fulcrum and identifies effort and resistance arms.','The question uses that definition directly instead of an uncited seesaw example; the machine choices are short category names.'),
45:('OpenStax Physics §13.1 classifies light as electromagnetic and says it propagates through vacuum; mechanical sound and water waves require a medium.','The stem asks wave category, not the vacuum capability also relevant to protected #7. Feedback preserves that useful contrast without echoing the key label.')}
for i,(src,ed) in profiles.items():
 r=by[i]['componentReasons'];r['whole_prompt_all_four_ordered_answers_correctIndex_key']['SOURCE']=src;r['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']=ed+' Frozen ID, easy class and correctIndex are preserved.'
 r['sourceMetadata']['SOURCE']=src+' Exact source URL, source bytes, typed paragraph/caption, response headers and transport ranges are hash-bound.'
# Specific source facts and per-note editorial roles for new/changed options.
for j,s in enumerate([
 'The source uses the force direction on positive charge to distinguish it from electron drift.',
 'The free-electron figure depicts longitudinal drift opposite the field, not a transverse path.',
 'The passage defines a nonzero average drift velocity superimposed on random motion.',
 'The figure caption directly says electron drift is opposite field and conventional current is opposite drift.' ]):
 by[46]['componentReasons'][f'note_{j}']['SOURCE']=s
 by[46]['componentReasons'][f'note_{j}']['EDITORIAL']=['This separates sign of charge from field direction.','This rejects a geometric direction confusion.','This distinguishes random microscopic motion from net drift.','This connects the electron answer to the familiar conventional-current convention.'][j]
by[44]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['SOURCE']=profiles[44][0]+' Alternatives distinguish liquid-gas boiling, solid-liquid melting, triple point, and solid-gas coexistence.'
for j,s in enumerate(['§13.5 states liquid and gas phases equilibrate at boiling in a closed container.','The same section gives the water solid-liquid boundary at 0 °C and 1.00 atm.','Its water phase diagram/text identifies simultaneous three-phase equilibrium at 273.16 K.','The phase diagram explains solid-gas coexistence at low pressure without a liquid region.']):
 by[44]['componentReasons'][f'note_{j}']['SOURCE']=s
 by[44]['componentReasons'][f'note_{j}']['EDITORIAL']=['Shows the boiling boundary is a different pair of phases.','Shows a two-phase boundary, not the triple point.','Adds a precise calibration consequence beyond the answer label.','Shows that phase pairs depend on the pressure region.'][j]
by[44]['componentReasons']['explanation']['SOURCE']=profiles[44][0]
by[44]['componentReasons']['explanation']['EDITORIAL']='The first sentence defines what is special about the triple point; the second gives water’s exact value in both temperature scales.'
by[44]['componentReasons']['difficulty']['SOURCE']=profiles[44][0]+' The source states the defining three-phase condition directly.'
by[44]['componentReasons']['difficulty']['EDITORIAL']='The player recognizes a named point from its defining phase combination; the numeric value stays in feedback.'
by[44]['componentReasons']['sourceMetadata']['SOURCE']=profiles[44][0]+' Source page is the full College Physics 2e §13.5 capture; typed paragraphs and original CNXML headers are bound.'
by[44]['componentReasons']['sourceMetadata']['EDITORIAL']='The exact §13.5 URL supports the phase diagram and water values; provenance stays in the audit packet.'
# precise #46 field reasons
by[46]['componentReasons']['explanation']['SOURCE']=profiles[46][0]+' The section also defines conventional current as the direction positive charge would flow.'
by[46]['componentReasons']['explanation']['EDITORIAL']='Two sentences explain the opposite signs and link them to conventional-current notation without adding a calculation.'
by[46]['componentReasons']['difficulty']['SOURCE']=profiles[46][0]+' The answer is a one-direction relation stated by the figure caption.'
by[46]['componentReasons']['difficulty']['EDITORIAL']='One-step recognition of a diagram’s arrow relation remains easy; no circuit or electron-force calculation is needed.'
by[46]['componentReasons']['sourceMetadata']['SOURCE']=profiles[46][0]+' The packet binds the full §20.1 CNXML bytes and the caption/figure media alt that states the arrow direction.'
by[46]['componentReasons']['sourceMetadata']['EDITORIAL']='A single section URL covers both electron drift and the conventional-current distinction used in the feedback.'
# changed #39 and #47 note source/editorial evidence.
for j,s in enumerate(['The law makes the two normal-referenced angles equal.','The mirror section describes virtual images and equal object/image distance.','The normal is perpendicular to the mirror, so a surface-referenced angle is complementary.','The right-angle relation belongs to the normal and surface, not a fixed reflected-ray angle.']):by[39]['componentReasons'][f'note_{j}']['SOURCE']=s
for j,s in enumerate(['Electron drift is described as opposite E and directed against conventional current.','The passage on free electrons says collisions transfer energy to the conductor.','Collision energy transfer can raise conductor temperature.','The figure caption distinguishes average drift from much faster electron motion.']):by[47]['componentReasons'][f'note_{j}']['SOURCE']=s
# Add complete typed exact §13.5 triple-point element and §20.1 drift figure/caption, retaining each source's exact raw-byte binding.
WT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');rootdir=WT/'docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals'
def binding(f):
 b=f.read_bytes();return {'path':str(f),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'gitBlobSha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
for fn,terms,source in [('openstax-m42218-index.cnxml',['triple point occurs in 273.16'], 'OpenStax College Physics 2e §13.5'),('openstax-m42341-index.cnxml',['direction opposite to the electric field'], 'OpenStax College Physics 2e §20.1')]:
 f=rootdir/fn;tree=ET.parse(f).getroot()
 for el in tree.iter():
  txt=' '.join(''.join(el.itertext()).split())
  attrs=[x.attrib.get('alt') for x in el.iter() if x.tag.split('}')[-1]=='media' and x.attrib.get('alt')]
  if any(t in txt.lower() for t in terms) or any(any(t in a.lower() for t in terms) for a in attrs):
   ctx={'kind':'cnxml-element-and-media-alt','source':source,'elementId':el.attrib.get('id'),'tag':el.tag.split('}')[-1],'literalText':txt,'mediaAlt':attrs,'binding':binding(f)}
   if not any(x.get('elementId')==ctx['elementId'] and x.get('source')==source for x in d['primaryContexts']):d['primaryContexts'].append(ctx)
# Rebind source note reasons for #42 phase answer after replacing plasma.
by[42]['componentReasons']['note_3']['SOURCE']='The §13.5 full paragraph says liquid and gas phases are in equilibrium at boiling temperature inside a closed container.'
by[42]['componentReasons']['note_0']['SOURCE']='§13.5 gives the gas-to-liquid condensation transition as real gas is cooled.'
# Exact frozen-contract and reason structure checks.
for i,e in by.items():
 if 'card' in e:
  c=e['card'];assert c['id']==d['scope']['ids'][i-30] and c['difficulty']=='easy' and c['correctIndex']==d['scope']['keySlots'][i-30]
  assert len(c['answers'])==4 and len(e['componentReasons'])==8
  assert all(set(x)=={'SOURCE','EDITORIAL'} for x in e['componentReasons'].values())
b=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();P.write_bytes(b);print(len(b),hashlib.sha256(b).hexdigest())
