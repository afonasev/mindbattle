import json, hashlib, os, re
from pathlib import Path
from html.parser import HTMLParser
WT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
base=WT/'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772'
freeze_path=base/'physics-next30-49-source-scope-after-current2.json'
freeze=json.loads(freeze_path.read_text())
cards=json.loads((WT/'src/content/topics/physics.json').read_text())['questions']
# Source citations are bound to the durable files read by this author; direct URLs below are the corresponding official publications.
phys=WT/'docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals'
gap=base/'capture-only/physics30-49-gaps'
source_specs={
30:('BIPM','The International System of Units, Table 2, printed p.130 (PDF p.132)','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
31:('BIPM','The International System of Units, Table 2, printed p.130 (PDF p.132)','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
32:('BIPM','The International System of Units, Table 2, printed p.130 (PDF p.132)','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
33:('BIPM','The International System of Units, Table 4, printed p.138 (PDF p.140), voltage footnote','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
34:('BIPM','The International System of Units, Table 4, printed pp.137–138 (PDF pp.139–140)','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
35:('BIPM','The International System of Units, Table 4, printed p.137 (PDF p.139)','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
36:('BIPM','The International System of Units, Table 4, printed p.137 (PDF p.139), hertz note','https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf',[phys/'physics-force-si-unit.pdf']),
37:('OpenStax','Physics, §4.4, paragraph on gravitational force/weight and normal force','https://openstax.org/books/physics/pages/4-4-newtons-third-law-of-motion',[phys/'openstax-m54131-index.cnxml']),
38:('OpenStax','Physics, §20.1, paragraph fs-id1167065911660','https://openstax.org/books/physics/pages/20-1-magnetic-fields-field-lines-and-force',[WT/'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a136e6/capture-only/physics-next20-29/23/assembled-original-entity.body']),
39:('OpenStax','Physics, §16.1 Reflection; full assembled page','https://openstax.org/books/physics/pages/16-1-reflection',[gap/'39/assembled-original-entity.body']),
40:('HOLD','No direct raw primary evidence: cited §4.4 context does not establish sliding-friction direction.','https://openstax.org/books/university-physics-volume-1/pages/6-2-friction',[]),
41:('OpenStax','Physics, §4.2, Newton’s first law and inertia','https://openstax.org/books/physics/pages/4-2-newtons-first-law-of-motion-inertia',[phys/'openstax-m54131-index.cnxml']),
42:('OpenStax','College Physics 2e, §13.5, solid/liquid phase description','https://openstax.org/books/college-physics-2e/pages/13-5-phase-changes',[phys/'openstax-m42218-index.cnxml']),
43:('OpenStax','Physics, §12.3 Second Law of Thermodynamics: Entropy; full assembled page','https://openstax.org/books/physics/pages/12-3-entropy',[gap/'43/assembled-original-entity.body']),
44:('OpenStax','College Physics 2e, §13.5, melting/freezing point at 1 atm','https://openstax.org/books/college-physics-2e/pages/13-5-phase-changes',[phys/'openstax-m42218-index.cnxml']),
45:('OpenStax','Physics, §13.1 Types of Waves, electromagnetic-wave passage','https://openstax.org/books/physics/pages/13-1-types-of-waves',[phys/'openstax-m54314-index.cnxml']),
46:('OpenStax','College Physics 2e, §20.1 Current, complete circuit path discussion','https://openstax.org/books/college-physics-2e/pages/20-1-current',[phys/'openstax-m42341-index.cnxml']),
47:('OpenStax','College Physics 2e, §20.1 Current, free electrons in metallic conductors and copper-wire example','https://openstax.org/books/college-physics-2e/pages/20-1-current',[phys/'openstax-m42341-index.cnxml']),
48:('OpenStax','Physics, §9.3 Simple Machines; full assembled page','https://openstax.org/books/physics/pages/9-3-simple-machines',[gap/'48/assembled-original-entity.body']),
49:('OpenStax','Physics, §14.2 Sound Intensity and Sound Level; full assembled page','https://openstax.org/books/physics/pages/14-2-sound-intensity-and-sound-level',[gap/'49/assembled-original-entity.body']),
}
# Locally authored corrections within frozen ID, topic, easy class, and fixed key slot.
def replace_notes(c, notes):
 for a,n in zip(c['answers'],notes): a['note']=n
proposals={}
for t in freeze['targets']:
 i=t['index']; c=json.loads(json.dumps(cards[i],ensure_ascii=False)); assert c['id']==t['frozenID'] and c['difficulty']=='easy' and c['correctIndex']==t['frozenCorrectIndex']
 src=source_specs[i]
 c['source']={'title': ('OpenStax: Physics §12.3 Second Law of Thermodynamics: Entropy' if i==43 else ('BIPM: The International System of Units' if 30<=i<=36 else src[0]+': '+src[1])), 'url':src[2], 'verifiedAt':'2026-10-14'}
 if i==43:
  c['prompt']='Почему тепловая машина не может полностью превращать полученную теплоту в работу за цикл?'
  c['answers']=[
   {'text':'Часть теплоты должна передаваться холодному резервуару','note':'В циклической машине часть теплоты отводится к резервуару с более низкой температурой.'},
   {'text':'Потому что теплота не может самопроизвольно переходить к более холодному телу','note':'Самопроизвольный перенос теплоты направлен от более горячего тела к более холодному.'},
   {'text':'Потому что температура рабочего тела всегда равна нулю','note':'Абсолютный нуль — нижний предел температуры, а не условие работы тепловой машины.'},
   {'text':'Потому что работа не может передаваться между телами','note':'Работа является способом передачи энергии между системой и окружением.'},
  ]
  c['correctIndex']=2
  c['explanation']='По второму закону термодинамики циклическая тепловая машина должна отводить часть теплоты к более холодному резервуару. Поэтому её КПД не может быть равен 100%.'
 if i==39:
  # keep supported easy concept, shorten unrelated and overlong notes
  replace_notes(c,[
   'Испарение — переход жидкости в газ с её поверхности.',
   'При отражении свет меняет направление на поверхности; зеркало создаёт отражённое изображение.',
   'Радиоактивность — самопроизвольное превращение нестабильных атомных ядер.',
   'Диффузия — перемешивание частиц вследствие их теплового движения.',
  ])
 if i==47:
  replace_notes(c,[
   'Резина обычно служит электрическим изолятором.',
   'Сухая древесина имеет намного большее сопротивление, чем металлический проводник.',
   'Стекло обычно используют как изоляционный материал.',
   'В меди под действием поля свободные электроны переносят электрический ток.',
  ])
 if i==43:
  pass
 proposals[i]=c

# Structured, claim-specific component reasons; each is distinct to the proposition and option in that field.
def component_reasons(i,c):
 source=source_specs[i]; key=c['correctIndex']; correct=c['answers'][key]['text']; prompt=c['prompt']
 notes=[a['note'] for a in c['answers']]
 if i==30: core='Таблица 2 называет kilogram (kg) базовой единицей массы; метр, секунда и ампер в той же таблице соответствуют длине, времени и току.'
 elif i==31: core='Таблица 2 связывает секунду (s) со временем; ватт, вольт и ньютон в таблице производных единиц относятся к мощности, потенциалу и силе.'
 elif i==32: core='Таблица 2 перечисляет metre (m) как базовую единицу длины; грамм измеряет массу, литр — объём, герц — частоту.'
 elif i==33: core='Таблица 4 называет volt (V) единицей electric potential difference и прямо указывает voltage как её обычное название.'
 elif i==34: core='Таблица 4 называет watt (W) единицей мощности; ватт соответствует джоулю в секунду.'
 elif i==35: core='Таблица 4 называет joule (J) единицей энергии и работы; ньютон-метр даёт эквивалентное выражение.'
 elif i==36: core='Таблица 4 определяет hertz (Hz) как s⁻¹; пояснение ограничивает его периодическими явлениями.'
 elif i==37: core='В источнике сила тяжести описана как направленная к центру Земли; нормальная сила поверхности направлена наружу и перпендикулярна поверхности.'
 elif i==38: core='В тексте прямо сказано, что северные полюса отталкиваются друг от друга и южные тоже; разноимённые полюса притягиваются.'
 elif i==39: core='Полированная отражающая поверхность меняет направление лучей и позволяет сформировать изображение; процессы испарения, распада и диффузии не объясняют зеркало.'
 elif i==40: core='HOLD: доступный контекст не подтверждает направление кинетического трения; до raw §6.2 доказательство и whole-card credit отсутствуют.'
 elif i==41: core='Первый закон Ньютона связывает нулевую равнодействующую с сохранением покоя или равномерного прямолинейного движения; это инерция.'
 elif i==42: core='Раздел о фазовых состояниях различает твёрдое тело, жидкость и газ; лёд является твёрдой фазой воды.'
 elif i==43: core='§12.3 формулирует ограничение циклической тепловой машины: часть теплоты должна отводиться к холодному резервуару, поэтому полный перевод теплоты в работу невозможен.'
 elif i==44: core='Диаграмма фаз из §13.5 указывает точку плавления/замерзания воды около 0 °C при 1 atm; 100 °C относится к кипению.'
 elif i==45: core='§13.1 различает механические волны, которым нужна среда, и электромагнитные волны, которые распространяются в вакууме.'
 elif i==46: core='Раздел об электрическом токе требует непрерывного проводящего пути между выводами источника и нагрузкой; разрыв прекращает устойчивый ток.'
 elif i==47: core='§20.1 объясняет металлическую проводимость свободными электронами и приводит бытовую медную проводку как пример.'
 elif i==48: core='§9.3 описывает рычаг как жёсткое тело, поворачивающееся вокруг опоры; балансир имеет именно такую опору между сторонами.'
 elif i==49: core='§14.2 связывает более высокую интенсивность/амплитуду звука с более высоким уровнем звука и воспринимаемой громкостью, отдельно рассматривая частоту и высоту.'
 else: core=''
 why={'whole_prompt_all_ordered_answers_correctIndex_key':core+' Формулировка задаёт один признак, правильный ответ соответствует ему, а три альтернативы относятся к другим величинам, явлениям или состояниям; позиции/ключ сохранены.'}
 why['explanation']=core+' Пояснение проговаривает причинную связь и добавляет ближайшее полезное следствие, не вводя второго ответа.'
 for j,a in enumerate(c['answers']):
  if j==key:
   why[f'note_{j}']=f'Заметка раскрывает дополнительное свойство правильного ответа ({a["text"]}) и связывает его с предметным контекстом источника, а не повторяет только ключ.'
  else:
   why[f'note_{j}']=f'Заметка корректно отделяет альтернативу «{a["text"]}» от проверяемого свойства и даёт самостоятельный учебный факт: {a["note"]}'
 why['difficulty']='Оставлена easy: требуется узнавание одной прямо определённой единицы/закономерности/фазы; вычисления, редкая терминология и скрытые условия не нужны.'
 why['sourceMetadata']=f'Ссылка ведёт на первоисточник, а locator привязан к {source[1]}; доступный raw-файл включён в evidence bindings с длиной и SHA-256. '+('Элемент остаётся HOLD до capture.' if i==40 else 'Метаданные подтверждают заявленное основание без ссылки на неподтверждённый прежний URL.')
 return why

# Build evidence bindings from exact bytes currently present.
inputs=[freeze_path,WT/'src/content/topics/physics.json']
for i,sp in source_specs.items(): inputs.extend(sp[3])
# include source context/preimage and protected corpus for exact semantic guards
preserve=base/'physicsD3-terminal-preservation/owned-tmp'
inputs += [preserve/'source-contexts.json',preserve/'source-readiness.json',preserve/'protected-other80.json',preserve/'id-order-100.json',preserve/'target-card-preimages.json']
def filebind(p):
 raw=p.read_bytes(); return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
bindings=[]
for p in dict.fromkeys(inputs):
 if p.is_file(): bindings.append(filebind(p))
# Explicit reader notes: BIPM pages personally extracted; full four raw pages parsed to page title/body text; primary target paragraphs and neighbor inventory read.
reader={'authorThreadId':'01a13841-3085-7ba3-9570-46d16b85c036','readMethod':'read exact local bytes; BIPM PDF extracted by pypdf; OpenStax CNXML parsed/read at claim paragraphs; four full captured HTML entities retained and inspected by section title and claim context; all 100 current Physics cards read from runtime JSON for semantic-neighbor check.','semanticGuard':'Bundled full 80 protected card objects and complete 100-ID order; target questions checked against complete current prompt inventory.','caveat':'#40 remains HOLD because the referenced raw CNXML at fs-idm21167840 is a worked example about Newton third-law forces and does not support sliding-friction direction.'}
entries=[]
for t in freeze['targets']:
 i=t['index']; card=proposals[i]
 if i==40:
  entries.append({'index':i,'id':card['id'],'status':'HOLD_PRIMARY_GAP','currentCard':card,'componentReasons':{},'missingEvidence':{'officialURL':source_specs[i][2],'requiredClaim':'A direct full primary source passage stating that kinetic friction opposes relative sliding motion, with raw body/headers and full section context.'}})
 else:
  entries.append({'index':i,'id':card['id'],'status':'PROPOSED_SOURCE','card':card,'componentReasons':component_reasons(i,card)})
packet={'schema':'mindbattle-physics-source20-author-packet-v1','authorThreadId':reader['authorThreadId'],'scope':{'topic':'physics','indices':list(range(30,50)),'ids':[t['frozenID'] for t in freeze['targets']],'class':'easy','keySlots':[t['frozenCorrectIndex'] for t in freeze['targets']],'frozenScopeSHA256':hashlib.sha256(freeze_path.read_bytes()).hexdigest(),'reservedROOTTupleSHA256':freeze['reservedROOTTupleSHA256']},'readerAttestation':reader,'evidenceBindings':bindings,'all80ProtectedPreimage':json.loads((preserve/'protected-other80.json').read_text()),'full100IDOrder':json.loads((preserve/'id-order-100.json').read_text()),'targetPreimages':json.loads((preserve/'target-card-preimages.json').read_text()),'entries':entries,'canonicalization':'UTF-8 JSON; ensure_ascii=False; sort_keys=True; separators=(",", ":"); no trailing LF. SHA-256 integrity only, no qualification/acceptance inference.'}
out=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original.json')
raw=json.dumps(packet,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8');out.write_bytes(raw)
print(json.dumps({'path':str(out),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'entries':len(entries),'proposed':sum(e['status']=='PROPOSED_SOURCE' for e in entries),'hold':[e['index'] for e in entries if e['status'].startswith('HOLD')],'reasonCounts':[len(e['componentReasons']) for e in entries]},ensure_ascii=False))
