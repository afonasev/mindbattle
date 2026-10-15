"""Bind personally reviewed FINAL cycle1; writes only this new audit directory."""
import hashlib
import itertools
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
BASE = ROOT / 'docs/content-audits/question-quality-wave-8'
COORD = BASE / 'coordinator-01a13f31'
AUTHOR = BASE / 'process-v2-gear-newsolution3-cycle1-01a13f31/author'
def read(p): return json.loads(p.read_text())
def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha(v): return hashlib.sha256(canonical(v)).hexdigest()
def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
apply_path = COORD/'apply-gear-newsolution3-cycle1.json'
qa_path = COORD/'qa-gear-newsolution3-cycle1.json'
apply = read(apply_path)
qa = read(qa_path)
topic_path = ROOT/'src/content/topics/engineering-machines.json'
topic = read(topic_path)
byid = {q['id']:q for q in topic['questions']}
initial_path = OUT.parent/'receipt.json'
initial = read(initial_path)
proof = read(AUTHOR/'sourceproof.json')
author_peers = read(AUTHOR/'peer-snapshot.json')
raw_sources = {s['key']:s for s in proof['rawSources']}
def loc(key,locator):
 s=raw_sources[key]
 return {'path':s['path'],'url':s['url'],'locator':locator}
spur=loc('spur','L37-L41: parallel-axis spur/no thrust; L39 pressure angle/involute; L40 profile shift')
helix=loc('dims','Section 4.3 L246-L269; definitions L250-L258, hob L264-L266, necessary mating conditions L268')
thrust=loc('helical','P1 L169-L218, especially L216-L217; P2 L339-L350, especially L344-L346')
bevel=loc('dims','L420-L423 (bevel axes and pitch cones); L568-L572 (complete retained Zerol section)')
worm=loc('dims','L680-L691: complete retained worm geometry/type context; 90° L683, nonparallel/nonintersecting L689')
locking=loc('worm','Physical lines 1-6: entire retained bounded section ② Self-locking of worm gears')

J={
11:{'status':'PASS',
 'level':'PASS hard: specialized relation between tooth orientation and axial force is required. The helical alternative shares parallel shaft geometry and is substantive; bevel/worm can be excluded using shaft arrangement. No mandatory calculation.',
 'extra':'PASS: typical 20° pressure angle and common industrial involute profile are facts about the spur option beyond absence of axial thrust (KHK spur L39).',
 'grounds':[
  ('KHK spur L37 establishes parallel tooth traces and no axial thrust. Helical catalog P2 L344-L346 gives the contrast. All four answers now consistently name transmission families; one key in the stated ideal parallel-axis case.',[spur,thrust,bevel,worm]),
  ('Explanation names the spur construction and correctly limits the absent force to tooth inclination; does not claim the complete mechanism is immune to axial loads from other components.',[spur]),
  ('L39 supports typical pressure angle and industrial involute prevalence. Useful extra own-option facts.',[spur]),
  ('L250-L265 defines normal/transverse tooth systems and modules. Compatible parameters of mating are a true qualification, not a false universal claim.',[helix]),
  ('L569 explicitly says zero mean spiral angle and straight-bevel calculation equations apply. The previous unsupported assertion that Zerol has straight teeth is removed. No inherited tooth-shape inference.',[bevel]),
  ('L689 directly says worm mesh connects nonparallel/nonintersecting axes. The former unsupported material/friction/wear attribution is gone; this is a sourced own-option geometry fact.',[worm])],
 'variants':[
  ('PASS: nominative transmission label answers the requested type.','Strong candidate in the stipulated parallel-axis pair.','KEY: KHK spur L37 says no axial thrust from axis-parallel tooth faces; other listed type with parallel external axes, helical, has thrust.','PASS: usual pressure angle and involute prevalence are sourced extra facts of this option.',[spur,thrust]),
  ('PASS: same transmission category and syntax.','Strong distractor with same shaft arrangement; requires force/helix knowledge.','WRONG: helix produces axial force, catalog P2 L344-L346.','PASS: normal/transverse modules and compatible mating parameters belong to helical gears.',[helix,thrust]),
  ('PASS: same transmission category.','Related gear family, eliminable by intersecting-axis geometry. This is meaningful context narrowing.','WRONG for parallel-axis pair; KHK L422 describes intersecting bevel axes.','PASS: zero spiral angle and applicability of straight-bevel equations are precisely supported at L569; no claim of straight Zerol teeth.',[bevel]),
  ('PASS: now a transmission label like the other options; former wheel/transmission mismatch resolved.','Related gearing; skew shafts distinguish it from the stipulated parallel arrangement.','WRONG: worm geometry L689 is nonparallel/nonintersecting, contrary to the prompt context.','PASS: note teaches that same source-backed geometry about its own option; canonical overlap with #14 is allowed.',[worm])],
 'defects':[]},
12:{'status':'HOLD',
 'level':'PASS hard: equal helix-angle magnitude and opposite hand in external parallel-axis meshing are a specific technical condition. Wrong alternatives change a meaningful geometric parameter; straight teeth can be eliminated without resolving the remaining pair. No mathematics required.',
 'extra':'PASS: same hob reusable across different helix angles at fixed normal-system module/pressure-angle parameters is a manufacturing fact beyond the mating answer (L257-L266). «Червячный инструмент» is understandable but «червячная фреза» is more precise; that wording alone is not a HOLD. Normal-system context supplies the meaning of mn and pressure angle.',
 'grounds':[
  ('L268 says meshing helical gears MUST have equal angle and opposite hands. The prompt asks a required combination, so the key itself is correct and unique. Same-hand/different-angle choices fail required conditions.',[helix]),
  ('HOLD: first sentence accurately states the helix conditions. New second sentence says these TWO conditions ENSURE geometric mating, converting necessary conditions into sufficient ones. Equal/opposite helices cannot mesh if tooth modules/pitches are incompatible. The retained catalog explicitly also requires identical module (P1 L216); L253-L258 defines normal pitch/module. This is a new error introduced by replacing the former editorial sentence, not a new audit rule.',[helix,thrust]),
  ('L257-L258 defines the normal system; L264-L266 permits the same hob for fixed mn/pressure angle regardless of beta. Current Russian conveys an own-option manufacturing fact; no confusion between gear fabrication and the meshing of two different-angle gears is asserted.',[helix]),
  ('The old same-hands calque is removed. Current note explicitly states same direction fails the external parallel pair, correctly naming the particular mistaken rule instead of a generic negative placeholder.',[helix]),
  ('Current note identifies the exact necessary angle equality that the compound wrong statement violates. Specific correction of a false rule is allowed and supported by L268.',[helix]),
  ('Spur L37 describes cylindrical gears whose tooth faces run parallel to the axis. Current note is true and about this straight-tooth option, without assigning the key properties to it.',[spur])],
 'variants':[
  ('PASS: answer supplies the requested combination of helix-line attributes.','Specific combination; not a name lottery or length cue.','KEY: necessary equal-angle/opposite-hand condition at L268; no second valid choice supplied. The explanation sufficiency error does not change the key.','PASS: normal-system hob reuse is independently supported; manufacturing extra fact is not a repeat of mating conditions.',[helix]),
  ('PASS: answer and note use clear Russian; no «руки» calque.','Plausible reversal of required hand condition for an external pair.','WRONG: identical directions contradict opposite-hand condition at L268.','PASS: note describes precisely the erroneous same-direction assertion in its stated external parallel context.',[helix]),
  ('PASS: parallel compound construction.','Plausible confusion with crossed-axis screw gearing; varies angle but retains opposite hand.','WRONG: different angles fail L268 for this parallel pair.','PASS: exact confused equality rule is named; not a generic placeholder.',[helix]),
  ('PASS: a complete descriptive option for a tooth-line arrangement.','Related limiting case; easily eliminated from a helical pair but leaves the two specific helix tests to solve.','WRONG: straight axis-parallel teeth describe spur, not the stated helical pair.','PASS: spur L37 supports the classification and tooth direction of its own option.',[spur])],
 'defects':[{'code':'NECESSARY_CONDITIONS_CLAIMED_SUFFICIENT','field':'explanation sentence 2','literal':'Эти два условия вместе обеспечивают геометрическое сопряжение пары.','ground':'Angle equality and opposite hand are necessary helix conditions, but do not alone ensure geometric mating. A same-angle/opposite-hand pair with incompatible modules has incompatible tooth pitch. KHK dimensions L253-L258 defines pitch/module, L268 says must, and helical catalog P1 L216 separately requires identical module. The catalog-specific number-of-teeth condition is not generalized here.','sourcesLocators':[helix,thrust],'nextAction':'Coordinator retains FINAL HOLD and records adjudication. If later authorized as a concrete new solution, qualify the helix statement as necessary conditions with compatible remaining tooth geometry; this FINAL does not authorize another cycle.'}]},
14:{'status':'PASS',
 'level':'PASS hard: the reader must apply spatial shaft classification, distinguishing perpendicular intersecting bevel axes from perpendicular nonintersecting skew axes and associate the latter with worm gearing. Spur and explicitly parallel external helical options can be narrowed logically, but the remaining bevel-versus-worm choice needs specific mechanical knowledge. No worm noun cue appears in the prompt, no mandatory math, and not merely knowing the angle is enough.',
 'extra':'PASS: non-universality and material/lead/accuracy/bearings/lubrication factors of worm self-locking are independent of the new shaft-layout MAIN. Section ② explicitly supplies this own-option extra fact, whether or not it appeared in an earlier explanation.',
 'grounds':[
  ('KHK L683 says worm meshes generally have 90° shaft angle; L689 says axes are nonparallel/nonintersecting. L422 makes ordinary bevel axes intersect; spur L37 has parallel axes and option3 explicitly restricts helical to parallel axes. Exactly one supplied answer fits. This is not a claim worm is the only possible gearing in all engineering: crossed-helical/hypoid alternatives are not supplied.',[worm,bevel,spur,helix]),
  ('Explanation correctly distinguishes intersecting bevel axes from the required skew axes, then identifies worm. Its comparisons are explicitly with the offered types. The final sentence explains why angle alone is insufficient. All three sentences are useful to the engineering reasoning.',[worm,bevel,spur,helix]),
  ('L422 gives intersecting bevel shafts; L569 supplies Zerol at zero spiral angle. Both are concrete facts about the bevel distractor.',[bevel]),
  ('Complete bounded section ② gives the non-universal self-locking property and each listed factor. This is a useful own-option extra fact unrelated to selecting the shaft geometry.',[locking]),
  ('Korean spur L40 directly gives increased bending strength with positive profile shift and says negative shift may slightly reduce center distance and interference. Current «может» preserves the conditional scope. No former unsupported backlash-versus-center-distance attribution remains.',[spur]),
  ('L268 supplies equal helix-angle/opposite hands. Current note inherits the explicit external parallel-axis scope from its own answer and repeats it in note, closing the earlier scope defect.',[helix])],
 'variants':[
  ('PASS: nominative transmission type fits the question.','Strong distractor: bevel often serves a right-angle drive, so the no-intersection constraint must be understood.','WRONG: bevel axes intersect (L422), violating the key layout constraint.','PASS: intersecting-axis bevel use and Zerol zero spiral angle are both own-family facts.',[bevel,worm]),
  ('PASS: consistent transmission family label.','Requires knowing worm shaft layout; prompt contains no component noun identifying the key.','KEY: generally 90° L683 plus nonparallel/nonintersecting L689 matches the specified layout; unique among offered scopes.','PASS: conditional self-locking and listed influencing factors are independently supported in section ②; note does not imply guaranteed reverse protection.',[worm,locking]),
  ('PASS: consistent category with informative cylindrical qualifier.','Related transmission; can be eliminated using parallel-axis construction without deciding between bevel and worm.','WRONG: spur cylindrical gears connect parallel axes, spur L37; prompt requires perpendicular directions.','PASS: positive/negative profile-shift facts are stated directly in retained Korean L40 and pertain to spur gearing.',[spur]),
  ('PASS: a grammatically complete and explicitly scoped transmission option.','Parallel-shaft qualifier makes this eliminable from the layout, but that narrowing does not reveal worm versus bevel; not itself a key cue.','WRONG: this offered external helical configuration explicitly requires parallel shafts. Crossed-helical gearing would be a different offered type, so it is not a second key.','PASS: equal-angle/opposite-hand rule is true for the same external parallel pair named by the answer; canonical overlap with #12 allowed.',[helix,worm])],
 'defects':[]}
}

entries=[]
for a in apply['applied']:
 n=a['sourceOrder'];q=byid[a['id']];j=J[n]
 assert sha(q)==a['proposedSHA256']==sha(a['proposedCard'])
 literals=[('prompt_ordered_answers_key',{'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']}),('explanation',q['explanation'])]+[('note'+str(i),x['note']) for i,x in enumerate(q['answers'])]
 groups=[{'group':name,'literal':v,'canonicalSHA256':sha(v),'individualGround':g,'sourcesLocators':s} for (name,v),(g,s) in zip(literals,j['grounds'])]
 variants=[]
 for i,(ans,v) in enumerate(zip(q['answers'],j['variants'])):
  triple={'prompt':q['prompt'],'answer':ans['text'],'note':ans['note']}
  variants.append({'slot':i,**triple,'tripleCanonicalSHA256':sha(triple),**dict(zip(['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'],v))})
 entries.append({'id':q['id'],'sourceOrder':n,'stage':'FINAL_SOLE_SUBSTANTIVE_CYCLE1','currentCard':q,'currentCardCanonicalSHA256':sha(q),'matchesAppliedSHA256':True,'status':j['status'],'sixLiteralCanonicalGroups':groups,'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':j['level'],'correctNoteExtraFact':j['extra'],'defects':j['defects'],'frozen':{'id':q['id']==a['beforeCard']['id'],'topicId':topic['id']==apply['topicId'],'sourceOrder':topic['questions'][n-1]['id']==q['id'],'difficulty':q['difficulty']==a['beforeCard']['difficulty'],'correctIndex':q['correctIndex']==a['beforeCard']['correctIndex']}})

previous_sources={x['path']:x for x in initial['evidence']['sources']}
sources=[]
read_notes={
 'spur':('L37-L41 full retained explanatory body','Personally reread Korean spur context, including newly used profile-shift statements L40 for #14. No-thrust L37, extra facts L39, and positive/negative shift are supported; source does not say straight Zerol teeth.'),
 'dims':('L246-L269; L420-L423; L568-L572; L680-L691; L845-L849','Personally reread complete retained normal/transverse/hob context, bevel and Zerol context, and worm geometry context. New MAIN14 is supported by joint 90° L683 and nonintersecting axes L689. L268 states necessary conditions, not sufficiency of only those conditions.'),
 'helical':('P1 L169-L218 and P2 L339-L350','Personally reread product-selection/common-notes context including identical-module requirement L216 and thrust P2 L344-L346. Do not generalize catalog-specific tooth-number requirement. Identical module supplies a concrete omitted geometric compatibility condition.'),
 'worm':('Physical lines 1-6, complete bounded section ②','Personally reread full retained bounded source: wheel-to-worm direction, listed factors, usual single-start 4° threshold and extra brake. New correctnote14 accurately summarizes non-universality/factors.')}
for key,s in raw_sources.items():
 p=ROOT/s['path'];old=previous_sources[s['path']];scope,evidence=read_notes[key]
 assert raw(p)==s['sha256']==old['rawReadSHA256']
 sources.append({'key':key,'path':s['path'],'rawReadSHA256':raw(p),'url':s['url'],'locator':scope,'readEvidence':evidence,'sameSHAAsPersonallyReadINITIAL':True,'INITIALReceipt':str(initial_path.relative_to(ROOT)),'limitations':'Retained rendered primary sections, not newly downloaded full binary. No claim of reading absent diagrams/equation images.'})
save('sources.json',sources)

rels={11:['spur transmission','tooth-inclination axial force','none in ideal mesh','parallel shaft pair'],12:['external helical pair','necessary mating helix geometry','equal angle/opposite directions','parallel shafts'],13:['bevel transmission','pitch-surface geometry','common cone apex enabling intersecting shafts','bevel family'],14:['worm transmission','shaft layout compatibility','90-degree nonintersecting axes','drive layout; among four supplied configurations'],15:['ball bearings','contact/speed choice','high-speed point contact','comparable rolling bearings'],16:['roller bearings','capacity/speed choice','high radial capacity','compact node'],17:['plain bearing','support mechanism','sliding without rolling bodies','sleeve/liner'],18:['thrust bearings','main load direction','axial','rolling-bearing taxonomy'],19:['lap joint','part arrangement','overlap','sheet joint'],20:['butt joint','part arrangement','ends in one plane','joint'],28:['gear drive','transmission principle','tooth engagement','generic drive'],36:['tee joint','part arrangement','end-to-face near right angle','joint']}
actual=[{'sourceOrder':n,'currentCard':topic['questions'][n-1],'canonicalSHA256':sha(topic['questions'][n-1]),'MAIN':m} for n,m in rels.items()]
pairs=[]
for a,b in itertools.combinations(sorted(rels),2):
 if not ({a,b}&{11,12,14}):continue
 reason='Different entity-relation-value-context. Shared gear/load terminology or reuse of canonical note facts is not a MAIN duplicate.'
 if (a,b)==(11,12):reason='Axial force generated by tooth inclination versus mating requirements for the two helix geometries. Neither is the forward/reverse form of the other relation.'
 if (a,b)==(13,14):reason='Both are read in full. #13 asks identification from common-apex pitch-surface geometry for intersecting shafts; #14 selects worm for perpendicular but NONINTERSECTING shafts. They do not ask the same geometry/value or reverse one entity-property mapping. The bevel note in #14 and worm note in #13 are allowed canonical explanatory facts, not MAIN duplication. No protected #13 reopening.'
 if b==28:reason='Generic toothed-wheel engagement definition differs from axial-force, helix-mating and spatial shaft-layout relations. Current #28 was read, not author old snapshot.'
 pairs.append({'a':a,'b':b,'aMAIN':rels[a],'bMAIN':rels[b],'semanticDuplicate':False,'directReverse':False,'ground':reason})
cross=[];topic_hashes=[]
for p in sorted((ROOT/'src/content/topics').glob('*.json')):
 d=read(p);topic_hashes.append({'path':str(p.relative_to(ROOT)),'rawSHA256':raw(p)})
 for n,q in enumerate(d.get('questions',[]),1):
  key=q['answers'][q['correctIndex']];key=key['text'] if isinstance(key,dict) else key
  if re.search(r'шестер|червяч|косозуб|прямозуб|самоторм|зубчат|осев|винтов|храпов|непересека|пересека.*вал|геометри.*ос',q['prompt']+' '+key,re.I):cross.append({'topicId':d['id'],'sourceOrder':n,'currentCard':q,'canonicalSHA256':sha(q),'duplicateWithReviewedMAIN':False,'ground':'Relevant current MAIN selected for full reading; geometric/gear candidates compared with target relations. Icons, gear surface hardening, rack railway, and lexical false positives test different entities/relations.'})
proposed=[{'sourceOrder':x['sourceOrder'],'card':x['card'],'canonicalSHA256':sha(x['card']),'equalsActualCURRENT':sha(x['card'])==sha(byid[x['id']]),'authorStatusInherited':False,'MAIN':rels[x['sourceOrder']]} for x in author_peers['finalProposedCards']]
save('peers.json',{'actualCurrentPeers':actual,'proposedBothSides':proposed,'bilateralMAINcomparison':pairs,'proposedPairComparisons':[x for x in pairs if x['a'] in J and x['b'] in J],'authorSnapshotDrift':[{'id':x['id'],'authorSnapshotSHA256':sha(x['card']),'actualCURRENTCanonicalSHA256':sha(byid[x['id']]),'equal':sha(x['card'])==sha(byid[x['id']])} for x in author_peers['actualCurrentPeers']],'crossCatalogCandidates':cross,'topicSnapshotRawHashes':topic_hashes,'scope':'Protected peers read for comparisons only, not recertified. #37 excluded sourceHOLD. Author mainCurrentPeers is old main context, not actual CURRENT verdict.'})

receipt={'scope':[11,12,14],'stage':'FINAL_SOLE_SUBSTANTIVE_CYCLE1','reviewer':'01a13f48-a5b8-7d92-9904-65117a9c5e3b','branch':'codex/question-quality-wave-6','appliedCommit':'62b8cdb1c5a8ae47e2416797da3dc818695fff54','qaCommit':'cc4dc658e924679464a66760de6e550d79712107','freshRefProvidedByCoordinator':'3952554724f11ce1b3a209aaca722bd7bb148fd2','bindingAuthority':'Exact current-card canonical hashes compared to cycle1 apply, not the age of the provided ref. No Git/index commands used in this FINAL.','pinnedProcess':'12e5581b:.agents/references/question-revision.md','packetContract':{'path':str((COORD/'packet-contract.json').relative_to(ROOT)),'rawSHA256':raw(COORD/'packet-contract.json')},'INITIALHistory':{'path':str(initial_path.relative_to(ROOT)),'rawSHA256':raw(initial_path),'unchanged':True},'hashMethod':'SHA256 UTF8 json.dumps(sort_keys=True,separators=(comma,colon),ensure_ascii=False); rawReadSHA256 over exact bytes.','entries':entries,'counts':{'PASS':2,'HOLD':1},'qualityCredit':0,'evidence':{'sources':'sources.json','peers':'peers.json','apply':{'path':str(apply_path.relative_to(ROOT)),'rawSHA256':raw(apply_path)},'authorSourceproof':{'path':str((AUTHOR/'sourceproof.json').relative_to(ROOT)),'rawSHA256':raw(AUTHOR/'sourceproof.json')},'authorCandidate':{'path':str((AUTHOR/'candidate.json').relative_to(ROOT)),'rawSHA256':raw(AUTHOR/'candidate.json')}},'qaObservedNotReexecuted':{'path':str(qa_path.relative_to(ROOT)),'rawSHA256':raw(qa_path),'passed':qa['numPassedTests'],'total':qa['numTotalTests'],'success':qa['success'],'meaning':'Focused schema checks do not establish editorial truth.'},'execution':{'gitIndexCatalogPlanningClaimsMutated':False,'runtime':'NotRun','tests':'NotRun per assignment; existing QA19 read','build':'NotRun','deploy':'NotRun','subagentsOrNewChats':False,'ownPersistentProcesses':False,'sourceDownloads':False,'temporaryFiles':[]},'nextAction':'Coordinator preserves these new files and adjudicates FINAL PASS11/PASS14 and HOLD12; credit stays zero until root binding. No second fix-cycle authorized. Any later new solution requires explicit scope; do not reopen protected cards without concrete defect.','preservation':'Only final-cycle1 files written; coordinator owns Git preservation. No assertion that this report has been committed or integrated in main.'}
save('receipt.json',receipt)
verify={'entries':len(entries),'groups':sum(len(x['sixLiteralCanonicalGroups']) for x in entries),'variants':sum(len(x['fourFullPromptAnswerNoteVariants']) for x in entries),'currentExactApply':True,'allFrozen':all(all(x['frozen'].values()) for x in entries),'sourceHashesMatchINITIAL':True,'receiptRawSHA256':raw(OUT/'receipt.json'),'sourcesRawSHA256':raw(OUT/'sources.json'),'peersRawSHA256':raw(OUT/'peers.json'),'catalogRawSHA256':raw(topic_path),'INITIALReceiptRawSHA256':raw(initial_path),'checks':'JSON parsing; exact CURRENT/apply hash comparison; frozen fields; 18 group and 12 triple hashes; source hashes; persistent output scope; no runtime/full tests.','qualityCredit':0}
assert verify['allFrozen'] and (verify['entries'],verify['groups'],verify['variants'])==(3,18,12)
save('verification.json',verify)
print(json.dumps(verify,ensure_ascii=False,indent=2))
