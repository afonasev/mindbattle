# Explicit manual decisions after pilot5 roundtrip; executed in author.py namespace.
REVISIONS.update({
'card-games-history-tarocchi':{2:'Вера, Надежда и Любовь — три богословские добродетели, представленные на этих картах.'},
'card-games-history-poker':{3:'По воспоминаниям Вандербильта, слово «уязвимый» для этого состояния предложила пассажирка парохода Finland.'}
})
P['vulnerable-name']=copy.deepcopy(P['vanderbilt-penalties']);P['vulnerable-name']['passage']='Fortunately for us, a young lady on board the Finland solved that problem by suggesting the word vulnerable.'
def newproof(id,file,title,url,locator,passage):
 P[id]=dict(sourceClass='official publisher current-linked rules',title=title,url=url,rawCapture='sources/'+file,captureFormat='text original full fetched response or fully documented original extracted content',captureMethod='Complete original PDF web extraction, every line retained in order; source response hashes and transformation in same-prefix provenance.json. Direct partial PDF excluded. Selected passage read in full surrounding section by current author.',locator=locator,passage=passage)
PU='https://asia.pokemon-card.com/sg/wp-content/uploads/sites/6/2025/10/EN_advanced_manual-2025.pdf'
def poke(id,page,section,passage):newproof(id,'pokemon-asia-full-extracted.txt','Pokémon — Advanced Player’s Rulebook v3.4, current official link checked 2026-10-11',PU,dict(pdfPage=page,section=section),passage)
poke('current-evolve',9,'A-05 Evolution, web277–280','◆ When a Pokémon evolves, it keeps all attached cards (Energy, Pokémon Tools, Items) and all\ndamage counters it had before evolving.\n◆ When an Active Pokémon evolves, any Special Conditions or effects of attacks it had on it (such\nas “This Pokémon can’t attack during your next turn”) disappears after evolving.')
poke('current-special',14,'F Pokémon Checkup','Pokémon Checkup is the step after the end of each turn, where each player checks their\nPoisoned / Burned / Asleep / Paralyzed Pokémon’s Special Conditions, among other things.')
poke('current-prize-setup',15,'G Setting Up step7','7. Set your Prize cards\nPut the top 6 cards of your deck face down as your Prize cards without looking at them,\nplacing them in your Prize cards zone on the side opposite to your deck.')
poke('current-prize-win',13,'E Win and Loss','E. Win and Loss\n◆ Once a game has started, as soon as either player (or both) fulfil any of the conditions below,\nbegin the game resolution process:\n◆ The opponent has taken all of their Prize cards.\n◆ The player doesn’t have any Pokémon in play.\n◆ The player didn’t have any cards in their deck left to draw at the beginning of their turn.\n◆ How to resolve a game when both players fulfil loss conditions at the same time:')
poke('current-prize-ko',12,'D Knock Out step4','4. Both players take any Prize cards they get to take from those Knock Outs.')
poke('current-battle',4,'A Pokémon','Cards put into play to take part in battles. Players can use the attacks and Abilities written on Pokémon\ncards, among other actions such as having them Retreat, and Evolving them by playing specific\nPokémon with a different name from their hand.')
poke('current-opponent',5,'A-01 Attacks, example','During your opponent’s next turn, if the Defending Pokémon tries to use an attack, your\nopponent flips a coin. If tails, that attack doesn’t happen.')
LU='https://files.disneylorcana.com/Sussurri-nel-Pozzo_StarterDeckA_RULES_IT.pdf'
def lor(id,page,section,passage):newproof(id,'lorcana-it-full-extracted.txt','Ravensburger — Disney Lorcana Sussurri nel Pozzo, current Quick Start resource',LU,dict(pdfPage=page,section=section),passage)
lor('current-ink',8,'Il tuo calamaio, printed12','Il tuo calamaio è il luogo dove metti le tue carte inchiostro, a faccia\nin giù. Le carte nel calamaio vengono usate per pagare i costi, ad\nesempio per le carte che giochi dalla tua mano.')
lor('current-one-ink',8,'Il tuo calamaio, printed12','Ogni carta del tuo calamaio rappresenta 1 {I}, non\nimporta cosa ci sia sul fronte.')
lor('current-lore',2,'Vincere, printed1','Il tuo obiettivo è essere il primo giocatore a raggiungere 20\no più punti, chiamati leggenda.')
D['card-games-history-mamluk']=('PASS','Hard: исторические названия трёх рангов; Ober/Unter среди дистракторов позволяют тематическое сужение. Четыре прилагательных согласованы с «в какой колоде», ключ1. Curatorial Notes прочитан как первичный авторский музейный ТЕКСТ. note1 не основан на рисунке и не заявлен VISUAL OBSERVATION. Старый visual HOLD и partial image остаются историей; proof-format imageRule применяется только при использовании IMAGEproof. Здесь полный кураторский текст напрямую утверждает факт и принят как TEXTproof; новый independent решает сам.',[
('prompt-key','PASS',['mamluk-deck'],'Куратор прямо именует Mamluk court cards king,governor,deputy governor. Наместник и заместитель передают исторические ранги; индекс1.'),
('note0','PASS',['french-suits'],'Yale Appendix A FRENCH перечисляет Hearts,Diamonds,Clubs,Spades. Прочитан исходный раздел; перевод четырёх мастей точный.'),
('note1','PASS',['mamluk-court'],'Прямое кураторское утверждение do not feature figural imagery / symbols and label-like inscriptions поддерживает отсутствие людей и обозначения. Это дополнительный факт о мамлюкской колоде, основанный на тексте LACMA, не визуальное заключение по фрагменту. Изображение не заявляется просмотренным и не включено в proofs.'),
('note2','PASS',['german-court'],'Yale Appendix A GERMAN перечисляет Ober,Unter; именно немецкие ранги. Самостоятельный факт о дистракторе.'),
('note3','PASS',['swiss-suits'],'Swiss National Museum прямо Swiss-German Schellen/Schilten/Eicheln/Rosen, русский перевод бубенцы/щиты/жёлуди/розы точен.'),
('explanation','PASS',['mamluk-deck'],'Куратор явно fifty-two, four suits, ten number +threecourt. Два предложения верны; вычисление4×13 также совпадает, без изобретённой датировки.')])
D['card-games-history-tarocchi']=('PASS','Hard: точная особенность раннего Visconti относительно стандартных козырей. Четыре тройки одной категории, знание христианской символики позволяет сузить. Ключ2. Старый ID сохранён. Изменён только note2, чтобы дополнительная классификация относилась к трём выбранным добродетелям.',[
('prompt-key','PASS',['tarot-virtues','tarot-early-courts'],'Met L26–27 связывает older Visconti с extra theological virtues faith,hope,charity. Charity здесь Любовь, не обычный козырь Love. Ключ2.'),
('note0','PASS',['tarot-trump-list'],'Justice,Fortitude,Temperance перечислены в Visconti-Sforza. Перевод Сила для Fortitude точен; не утверждается отсутствие в раннемVisconti.'),
('note1','PASS',['tarot-trump-list'],'Sun,Moon,Star в обычном списке Visconti-Sforza; note именно о выбранной тройке.'),
('note2','PASS',['tarot-virtues'],'Новый note сообщает классификацию богословские добродетели, которую prompt/key не раскрывают. Относится точно к Вере,Надежде,Любви, а не к другим придворным картам. Совпадение дополнительной классификации с explanation допустимо.'),
('note3','PASS',['tarot-trump-list'],'World,Chariot,Wheel of Fortune в том же списке. Самостоятельный факт о тройке, не перенос свойств theologicalvirtues.'),
('explanation','PASS',['tarot-virtues','tarot-early-uncertain'],'Оба предложения соответствуют Met: три добродетели и неопределённость unique/earlier stage. Сохранена неопределённость музея, нет ложной датировки.')])
D['card-games-history-poker']=('PASS','Hard: историческое новшество конкретной версии1925; реальные правила dummy,auction,double позволяют логически исключать более ранние элементы. Ключ3. Все четыре винительные конструкции согласуются с «какое ... правило ... включил». Стабильный legacyID poker не меняется. Новый note3 рассказывает именно о термине уязвимости.',[
('prompt-key','PASS',['vanderbilt-innovations','bridge-auction','bridge-dummy','bridge-double-history'],'Сам Вандербильт в цитате EBU относит vulnerability к новшествам таблицы1925. Остальные три установлены раньше в хронологии EBU; единственен индекс3.'),
('note0','PASS',['bridge-auction'],'Auction principle введён1904, раньше1925. Формулировка не выбирает спорное место India/England.'),
('note1','PASS',['bridge-dummy'],'EBU называет exposure of dealer partner dummy важным изменением при переходе от whist. Note передаёт происхождение открытой руки, не дату1925.'),
('note2','PASS',['bridge-double-history'],'Double/redouble описаны до Auction. Note не утверждает тождество всех лимитов исторических и современных правил.'),
('note3','PASS',['vulnerable-name','vanderbilt-penalties'],'В мемуарной цитате юная пассажирка Finland предложила vulnerable для статуса higher penalties after won game. Note атрибутирован воспоминаниям, напрямую связан с термином выбранного правила; общая история поездки заменена.'),
('explanation','PASS',['vanderbilt-innovations','vanderbilt-penalties'],'Уязвимость названа среди новшеств; won a game ведёт к higher penalties. Два предложения верно объясняют повышенный риск, не добавляют неуказанных премий.')])
D['card-games-tarot-coins']=('PASS','Medium: базовое правило эволюции для знакомого с TCG; четыре параллельных глагольных ответа отвечают на «что происходит». Ключ3. Сохранение урона отличается от прекращения SpecialConditions — содержательные дистракторы, нет грамматической подсказки. Current-linked Advanced v3.4 подтверждает ровно нужные инварианты; стараяPARневыдаетсязановую. Полный78fieldauthorсрез.',[
('prompt-key','PASS',['current-evolve'],'A-05 текущей официальной ссылки: all damage counters it had before evolving сохраняются. Обычно учитывает частные эффекты карт; индекс3. Это не требование снять урон.'),
('note0','PASS',['current-evolve','current-special'],'SpecialConditions исчезают, damage counters остаются. Asleep/Poisoned прямо отнесены к SpecialConditions в F. Ложный составной ответ исправлен конкретным различием состояний и урона.'),
('note1','PASS',['current-evolve'],'Keeps all damage counters it had — адресат остаётся тот же Pokémon, не opponent. Прямое пояснение ошибочного адресата, не абстрактное «неверно».'),
('note2','PASS',['current-evolve'],'All counters сохраняются, поэтому без деления2. Указана конкретная ошибочная величина в варианте, поддержанная текущим правилом.'),
('note3','PASS',['current-evolve'],'All attachedcards(Energy...) — полезное дополнительное сохранение помимо спрашиваемого урона. Тот же эволюционировавший Pokémon, не другой объект.'),
('explanation','PASS',['current-evolve'],'Два предложения: урон остаётся, SpecialConditions прекращаются. Сама по себе эволюция не лечит — точный вывод из all damage counters, не запрет отдельного card effect.')])
D['card-games-magic-mana']=('PASS','Medium: узнавание основного ресурса Magic среди4 коллекционных игр. Ключ2; одинаковые названия игр и согласование «в какой». Независимый основной факт от Lorcana ink и Pokémon prizes. Актуальные первичные документы для всех игр сверены; описание Pokémon battle поддержано новым Advanced.',[
('prompt-key','PASS',['mana'],'106.1 Magic mana primary resource, pays costs usually spells. Ключ2. Живая страница rules ведёт на TXT September25,2026, не переименована старая версия.'),
('note0','PASS',['poke-team','current-battle','current-opponent'],'Pokémon против Pokémon оппонента в PARстр3 явно; текущий AdvancedA описывает battle cards и атаку DefendingPokémon противником. Базовая связь подтверждена текущими правилами, не толькоPAR.'),
('note1','PASS',['yu-types'],'Konami FAQ прямо Monster,Spell,Trap cards; свежая официальная страница содержит то же утверждение. Note именно о Yu-Gi-Oh TCG.'),
('note2','PASS',['life'],'103.4 starting20; соседние103.4a-e содержат варианты30/40/25. «Обычная» не универсализирует Commander. Дополнение к мане — старт жизни.'),
('note3','PASS',['current-ink'],'Итальянский официальный Quick Start из текущего resources: carte inchiostro/calаmaio/paycosts. Calamaio=чернильница, ресурс чернила, перевод проверен с английским QuickStart.'),
('explanation','PASS',['mana'],'Два предложения, primaryresource/buycosts/castspells/activateabilities точно106.1; не утверждается, что каждая способность требуетману.')])
D['card-games-pokemon-prizes']=('PASS','Medium: основное условие победы Pokémon среди4TCG. «Одним из условий» не исключает другие победные условия и специальные эффекты; ключ3. Обычная подготовка6 и механизм KO подтверждены текущим Advanced; источник карточки обновляется на него.',[
('prompt-key','PASS',['poke-win','current-prize-win'],'Текущий E называет взятие всех Prize соперником условием завершения/поражения игрока, PARстр3 прямо поясняет first takeallwins. Проверены и альтернативные условия, и одновременные результаты; первый взявший все удовлетворяет победному условию.'),
('note0','PASS',['yu-types'],'Официальный FAQ подтверждает Monster/Spell/Trap — три базовых вида карт именно Yu-Gi-Oh.'),
('note1','PASS',['current-ink'],'Current-linked итальянский Il tuo calamaio подтверждает оплату карт чернилами. Это оLorcana, не о Prize.'),
('note2','PASS',['mana'],'106.1 тратить ману при spells and activating abilities. «Многих» не навязывает стоимость всемспособностям.'),
('note3','PASS',['current-prize-setup'],'Текущий Gstep7: top6 facedown asPrize. Обычная партия сохраняет различие специальных форматов, число6 и ориентация прямо в тексте.'),
('explanation','PASS',['poke-win','current-prize-win','current-prize-ko'],'Два предложения о победе и обычномKO. Step4KO связывает причитающиеся призы сKnockOut; «обычно» не отрицает особые карты или несколько призов. Первый all — не одновременная ничья.')])
D['card-games-yu-gi-oh-life']=('PASS','Medium: базовое стартовое значение обычногоYu-Gi-OhTCG, не trivia вне игровойаудитории. Ключ3; именные названия4игр сопоставимы. Не смешаны Speed/RushDuel. Оба преждеHOLDдистрактора проверены текущими первичными правилами.',[
('prompt-key','PASS',['yu-life'],'Конкретный официальный FAQ явно8000LP дляYu-Gi-OhTCG, текущаястраница прочитана. Вариант3однозначен.'),
('note0','PASS',['current-ink'],'Текущий QuickStartИталия:картычернильницы оплачиваютcosts, конкретное свойствоLorcana.'),
('note1','PASS',['life'],'Обычные20 из103.4, соседниеварианты прочитаныиучтенысловомобычной. Magicне8000.'),
('note2','PASS',['poke-team','current-battle','current-opponent'],'ПрямойPARтекстоPokémonпротивPokémonподтверждёнтекущимиAdvancedA battle/attacks/DefendingPokémon. NoteнеприписываетLPпокемонам.'),
('note3','PASS',['yu-types'],'Monster,Spell,Trap точноподтвержденыKonami. Полезная структураигрыдополняет8000.'),
('explanation','PASS',['yu-life'],'FAQ8000LPистремлениеснизитьсоперникудо0. Один изспособов неотрицаетиныхусловийпобеды. Двапредложения.')])
D['card-games-lorcana-ink']=('PASS','Medium: характерныйресурсTCG, 4 однородных названия. Ключ3. Издательский QuickStartИТ по текущей ссылке resources проверен полностьюнацелостность, разделыVincere/Il tuo calamaioфактическипрочитаны. НовыеCRсбудущейдатой16октябрянеиспользованыдля11октября. Не2024relabel, указанреальныйитальянскийдокумент.',[
('prompt-key','PASS',['current-ink'],'Il tuo calamaio буквально cardsfacedown usedpaycostsforcardsfromhand. РесурсодноимённойLorcana, индекс3.'),
('note0','PASS',['mana'],'Magic106.1 мана на spells/activatedabilities; точныйдистрактор, нечернильница.'),
('note1','PASS',['poke-team','current-battle','current-opponent'],'БоиPokémonсPokémonпротивника в исходномPAR, текущиеAdvancedA battle/attacks/DefendingPokémonподтверждаютбазовыйфакт; неPocketигра.'),
('note2','PASS',['yu-types'],'FAQKonamiперечисляетMonster,Spell,Trap, самостоятельнаясправкаигры.'),
('note3','PASS',['current-lore','lore-win'],'Vincere20o più points leggenda — тотжересурсчтоEnglishlore. Сохранёнанглийскийтермин, знаниякакрусскоепояснение. Дополнительныйпобедныйпорогнеповторяетчернильницу.'),
('explanation','PASS',['current-one-ink'],'Каждаякартаcalamaio1{I}, non importa cosa fronte — независимоотлицевойстороны. Двапредложениясоответствуютправилу; неутверждается, чтолюбуюкартуможноположитьобычнымдействием.')])
SOURCE_UPDATES={
'card-games-tarot-coins':dict(title='Pokémon — Advanced Player’s Rulebook',url=PU,verifiedAt='2026-10-11'),
'card-games-pokemon-prizes':dict(title='Pokémon — Advanced Player’s Rulebook',url=PU,verifiedAt='2026-10-11'),
'card-games-lorcana-ink':dict(title='Ravensburger — Disney Lorcana, Sussurri nel Pozzo Quick Start Rules',url=LU,verifiedAt='2026-10-11')}
