"""Serialize the explicitly written independent decisions below; never infer verdicts.

Only hash/bind already-read cards, original sources and explicitly selected passages.
Run from repository root. No catalog or other reader's evidence is modified.
"""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / 'docs/content-audits/question-quality-wave-6'
OUT = Path(__file__).resolve().parent
IDENTITY = '01a12b98-18ee-7b73-bf14-b432d49a7df1'
assert os.environ['CODEX_THREAD_ID'] == IDENTITY

def canonical(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def sha(v):
    return hashlib.sha256(v).hexdigest()

def save(name, v):
    (OUT / name).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n')

SOURCES = {
    'how': ('Earthquakes — How Earthquakes Happen, USGS', 'https://pubs.usgs.gov/gip/earthq1/how.html'),
    'severity': ('The Severity of an Earthquake, USGS', 'https://pubs.usgs.gov/gip/earthq4/severity_text.html'),
    'inside': ('Inside the Earth — This Dynamic Earth, USGS', 'https://pubs.usgs.gov/gip/dynamic/inside.html'),
    'ground': ('Earthquake Processes and Effects — Ground Movements, USGS', 'https://earthquake.usgs.gov/research/eqproc/grdmotion.php'),
}

# Exact passages selected after reading the full visible text of all four originals.
# Whitespace only is collapsed in HTML passages; the validator records this mode.
PASSAGES = {
    'epicenter-definition': ('how', 'Main text, paragraph beginning The epicenter', "The epicenter of an earthquake is the point on the Earth's surface directly above the focus. The location of an earthquake is commonly described by the geographic position of its epicenter and by its focal depth."),
    'focus-depth': ('how', 'Main text, paragraph beginning The focal depth', "The focal depth of an earthquake is the depth from the Earth's surface to the region where an earthquake's energy originates (the focus )."),
    'focus-rupture': ('severity', 'Introductory text before The Richter Magnitude Scale', 'The area of the fault where the sudden rupture takes place is called the focus or hypocenter of the earthquake.'),
    'intensity-effects': ('severity', 'Introductory text, intensity versus magnitude', 'Intensity is based on the observed effects of ground shaking on people, buildings, and natural features. It varies from place to place within the disturbed region depending on the location of the observer with respect to the earthquake epicenter.'),
    'maximum-intensity': ('severity', 'The Modified Mercalli Intensity Scale, after isoseismal maps', 'The maximum observed intensity generally occurs near the epicenter.'),
    'displacements': ('ground', 'Ground Movements, first body paragraph below Hector Mine caption', 'Measureable permanent ground displacements are produced by shallow earthquakes of magnitude 5 and greater. These displacements are used by seismologists to understand the earthquake source in detail, such as the amount of slip and the type of underground fault which ruptured.'),
    'earth-layers': ('inside', 'Opening body paragraph', 'our planet is made up of three main layers: crust, mantle, and core.'),
    'crust-definition': ('inside', 'Opening body paragraph, crust description', 'The crust, the outermost layer, is rigid and very thin compared with the other two.'),
    'crust-properties': ('inside', 'Opening body paragraph, immediately after crust definition', "Beneath the oceans, the crust varies little in thickness, generally extending only to about 5 km. The thickness of the crust beneath continents is much more variable but averages about 30 km; under large mountain ranges, such as the Alps or the Sierra Nevada, however, the base of the crust can be as deep as 100 km. Like the shell of an egg, the Earth's crust is brittle and can break."),
    'mantle': ('inside', 'Body paragraph beginning Below the crust', 'Below the crust is the mantle, a dense, hot layer of semi-solid rock approximately 2,900 km thick.'),
    'core': ('inside', 'Body paragraph beginning At the center', "At the center of the Earth lies the core, which is nearly twice as dense as the mantle because its composition is metallic (iron-nickel alloy) rather than stony. Unlike the yolk of an egg, however, the Earth's core is actually made up of two distinct parts: a 2,200 km-thick liquid outer core and a 1,250 km-thick solid inner core. As the Earth rotates, the liquid outer core spins, creating the Earth's magnetic field."),
}

proofs = {}
for pid, (source, locator, passage) in PASSAGES.items():
    raw = OUT / 'raw' / (source + '.html')
    title, url = SOURCES[source]
    proofs[pid] = {
        'proofId': pid, 'sourceClass': 'primary institutional educational publication, USGS',
        'title': title, 'url': url, 'rawCapture': str(raw.relative_to(OUT)),
        'rawCaptureSha256': sha(raw.read_bytes()), 'captureFormat': 'html original bytes',
        'captureMethod': 'Independent curl HTTPS GET with certificate verification; HTTP 200 and hashes in fetch-log.json. Full visible source text read; independently fetched normalized visible text equals the already-read original.',
        'locator': {'textLocation': locator}, 'passage': passage, 'passageSha256': sha(passage.encode()),
    }

# Read independently from the complete original PDF, page 292, including context.
local_passage = 'The key factor in this regard is the nature of\nthe underlying geological materials, and the weaker those are, the more likely it is that there will be strong\nshaking. Areas underlain by strong solid bedrock tend to experience much less shaking than those underlain by\nunconsolidated river or lake sediments.'
pdf = BASE / 'geology-earth/resume-2026-10-11-fix2/sources/earle-physical-geology.pdf'
proofs['local-geology'] = {
    'proofId': 'local-geology', 'sourceClass': 'original author educational textbook hosted by university',
    'title': 'Stephen Earle — Physical Geology, Earthquake Intensity',
    'url': 'https://pita.ess.washington.edu/tswanson/wp-content/uploads/sites/9/2018/10/Physical-Geology_StephenEarle.pdf',
    'rawCapture': os.path.relpath(pdf, OUT), 'rawCaptureSha256': sha(pdf.read_bytes()),
    'captureFormat': 'pdf original bytes with pdfPage locator',
    'captureMethod': 'Existing complete tracked original independently opened with pypdf; physical PDF pages 292 and 293 read in full. Original retained at its existing path without duplicate download.',
    'locator': {'pdfPage': 292, 'section': 'Earthquake Intensity, final paragraph; printed page 283'},
    'passage': local_passage, 'passageSha256': sha(local_passage.encode()),
}

# These verdicts and analyses were written by this reader, not copied or inferred
# from an author receipt. Format automation cannot change them.
DECISIONS = [
    {
        'questionId': 'geology-earth-earthquake-epicenter', 'verdict': 'PASS',
        'editorialAnalysis': 'Полностью прочитаны текущие prompt/key, четыре варианта с notes и explanation. Ключ определяет эпицентр как точку поверхности над очагом. Вопрос спрашивает устойчивую связь, поэтому частное совпадение максимума интенсивности или смещения с эпицентром не создаёт второго определения. Все четыре варианта теперь законченные предложения о местоположении; прежнего несопоставимого одиночного варианта «разлом» нет. Все подстановки грамматичны: «Он» относится к эпицентру. Длина, пунктуация и форма не выделяют ключ. Easy оправдан общеобразовательной географией; тематическая связь прямая. Notes самостоятельны и относятся к своим утверждениям, correct-note добавляет координату и отдельное указание глубины. Два предложения explanation укладываются в лимит. В пределах двух назначенных карточек повтора нет; ранее сохранённые 165 не переаудированы. Решение по общему зачёту волны остаётся координатору.',
        'fields': [
            ('prompt-key', 'PASS', 'Буквальная связь «на поверхности прямо над очагом» точно соответствует directly above the focus. Вариант 0 описывает гипоцентр; 2 — наблюдаемое смещение, а 3 — максимум интенсивности, ни один не задаёт универсальную связь эпицентра с очагом. В частности generally near не означает определение. Разовая пространственная общность допустима и не служит причиной FIX.', ['epicenter-definition', 'focus-rupture', 'displacements', 'maximum-intensity']),
            ('note0', 'PASS', 'Источник называет зону начала внезапного разрыва focus or hypocenter, а второй абзац определяет её глубину относительно поверхности. Русская справка корректно связывает эти синонимы с подповерхностным началом землетрясения и объясняет именно вариант 0.', ['focus-rupture', 'focus-depth']),
            ('note1', 'PASS', 'USGS прямо говорит, что местоположение задают географическим положением эпицентра и глубиной очага. «Поверхностная координата» передаёт geographic position, «глубину ... отдельно» — второй независимый параметр. Это полезное дополнение к спрашиваемому «прямо над», а не пустое повторение ключа.', ['epicenter-definition']),
            ('note2', 'PASS', 'Оба предложения USGS подтверждают постоянные измеримые смещения при shallow earthquakes магнитудой 5 и выше и применение к источнику/типу разлома. «Мелких» здесь читается как неглубоких, не малых по магнитуде: порог магнитуды прямо указан. Фраза не утверждает, что смещения бывают только при M≥5; это частный положительный факт источника. Справка относится к измеренному смещению в варианте 2. Для ясности можно предпочесть «неглубоких», но фактического опровержения текущего текста нет.', ['displacements']),
            ('note3', 'PASS', 'Intensity — наблюдаемые эффекты сотрясения, различающиеся по месту. Generally near the epicenter подтверждает «часто около», а не обязательное совпадение; зависимость от грунтов поясняет ограничение «не всегда». Справка описывает интенсивность варианта 3, не приписывает ей определение эпицентра.', ['intensity-effects', 'maximum-intensity', 'local-geology']),
            ('explanation', 'PASS', 'Первая фраза точно связывает поверхностный эпицентр с очагом разрыва; придаточное «где начинается разрыв» относится к очагу. Вторая разделяет типичное расположение максимума интенсивности и влияние местных условий. USGS подтверждает generally near, оригинальный Earle — различную силу сотрясения на скале и рыхлых осадках. Это не утверждение о невозможности совпадения.', ['epicenter-definition', 'focus-rupture', 'maximum-intensity', 'local-geology']),
        ],
    },
    {
        'questionId': 'geology-earth-gypsum-plaster', 'verdict': 'FIX_REQUIRED',
        'editorialAnalysis': 'Все шесть текущих полей прочитаны заново и фактически верны; старый вопрос о гипсе не оценивался как текущий. Школьное знание внешнего основного слоя соответствует easy. Четыре названия оболочек грамматичны как последовательные именные подписи; правильная Земная кора не выделена длиной. Единственный правильный ответ подтверждён USGS. Но новый основной факт уже спрашивает geology-earth-earth-crust: «Как называется самый внешний твёрдый слой Земли?» с теми же четырьмя вариантами, порядком и correctIndex=1. Уточнение «из основных» не даёт нового факта. Это точная найденная причина разрешённого узкого чтения этой сохранённой карточки; её тексты/статус не изменялись. Новая карточка требует замены независимым easy-фактом с сохранением слота/квот. Все notes остаются фактически PASS; общего PASS нет из-за смыслового дубля.',
        'fields': [
            ('prompt-key', 'FIX_REQUIRED', 'Факт верен: crust, mantle, core названы основными слоями, а crust — outermost. Ни мантия, ни часть ядра не внешние. Однако это тот же проверяемый факт и тот же ключ, что в geology-earth-earth-crust; проверяемое знание не изменилось от замены слова «твёрдый» на «из основных». FIX относится к разнообразию, не к истинности и не к прежнему literal key «гипс».', ['earth-layers', 'crust-definition']),
            ('note0', 'PASS', 'Оригинал одновременно подтверждает положение мантии ниже коры, высокую температуру, плотность и мощность приблизительно 2900 км. Справка о мантии самостоятельна, не подменяет её свойствами коры.', ['mantle']),
            ('note1', 'PASS', 'Rigid подтверждает жёсткость, brittle and can break — хрупкость. Около 5 км под океанами против средней 30 км под континентами обосновывают осторожное «обычно тоньше». Это полезный дополнительный факт к внешнему положению коры и разрешённый рубрикой correct-note.', ['crust-definition', 'crust-properties']),
            ('note2', 'PASS', 'Источник характеризует ядро как металлическое (железо-никелевое), внешнюю часть как жидкую и описывает движение внешнего ядра при создании магнитного поля. Формулировка «участвует» осторожнее популярного упрощения spins, creating; не утверждает, что одного вращения достаточно. Все три части справки относятся к внешнему ядру.', ['core']),
            ('note3', 'PASS', 'Core at the center плюс solid inner core и liquid outer core обосновывают твёрдую центральную часть внутри жидкой внешней. Отношение вложенности следует из inner/outer в исходном описании структуры; это явный пространственный вывод, не выдуманная цитата.', ['core']),
            ('explanation', 'PASS', 'Два предложения: outermost/rigid/very thin описывают кору; Below the crust is the mantle и центральное ядро подтверждают порядок; liquid outer и solid inner подтверждают подразделение. Фактическое explanation верно, хотя повторяемый prompt/key не проходит gate разнообразия.', ['crust-definition', 'mantle', 'core']),
        ],
    },
]

topic = json.loads((ROOT / 'src/content/topics/geology-earth.json').read_text())
catalog = {c['id']: c for c in topic['questions']}
author = json.loads((BASE / 'geology-earth/resume-2026-10-11-fix2/author-receipt.json').read_text())
author_hashes = {c['questionId']: c['cardCanonicalSha256'] for c in author['cards']}
cards = []
index = []
for decision in DECISIONS:
    c = catalog[decision['questionId']]
    card_hash = sha(canonical(c))
    assert card_hash == author_hashes[c['id']], 'Current snapshot changed; stop and reread.'
    literals = {'prompt-key': canonical([c['prompt'], c['correctIndex'], c['answers'][c['correctIndex']]['text']]), 'explanation': c['explanation'].encode(), **{f'note{i}': a['note'].encode() for i, a in enumerate(c['answers'])}}
    fields = []
    for field, verdict, analysis, pids in decision['fields']:
        fields.append({'field': field, 'literalSha256': sha(literals[field]), 'verdict': verdict, 'substantiveRead': True, 'substantiveReadBy': IDENTITY, 'claimAnalysis': analysis, 'proofs': [proofs[p] for p in pids]})
        index.append({'questionId': c['id'], 'cardCanonicalSha256': card_hash, 'field': field, 'literalSha256': sha(literals[field]), 'role': 'independent', 'agentIdentity': IDENTITY, 'verdict': verdict, 'proofIds': pids})
    cards.append({'questionId': c['id'], 'cardCanonicalSha256': card_hash, 'verdict': decision['verdict'], 'editorialAnalysis': decision['editorialAnalysis'], 'fields': fields})

save('independent-receipt.json', {'schemaVersion': 1, 'role': 'independent', 'agentIdentity': 'CODEX_THREAD_ID:' + IDENTITY, 'readDate': '2026-10-11', 'scope': 'Two current cards from author commit 08acaf4; independent full six-field read. No wave/root certification.', 'readerMethod': 'Original full HTML visible text and PDF pages read before these manual decisions. Author verdicts used only as prior context; no PASS inheritance.', 'cards': cards})
save('proof-index.json', {'role': 'independent', 'agentIdentity': IDENTITY, 'bindings': index, 'proofs': proofs})
save('current-snapshot.json', {'cards': [catalog[x['questionId']] for x in DECISIONS], 'duplicateFindingOnly': catalog['geology-earth-earth-crust']})
save('qa-scope.json', {
    'baselineHead': '3d24a899d7ce741fa824f1da8c80897e24010e89',
    'requestedAuthorCommit': '08acaf4',
    'ownedPath': str(OUT.relative_to(ROOT)),
    'reason': 'Evidence-only independent review of exactly two current cards; no runtime or validator changes. Mechanical identity/passage roundtrip plus invariant checks are sufficient for this evidence slice; they do not certify factual PASS.',
    'commands': ['python3 docs/content-audits/question-quality-wave-6/verify-proof-format.py <owned>/independent-receipt.json --repo . --output <owned>/proof-validation.json', 'Targeted saved-snapshot/current-card/author hashes; ID/order/difficulty/correctIndex and quota comparison against baseline; git diff --check -- <owned>'],
    'notRun': ['full suite', 'npm run check', 'qa', 'test:browser', 'build', 'deploy', 'release', 'archive'],
    'newCertifiedCards': 0,
})
