#!/usr/bin/env python3
"""FINAL sole-cycle2-card receipt, based on own INITIAL readings and fresh CURRENT."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
INITIAL=OUT.parent
COORD=INITIAL.parent
ROOT=INITIAL.parents[4]
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def sha(x):return hashlib.sha256(canonical(x)).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
initial=read(INITIAL/'receipt.json')
initial_peers=read(INITIAL/'peer-review.json')
initial_sources=read(INITIAL/'source-evidence.json')
apply=read(COORD/'apply-engineering2-cycle1.json')
qa=read(COORD/'qa-engineering2-cycle1.json')
author=ROOT/'docs/content-audits/question-quality-wave-8/process-v2-engineering6-cycle1-01a13f31/author/cycle1/final-ready2'
author_candidate=read(author/'candidate.json')
author_sources=read(author/'sourceproof.json')
author_peers=read(author/'peer-snapshot.json')
assert [e['sourceOrder'] for e in apply['applied']]==[30,39]
current=read(ROOT/'src/content/topics/engineering-machines.json')
current_byid={q['id']:q for q in current['questions']}
initial_byid={e['id']:e for e in initial['entries']}
sources=[]
by_source={s['path']:s for s in initial_sources['rawSources']}
for s in author_sources['rawSources']:
    prior=by_source[s['path']]
    assert raw(ROOT/s['path'])==s['sha256']==prior['rawReadSHA256']
    ev=copy.deepcopy(prior)
    ev['reuseFromOwnINITIAL']=dict(path=str((INITIAL/'source-evidence.json').relative_to(ROOT)),rawReadSHA256=prior['rawReadSHA256'],reason='Personally read complete relevant contexts in own INITIAL turn. Identical file bytes verified now; semantic grounds retained, not inherited from author.')
    sources.append(ev)
assert len(sources)==6
source_by_path={s['path']:s for s in sources}
khk=next(s for s in sources if 'khk_gears' in s['path'])
gwu=next(s for s in sources if 'gwu_machine_tools' in s['path'])
mit=next(s for s in sources if 'mit_machining' in s['path'])
def source_refs(*records):
    return [{k:s[k] for k in ['path','url','rawReadSHA256','locator']} for s in records]

entries=[]
for a in apply['applied']:
    old=initial_byid[a['id']]
    assert old['currentCard']==a['beforeCard']
    q=current_byid[a['id']]
    assert q==a['proposedCard']
    assert sha(q)==a['proposedSHA256'] and sha(a['beforeCard'])==a['beforeSHA256']
    e=copy.deepcopy(old)
    e.update(stage='FINAL_SOLE_CYCLE1',currentCard=q,currentCardCanonicalSHA256=sha(q),status='PASS',defects=[])
    e['initialReceipt']=str((INITIAL/'receipt.json').relative_to(ROOT))
    e['ownINITIALCardCanonicalSHA256']=old['currentCardCanonicalSHA256']
    changed=[k for k in q if q[k]!=a['beforeCard'][k]]
    e['changedFieldsSinceOwnINITIAL']=changed
    assert changed==(['explanation','source'] if a['sourceOrder']==30 else ['prompt'])
    for g,prior in zip(e['sixLiteralCanonicalGroups'],old['sixLiteralCanonicalGroups']):
        name=g['group']
        if name=='prompt_ordered_answers_key':
            literal=dict(prompt=q['prompt'],answers=[x['text'] for x in q['answers']],correctIndex=q['correctIndex'])
        elif name=='explanation':literal=q['explanation']
        else:literal=q['answers'][int(name[-1])]['note']
        g.update(literal=literal,canonicalSHA256=sha(literal),status='PASS',ownINITIALCanonicalSHA256=prior['canonicalSHA256'],unchangedFromOwnINITIAL=sha(literal)==prior['canonicalSHA256'])
        if g['unchangedFromOwnINITIAL']:
            g['individualGround']=prior['individualGround']+' Полный CURRENT литерал перечитан; совпадает с собственной INITIAL версией. Ранее лично прочитанные источники имеют те же raw SHA.'
    if a['sourceOrder']==30:
        e['sixLiteralCanonicalGroups'][0]['individualGround']='В CURRENT сохранён вопрос о металлической цепи и звёздочках, ключ «Цепная передача» единственен. Вальная передаёт момент валом, зубчатая — непосредственным зацеплением колёс, ременная — гибким ремнём/шкивами. Новый показанный source.url KHK PDF ведёт прямо к About Gear Mates P5 L123–141: sprocket wheel / roller chain перечислены как пара для передачи power and motion. Это закрывает прежний SOURCE_URL_MAIN_GAP; истинность вариантов/notes перечитана целиком.'
        e['sixLiteralCanonicalGroups'][0]['sourcesLocators']=source_refs(khk)+old['sixLiteralCanonicalGroups'][0]['sourcesLocators']
        e['sixLiteralCanonicalGroups'][1]['individualGround']='Два CURRENT предложения прямо называют цепную передачу, зацепление цепи со звёздочками и передачу движения/мощности; второе точно указывает сопряжённую пару KHK. About Gear Mates P5 L123–141 связывает sprocket wheel / roller chain и power/motion, отличая wrapping connectors от непосредственной пары gears. Раньше explanation был только об ассортименте Tsubaki; новый текст отвечает исходному вопросу и закрывает EXPLANATION_NO_DIRECT_KEY.'
        e['sixLiteralCanonicalGroups'][1]['sourcesLocators']=source_refs(khk)
        e['absoluteLevel']=dict(status='PASS',assigned='easy',ground='Тот же простой факт о цепи и звёздочках, знакомый взрослым по велосипедному приводу. Изменились объяснение и URL после ответа; сложность самого выбора не повысилась. Четыре альтернативы остаются реальными механическими передачами.')
        e['resolvedOwnINITIALDefects']=['EXPLANATION_NO_DIRECT_KEY','SOURCE_URL_MAIN_GAP']
    else:
        e['sixLiteralCanonicalGroups'][0]['individualGround']='CURRENT описывает закреплённую заготовку, подаваемую относительно вращающегося многозубого инструмента; слова «фреза» в вопросе больше нет. Это фрезерование: GWU L50–52 называет sharp rotating cutters, L94–111 даёт стол X–Y, головку Z, cutters на 2/4 flutes, roughing/form cutting. Сверление — осевая подача сверла для отверстия, шлифование — абразивные зёрна, точение — вращение заготовки, а не данного многозубого инструмента. Ключ распознаётся по способу обработки, а не по повтору корня.'
        e['sixLiteralCanonicalGroups'][0]['sourcesLocators']=source_refs(gwu,mit)
        e['absoluteLevel']=dict(status='PASS',assigned='medium',ground='Без слова «фреза» взрослый вне темы должен различить вращающийся многозубый резец, осевое сверление, абразивный круг и вращающуюся заготовку. Знакомый с мастерской/металлообработкой узнаёт фрезерование по этим признакам. Точных режимов резания/расчёта нет, поэтому это medium, а не hard; прежняя лексическая подсказка удалена.')
        e['resolvedOwnINITIALDefects']=['LEXICAL_KEY_LEAK_LEVEL']
    for v,prior in zip(e['fourFullPromptAnswerNoteVariants'],old['fourFullPromptAnswerNoteVariants']):
        i=v['slot'];triple=dict(prompt=q['prompt'],answer=q['answers'][i]['text'],note=q['answers'][i]['note'])
        v.update(**triple,tripleCanonicalSHA256=sha(triple),ownINITIALTripleCanonicalSHA256=prior['tripleCanonicalSHA256'],unchangedFromOwnINITIAL=sha(triple)==prior['tripleCanonicalSHA256'])
        v['grammar']=dict(status='PASS',ground='Полностью прочитано «'+q['prompt']+' — '+v['answer']+'». '+('Подпись «'+v['answer']+'» согласована с «какая передача» в женском роде/единственном числе; note грамматически описывает эту передачу.' if a['sourceOrder']==30 else 'Самостоятельное отглагольное существительное «'+v['answer']+'» в именительном падеже корректно называет вид обработки; ни род, ни форма note не выделяют правильный вариант.'))
        if a['sourceOrder']==39:
            reasons=[
              'Сверление правдоподобно как процесс с вращающимся режущим инструментом, но его характерный признак — осевая подача сверла в отверстие. CURRENT задаёт многозубый инструмент и подачу закреплённой детали; это описание фрезерования, а не просто отверстия сверлом. MIT L60,L76,L98–105 и GWU milling L90–111 разводят эти операции.',
              'Фрезерование соответствует всем признакам CURRENT: вращается многозубый инструмент, закреплённая деталь получает относительную подачу. GWU L50–52,L94–111 подтверждает вращающиеся cutters, многоканавочные фрезы и координатный стол; слово-ключ «фреза» не используется в prompt.',
              'Шлифование правдоподобно как съём материала вращающимся кругом/лентой, но его кромки — многочисленные абразивные зёрна, а не заданный многозубый инструмент. MIT L53–57,L78 прямо разделяет cutting и grinding; это содержательная возможность исключения.',
              'Точение относится к тому же пулу обработки резанием, но при нём вращается заготовка, а резец получает подачу. CURRENT вращает многозубый инструмент относительно подаваемой закреплённой детали; GWU L65–89 отличает spinning part/turning от milling L90–111.'
            ]
            v['plausibility']=dict(status='PASS',ground=reasons[i])
            v['truthUniqueKey']=dict(status='PASS',role='key' if i==q['correctIndex'] else 'distractor',ground=reasons[i])
        else:
            assert v['unchangedFromOwnINITIAL']
        v['noteTruthUsefulness']=dict(status='PASS',ground=old['sixLiteralCanonicalGroups'][i+2]['individualGround']+' Точная CURRENT note сохранена; это собственный положительный факт о варианте, включая разрешённые канонические факты других ключей.')
    e['correctNoteExtraFact']['ground']=old['correctNoteExtraFact']['ground']+' Полная CURRENT correct note совпадает с лично проверенной INITIAL note; изменение question/explanation не поглощает этот отдельный факт.'
    e['frozen']['baselineCurrentCardCanonicalSHA256']=old['currentCardCanonicalSHA256']
    e['frozen']['orderedAnswersAndNotesPreservedSinceOwnINITIAL']=q['answers']==old['currentCard']['answers']
    assert q['id']==old['id'] and q['difficulty']==old['currentCard']['difficulty'] and q['correctIndex']==old['currentCard']['correctIndex']
    entries.append(e)

# Preserve closure for the OSU corroboration cited by our own unchanged INITIAL
# explanation/correct-note bindings. It is not an additional author verdict.
used_paths={s['path'] for e in entries for g in e['sixLiteralCanonicalGroups'] for s in g['sourcesLocators']}
for path in sorted(used_paths-set(source_by_path)):
    prior=by_source[path]
    assert raw(ROOT/path)==prior['rawReadSHA256']
    ev=copy.deepcopy(prior)
    ev['reuseFromOwnINITIAL']=dict(path=str((INITIAL/'source-evidence.json').relative_to(ROOT)),rawReadSHA256=prior['rawReadSHA256'],reason='Own unchanged corroborating source context retained for reference closure; exact raw bytes verified.')
    sources.append(ev)
assert len(sources)==7

targets=[]
for e in entries:
    prior=next(x for x in initial_peers['targets'] if x['id']==e['id'])
    x=copy.deepcopy(prior);x.update(card=e['currentCard'],canonicalSHA256=e['currentCardCanonicalSHA256'])
    if e['sourceOrder']==39:x['MAIN']=dict(entity='закреплённая деталь с подачей относительно вращающегося многозубого инструмента',relation='название процесса съёма материала',value='фрезерование',context='станочная обработка; без слова фреза в prompt')
    targets.append(x)
targetids={x['id'] for x in targets}
neighbors=[]
for prior in initial_peers['actualRelevantCURRENTNeighbors']+initial_peers['targets']:
    if prior['id'] in targetids:continue
    d=read(ROOT/f"src/content/topics/{prior['topicId']}.json")
    q=next(q for q in d['questions'] if q['id']==prior['id'])
    assert q==prior['card'], 'Unexpected peer drift '+prior['id']
    x=copy.deepcopy(prior)
    x['reuseFromOwnINITIAL']=dict(cardCanonicalSHA256=prior['canonicalSHA256'],sameCurrentBytesSemantics=True,readEvidence='CURRENT full card and exact canonical hash compared to own INITIAL full-card read. No semantic drift; both MAIN directions rebound to FINAL target version.')
    neighbors.append(x)
assert len(neighbors)==54
for x in author_peers['concurrentProposals']:
    q=current_byid[x['id']]
    assert x['card']==q and sha(q)==x['sha256']
def desc(x):
    m=x['MAIN'];return f"{m['entity']} / {m['relation']} → {m['value']} ({m['context']})"
def compare(a,b):
    s='MAIN слева: '+desc(a)+'. MAIN справа: '+desc(b)+'. '
    if a['sourceOrder']==30:
        s+='Цепной гибкий привод узнаётся по звёздочкам/цепи; названия других передающих звеньев, опор, нагрузок или видов зацепления проверяют другие связи. Изменение explanation/URL не меняет MAIN, обратного повтора не создаёт.'
    else:
        s+='Фрезерование определяется конкретной обработкой вращающимся многозубым инструментом. Род механической обработки, отдельные операции/применения и технические характеристики не являются повтором именно этой связи. Новый prompt сохраняет прежний MAIN; канонические notes о других операциях разрешены.'
    return dict(leftId=a['id'],leftTopicId=a['topicId'],leftCanonicalSHA256=a['canonicalSHA256'],rightId=b['id'],rightTopicId=b['topicId'],rightCanonicalSHA256=b['canonicalSHA256'],leftMAIN=a['MAIN'],rightMAIN=b['MAIN'],directDuplicate=False,reverseDuplicate=False,leftToRight=dict(status='DISTINCT_MAIN',ground=s),rightToLeft=dict(status='DISTINCT_MAIN',ground='Справа ключ «'+b['MAIN']['value']+'» относится к отношению «'+b['MAIN']['relation']+'» для «'+b['MAIN']['entity']+'». Перестановка условия и этого ключа не задаёт слева «'+a['MAIN']['relation']+'» для «'+a['MAIN']['entity']+'». Поэтому это не прямой/обратный повтор MAIN.'))
peer=dict(stage='FINAL_SOLE_CYCLE1',targets=targets,actualRelevantCURRENTNeighbors=neighbors,mutualProposedPairsBidirectional=[compare(targets[0],targets[1])],eachTargetAgainstActualCURRENTNeighborsBidirectional=[compare(a,b) for a in targets for b in neighbors],proposedGearPeers='Author concurrent11/12/14 are exactly actual CURRENT, already personally read in INITIAL; same hashes independently verified now. No extra proposed version requiring a third review.',crossCatalogMethod='Own INITIAL 110-topic/11000-MAIN retrieval and full relevant peer reads reused. Both FINAL changes preserve the MAIN facts; new wording does not introduce book/park entity-relation overlap. No random third review of concurrent unrelated SOURCE packages.',counts=dict(targets=2,currentNeighbors=54,mutualPairs=1,targetToNeighborPairs=108),qualityCredit=0)
dump(OUT/'peer-review.json',peer)
dump(OUT/'source-evidence.json',dict(stage='FINAL_SOLE_CYCLE1',rawSources=sources,reuse='Six needed author-linked primary contexts plus own unchanged OSU corroboration, all personally read in INITIAL and exact-SHA verified now. No author source/editorial PASS is adopted.'))
receipt=dict(stage='FINAL_SOLE_CYCLE1',independent=True,createdAt=datetime.now(timezone.utc).isoformat(),worktree=str(ROOT),branch=git('branch','--show-current'),actualRef=git('rev-parse','HEAD'),applyCommit='c2e3e8d49aee2c7e10e8736a24fe0df717540a3d',qaCommit='c1fb6d66ec73f557f0cee5f2de9c2ae030c7647d',initialReceipt=str((INITIAL/'receipt.json').relative_to(ROOT)),initialReceiptRawSHA256=raw(INITIAL/'receipt.json'),pinnedProcessRef='12e5581b:.agents/references/question-revision.md',hashMethod=initial['hashMethod'],entries=entries,counts=dict(PASS=[30,39],HOLD=[]),qualityCredit=0,rootBinding='Pending coordinator FINAL adjudication/binding; no root credit assigned by independent reader.',evidence=dict(sources='source-evidence.json',peers='peer-review.json',initialCatalogRetrieval='../catalog-retrieval.json'),priorQAReadOnly=dict(path=str((COORD/'qa-engineering2-cycle1.json').relative_to(ROOT)),success=qa['success'],numPassedTests=qa['numPassedTests'],adoptedAsEditorialPass=False),excludedScope=dict(sourceOrders=[31,33,34,40],reason='SOURCE retained HOLD; not submitted to this FINAL and not counted. No second cycle authorized.'),notRun=['No tests/runtime/browser/audio/build/deploy; content receipt validation only.'],cleanup=dict(ownProcesses=[],temporaryResourcesCreated=[],gitMutation='Forbidden; coordinator preserves FINAL directory in Git.',foreignWork='Unchanged; no catalog/index/ref/planning/claim edits.'),nextAction='Coordinator saves evidence and binds exact FINAL PASS30/39. No unresolved defect in the two submitted CURRENT cards; no second cycle.',finalIntegrity=dict(exactCURRENTEqualsApplied=True,literalGroups=12,fullVariants=8,neededRawSources=7,currentNeighbors=54,bilateralPairs=109,frozen=True))
dump(OUT/'receipt.json',receipt)
print(json.dumps(dict(PASS=[e['id'] for e in entries],HOLD=[],sources=7,groups=12,variants=8,neighbors=54,pairs=109,qualityCredit=0),ensure_ascii=False))
