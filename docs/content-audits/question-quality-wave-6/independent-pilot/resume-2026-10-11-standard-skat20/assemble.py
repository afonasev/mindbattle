"""Bind explicitly written independent judgments to frozen literals and raw sources.
No inference of substantive verdicts: every verdict below is a reader decision.
"""
import hashlib, json, os, re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
BASE = REPO / 'docs/content-audits/question-quality-wave-6'
AUTHOR = BASE / 'card-games/resume-2026-10-11-standard-skat20'
IDENTITY = '01a12b13-a24c-7ae2-9c1c-3a7952b3076c'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self,t,a):
        if t in ('script','style'): self.hidden+=1
    def handle_endtag(self,t):
        if t in ('script','style'): self.hidden=max(0,self.hidden-1)
    def handle_data(self,s):
        if not self.hidden: self.parts.append(s)

SOURCES = {
 'french':(AUTHOR/'sources/french.html','Pagat — French suited cards','https://www.pagat.com/class/french.html','original rules/reference authored by John McLeod'),
 'spades':(AUTHOR/'sources/pagat-spades.html','Pagat — Spades','https://www.pagat.com/auctionwhist/spades.html','original rules authored by John McLeod and contributors'),
 'bicycle-spades':(BASE/'card-games/sources/bicycle-spades-web-open-full.txt','Bicycle Cards — Spades complete rendered rules','https://bicyclecards.com/how-to-play/spades/','official publisher game rules'),
 'rummy':(AUTHOR/'sources/rummy.html','Pagat — Basic Rummy','https://www.pagat.com/rummy/rummy.html','original rules authored by John McLeod'),
 'isko':(AUTHOR/'sources/isko-correct-url.pdf','International Skat Order — May 2023 English translation','https://ispa-usa.org/docs/rules/505fc8_e561984976a345bc8404e4474ce066ef.pdf','official International Skat Order / authorized ISPA Canada translation'),
 'atlas':(BASE/'card-games/sources/atlas-inv0072-2015-bicycle.jpg','Atlas of Playing Cards — INV0072 Bicycle 2015 specimen','https://atlasofplayingcards.org/pics001/inv0072.jpg','original playing-card specimen image in curator photographic archive'),
 'atlas-french':(AUTHOR/'sources/atlas-french.jpg','Atlas of Playing Cards — INV2708a French specimen','https://atlasofplayingcards.org/pics2600/inv2708a.jpg','original playing-card specimen image in curator photographic archive'),
 'war':(BASE/'card-games/sources/bicycle-war-official-full-rendered-source.txt','Bicycle Cards — War','https://bicyclecards.com/how-to-play/war/','official publisher game rules'),
 'klondike':(BASE/'card-games/sources/bicycle-klondike-primary.html','Bicycle Cards — Klondike','https://bicyclecards.com/how-to-play/klondike/','official publisher game rules'),
 'euchre':(AUTHOR/'sources/euchre.html','Pagat — Euchre','https://www.pagat.com/euchre/euchre.html','original rules authored by John McLeod and named contributors'),
 'belote':(AUTHOR/'sources/belote.html','Pagat — Belote','https://www.pagat.com/jass/belote.html','original rules contributed by Jean-Pierre Coulon, edited by Nick Wedd and John McLeod'),
 'durak':(AUTHOR/'sources/durak.html','Pagat — Podkidnoy Durak','https://www.pagat.com/beating/podkidnoy_durak.html','original rules authored by John McLeod with Alexey Lobashev'),
}
PROOFS={}
def proof(key,source,locator,passage,method=None):
    p,title,url,cls=SOURCES[source]; b=p.read_bytes()
    fmt=('pdf original bytes with pdfPage locator' if p.suffix=='.pdf' else 'original institutional image/deck scan with pixel locator and explicit visual observation' if p.suffix=='.jpg' else 'html original bytes' if p.suffix=='.html' else 'text original full fetched response or fully documented original extracted content')
    PROOFS[key]={'sourceClass':cls,'title':title,'url':url,'rawCapture':os.path.relpath(p,HERE),'rawCaptureSha256':sha(b),'captureFormat':fmt,'captureMethod':method or ('curl full original response retained by author; independently read from bytes' if source not in ('war','klondike','atlas') else 'historical complete capture retained in Git; independently read full relevant rules or viewed original image'),'locator':locator,'passage':passage,'passageSha256':sha(passage.encode()),'readerRole':'independent','readerIdentity':IDENTITY}
def rule(key,page,start,end):
    text=PdfReader(SOURCES['isko'][0]).pages[page-1].extract_text()
    a=text.index(start); z=text.index(end,a+len(start)) if end else len(text)
    proof(key,'isko',{'pdfPage':page,'rule':start},text[a:z].strip(),'independent live HTTPS 200 full byte comparison on 2026-10-11; pypdf extraction of specified original page/rule')

proof('ranks','french',{'heading':'The 52 card pack'},'The standard international pack consists of 52 cards: ace, king, queen, jack, 10, 9, 8, 7, 6, 5, 4, 3, 2 in each of the four suits.')
proof('ace','french',{'heading':'The 52 card pack'},'The ace is of course the numeral one, but in the international pack it is marked in the corner with a letter "A" rather than a figure "1" and in most modern card games in which the order of cards matters the ace ranks above the king rather than below the 2.')
proof('spades-ranks','spades',{'heading':'Spades for Four Players / Players and Cards'},'A standard pack of 52 cards is used. The cards, in each suit, rank from highest to lowest: A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2.')
proof('king-image','atlas',{'imageSize':[656,229],'pixelRegion':[164,0,327,229],'object':'K hearts, second card'},'VISUAL OBSERVATION: In the second card, K hearts marks a bearded male court figure wearing a crown. This is an observed picture, not a textual quotation.')
proof('queen-image','atlas',{'imageSize':[656,229],'pixelRegion':[328,0,490,229],'object':'Q spades, third card'},'VISUAL OBSERVATION: The third card, Q spades, depicts a female court figure wearing a crown. A is a single suit-symbol card; K and J depict different court figures. This is an observed picture, not a textual quotation.')
proof('draw','rummy',{'heading':'Basic Rummy / Play / The Draw'},'You must begin by taking one card from either the top of the Stock pile or the top card on the discard pile, and adding it to your hand.')
proof('visible','rummy',{'heading':'Basic Rummy / Play / The Draw'},'The discard pile is face up, so you can see in advance what you are getting. The stock is face down, so if you choose to draw from the stock you do not see the card until after you have committed yourself to take it.')
proof('discard','rummy',{'heading':'Basic Rummy / Play / The Discard'},'At the end of your turn, one card must be discarded from your hand and placed on top of the discard pile face up.')
proof('exit','rummy',{'heading':'Basic Rummy / Play / going out'},'A player wins an individual hand by either melding, laying off, or discarding all of his or her cards.')
proof('war-deal','war',{'lines':[28,30],'heading':'The Deal'},'The deck is divided evenly, with each player receiving 26 cards, dealt one at a time, face down.')
rule('shuffle',9,'3.2.2','3.2.3')
rule('cut',9,'3.2.4','3.2.5')
rule('skat-deal',9,'3.2.6','3.2.7')
proof('courts-image','atlas',{'imageSize':[656,229],'pixelRegion':[0,0,656,229],'object':'A spades, K hearts, Q spades, J diamonds'},'VISUAL OBSERVATION: A spades has a single large spade rather than a human figure; K hearts, Q spades and J diamonds have court figures. The printed hearts and diamonds are red; the printed spades are black. This records actual inspection of the entire original image.')
proof('colors-image','atlas-french',{'imageSize':[557,213],'pixelRegion':[0,0,557,213],'object':'A spades, K hearts, Q diamonds, J clubs'},'VISUAL OBSERVATION: The original four-card specimen shows a black spade on the left, red heart on the king, red diamond on the queen, and black clubs on the jack at the right. These four suit symbols form two observed color pairs, red and black. This is visual observation, not quoted source text.')
proof('rummy-object','rummy',{'heading':'Basic Rummy / Object of the Game'},'The object of the game is to dispose of all the cards in your hand. There are three ways to get rid of cards: melding, laying off, and discarding.')
proof('melds','rummy',{'heading':'Basic Rummy / Object of the Game / Melding'},'There are two kinds of combination which can be melded: sequences (also known as runs) and groups (also known as sets or books). a sequence or run consists of three or more cards of the same suit in consecutive order, such as')
proof('sets','rummy',{'heading':'Basic Rummy / Object of the Game / Melding'},'a group , set or book is three or four cards of the same rank, such as')
proof('meld-turn','rummy',{'heading':'Basic Rummy / Play / Melding'},'If you have a valid group or sequence in your hand, you may lay one such combination face up on the table in front of you.')
proof('score','rummy',{'heading':'Basic Rummy / Scoring'},"The total value of all the cards in the hands of the other players is added to the winner's cumulative score.")
proof('facecards','rummy',{'heading':'Basic Rummy / Scoring'},'Face cards (K,Q,J) are worth 10 points each Aces are worth 1 point each')
proof('spades-deal','spades',{'heading':'Spades for Four Players / The Deal'},"The first dealer is chosen at random, and the turn to deal rotates clockwise. The cards are shuffled and then dealt singly, in clockwise order beginning with the player on dealer's left, until all 52 cards have been dealt and everyone has 13.")
proof('spades-facedown','bicycle-spades',{'lines':[43,43],'heading':'The Deal'},"The entire deck is dealt one at a time, face down, beginning on the dealer's left.",'Historical complete returned substantive transcription lines3–99 with original URL/capture method/date retained, not selected quotes; independently read entire relevant rule text')
proof('war-goal','war',{'lines':[26,26]},'The goal is to be the first player to win all 52 cards')
proof('war-end','war',{'lines':[37,37],'heading':'How to Keep Score'},'The game ends when one player has won all the cards.')
proof('war-play','war',{'lines':[33,33],'heading':'The Play'},'Each player turns up a card at the same time and the player with the higher card takes both cards and puts them, face down, on the bottom of his stack.')
proof('war-tie','war',{'lines':[34,34],'heading':'The Play'},'If the cards are the same rank, it is War. Each player turns up one card face down and one card face up.')
proof('klondike-goal','klondike',{'heading':'Object of the Game'},'The goal is to get the four suits built onto the foundations from aces up through kings.')
proof('klondike-play','klondike',{'heading':'The Play'},'Any movable card may be placed on a card next-higher in rank if it is of opposite color.')
proof('klondike-space','klondike',{'heading':'The Play'},'Only a king may fill an open space in the layout.')
proof('euchre-goal','euchre',{'heading':'British Euchre / Players and Object'},'Euchre is a plain-trick game for four players in fixed partnerships, partners sitting opposite. Just 5 cards are dealt to each player and the object is to win at least three of the five tricks - with an extra bonus for winning all five.')
proof('bowers','euchre',{'heading':'British Euchre / Rank of Cards'},'Right Bower (the jack of the trump suit) Left Bower (the other jack of the same colour as the trump suit)')
proof('left-suit','euchre',{'heading':'British Euchre / Rank of Cards'},'Note that Benny and Left count for all purposes as belonging to the trump suit. For example if hearts are trumps, the jack of diamonds is a heart not a diamond. It can be played to a heart lead and if it is led, hearts must be followed.')
proof('belote-rank','belote',{'htmlId':'card-points','tableColumns':'Trump suit rank/value; Other suits rank/value','rows':'first three'},'Cards in the trump suit both rank and score differently from those in other suits. Notice the promotion of the trump 9 and J. Trump suit Other suits J 20 A 11 9 14 10 10 A 11 K 4')
proof('durak-add','durak',{'heading':'The Play / Attack and Defence'},'each new attack card must be of the same rank as some card already played during the current bout - either an attack card or a card played by the defender;')
rule('skat-players',5,'1.1.1','1.1.2')
rule('skat-deck',5,'1.2.2',None)
rule('types',6,'2.1.1','2.1.2')
rule('types-table',6,'2.1.2','2.2 Ranking')
rule('suit',6,'2.2.1','2.2.2')
rule('jacks',6,'2.2.2','2.2.3')
rule('grand',6,'2.2.3','2.2.4')
rule('null-ranks',6,'2.2.4','2.3 Tops')
rule('levels',7,'2.5.1',None)
rule('61',8,'2.5.4','2.5.5')
rule('ouvert',8,'2.5.8','2.5.9')
rule('null-win',8,'2.5.9','2.5.10')
rule('open-show',9,'2.6.5','3.0 Initiating')
rule('hand-forbidden',12,'3.5.5','3.5.6')
SOURCES['uno-decoded']=(HERE/'uno-complete-independent-extraction.txt','Mattel UNO — complete independently decoded original document','https://service.mattel.com/instruction_sheets/42001pr.pdf','official creator instruction sheet, complete documented extraction')
proof('uno-object','uno-decoded',{'pdfPage':1,'heading':'OBJECT','originalRaw':'../../card-games/sources/mattel-uno-instruction-sheet-42001.pdf','originalRawSha256':'7b563ac2e1c612f0506846a0fc8253197c8491cd3d88a406a7024b4881a98033'},'The first player to play all of the cards in their hand in each\nround scores points for the cards their opponents are left\nholding. The first player to score 500 points wins the game.','Independent pypdf complete two-page extract; /Kxx glyph hex decoded cp1252; independently visually read original page1 OBJECT and SCORING in uno-page1-visual.png; full extraction and raw hash retained')
proof('uno-score','uno-decoded',{'pdfPage':1,'heading':'SCORING','originalRaw':'../../card-games/sources/mattel-uno-instruction-sheet-42001.pdf','originalRawSha256':'7b563ac2e1c612f0506846a0fc8253197c8491cd3d88a406a7024b4881a98033'},'If you are first to get rid of all your cards, you get points for\nthe cards left in the other players hands.','Independent full extraction and actual visual original-page1 read; SCORING, not alternative penalty-scoring paragraph')

# Six indexed decisions in exact order: prompt-key, note0, note1, note2, note3, explanation.
PILOT=[
('card-games-king-rank','PASS','Easy: recognition of a familiar crowned male court card. Four rank nouns substitute correctly. Queen and Jack images are separate targets; this is not the ace-letter question. Each note adds rank information rather than merely repeating the male picture.',[
 ('PASS',['king-image'],'Observed crowned bearded K figure matches Король; other offered ranks do not identify this pictured ruler.'),
 ('PASS',['spades-ranks'],'Read descending Spades list Q,J,10; note is about the actual Валет option and supplies its neighbours.'),
 ('PASS',['ranks','ace'],'The listed order A,K,Q gives both neighbouring ranks for Король; adds ordering beyond the male crown asked by the prompt.'),
 ('PASS',['ace'],'McLeod explicitly qualifies most modern games where order matters; Russian note keeps that qualifier, so no universal ace-high assertion.'),
 ('PASS',['ranks'],'Listed K,Q,J places Дама after king and before jack; note describes this distractor itself.'),
 ('PASS',['king-image','ranks','ace'],'Image supports ruler figure; rank list and stated ace variability support both ordering clauses. Two sentences; extra ace caveat prevents treating one order as every game.')]),
('card-games-queen-rank','PASS','Easy: familiar female court figure. All offered rank names are grammatically parallel. Female picture is distinct from king picture and jack-order target. Correct note names the three court ranks and adds classification.',[
 ('PASS',['queen-image'],'Q spades visibly depicts the crowned female figure, giving Дама as the unique offered rank.'),
 ('PASS',['ace'],'The original expressly says ace outranks king in most modern games where order matters; qualifier preserved.'),
 ('PASS',['ranks'],'A,K,Q,J order entails immediate K before Q; fact belongs to Король option.'),
 ('PASS',['courts-image','facecards','ranks'],'Court figures are K,Q,J and the list names them; Q is one of those three, adding classification beyond woman image. J court figure was visually inspected in the rightmost card.'),
 ('PASS',['spades-ranks'],'Spades descending order has Q,J,10, so Валет follows queen and precedes ten.'),
 ('PASS',['queen-image','ranks'],'Female figure verified visually; K,Q,J order supports lower than king and higher than jack. Two concise sentences.')]),
('card-games-jack-rank','PASS','Easy: familiar court-card order; generic usually qualifier is appropriate. King/queen questions identify pictures, not inverse rank questions. Four rank nouns fit. Correct note adds ten as a lower neighbour in named Spades rules.',[
 ('PASS',['ranks'],'Descending international pack sequence Q,J,10 identifies Валет as the court rank immediately below queen.'),
 ('PASS',['ranks'],'K precedes Q and J in the explicitly read list; standalone ordering information about Король.'),
 ('PASS',['ranks'],'K,Q,J establishes Дама between king and jack; concrete distractor fact.'),
 ('PASS',['spades-ranks'],'Named Spades rank list places J below Q and above 10; ten is additional information beyond the prompt.'),
 ('PASS',['ace'],'Most-modern-order qualification preserved, and ace above king is stated explicitly.'),
 ('PASS',['ranks','courts-image','facecards'],'The three visually read courts K,Q,J occur in descending order, making J the lowest court rank. Its next listed neighbour is ten; this is usual international order, not trump-game order.')]),
('card-games-shuffle-action','PASS','Easy: familiar card preparation verb. All four action nouns fit the question and are distinct. Shuffle changes order; deal distributes; draw adds; discard removes. This target differs from the other three actions. Notes include concrete named-game rules.',[
 ('PASS',['shuffle'],'Rule 3.2.2 orders thoroughly shuffle, then cut, then deal. Перемешивание is the Russian semantic equivalent of shuffle, hence Тасование.'),
 ('PASS',['shuffle','cut','skat-deal'],'Read required cut and 3-4-3 packet deal. Note adds mandatory preparation and packet structure, beyond mixing asked in prompt.'),
 ('PASS',['discard','exit'],'Ordinary-turn face-up discard read together with explicit going-out by meld/lay-off/discard; note retains the exception and avoids old every-turn overclaim.'),
 ('PASS',['skat-deal'],'Rule specifies one round of three, skat two, four each, then three each. Note states player packets only, not that skat is absent.'),
 ('PASS',['draw','visible'],'Draw offers one card from face-down stock or top face-up discard; each source pile and visibility qualification checked.'),
 ('PASS',['shuffle','skat-deal'],'Preparation rule puts shuffle before distributing packets. Mixing changes relative order by meaning of shuffle; deal distributes cards to participants. Two sentences, no unsupported randomness guarantee.')]),
('card-games-deal-action','PASS','Easy: distribution action in familiar card play. Four action nouns substitute correctly. War rule specifies distribution, while distractors describe different operations. Rummy ordinary-turn exception now explicit.',[
 ('PASS',['war-deal','skat-deal'],'Dealt cards are issued to participants before play; Russian Раздача names this distribution, unlike mixing, drawing or discarding.'),
 ('PASS',['war-deal'],'War original says deck divided evenly with 26 cards each; half-deck count is explicitly supported and adds game-specific detail.'),
 ('PASS',['shuffle','cut'],'In Skat the player to dealers right cuts after shuffle; cutting mandatory. Named Skat scope avoids universal card-game cutting claim.'),
 ('PASS',['draw'],'Basic Rummy draw must begin the turn and offers stock or discard top; note correctly describes Добор.'),
 ('PASS',['discard','exit'],'Ordinary discard and terminal meld/lay-off exception were both read. Note no longer implies every winning turn requires discard.'),
 ('PASS',['war-deal','skat-deal'],'War gives 26 one at a time, Skat gives 3-4-3 packets. Together these independently read concrete rules substantiate distribution and game-dependent count/order; two sentences.')]),
]

REMAINING=[
('card-games-draw-action','PASS','Easy: everyday card action name. Obtaining a card differs from dealing, discarding and shuffling. All four action names fit. Correct note adds the two alternative Rummy piles. This is not the blackjack-specific Hit question.',[
 ('PASS',['draw','visible'],'Taking from face-down stock and adding to hand is called Draw in the source; Russian Добор is the matching action noun.'),
 ('PASS',['spades-deal','spades-facedown'],'Spades source explicitly deals singly clockwise beginning at dealers left, until52 dealt; face-down aspect independently corroborated by Bicycle Spades complete rules.'),
 ('PASS',['draw','visible'],'Exact two sources for draw are stock top or discard top. Literal gives one card rather than entire discard pile, appropriate to Basic Rummy.'),
 ('PASS',['discard','draw','visible'],'Discard placed face-up on top, then next turn can select that top; the fact is about the discarded card, not a forced next-player choice.'),
 ('PASS',['shuffle','cut'],'Skat right-hand neighbour cuts; mandatory cut is read separately, and temporal order is shuffle-cut-deal.'),
 ('PASS',['draw','visible','meld-turn'],'Draw adds to hand before optional meld. Source says must begin by draw, then may meld; no assertion that melding is compulsory.')]),
('card-games-discard-action','PASS','Easy: removing a hand card to an open pile. Four nouns parallel; only Сброс describes the direction. Notes are indexed correctly. Correct note supplies availability to the next player; repeats a useful extra explanation fact legitimately.',[
 ('PASS',['discard'],'Source calls the move from hand to face-up discard pile The Discard; Russian Сброс is the action in the prompt.'),
 ('PASS',['draw','visible'],'Top of face-up discard is one permitted Draw source. Добор note names that source and can be checked independently.'),
 ('PASS',['discard','draw'],'The discarded card becomes the top and is available to next Draw; adds accessibility beyond placing a card asked by the prompt.'),
 ('PASS',['shuffle','cut'],'Skat is named rather than universal card play; rule3.2.2 and mandatory cut3.2.4 support sequence.'),
 ('PASS',['spades-deal','spades-facedown'],'Pagat says dealt singly; face-down clause corroborated by original complete Bicycle Spades transcription read independently.'),
 ('PASS',['discard','draw','exit'],'Three sentences accurately separate ordinary face-up end-of-turn discard from terminal meld/lay-off possibility. Neither forces last discard nor says every Rummy variant has identical rules.')]),
('card-games-deck-cards-52','PASS','Easy: familiar standard-deck total. Numbers are plausible deck-related quantities and have self-contained notes. Target total52 differs from suit count4 and court-rank count3; the former inverse ranks13 target was removed. Correct note adds structure4x13.',[
 ('PASS',['ranks'],'Original expressly standard international pack52; exclusion of jokers agrees with following source section describing jokers as additional cards.'),
 ('PASS',['ranks'],'Read thirteen distinct ranks in each of four suits: A,K,Q,J,10 through2. Counting13x4=52 is an explicit computation, not a fabricated source quotation.'),
 ('PASS',['colors-image','courts-image'],'Two original specimens show conventional red/black suit signs. This is a fact about the number2 option in ordinary deck printing, not a claim that all custom decks have only two colors.'),
 ('PASS',['colors-image','ranks'],'Specimen visibly shows all four suit signs; French source identifies four suits. Russian names translated as hearts/diamonds/clubs/spades.'),
 ('PASS',['ranks'],'The thirteen named ranks are present in each suit; count is computed from the enumerated list.'),
 ('PASS',['ranks'],'Source explicitly52 and four suits; counting listed ranks13 yields stated equal distribution. Two sentences; joker exclusion is retained.')]),
('card-games-deck-suits-4','PASS','Easy: standard-deck suit count. Four numeric options are the same answer type. Named suits in correct note add information beyond count. Suit names and pack count are related but this target is not an inverse question asking cards per suit.',[
 ('PASS',['ranks','colors-image'],'Original says four suits and specimen shows four distinct marks. Unique numeric answer4 among52,4,13,2.'),
 ('PASS',['ranks'],'Standard international pack52 is explicitly stated; understood ordinary French international pack rather than every truncated regional pack.'),
 ('PASS',['colors-image','ranks'],'Four visible conventional marks map to червы, бубны, трефы, пики. Adds their identities rather than repeating only four.'),
 ('PASS',['ranks'],'Thirteen listed ranks apply in each of the four suits. Count justified by explicit enumeration, not source claim invented verbatim.'),
 ('PASS',['colors-image','courts-image'],'Both inspected original specimens show red heart/diamond and black spade/club signs; concrete conventional color fact about2.'),
 ('PASS',['colors-image','ranks'],'Four suit identities visually verified; source enumerates thirteen ranks per suit. Two sentences, correct count and names.')]),
('card-games-deck-ranks-13','PASS','Easy: court-card classification. ID retained but target now count3, no inverse52/13 duplication. Four numeric choices fit. Correct note names K,Q,J and excludes A, adding membership beyond count.',[
 ('PASS',['facecards','courts-image'],'Original distinguishes face cards K,Q,J from aces; image confirms exactly these three pictured ranks. Counting categories gives3, not twelve individual court cards.'),
 ('PASS',['ranks','colors-image'],'Four suits in source and four marks observed. This describes number4 independently, not number of court ranks.'),
 ('PASS',['facecards','courts-image'],'K,Q,J are named face cards; A appears on its own symbol card and separately valued in Rummy. Explicitly adds rank membership and ace exclusion.'),
 ('PASS',['colors-image'],'Ordinary French suit marks have red/black colors, seen in fresh original specimen. Note does not imply every pixel/artwork uses only two inks.'),
 ('PASS',['ranks'],'The source standard international deck52 with additional jokers later discussed supports without-joker ordinary deck count.'),
 ('PASS',['facecards','courts-image'],'Court rank membership is directly corroborated by facecards distinction and observed pictures; ace is separate. Two sentences, not confused with total12 court cards.')]),
('card-games-deck-colors-2','PASS','Easy: conventional suit colors. The word основных and standard scope excludes special four-color designs. Correct note gives the mapping of four suits to colors. Suits shape-identification questions ask different targets.',[
 ('PASS',['colors-image','courts-image'],'Fresh French and Bicycle original specimens show conventional two suit colors. Counting distinct suit-symbol colors gives2.'),
 ('PASS',['ranks'],'Descending source list A,K,Q,J,10..2 has13 entries. От туза до двойки describes that displayed ordering, not a universal ace-high rule.'),
 ('PASS',['ranks'],'Explicit52 standard international cards fact applies to number52.'),
 ('PASS',['colors-image','courts-image'],'Observed hearts/diamonds red, clubs/spades black; additional mapping beyond prompt count. Repetition in explanation is allowed because useful and not merely two colors.'),
 ('PASS',['colors-image','ranks'],'Four suit signs/names verified. Conventional Russian translations of hearts, diamonds, clubs, spades used.'),
 ('PASS',['colors-image','courts-image'],'Exact color mapping independently viewed, pair-count inference4 marks grouped2+2 stated explicitly; two sentences.')]),
('card-games-goal-uno-empty','PASS','Easy: popular UNO round goal. Prompt explicitly individual deal, avoiding confusion with500-point session. Four complete infinitive constructions fit. Correct note adds scoring; distinct from UNO action cards and other game goals.',[
 ('PASS',['uno-object','uno-score'],'OBJECT names first player to play all hand cards in each round; separate500-point game goal. Correct key is First dispose of all cards for the stated round.'),
 ('PASS',['klondike-goal'],'Klondike bases built by suit from ace through king, directly a fact about the foundations-goal distractor.'),
 ('PASS',['melds','sets'],'Rummy melds are same-suit consecutive sequences and same-rank groups; this describes the meld-goal distractor rather than UNO.'),
 ('PASS',['uno-score'],'SCORING awards first-out player points for opponents remaining cards. Extra fact beyond going out; read visually and decoded from raw original.'),
 ('PASS',['war-end'],'War ends when one player owns all cards; note directly identifies the collect-entire-deck distractor goal.'),
 ('PASS',['uno-object','uno-score'],'Round first-out victory and winner scoring read in OBJECT/SCORING; first500 wins session. Literal separates deal from whole-game target; two sentences.')]),
('card-games-goal-klondike-foundations','PASS','Easy: familiar solitaire goal; foundations vs table play distinguished. Four goal constructions fit. Correct note adds tableau descent, alternating colors and king-only empty space, rather than repeating foundation goal. Foundation terminology question asks name of a pile, a distinct target.',[
 ('PASS',['klondike-goal'],'Original OBJECT names four suits on foundations from aces through kings; key refers to this goal uniquely.'),
 ('PASS',['rummy-object','exit'],'For sets/sequences option, identifies Basic Rummy where disposing all hand cards wins. Useful independent game-goal context tied to meld activity.'),
 ('PASS',['war-end','war-play'],'War comparison mechanism continues to full-deck possession; directly linked to collect-entire-deck option.'),
 ('PASS',['uno-score'],'First-dispose goal is identified with UNO scoring remaining cards; factual contextual link to this distractor.'),
 ('PASS',['klondike-play','klondike-space'],'Original movable-card rule demands next-higher opposite color; translated as build descending alternating colors. Only king fills vacant place. Adds tableau constraints beyond foundation goal.'),
 ('PASS',['klondike-goal','klondike-play'],'Foundation goal and opposite-color descending tableau rule both present in original. Two sentences; foundation and tableau directions not conflated.')]),
('card-games-goal-rummy-melds','PASS','Easy: goal of explicitly Basic Rummy single deal, not all Rummy variants. Four complete infinitive constructions. Correct note adds scoring; losing-card option note explains why accumulating is disadvantageous. Sets/run name questions ask composition or labels, not this goal.',[
 ('PASS',['rummy-object','exit'],'Object dispose of all hand cards and individual-hand win by three routes supports key. Other offered objectives are not Basic Rummy deal goal.'),
 ('PASS',['war-tie'],'Collect-entire-deck distractor is War goal; note names that game and explains its same-rank comparison phase, useful related game-specific detail.'),
 ('PASS',['score'],'Remaining-card total credited to winner shows direct consequence of accumulating hand cards. Note relates to the false maximize-hand goal and avoids claiming basic penalty scoring.'),
 ('PASS',['klondike-goal'],'Foundations from aces through kings are Klondike goal, directly related to that distractor action.'),
 ('PASS',['score'],'Winner cumulative score gains all remaining-card total; adds scoring beyond disposing hand cards asked by prompt.'),
 ('PASS',['rummy-object','exit'],'Last card can leave hand by meld, lay-off or discard. Exact original explicitly allows all three and says play ceases as soon as someone goes out; two sentences.')]),
('card-games-goal-war-cards','FIX_REQUIRED','Easy goal and key are factual, and grammar of four goal options is parallel. Goal differs from previously reviewed higher-card mechanism. However note0 is about a War tie, not the disposal-of-all-cards distractor; it fails option-specific informativeness despite factual accuracy. Fix note0 only, preserving ID/order/difficulty/index.',[
 ('PASS',['war-goal','war-end'],'Publisher rules explicitly first win all52 and finish when player has all cards. Unique correct goal is collect whole deck.'),
 ('FIX_REQUIRED',['war-tie'],'Literal is factually supported by War tie rule, but option0 says First dispose of all cards. A tie-stage fact about War does not characterize that shedding-goal option, identify its game, or explain the mistaken rule. Violates guide: note must give a verified fact about its specific distractor. Replace with an independently supported shedding-game goal/scoring fact (e.g. Basic Rummy or UNO), not unrelated War mechanics.'),
 ('PASS',['klondike-goal'],'Foundations distractor note correctly describes Klondike suit bases; useful and directly tied to that action.'),
 ('PASS',['melds','sets'],'Same-rank groups and same-suit sequences are valid Rummy meld types, concretely tied to sets/sequences distractor.'),
 ('PASS',['war-deal'],'Publisher explicitly26 dealt to each of two players, adding start distribution beyond goal of winning all cards.'),
 ('PASS',['war-play','war-end'],'Original states same-time reveal, higher card takes both, termination when one owns all. Two sentences; newly explicit simultaneously clause checked.')]),
('card-games-skat-suit-game','PASS','Hard retained: named Skat contract taxonomy and trump composition require specific rules. Main-category wording excludes Ouvert as competing variant, so only Suit games fits. All category names substitute as labels. Goal/count details in correct note add information beyond trump identity. Distinct from Grand/Null rules.',[
 ('PASS',['types','suit','jacks'],'Three primary types read; Suit games designate one trump suit and Jacks are its highest trumps. Ouvert is level/variant, not a fourth main type, so prompt is unique.'),
 ('PASS',['types-table','ouvert','open-show'],'Suit/Grand open games in Hand column; must win every trick and expose ten hand cards before lead. Null Ouvert separate; note explicitly restricts to Suit/Grand.'),
 ('PASS',['grand'],'Only four Jacks trump in Grand, directly describes the Гран alternative.'),
 ('PASS',['61','skat-deck'],'Basic game won61+ including skat; deck120 total from four30-point suits. Adds win threshold rather than only trump-suit fact asked.'),
 ('PASS',['null-ranks','null-win'],'Null has no trump; declarer wins taking no tricks. Directly substantiates the Null alternative.'),
 ('PASS',['suit','jacks','61'],'Four Jacks followed by next seven trump-suit cards; basic win61+. Usually qualifier prevents attributing61 goal to announced Ouvert Schwarz contracts.')]),
('card-games-skat-grand','PASS','Hard retained: exact Grand trump restriction and taxonomy. Main-category language prevents Grand Ouvert from becoming second correct answer. Four labels grammatically parallel. Correct note adds ordinary61-point victory; distinct from suit composition question.',[
 ('PASS',['types','grand'],'Original Grand main type explicitly only four Jacks trump; main categories not variants ensure unique Гран.'),
 ('PASS',['jacks'],'Suit game highest four Jacks followed by seven cards of selected suit. Describes Suit alternative precisely.'),
 ('PASS',['null-ranks','null-win'],'Null no trump; win no tricks entails lose on at least one trick. This is an explicit logical complement of win criterion, not fabricated quotation.'),
 ('PASS',['types-table','ouvert','open-show'],'Suit/Grand Ouvert are Hand, expose hand before lead and require all tricks. Restriction excludes Null Ouvert pickup possibility.'),
 ('PASS',['61','types'],'Basic game win61+, applicable Suit/Grand basic games. Note adds victory criterion beyond four Jacks asked; usual win scope retained.'),
 ('PASS',['grand','61'],'Grand four Jacks ordered same as suits is explicit; ordinary61+ threshold checked. Two sentences with ordinary qualification, no trump suit cards added.')]),
('card-games-skat-null','PASS','Hard retained: exact Null contract rule. Prompt asks main category, not any open variant, making Null unique despite Null Ouvert distractor note. Four labels parallel. Correct note adds ace-high order and ten below Jack. Three main categories ask three distinct rule targets.',[
 ('PASS',['types','null-win'],'Null main category identified by no-trick declarer win. Open variant can share aim but is not a main category; new wording resolves ambiguity.'),
 ('PASS',['null-ranks'],'No trump and exact A,K,Q,J,10,9,8,7 list read; ten below Jack is direct comparison and additional ordering fact.'),
 ('PASS',['grand'],'Only four Jacks, ranked same order as suits, trump in Grand; alternative note matches its name.'),
 ('PASS',['types-table','open-show','null-win'],'Table includes Null Ouvert under Null, both pickup and Hand variants; hand exposed and no-trick goal remains Null. Note correctly calls it a Null variant.'),
 ('PASS',['jacks'],'Four Jacks plus seven selected suit cards is explicit in Suit rank rule; describes the suit-game alternative.'),
 ('PASS',['null-win','null-ranks'],'Null no-trick goal, no trump, ten below Jack all explicitly read. Two sentences; contrasting goal is with point-trick Suit/Grand, not all imaginable Skat variants.')]),
('card-games-skat-ouvert','PASS','Hard: precise highest multiplier level after Schwarz announced, beyond basic category names. The phrase level distinguishes Ouvert from Suit/Grand/Null types. Source table has6 Schwarz Announced then7 Open. Correct note adds Hand restriction after skat pickup. Not duplicate of any primary-category question.',[
 ('PASS',['levels'],'Table ClassII Hand levels6 Schwarz Announced,7 Open verifies following and final highest level. Открытая игра translates Open/Ouvert; other choices are game types, not that level.'),
 ('PASS',['null-ranks','null-win'],'No trumps and zero-trick goal verified for Null; useful concrete alternative fact.'),
 ('PASS',['hand-forbidden','types-table'],'After skat pickup Hand announcement and win levels forbidden; Suit/Grand Ouvert Hand-column association gives the stated consequence. Logical inference explicitly based on both rules.'),
 ('PASS',['suit','jacks'],'One selected trump suit plus Jacks describes Suit game; direct rules2.2.1–2.2.2.'),
 ('PASS',['grand'],'Only four Jacks as trump in Grand stated explicitly.'),
 ('PASS',['levels','types-table','ouvert'],'Hand table6 then7, Suit/Grand Ouvert Hand, must win every trick. Null games distinct type and separate values, not multiplier level7. Three sentences; no claim all Ouvert requires all tricks.')]),
('card-games-euchre-bowers','PASS','Medium: characteristic naming that regular trick-game readers may recognize; four real game names with parallel grammar. Bower key distinct from Belote promoted J/9 and Skat four-Jack mechanism. Correct note adds partnership win threshold beyond naming two Jacks.',[
 ('PASS',['bowers'],'Original Euchre names right as trump Jack, left as other same-color Jack. Among four named games unique terminology is Euchre/Юкер.'),
 ('PASS',['euchre-goal'],'Four-player partnerships, five cards and at least three tricks are explicit in main rules. Note identifies maker-team threshold, not requiring five to win normally.'),
 ('PASS',['belote-rank'],'Read original two-column table with Trump rows J20,9 14,A11. Note compares rank order in left Trump column, not mixing other-suit values or only point counts.'),
 ('PASS',['skat-players'],'Skat one declarer against two defenders is explicit rule1.1.1, directly useful about Скат.'),
 ('PASS',['durak-add'],'Each new attack matches a rank already in current bout, attack or defence card. Note states permissibility, not ignoring hand-size/six-card limits by claiming unlimited attack.'),
 ('PASS',['bowers','left-suit'],'Two Jack identities and left bower counting as trump for all purposes directly read. Actual printed suit distinction explained by hearts/diamonds example. Two sentences.')]),
]

def assemble(rows,name):
    frozen=json.loads((AUTHOR/'frozen-current20.json').read_text()); cards={c['id']:c for c in frozen}
    actual={c['id']:c for c in json.loads((REPO/'src/content/topics/card-games.json').read_text())['questions']}
    binding={r['questionId']:r['currentCanonicalSha256'] for r in json.loads((AUTHOR/'freeze-for-independent.json').read_text())['cards']}
    result={'schemaVersion':1,'role':'independent','agentIdentity':IDENTITY,'authorIdentity':'01a12b13-9e51-76e2-b0aa-6f0e03f539f1','readDate':'2026-10-11','frozenAuthorCommit':'9fbbe9e0a28cb00d19c906febf46ed067b9f3b8d','status':'Independent substantive decisions; coordinator certification remains separate','cards':[]}
    for qid,verdict,editorial,decisions in rows:
        c=cards[qid]; assert canonical(c)==canonical(actual[qid]); assert sha(canonical(c))==binding[qid]
        assert len(decisions)==6
        literals=[canonical([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),*[a['note'].encode() for a in c['answers']],c['explanation'].encode()]
        fields=[]
        for field,literal,(fv,refs,analysis) in zip(['prompt-key','note0','note1','note2','note3','explanation'],literals,decisions):
            fields.append({'field':field,'literalSha256':sha(literal),'literal':json.loads(literal) if field=='prompt-key' else literal.decode(),'verdict':fv,'substantiveRead':True,'claimAnalysis':analysis,'proofs':[PROOFS[k] for k in refs]})
        result['cards'].append({'questionId':qid,'cardCanonicalSha256':sha(canonical(c)),'verdict':verdict,'editorialAnalysis':editorial,'fields':fields})
    save(name,result)
    save('independent-passages.json',PROOFS)
    return result
if __name__=='__main__':
    import sys
    assemble(PILOT+REMAINING if '--full' in sys.argv else PILOT,'independent-current20.json' if '--full' in sys.argv else 'independent-pilot5.json')
