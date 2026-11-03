import json, pathlib, hashlib, base64, copy
from pypdf import PdfReader
root=pathlib.Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036')
src=root/'author-original-edition2.json'
out=root/'author-original-edition3.json'
d=json.loads(src.read_bytes())
# Keep both earlier editions immutable; this is a separate author proposal.
d['edition']=3
d['parentArtifact']={'path':str(src),'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
d['authorNotes']={**d.get('authorNotes',{}),'scopeStatus':'20 source proposals, no primary-source holds; all remain unqualified until independent review.','revision':'edition3: repaired exact-field explanations/reasons; added typed literal UTF-8 bindings and source locators; incorporated complete official raw captures for #40 friction and #41 inertia; preserved all frozen IDs, key slots, easy classifications and source provenance. Updated scope to 20 source proposals with zero remaining primary-source holds; independent qualification is still pending.'}
# Add a direct BIPM full-page extract for the exact gram-prefix rule used in #30.
pdf=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/physics-force-si-unit.pdf')
pdfbytes=pdf.read_bytes(); reader=PdfReader(str(pdf))
def page_context(pdf_page, label):
    text=reader.pages[pdf_page-1].extract_text() or ''
    # Include the full extracted page. PDF physical page 146 has printed page 144.
    return {'binding':{'bytes':len(pdfbytes),'path':str(pdf),'sha256':hashlib.sha256(pdfbytes).hexdigest()},'extraction':'pypdf full-page text extraction; PDF page and printed page retained','kind':'pdf_page_full_text','literalExtractedText':text,'pdfPage':pdf_page,'printedPage':pdf_page-2,'source':'BIPM SI Brochure, 9th edition'}
# Add pages that support the current prompts/notes more closely than nearby-page context.
for pno in [133,134,140,146]:
    found=next((x for x in d['primaryContexts'] if x.get('kind')=='pdf_page_full_text' and x.get('pdfPage')==pno),None)
    if not found: d['primaryContexts'].append(page_context(pno,'BIPM'))
# Incorporate already captured, range-assembled official OpenStax pages #40 and #41.
caproot=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13854/capture-only/official-alternatives-54')
from html.parser import HTMLParser
from html import unescape
class TextOnly(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data):
        if data.strip(): self.parts.append(data.strip())
def innertext(fragment):
    p=TextOnly(); p.feed(fragment); return ' '.join(' '.join(p.parts).split())
def add_html_capture(name,url,source,selectors):
    folder=caproot/name; body=folder/'assembled.body'; data=body.read_bytes(); html=data.decode('utf-8','replace')
    manifest=json.loads((folder/'range-manifest.json').read_text())
    selected=[]
    import re
    for tag,element in selectors:
        pattern=rf'<{tag}\b[^>]*\bid=["\']{re.escape(element)}["\'][^>]*>.*?</{tag}>'
        m=re.search(pattern,html,re.I|re.S)
        if not m: raise RuntimeError(f'missing raw element {tag}#{element} in {name}')
        selected.append({'elementId':element,'tag':tag,'literalText':innertext(m.group(0))})
    ctx={'kind':'captured_full_html_claim_paragraphs','source':source,'url':url,'pageTitle':source,'fullEntityBinding':{'path':str(body),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'strongETag':manifest['strongETag']},'selectedFullParagraphs':selected}
    d['primaryContexts'].append(ctx)
    prov={'assembledEntity':{'kind':'captured_full_html_claim_paragraphs','source':source,'url':url,'pageTitle':source,'fullEntityBinding':ctx['fullEntityBinding'],'selectedFullParagraphs':selected},'captureManifest':{'path':str(folder/'range-manifest.json'),'bytes':(folder/'range-manifest.json').stat().st_size,'sha256':hashlib.sha256((folder/'range-manifest.json').read_bytes()).hexdigest(),'status':manifest['status'],'rangeRecordCount':manifest['rangeRecordCount'],'entityBytes':manifest['entityBytes'],'assembledSHA256':manifest['assembledSHA256'],'strongETag':manifest['strongETag']},'initialManifest':{'path':str(folder/'initial-manifest.json'),'bytes':(folder/'initial-manifest.json').stat().st_size,'sha256':hashlib.sha256((folder/'initial-manifest.json').read_bytes()).hexdigest()},'headHeaders':{'path':str(folder/'head.headers'),'bytes':(folder/'head.headers').stat().st_size,'sha256':hashlib.sha256((folder/'head.headers').read_bytes()).hexdigest()}}
    d.setdefault('captureProvenance',[]).append(prov)
    bindfiles=[body,folder/'range-manifest.json',folder/'initial-manifest.json',folder/'head.headers']
    for fn in ['response.headers','head-manifest.json']:
        if (folder/fn).exists(): bindfiles.append(folder/fn)
    for recpath in json.loads((folder/'range-manifest.json').read_text())['rangeRecords']:
        rec=json.loads(pathlib.Path(recpath).read_text())
        recdir=folder/'ranges'; basename=pathlib.Path(recpath).name
        for suffix in ['.body','.headers','.record.json']:
            candidate=recdir/(basename[:-len('.record.json')]+suffix)
            if candidate.exists(): bindfiles.append(candidate)
    for f in bindfiles:
        b=f.read_bytes(); d['evidenceBindings'].append({'path':str(f),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'gitBlobSha1':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()})
    return ctx
ctx40=add_html_capture('physics-40-friction','https://openstax.org/books/university-physics-volume-1/pages/6-2-friction','OpenStax University Physics Volume 1 §6.2 Friction',[('p','fs-id1165037201472'),('p','fs-id1165038379266')])
ctx41=add_html_capture('physics-41-inertia','https://openstax.org/books/physics/pages/4-2-newtons-first-law-of-motion-inertia','OpenStax Physics §4.2 Newton’s First Law of Motion: Inertia',[('p','fs-idp3596416'),('ol','fs-idm15224208')])
# Give every source context a stable identifier in this edition.
for i,c in enumerate(d['primaryContexts']): c['contextId']=f'ctx-{i:03d}'
# IDs for context refs by index in the edition 2 list, computed after additions by source identity.
def find_ctx(pred):
    return [c for c in d['primaryContexts'] if pred(c)]
def by_element(element, filetail=None):
    return find_ctx(lambda c:c.get('elementId')==element and (not filetail or filetail in c.get('binding',{}).get('path','')))
def by_pdf(pages): return find_ctx(lambda c:c.get('kind')=='pdf_page_full_text' and c.get('pdfPage') in pages)
def by_kind(kind, token=None): return find_ctx(lambda c:c.get('kind')==kind and (token is None or token.lower() in json.dumps(c,ensure_ascii=False).lower()))
# Source context coverage per card, with typed locator records preserved for exact groups.
context_for={
30: by_pdf([132,146]),31:by_pdf([132,133]),32:by_pdf([133]),33:by_pdf([134]),34:by_pdf([140]),35:by_pdf([140]),36:by_pdf([140]),
37:by_element('fs-idm15080864'),38:by_element('fs-id1167065911660'),39:by_kind('captured_full_html_claim_paragraphs','16.1 Reflection'),
42:by_element('import-auto-id1848208'),43:by_kind('captured_full_html_claim_paragraphs','12.3')+by_kind('full-capture-claim-paragraph','12.3'),
44:by_element('import-auto-id1848208'),45:by_element('fs-id1167065809902')+by_element('fs-id1167065854785'),
46:by_element('import-auto-id2931325'),47:by_element('import-auto-id2446845')+by_element('import-auto-id2691415'),
48:by_kind('captured_full_html_claim_paragraphs','9.3'),49:by_kind('captured_full_html_claim_paragraphs','14.2')}
context_for[40]=[ctx40]
context_for[41]=[ctx41]
context_for[42]+=by_kind('cnxml-full-element-context','Phase Changes')
context_for[44]+=by_kind('cnxml-full-element-context','Phase Changes')
# Remove duplicate context object refs while retaining order.
for i,v in list(context_for.items()):
 seen=set(); context_for[i]=[x for x in v if not (x['contextId'] in seen or seen.add(x['contextId']))]
# Card corrections constrained to the frozen topic/key slots.
entries={e['index']:e for e in d['entries']}
def set_note(ix,n,text): entries[ix]['card']['answers'][n]['note']=text
def set_answer(ix,n,text): entries[ix]['card']['answers'][n]['text']=text
# Resolve both previously held cards now that complete official primary captures are bound.
entries[40]['status']='PROPOSED_SOURCE'
entries[40]['card']={'id':'physics-friction-effect','prompt':'Как направлена сила кинетического трения относительно скольжения соприкасающихся поверхностей?','answers':[
 {'text':'В направлении относительного скольжения','note':'Это направление движения поверхностей друг относительно друга.'},
 {'text':'Перпендикулярно контактным поверхностям','note':'Кинетическое трение параллельно контактным поверхностям.'},
 {'text':'Против направления относительного скольжения','note':'Сила кинетического трения направлена против относительного движения.'},
 {'text':'Вдоль нормальной реакции опоры','note':'Нормальная сила перпендикулярна поверхности, а трение направлено вдоль неё.'}],
 'correctIndex':2,'difficulty':'easy','explanation':'Кинетическое трение возникает, когда соприкасающиеся поверхности скользят относительно друг друга. Оно направлено против этого относительного движения.','source':{'title':'OpenStax University Physics Volume 1 §6.2 Friction, paragraph fs-id1165037201472','url':'https://openstax.org/books/university-physics-volume-1/pages/6-2-friction','verifiedAt':'2026-10-14'}}
entries[40]['componentReasons']={}
entries[41]['status']='PROPOSED_SOURCE'
entries[41]['card']={'id':'physics-inertia','prompt':'Как ведёт себя тело, если равнодействующая внешних сил равна нулю?','answers':[
 {'text':'Его скорость обязательно возрастает','note':'Ускорение требует ненулевой равнодействующей силы.'},
 {'text':'Оно непрерывно меняет направление движения','note':'При нулевой равнодействующей скорость тела не меняется.'},
 {'text':'Оно остаётся в покое или движется равномерно и прямолинейно','note':'При нулевой равнодействующей тело сохраняет покой или постоянную скорость.'},
 {'text':'Оно само по себе замедляется и останавливается','note':'Остановка движущегося тела требует внешней силы, например трения.'}],
 'correctIndex':2,'difficulty':'easy','explanation':'При нулевой равнодействующей внешних сил тело сохраняет состояние покоя или движется с постоянной скоростью по прямой. Это формулировка первого закона Ньютона; свойство сохранять состояние движения называют инерцией.','source':{'title':'OpenStax Physics §4.2 Newton’s First Law of Motion: Inertia, paragraph fs-idp3596416 and list fs-idm15224208','url':'https://openstax.org/books/physics/pages/4-2-newtons-first-law-of-motion-inertia','verifiedAt':'2026-10-14'}}
entries[41]['componentReasons']={}
# #30: kilogram is the base mass unit; prefixes for multiples/submultiples attach to gram.
entries[30]['card']['explanation']='Килограмм (kg) — единица массы СИ. Для кратных и дольных единиц приставку присоединяют к грамму: например, 10⁻⁶ kg записывают как миллиграмм (mg), а не микрокилограмм.'
# #38: remove duplicate attraction choices and make alternatives distinct and parallel.
for n,t in enumerate(['Притягиваются друг к другу','Отталкиваются друг от друга','Не взаимодействуют друг с другом','Действуют только при соприкосновении']): set_answer(38,n,t)
for n,t in enumerate([
'Разноимённые полюса притягиваются друг к другу.',
'Одноимённые полюса отталкиваются друг от друга.',
'Магнитные полюса оказывают силу и без соприкосновения.',
'Магнитные полюса взаимодействуют на расстоянии; соприкосновение не требуется.'
]): set_note(38,n,t)
# #42: remove inline source identifiers and add field-specific facts without tipping off the key.
for n,t in enumerate([
'При охлаждении водяной пар может перейти в жидкую воду.',
'При дальнейшем охлаждении жидкая вода может перейти в твёрдый лёд.',
'При обычных условиях лёд — твёрдая вода; повышение давления может изменить фазу.',
'При некоторых сочетаниях температуры и давления вода может существовать сразу в двух фазах.'
]): set_note(42,n,t)
# #43: retain only the direct punctured-tyre fact in §12.3; remove source-name cues.
entries[43]['card']['explanation']='После прокола воздух выходит из шины и рассеивается во все стороны. Этот пример иллюстрирует самопроизвольное рассеивание энергии и рост энтропии.'
for n,t in enumerate([
'Через отверстие воздух выходит наружу и смешивается с окружающей средой.',
'После выхода газ распространяется в окружающее пространство, а не собирается у прокола.',
'Рассеивание энергии связано с тем, что её становится труднее использовать для работы.',
'Чтобы воздух самопроизвольно вернулся, понадобилась бы обратная концентрация газа.'
]): set_note(43,n,t)
# #44: preserve the frozen water-freezing topic with an elementary, source-supported threshold.
entries[44]['card'].update({'prompt':'При какой температуре чистая вода замерзает при нормальном атмосферном давлении?','explanation':'При давлении 1 atm температура плавления льда и замерзания воды составляет 0 °C. При изменении давления фазовая граница может смещаться.','answers':[
 {'text':'100 °C','note':'При нормальном давлении это температура кипения воды.'},
 {'text':'−273,15 °C','note':'Это абсолютный ноль по шкале Цельсия, а не температура замерзания воды.'},
 {'text':'0 °C','note':'При давлении 1 atm это точка равновесия жидкой воды и льда.'},
 {'text':'20 °C','note':'При 1 atm эта температура выше границы плавления льда.'}
]})
# #46: stay on the closed-circuit concept, avoiding the drift-velocity interpretation ambiguity.
entries[46]['card'].update({'prompt':'Что необходимо для непрерывного тока через нагрузку в простой электрической цепи?','explanation':'Нужен замкнутый проводящий путь от одного вывода источника через нагрузку к другому выводу. Разрыв этого пути прекращает непрерывный ток.','answers':[
 {'text':'Разрыв провода между источником и нагрузкой','note':'Разрыв устраняет непрерывный путь для тока.'},
 {'text':'Изолирующий участок внутри цепи','note':'Изолятор не соединяет проводящие части цепи.'},
 {'text':'Только источник без соединительных проводов','note':'Источник сам по себе не образует замкнутый путь через нагрузку.'},
 {'text':'Замкнутый проводящий путь через источник и нагрузку','note':'Проводники соединяют нагрузку с обоими выводами источника и образуют замкнутый путь.'}
]})
# #47: balance answer length and avoid keyed option being uniquely elaborate.
for n,t in enumerate([
'Остаётся у электрона после его столкновения с решёткой',
'Переходит в упорядоченное движение свободных электронов',
'Передаётся атомам решётки и нагревает металл',
'Уходит в окружающую среду, не передаваясь атомам решётки'
]): set_answer(47,n,t)
for n,t in enumerate([
'Столкновения свободных электронов с атомами решётки передают энергию проводнику.',
'Средняя дрейфовая скорость описывает перенос заряда, а не исчезновение энергии.',
'При столкновениях энергия передаётся атомам и может повышать температуру.',
'Энергия передаётся проводнику, даже если видимого свечения нет.'
]): set_note(47,n,t)
# #48 correct note must describe the actual key text, not merely restate the question definition.
set_note(48,3,'У рычага силы действуют на разных плечах; больший выигрыш в силе требует большего перемещения точки приложения усилия.')
# #46 key stays in slot 3, #44 key stays in slot 2, and all other frozen key positions stay untouched.
# Rewrite paired reasons for the newly corrected exact fields.
def reason(ix,component,source,editorial):
    entries[ix]['componentReasons'][component]={'SOURCE':source,'EDITORIAL':editorial}
reason(30,'explanation','BIPM SI Brochure §2.3.1 names kilogram (kg) as the SI base unit of mass; §3 states prefixes for mass are attached to gram and gives 10⁻⁶ kg = milligram (mg), not microkilogram.','The first sentence answers the unit question directly. The second clarifies the prefix exception with the exact example stated in the BIPM text.')
reason(30,'sourceMetadata','The BIPM SI Brochure §2.3.1 lists kilogram (kg) as the mass base unit; §3 directly states the special gram-prefix rule and its milligram example.','The metadata points to the official brochure containing the exact unit definition and explanation used in the card.')
reason(32,'note_0','BIPM SI Brochure defines the metre from the fixed value of the speed of light in vacuum.','The note adds the current SI definition of the metre, rather than a decimal-conversion fact.')
reason(35,'note_1','BIPM Table 4 assigns the symbol J to the joule.','The note states the international unit symbol, as printed in the BIPM table.')
reason(36,'note_1','BIPM Table 4 states the hertz relation Hz = s⁻¹.','The note gives the unit relation, distinct from the stem’s question about the phenomena for which hertz is used.')
reason(37,'note_1','OpenStax Physics §4.4 states that the normal force is exerted by the surface and distinguishes it from the gravitational force; Newton’s third-law partner acts on the other body.','This note explains why the support force on the object is not the equal-and-opposite partner of Earth’s gravitational force on that same object.')
reason(39,'note_2','OpenStax Physics §16.1 defines both incidence and reflection angles relative to the normal to the reflecting surface.','The note describes the actual reference line for both angles.')
reason(39,'note_3','OpenStax §16.1 identifies the normal as perpendicular to the reflecting surface; the reflected ray is measured relative to that normal, not required to coincide with it.','This note corrects the specific misconception that the reflected ray must run along the normal.')
reason(38,'whole_prompt_all_four_ordered_answers_correctIndex_key','OpenStax Physics §20.1 states like magnetic poles repel and unlike poles attract; the four current choices distinguish attraction, repulsion, absence of interaction, and an alleged contact-triggered reversal.','The stem asks about like poles; the keyed choice states repulsion. The distractors are distinct misconceptions and none repeats the same attraction claim.')
for n,(s,e) in enumerate([
('OpenStax §20.1 states unlike north/south poles attract.','This choice expresses the contrasting unlike-pole rule.'),
('OpenStax §20.1 states like poles repel.','This is the direct rule for the two poles named in the stem.'),
('OpenStax §20.1 describes magnetic forces between poles without contact.','This rejects the misconception that poles must touch to interact.'),
('OpenStax §20.1 describes attraction and repulsion between magnetic poles without contact.','This note explains why contact is not required for the interaction.')]): reason(38,f'note_{n}',s,e)
reason(40,'whole_prompt_all_four_ordered_answers_correctIndex_key','OpenStax University Physics Volume 1 §6.2 states that kinetic friction between relatively sliding systems is parallel to the contact surface and opposes their relative motion.','The stem asks for that direction; four choices stay on one directional axis and the correct option remains in frozen slot 2.')
reason(40,'explanation','OpenStax §6.2 states that sliding friction is parallel to the contact surfaces and opposite the motion or attempted motion of the systems relative to one another; it names friction between moving systems kinetic friction.','The first sentence identifies when kinetic friction acts; the second states its direction relative to sliding.')
reason(40,'difficulty','The source states the direction of kinetic friction directly in one introductory paragraph.','This is a direct qualitative direction fact without force calculation or a free-body diagram.')
reason(40,'sourceMetadata','OpenStax University Physics Volume 1 §6.2 is the official source; its full capture is bound, and paragraph fs-id1165037201472 directly defines sliding/kinetic friction direction.','The source metadata names the exact section and paragraph that supports the prompt, key, and feedback.')
for n,(s,e) in enumerate([
('OpenStax §6.2 says friction opposes relative motion between contacting systems.','This choice captures the relative direction of sliding itself, which friction does not follow.'),
('OpenStax §6.2 says sliding friction is parallel to the contact surface.','This distinguishes a perpendicular normal direction from friction.'),
('OpenStax §6.2 directly says sliding friction opposes relative or attempted relative motion; moving contacting systems experience kinetic friction.','This note restates the source relationship that makes this the keyed direction.'),
('OpenStax §6.2 distinguishes surface-parallel friction from the normal direction.','This choice describes the support-force axis, not the friction direction.')]): reason(40,f'note_{n}',s,e)
reason(41,'whole_prompt_all_four_ordered_answers_correctIndex_key','OpenStax Physics §4.2 states that a body at rest remains at rest and a body in motion keeps constant velocity unless a net external force acts; constant velocity means straight-line motion at constant speed.','The stem gives the zero-resultant condition and all choices describe alternative motion outcomes; the keyed outcome is in frozen slot 2.')
reason(41,'explanation','OpenStax §4.2 states the first law for rest and motion, and defines constant velocity as straight-line motion at constant speed.','The first sentence gives both allowed states under zero net force. The second connects the law to inertia as the tendency to retain motion state.')
reason(41,'difficulty','The source gives the first-law rule directly, without calculation.','The item asks for one familiar qualitative rule and does not require force-vector arithmetic.')
reason(41,'sourceMetadata','OpenStax Physics §4.2 paragraph fs-idp3596416 introduces Newton’s first law, and ordered list fs-idm15224208 states its rest and constant-velocity clauses; the full raw page is bound.','The source metadata cites the exact official section and the two typed source elements used for the rule.')
for n,(s,e) in enumerate([
('OpenStax §4.2 says a moving body does not have to speed up when no net external force acts.','This rejects the misconception that motion automatically increases speed.'),
('OpenStax defines constant velocity in Newton’s first law as straight-line motion at constant speed.','This rejects turning as the zero-net-force behavior.'),
('OpenStax §4.2 states that a body at rest remains at rest and a moving body keeps constant velocity unless a net external force acts.','This note directly connects the zero-resultant condition to the keyed behavior.'),
('OpenStax explains that a net external force such as friction is needed to slow a moving body.','This rejects spontaneous stopping when the net force is zero.')]): reason(41,f'note_{n}',s,e)
for ix,items in {
42:[('OpenStax College Physics 2e §13.5 describes cooling gas condensing to liquid.','This explains the water-vapour distractor as a possible phase change.'),('The source contrasts solid, liquid, and gas phases and their properties.','This distinguishes liquid shape from its phase label.'),('OpenStax §13.5 describes water ice as solid and its pressure-dependent melting boundary.','The note adds a conditional pressure effect while the answer names ice’s ordinary phase.'),('OpenStax §13.5 describes coexistence of phase pairs on boundaries.','The note explains that two phases can coexist under a special condition.')],
43:[('OpenStax Physics §12.3 gives the punctured-tire example: air disperses in all directions.','The stem asks about that specific gas-release event.'),('The full §12.3 example says the air spreads in all directions rather than collecting near the puncture.','This note explains why localized accumulation is the wrong alternative.'),('OpenStax §12.3 relates entropy to energy dispersal and reduced availability for work.','This feedback adds the thermodynamic idea connected to the observed spreading.'),('The source presents spontaneous dispersal as the direction of the punctured-tire example.','This note describes the reverse-concentration misconception without naming the section in player-facing text.')],
44:[('OpenStax College Physics 2e §13.5 gives the water melting boundary as 0 °C at 1.00 atm.','The question tests the familiar freezing/melting threshold at ordinary pressure.'),('The source distinguishes low temperature from the phase boundary for water.','This identifies absolute zero as a different temperature concept.'),('OpenStax §13.5 gives 0 °C at 1.00 atm for the water solid-liquid boundary.','The note states the source condition directly.'),('OpenStax §13.5 gives the water solid-liquid boundary as 0 °C at 1.00 atm.','At the stated pressure, 20 °C lies above that freezing boundary.')],
46:[('OpenStax College Physics 2e §20.1 figure caption describes a closed path for current through wires, load, and battery terminals.','The question asks which circuit condition permits continuous current through the load.'),('The §20.1 figure identifies conducting wires as the elements supplying a closed path.','An insulating segment does not supply that conducting connection.'),('The same caption shows the battery connected by wires through the load to complete the path.','This distinguishes a source from the complete circuit needed for current.'),('OpenStax §20.1 caption explicitly calls the path for current flow closed and shows the load connected to both battery terminals.','This is the source-supported condition stated by the keyed choice.')],
47:[('OpenStax College Physics 2e §20.1 says collisions transfer energy from free electrons to atoms of the conductor.','The note states the collision transfer that resolves the stem.'),('OpenStax §20.1 says continuous power input is normally required to maintain current, with superconductors as an exception.','This adds the source’s steady-current energy requirement without confusing it with the collision transfer asked about.'),('The text says collisions transfer energy to the atoms, possibly raising temperature.','This is the direct thermal consequence of the collision transfer.'),('The text describes transfer into conductor atoms and possible heating.','The note rejects loss to surroundings as the described mechanism.')],
48:[('OpenStax Physics §9.3 describes effort and resistance forces acting at distances from a lever’s fulcrum.','The current key note now describes the lever-arm trade-off actually present in the answer explanation.'),('The section describes lever arms and mechanical advantage.','The note states how arm distances affect force and displacement.')]
}.items():
 for n,(s,e) in enumerate(items): reason(ix,f'note_{n}',s,e)
reason(48,'note_3','OpenStax Physics §9.3 describes effort and resistance forces acting at distances from a lever’s fulcrum.','The current key note now describes the lever-arm trade-off actually present in the answer explanation.')
# Rebuild component reasons for #44 and #46 composite/explanation after content replacement.
reason(44,'whole_prompt_all_four_ordered_answers_correctIndex_key','OpenStax College Physics 2e §13.5 states that water’s melting point is 0 °C at 1.00 atm; at this equilibrium boundary, freezing is the reverse phase change.','This returns the item to its frozen water-freezing topic and a direct elementary temperature fact. The four choices mix realistic phase-temperature and scale confusions while the keyed slot remains fixed.')
reason(44,'explanation','OpenStax College Physics 2e §13.5 identifies the water solid-liquid boundary at 0 °C and 1.00 atm and explains pressure-dependent melting.','The first sentence gives the asked threshold and pressure condition; the second supplies a source-backed boundary consequence.')
reason(44,'difficulty','OpenStax §13.5 gives the 0 °C water phase boundary directly.','This is direct recall of one familiar threshold, with no phase-diagram reading or calculation required.')
reason(44,'sourceMetadata','OpenStax College Physics 2e §13.5 states the water solid-liquid boundary at 0 °C and 1.00 atm; the exact paragraph is bound as a typed source context.','The metadata identifies the official section that supports the freezing threshold and pressure condition.')
reason(46,'whole_prompt_all_four_ordered_answers_correctIndex_key','OpenStax College Physics 2e §20.1 caption says conducting wires connect a load to both battery terminals to supply a closed path for current.','The question and all four options now share the same circuit-completion axis, and the keyed option remains in frozen slot 3.')
reason(46,'explanation','OpenStax §20.1 caption identifies a closed conducting path through battery, wires, and load as the path for current to flow.','The explanation names the necessary path and explains why a break stops continuous flow.')
reason(46,'difficulty','OpenStax §20.1 figure directly depicts a closed path from source through load and back.','Recognizing the basic condition for circuit current is direct, with no diagram analysis beyond reading the simple circuit or calculation.')
reason(46,'sourceMetadata','OpenStax College Physics 2e §20.1 figure caption import-auto-id2931325 says wires connect the load to the battery terminals to supply a closed path for current; the full CNXML capture and figure context are bound.','The metadata points to the official section and exact caption that supports the circuit requirement.')
for n,(s,e) in enumerate([
('OpenStax §20.1 figure caption says the wires must connect the load and battery terminals into a closed path.','A break in the wire interrupts the path.'),
('The same caption identifies conducting wires as the path for current through the load.','An insulating segment breaks that conducting path.'),
('OpenStax §20.1 depicts source, wires, and load together in the current path.','The source alone does not complete the path through the load.'),
('OpenStax §20.1 directly describes the required closed path connecting the battery terminals through the load.','This note gives the key condition and why it allows continuous current.')]): reason(46,f'note_{n}',s,e)
# Re-evaluate difficulty #44 as easy: simple standard freezing threshold, not a triple-point interpretation.
# Bind exact literals and per-field typed source locators.
def locator(c):
    k=c.get('kind')
    if k=='pdf_page_full_text': return {'type':k,'pdfPage':c.get('pdfPage'),'printedPage':c.get('printedPage'),'source':c.get('source'),'binding':c.get('binding')}
    if k in ('cnxml_element','cnxml-full-element-context','cnxml-element-and-media-alt','cnxml-full-element-context'):
        return {'type':k,'elementId':c.get('elementId'),'tag':c.get('tag'),'source':c.get('source'),'binding':c.get('binding')}
    if k=='captured_full_html_claim_paragraphs': return {'type':k,'url':c.get('url'),'source':c.get('source'),'fullEntityBinding':c.get('fullEntityBinding')}
    if k=='full-capture-claim-paragraph': return {'type':k,'claim':c.get('claim'),'source':c.get('source'),'fullEntityBinding':c.get('fullEntityBinding')}
    return {'type':k,'source':c.get('source'),'binding':c.get('binding') or c.get('fullEntityBinding')}
def literal(value):
    if isinstance(value,str): b=value.encode('utf-8'); kind='utf8-string'
    else: b=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'); kind='canonical-json-utf8'
    return {'encoding':kind,'utf8ByteLength':len(b),'utf8Base64':base64.b64encode(b).decode('ascii'),'sha256':hashlib.sha256(b).hexdigest()}
for ix,e in entries.items():
    if e['status']!='PROPOSED_SOURCE': continue
    card=e['card']; refs=context_for.get(ix,[])
    refobjs=[{'contextId':c['contextId'],'locator':locator(c)} for c in refs]
    content=[a['text'] for a in card['answers']]
    binds={
     'whole_prompt_all_four_ordered_answers_correctIndex_key': {'literal':literal({'prompt':card['prompt'],'orderedAnswerText':content,'correctIndex':card['correctIndex'],'keyText':content[card['correctIndex']]}),'sourceLocatorRefs':refobjs},
     'explanation':{'literal':literal(card['explanation']),'sourceLocatorRefs':refobjs},
     'difficulty':{'literal':literal(card['difficulty']),'sourceLocatorRefs':refobjs},
     'sourceMetadata':{'literal':literal(card['source']),'sourceLocatorRefs':refobjs}}
    for n,a in enumerate(card['answers']): binds[f'note_{n}']={'literal':literal(a['note']),'sourceLocatorRefs':refobjs}
    e['literalFieldBindings']=binds
# Keep two gaps explicit until their requested primary raw captures are provided.
d['sourceQualificationAudit']={**d.get('sourceQualificationAudit',{}),'authorStatus':'edition 3 author proposal; pending independent source/semantic/editorial qualification','explicitHolds':[],'literalBindingSchema':'Every proposed card binds each of the 8 reason groups to exact current literal UTF-8 preimages (base64, byte length, SHA-256) and typed primary source locator references.'}
d['readerAttestation']=None
# Preserve canonical form: UTF-8, ensure_ascii=False, sorted keys, compact separators, no LF.
raw=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
out.write_bytes(raw)
print(json.dumps({'path':str(out),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'proposed':sum(e['status']=='PROPOSED_SOURCE' for e in d['entries']),'holds':sum(e['status']=='HOLD_PRIMARY_GAP' for e in d['entries']),'contexts':len(d['primaryContexts'])},ensure_ascii=False))
