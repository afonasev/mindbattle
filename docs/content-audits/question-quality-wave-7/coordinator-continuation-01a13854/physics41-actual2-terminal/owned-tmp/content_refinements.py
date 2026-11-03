import json,hashlib
from pathlib import Path
P=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original-edition2.json');d=json.loads(P.read_bytes());by={e['index']:e for e in d['entries']}
def note(i,j,s):by[i]['card']['answers'][j]['note']=s
def exp(i,s):by[i]['card']['explanation']=s
# More informative extra key facts; explanations independently elaborate the relation.
note(37,1,'Нормальная сила поверхности перпендикулярна ей и не является парой действия-реакции силы тяжести.')
exp(37,'Сила тяжести направлена к центру Земли, а нормальная сила опоры — наружу, перпендикулярно поверхности. На покоящийся предмет у горизонтальной опоры результирующая этих сил равна нулю.')
note(38,1,'Магнитные концы различают как северный и южный полюса по их ориентации.')
exp(38,'Одноимённые полюса отталкиваются, а разноимённые притягиваются. Поэтому взаимодействие определяется тем, какие концы магнитов обращены друг к другу.')
note(39,1,'Плоское зеркало создаёт виртуальное изображение за поверхностью; его можно зарегистрировать камерой.')
exp(39,'Закон отражения приравнивает углы падения и отражения, отсчитываемые от нормали. Для плоского зеркала изображение виртуальное и находится на таком же расстоянии за зеркалом, как предмет перед ним.')
note(42,2,'При точке плавления твёрдая и жидкая фазы воды находятся в равновесии.')
exp(42,'При обычном давлении лёд — твёрдая фаза воды. Повышение давления может сдвинуть границу фаз и вызвать плавление даже при неизменной температуре.')
c=by[42]['card'];c['answers']=[
 {'text':'Состоянием газа без собственного объёма','note':'Газ не имеет фиксированного объёма и занимает доступное пространство.'},
 {'text':'Жидким состоянием','note':'Жидкость сохраняет объём, но принимает форму сосуда.'},
 {'text':'Твёрдым состоянием','note':'Лёд — твёрдая фаза воды; твёрдое тело сохраняет собственную форму.'},
 {'text':'Равновесием жидкости и газа','note':'В закрытом контейнере при температуре кипения жидкость и газ могут находиться в равновесии.'},
]
note(43,2,'§12.3 называет энтропию мерой рассеивания энергии и её доступности для совершения работы.')
exp(43,'После прокола воздух рассеивается во все стороны. §12.3 приводит этот бытовой пример, чтобы показать рассеивание энергии и рост энтропии.')
note(44,2,'На границе плавления твёрдая и жидкая фазы воды находятся в равновесии.')
note(47,1,'В обычном проводнике источник непрерывно подводит энергию; сверхпроводник указан как исключение.')
note(48,3,'В схеме рычага опора разделяет плечо приложения усилия и плечо сопротивления.')
# Editorial reasons for all eight component groups are specific to each question and option, with separate SOURCE statements retained.
# Source/core profiles are in the artifact; refine each non-note editorial slot to the actual learning decision.
exp_ed={30:'The note explains what the gram is while the explanation shows the base-unit/prefix relationship; this is the small but useful extra beyond “kilograms.”',31:'The exact atom-based definition is followed by why a reproducible reference matters, so the feedback teaches more than the word “seconds.”',32:'The definition through light speed and the kilometre conversion serve separate scales of length.',33:'The derived-unit expression adds dimensional context; no player needs to derive it during the round.',34:'The symbol and unit-rate meaning are split across feedback so “watt” gains a practical interpretation.',35:'The note states the SI mechanical equivalent; the explanation connects that identity to work by a force.',36:'The note supplies an equivalent unit form; the second sentence handles the important BIPM exception for random nuclear activity.',37:'Gravity and support are presented as separate forces; the second sentence resolves why a supported object may still have weight.',38:'The first sentence gives both interaction rules; the second explains why orientation of the two magnets matters.',39:'The first sentence explains angle measurement; the second extends the rule to the visible virtual image.',42:'The note adds phase coexistence; the explanation supplies a pressure-dependent consequence of the same diagram.',43:'The source’s tire example anchors the observation, and the second sentence names the entropy connection that explains why it matters.',44:'The phase-boundary note clarifies coexistence; the explanation identifies the same boundary in both freezing and melting directions.',45:'The note adds energy transport without matter transfer; the explanation contrasts electromagnetic and mechanical media needs.',46:'The note spells out the complete terminal-to-terminal route; the explanation explains what a break changes.',47:'The note distinguishes random electron motion from drift; the explanation follows energy into the lattice and heat.',48:'The note names the two lever arms; the explanation relates their distances to effort and mechanical advantage.',49:'The note gives the square-law fact; the explanation distinguishes perceived loudness, pitch and decibel level.'}
for i,v in exp_ed.items():by[i]['componentReasons']['explanation']['EDITORIAL']=v
# Exact #48 whole-card reason updated after changing from an uncaptured seesaw example to the captured definition.
by[48]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='The prompt paraphrases the source definition of a lever’s pivot, and each distractor remains another named simple machine. This removes the unsupported seesaw example while retaining the user’s frozen easy class and key slot.'
# Correct #42 editorial note rationale after using source-supported phase equilibrium as distractor.
by[42]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='All choices describe a phase or phase condition: gas, liquid, solid, or liquid-gas equilibrium. Only solid describes the ordinary phase of the ice named in the prompt.'
by[42]['componentReasons']['note_3']['EDITORIAL']='The note makes this phase-equilibrium distractor useful by explaining the closed-container boiling case; it does not imply that ordinary ice is a liquid-gas mixture.'
# #43 source justification now cites the literal full paragraph; update the top-level source description to its exact issue/claim.
by[43]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='The stem uses the source’s punctured-tire example verbatim in meaning, so recognition is direct. The three wrong choices contrast stillness, local concentration and reverse flow with the stated dispersal.'
# Check canonical card invariants and reason coverage.
for i,e in by.items():
 if 'card' in e:
  c=e['card'];assert c['id']==d['scope']['ids'][i-30] and c['difficulty']=='easy' and c['correctIndex']==d['scope']['keySlots'][i-30]
  assert len(c['answers'])==4 and len(e['componentReasons'])==8
  assert all(set(x)=={'SOURCE','EDITORIAL'} for x in e['componentReasons'].values())
b=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();P.write_bytes(b);print(len(b),hashlib.sha256(b).hexdigest())
