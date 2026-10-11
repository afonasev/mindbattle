# Авторская передача unresolved13

Ветка `codex/question-quality-wave-6`. Owned: только 13 ID manifest.json в src/content/topics/card-games.json и эта папка. Baseline e717b9f, точные исходные bytes — baseline-topic.json. Другие 87 карточек неизменны; ID/order/difficulty/correctIndex, 40/40/20, позиции 10/10/5 сохранены.

Автор `01a12ba6-cb18-7ad0-849f-b1a5baed8a00` фактически прочитал все 78 полей и относящиеся оригинальные разделы. `author13.json` — новый авторский кандидат 13 PASS / 78 PASS, **не сертификация**. Старые author23 и independent23 с 7 FIX_REQUIRED / 6 HOLD не изменены. Root зачёт и решение independent остаются за другими ролями.

Изменены семь notes: козырные A/10 теперь имеют свои места3/4; J/9 — дополнительный факт о некозырном порядке; обе справки красных троек включают условие выкладки и штраф без неё; три игрока ската получают разделение ролей; три карты Висконти — классификацию богословских добродетелей; vulnerability — происхождение самого термина из мемуаров. Три source обновлены (две Pokémon, одна Lorcana). Остальные3 из13 без literal-изменений, но все6 полей перечитаны.

Пилот5 сохранён и прошёл roundtrip **до** расширения. Затем `author13-roundtrip.json` проверил все13/78: ошибки0, созданных содержательных вердиктов скриптом0. Решения явно написаны автором в author.py и remaining-decisions.py; скрипт только сериализует записи и привязывает хеши. Сохранённый previous proof catalogue использован только как указатель на оригиналы/точные passages, не как PASS.

## Актуальность и тип доказательств

- Pokémon: текущий официальный Trainers Website /sg/rules/detail/ ссылается на Advanced Player’s Rulebook3.4. Сохранено полное документированное оригинальное извлечение 2230/2230 строк; исходные ответы инструмента и их hashes сохранены. Прочитаны A-05, battle/attack контекст A, D/E, Special Conditions F, setup G. Издание2025 не переименовано в2026: проверена действующая ссылка и нужные базовые инварианты. Западный MEG не удалось получить — challenge не используется как proof.
- Lorcana: текущий resources/QuickStart с датой2/19/26 ведёт по ITALIANO на Sussurri-nel-Pozzo. Полное извлечение447/447 строк; прочитаны Vincere и Il tuo calamaio с контекстом. Точные факты чернил и20lore совпадают с EnglishQuickStart, ещё прямо связанным с liveHowTo. Последний — corroboration, не единственный proof. АнглийскийCR недоступен из-за размера/таймаута; французскийCR датирован16октября, поэтому не используется как действующий11октября. Нет исторического year-scope обхода.
- LACMA note1: **TEXTproof**. Полный исходный Curatorial Notes прямо говорит no figural imagery / symbols and label-like inscriptions. Это не вывод по изображению. Actual-view не заявлен, fake visualquote отсутствует, partialimage исключён. `imageRule` применяется кIMAGEproof, которого здесь нет. Ранее зафиксированный visualHOLD сохранён; independent должен вынести новый вердикт, учитывая явное разрешение первичного кураторского текста.
- Magic актуальная ссылка ведёт наTXT25September2026; KonamiFAQ живьём подтверждает оба используемых утверждения. Подробности source-freshness.json. Ошибочные/неполные загрузки retained, явно помечены partial, не proofs.

## Проверки и продолжение

Typecheck exit0. Ограниченный content-набор9/11; два провала на чужом `middle-ages-cloister` (число предложений explanation), см. focused-content-tests.json. Прямой вызов неизменённого validateTopicPack для текущего card-games:100 вопросов, ошибок0. Full/browser/build/deploy не запускались. Review stamps и валидаторы не менялись.

Следующий шаг: координатор назначает отдельного independent reader на точные13 current hashes из preservation-check.json, все78полей, raw original sections и source-freshness. Особое внимание current official regional Pokémon rules, итальянскому current QuickStart и TEXTproof LACMA. После этого только координатор принимает/отклоняет авторские решения и обновляет root certification. Эта авторская сессия не редактирует planning/claim/ledger.
