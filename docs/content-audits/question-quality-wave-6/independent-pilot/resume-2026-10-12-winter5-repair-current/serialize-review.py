import json,hashlib,subprocess,os,logging
from pathlib import Path
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)
R=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
authorcanon=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':')).encode()
REV=subprocess.check_output(['git','rev-parse','70863ab']).decode().strip()
Q=json.loads((R/'current-topic-frozen.json').read_text())['questions']
A=json.loads((R/'author-receipt-frozen.json').read_text())
I=json.loads((R/'source-index.json').read_text()); byname={Path(m['frozenPath']).name:m for m in I}
SPECP=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md'); spec=SPECP.read_bytes();lines=spec.decode().splitlines()
rules={k:{'path':str(SPECP),'line':n,'quote':lines[n-1]} for k,n in [('easy',138),('note',143),('duplicate',144),('explanation',146),('source',153)]}
(R/'approved-rule-extract.json').write_text(json.dumps({'fullSpecSha256':sha(spec),'rules':rules},ensure_ascii=False,indent=2)+'\n')
meta={
'fis-equipment-2026.pdf':('FIS — primary international ski governing body','https://assets.fis-ski.com/f/252177/x/00f097325f/specifications_for_alpine_competition_equipment_08-10-2026.pdf'),
'figure-skating.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/figure-skating/'),
'long-track.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/long-track/'),
'curling.html':('World Curling — international governing body','https://worldcurling.org/about/curling/'),
'hockey-equipment-guide.pdf':('Hockey Canada — national governing body','https://cdn.hockeycanada.ca/hockey-canada/Hockey-Programs/game-change/downloads/hc-equipment-fitting-guide-player-e.pdf'),
'biathlon.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/biathlon/'),
'cross-country-skiing.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/cross-country-skiing/'),
'alpine-skiing.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/alpine-skiing/'),
'ski-jumping.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/ski-jumping/'),
'iihf-terminology.html':('IIHF — international governing body','https://canada-central.iihf.com/en/events/2026/olympic-w/static/71794/ice_hockey_terminology'),
'maine-ropeway-statute.html':('Maine Legislature — primary statute','https://legislature.maine.gov/statutes/32/title32sec15202.html'),
'bauer-sharpening.html':('Bauer — primary equipment manufacturer','https://www.bauer.com/pages/prosharp-faq'),
'zamboni-faq-full.html':('Zamboni — primary machine manufacturer','https://zamboni.com/about/frequently-asked-questions-2/'),
'white-ice-catalogue-2025.pdf':('White Ice — primary paint equipment supplier catalogue','https://white-ice.com/wp-content/uploads/2025/06/2025-Catalogue_060825_LoRes.pdf'),
'snowboard.html':('Canadian Olympic Committee — national Olympic institution','https://olympic.ca/sports/snowboard/')}
PDF={}
def proof(name,a,b=None,support=True):
 m=byname[name];urltype,url=meta[name]
 if name.endswith('.pdf'):
  if name not in PDF:PDF[name]=PdfReader(m['frozenPath'])
  passage=PDF[name].pages[a-1].extract_text();loc={'physicalPdfPage':a};method='pypdf extract_text, complete physical page; original PDF bytes preserved'
 else:
  b=a if b is None else b;passage=' '.join(m['visibleNodes'][a:b+1]);loc={'textNodeStart':a,'textNodeEnd':b,'index':'source-index.json visibleNodes; zero based'};method='HTMLParser; script/style excluded; whitespace collapsed within each visible node; complete response bytes preserved'
 return {'sourceType':urltype,'url':url,'locator':loc,'rawCapture':m['frozenPath'],'rawSha256':m['rawSha256'],'sourceGitRevision':m['sourceRevision'],'originalGitBlob':m['gitBlob'],'captureFormat':m['captureFormat'],'extractionMethod':method,'quotedPassage':passage,'quotedPassageSha256':sha(passage.encode()),'supportsCurrentClaim':support}
P=proof
# Analyses are the independent reader's judgments after reading the full passages, not author verdicts.
reviews={
'007':[
 ('FIX','FIS physical page24 defines a release binding freeing the boot at preset loads. The key is correct. But a ski and a boot are not credible separate connecting components under this wording; the fourth answer already says it is between ski and binding. Adding “functional alpine system” does not create easy-level reasoning and makes the Russian unnecessarily technical. Same broad equipment category is insufficient to make all four plausible.',[P('fis-equipment-2026.pdf',24)],['easy']),
 ('PASS','FIS page16 explicitly says edges of the running surface are mainly hard material resistant to wear. “Жёсткие канты” is an understandable short description of that property; the claim concerns the ski itself.',[P('fis-equipment-2026.pdf',16)],[]),
 ('PASS','FIS page25 defines ski boots as footwear enclosing the foot and page12 specifies sole thickness. Both clauses are supported; the regulation fact is useful even without adding numerical specifications.',[P('fis-equipment-2026.pdf',25),P('fis-equipment-2026.pdf',12)],[]),
 ('PASS','The prompt asks what connects the boot. The correct note adds release under preset load, a substantive safety/function fact beyond the prompt/key. Page24 supports release; overlap with explanation is allowed.',[P('fis-equipment-2026.pdf',24)],[]),
 ('FIX','The answer itself is “Интерфейс между лыжей и креплением”; the note says only that the interface is installed between ski and binding. FIS page24 confirms the fact, but this repeats the whole answer label without explaining what the interface is or adding a useful property. This is the established useful-own-fact rule, not a demand for unique trivia.',[P('fis-equipment-2026.pdf',24)],['note']),
 ('PASS','FIS pages16,24,25 identify ski/interface/binding/boot separately. Release at preset load is supported. Two short sentences are comprehensible; the four listed items are not claimed to be an exhaustive list (FIS also lists a retention device).',[P('fis-equipment-2026.pdf',16),P('fis-equipment-2026.pdf',24),P('fis-equipment-2026.pdf',25)],[])
],
'008':[
 ('PASS','The common short-program then free-skate format identifies figure skating. COC nodes80–85 explicitly give the sequence for singles and pairs. Naming the overall sport is acceptable here; ice dance uses rhythm/free dance, so these words must not be read as a universal claim about every discipline or every entrant. All four answers are winter sports, grammar is parallel and the fact is easy.',[P('figure-skating.html',80,85)],[]),
 ('PASS','COC node75 says all Olympic long-track events occur on a 400m oval. The answer explicitly specifies long track, so this note does not erroneously include short track.',[P('long-track.html',75)],[]),
 ('PASS','World Curling node41 explicitly states two teams take turns sliding granite stones toward a House. The independent fact is useful; it need not explain why curling lacks a short program.',[P('curling.html',41)],[]),
 ('PASS','The full Hockey Canada physical page8 states snug fitting improves balance/control. “Плотно подобранные” conveys snug fitting without claiming a harmful overly tight boot. This is a hockey-player equipment fact about the selected sport.',[P('hockey-equipment-guide.pdf',8)],[]),
 ('FIX','The prompt asks the sport with short then free program; the correct note says only that figure skating has short then free program. It adds no fact beyond prompt/key. The underlying format is supported, but the approved correct-note rule requires a useful addition, which may overlap explanation.',[P('figure-skating.html',80,85)],['note']),
 ('PASS','The format is supported for singles/pairs; COC long-track node76 describes racing, World Curling41 gives stones/House, and the institutional hockey terminology describes players/teams. This is a concise common-format explanation, not a claim that all disciplines or all qualifiers have an identical format.',[P('figure-skating.html',80,85),P('long-track.html',75,76),P('curling.html',41),P('iihf-terminology.html',71,72)],[])
],
'017':[
 ('FIX','COC biathlon nodes73,86–91 directly supports skiing with stops for shooting; the fact itself is easy and the revised wording no longer pads it with technical jargon. However winter-sports-014 already asks for the athlete who combines skiing and rifle shooting, with key Биатлонист. Changing athlete-name to sport-name checks the same relation, violating the approved direct/inverse duplicate calibration. The author linked snowboard instead of biathlon, so the displayed source must also be corrected.',[P('biathlon.html',73),P('biathlon.html',86,91)],['duplicate','source']),
 ('FIX','The correct note repeats skiing and stops for targets, the exact prompt/key fact. “По мишеням” does not add meaningful knowledge to “для стрельбы” in this context. It is true per COC biathlon86–91, but needs a useful own additional fact under the approved rule.',[P('biathlon.html',86,91)],['note']),
 ('PASS','COC cross-country node73 defines classic/free techniques and explains their difference. The current note accurately states the two techniques. Its author proof about parallel snowboard giant slalom is unrelated; independent support is rebound to the complete cross-country original.',[P('cross-country-skiing.html',73)],[]),
 ('PASS','COC alpine nodes71–85 divides alpine skiing into speed/technical categories and describes challenging turns/gates. The current note accurately covers the sport. Author halfpipe proof is unrelated; this receipt supplies the actual alpine passage.',[P('alpine-skiing.html',71,85)],[]),
 ('PASS','COC ski-jumping70–71 explicitly sums distance/style points. The short Russian note is a useful accurate fact about ski jumping. Author slopestyle proof is unrelated; the complete ski-jumping original supplies support.',[P('ski-jumping.html',70,71)],[]),
 ('FIX','COC biathlon88 gives a minute per miss specifically in the individual event; node91 gives a 150m penalty loop in sprint. “В описанном COC формате” never names the format and is editorial/source jargon rather than a usable scope qualification. The displayed source is Snowboard. The first sentence is correct, but the penalty claim needs named individual-race scope (or another clearly supported fact) and a matching biathlon source.',[P('biathlon.html',86,91)],['explanation','source'])
],
'019':[
 ('FIX','IIHF138–139 defines the resurfacer as a vehicle cleaning/smoothing the rink, matching the key. A skate-sharpening machine processes blades and does not traverse the hockey rink; line painting is also not a plausible intermission clean-and-level task. Broader “arena equipment” labels do not make these distractors credible under the actual prompt. The unfamiliar “эджер” adds terminology without resolving the weak alternatives.',[P('iihf-terminology.html',138,139),P('bauer-sharpening.html',708,713),P('white-ice-catalogue-2025.pdf',6)],['easy']),
 ('HOLD','The current author proof is IIHF face-off circles/spots, which contains no edger fact. The complete Zamboni FAQ only lists Ice Edgers as a product category; it does not establish a separate machine working at the boards. Two primary Zamboni retrievals stalled and are preserved as incomplete non-proof. The fact is plausible but cannot receive verified PASS from these captures. HOLD is an evidence deficit, not an assertion that the fact is false.',[P('zamboni-faq-full.html',7,9,False)],['note']),
 ('PASS','Bauer FAQ708–713 discusses skate edges and grinding wheels making new edges on blades. It supports blade processing and therefore the distinction from the rink surface. The note is an informative own fact rather than a bare “not correct” placeholder.',[P('bauer-sharpening.html',708,713)],[]),
 ('PASS','IIHF138–139 directly gives clean/smooth and colloquial Zamboni brand name. The naming fact adds beyond the prompt/key, and repetition of that addition in explanation is permitted.',[P('iihf-terminology.html',138,139)],[]),
 ('FIX','White Ice complete physical page6 states self-propelled Mark IV is designed for ice paint application. It does not establish that this machine paints arena markings. Page9 describes separate arena line/circle marking equipment. Current note merges self-propelled paint application with markings, while the author proof is a skate fitting page. Narrow the literal to supported paint application or provide a complete primary passage for the combined marking claim; do not treat paint application as automatic proof of line marking.',[P('white-ice-catalogue-2025.pdf',6),P('white-ice-catalogue-2025.pdf',9, support=False)],['note']),
 ('PASS','IIHF138–139 supports cleaning/smoothing and Zamboni as a colloquial brand name. Two sentences are accurate and understandable; overlap with correct note is allowed.',[P('iihf-terminology.html',138,139)],[])
],
'024':[
 ('PASS','Maine statute133,135,137,140–142 distinguishes cabin/chair/railcar/surface tow carriers. Open separate passenger seats identify a chair lift without repeating “кресло” in the question. All four are lifts and have credible contrasting carrier forms; the common chair-lift recognition fact remains easy despite one uncommon alternative. No broad ski-competition claim is made.',[P('maine-ropeway-statute.html',131,142)],[]),
 ('PASS','Maine140 defines surface lifts as passengers staying in contact with ground/snow;142 defines T-bar towing. This useful surface-contact fact is accurate for the T-bar example without claiming every surface lift uses a T.',[P('maine-ropeway-statute.html',140,142)],[]),
 ('PASS','Maine133 explicitly states gondolas transport people in open or enclosed cabins. The note says cabins without adding an unsupported enclosed-only restriction. It is a useful standalone definition of the distractor.',[P('maine-ropeway-statute.html',133)],[]),
 ('PASS','Maine137 states skimobiles use open/enclosed cars riding on a rigid structural system. “Вагоны” rather than “кабины” distinguishes these from gondolas; the unfamiliar label receives an informative accurate definition.',[P('maine-ropeway-statute.html',137)],[]),
 ('PASS','The question specifies open seating; the correct note additionally states partially enclosed chairs also occur, directly supported by Maine135. That useful definition extends beyond the exact asked configuration and can overlap the explanation.',[P('maine-ropeway-statute.html',135)],[]),
 ('PASS','Maine131–142 supports all four contrasts: chairs, cabins, cars on rigid structure and surface towing. Two sentences are clear, neither imposes a competition context nor conflates skimobile cars with gondola cabins.',[P('maine-ropeway-statute.html',131,142)],[])
]}
IDS=['winter-sports-'+s for s in reviews];cards=[]
for id in IDS:
 q=next(c for c in Q if c['id']==id);ar=next(c for c in A['cards'] if c['questionId']==id)
 assert sha(authorcanon(q))==ar['cardCanonicalSha256']
 fs=[]
 literals=[json.dumps([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],ensure_ascii=False,separators=(',',':'))]+[x['note'] for x in q['answers']]+[q['explanation']]
 for n,literal,(v,analysis,pr,rulekeys),af in zip(['prompt-key','note0','note1','note2','note3','explanation'],literals,reviews[id[-3:]],ar['fields']):
  assert literal==af['literal'];assert sha(literal.encode())==af['literalSha256']
  fs.append({'field':n,'literal':literal,'literalSha256':sha(literal.encode()),'verdict':v,'substantiveRead':True,'agentIdentity':os.environ['CODEX_THREAD_ID'],'claimAnalysis':analysis,'approvedRules':[rules[k] for k in rulekeys],'proofs':pr})
 cards.append({'questionId':id,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':sha(authorcanon(q)),'sortedCardSha256':sha(canonical(q)),'literalCard':q,'verdict':'FIX' if any(f['verdict']=='FIX' for f in fs) else 'HOLD' if any(f['verdict']=='HOLD' for f in fs) else 'PASS','fields':fs,'editorialAnalysis':' '.join(f['claimAnalysis'] for f in fs if f['verdict']!='PASS') or 'All six current fields source and editorial PASS.'})
from collections import Counter
base=json.loads(subprocess.check_output(['git','show','373136051452dc66c3abca6c15e5c6d677dc7b74:src/content/topics/winter-sports.json']))['questions']
assert [c['id'] for c in base]==[c['id'] for c in Q]
assert all((a['difficulty'],a['correctIndex'])==(b['difficulty'],b['correctIndex']) for a,b in zip(base,Q))
changed=[b['id'] for a,b in zip(base,Q) if a!=b];assert set(changed)==set(IDS)
assert Counter(c['difficulty'] for c in Q)=={'easy':40,'medium':40,'hard':20}
slots={d:dict(Counter(c['correctIndex'] for c in Q if c['difficulty']==d)) for d in ['easy','medium','hard']}
assert all(set(v.values())=={5 if d=='hard' else 10} and set(v)=={0,1,2,3} for d,v in slots.items())
receipt={'agentIdentity':os.environ['CODEX_THREAD_ID'],'nativeIdentityEvidence':'CODEX_THREAD_ID read from task environment; independent of author01a12cc1-9d5d-74a1-99ba-6377bdfaed21','role':'independent source and editorial reader','authorIdentity':A['agentIdentity'],'authorRevision':REV,'authorReceipt':str(R/'author-receipt-frozen.json'),'scopeExactIds':IDS,'scopeCount':5,'fieldCount':30,'canonicalRecipes':{'cardCanonicalSha256':'SHA256 UTF8 json.dumps(card,ensure_ascii=False,separators=(comma,colon)), preserves JSON property order, no newline; matches author receipt','sortedCardSha256':'same with sort_keys=True','literalSha256':'SHA256 literal UTF8, no newline; prompt-key compact JSON triple'},'cardVerdictCounts':dict(Counter(c['verdict'] for c in cards)),'fieldVerdictCounts':dict(Counter(f['verdict'] for c in cards for f in c['fields'])),'boundary':'Only five pilot cards reviewed; protected95 and remaining28 not certified or edited. Narrow partner014 comparison only. No content/planning/claim/runtime edits. Historical569e224 receipt unchanged. No novel note-fact criterion: definitions are useful; correct addition may overlap explanation. No full suite/build/deploy.','checks':{'changedIdsSinceAuthorBaseline':changed,'idsOrderClassesCorrectIndicesUnchanged':True,'difficultyCounts':dict(Counter(c['difficulty'] for c in Q)),'slotCounts':slots,'currentWorktreeTopicEqualsFrozen70863ab':Path('src/content/topics/winter-sports.json').read_bytes()==(R/'current-topic-frozen.json').read_bytes()},'duplicateFindings':[{'questionId':'winter-sports-017','partner':'winter-sports-014','type':'same skiing-plus-shooting defining relation; athlete vs sport inverse','partnerCardSha256':sha(canonical(Q[13])),'partnerPrompt':Q[13]['prompt'],'partnerKey':Q[13]['answers'][Q[13]['correctIndex']]['text'],'approvedRule':rules['duplicate']},{'questionId':'winter-sports-007','partner':'winter-sports-073','type':'related binding functions: joins versus releases; record candidate only, no automatic duplicate rejection and no remaining28 audit'}],'crossTopicDuplicateCheck':'Targeted prompt-key scan of catalogue for ski+shoot, short/free program, boot connection, resurfacer and open seated lift; no meaningful cross-topic partner found. Not global semantic absence certification.','cards':cards}
(R/'reader-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
protected=[{'questionId':c['id'],'sortedCardSha256':sha(canonical(c))} for c in Q if c['id'] not in IDS]
(R/'scope-readback.json').write_text(json.dumps({'authorRevision':REV,'protected95':protected,'protected95AggregateSha256':sha(canonical(protected)),'topicRawSha256':sha((R/'current-topic-frozen.json').read_bytes()),'topicGitBlob':subprocess.check_output(['git','rev-parse',REV+':src/content/topics/winter-sports.json']).decode().strip(),'evidenceOnly':True},indent=2)+'\n')
print(receipt['cardVerdictCounts'],receipt['fieldVerdictCounts'])
