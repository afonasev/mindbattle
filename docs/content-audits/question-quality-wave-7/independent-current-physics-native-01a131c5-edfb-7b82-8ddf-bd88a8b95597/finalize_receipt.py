from pathlib import Path
import json,hashlib,subprocess,collections,xml.etree.ElementTree as ET
w=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');assert Path.cwd()==w
o=Path('/private/tmp/mindbattle-physics-reader-01a131c5-current-b3cbbc8');p=w/'docs/content-audits/question-quality-wave-7/physics/first10-successor-native-01a13237-776c-7242-a52b-fff331e038f5'
load=lambda p:json.loads(p.read_text());compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':')).encode();sha=lambda b:hashlib.sha256(b).hexdigest();write=lambda n,d:(o/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
r=load(o/'independent-reader-receipt.json');ctx=load(o/'independent-source-contexts.json');ret=load(o/'catalog-independent-retrieval.json');ns=load(p/'catalog-neighbor-review.json')['fullReviewedCardSnapshots']
allc={c['id']:c for f in sorted((w/'src/content/topics').glob('*.json')) for c in load(f)['questions']}
extraids=['physics-carnot-efficiency-temperatures','physics-ext-thermal-conductivity','physics-ext-specific-heat','physics-ext-latent-heat','laboratories-measurement-balance-mass','engineering-machines-counterweight-balance','weather-climate-inversion-warmer-above','polar-regions-temperature-inversion-polar','oceans-seas-pycnocline-density','oceans-seas-deep-current','oceans-seas-convection-mix']
snap={**ns,**ret['extraCandidateSnapshots'],**{i:allc[i] for i in extraids}}
relations={
'physics-force-si-unit':{'verdict':'PASS','neighbors':['physics-time-unit','physics-length-unit','physics-mass-unit','physics-energy-unit','laboratories-measurement-spring-scale-force','physics-ext-force-interaction'],'reason':'Unit/quantity mapping for force is different from time/length/mass/energy mappings, force instrument and definition. Newton appearing in their distractor notes/explanations is shared supporting knowledge, not another direct or reversed force-unit prompt.'},
'physics-light-speed-vacuum':{'verdict':'PASS','neighbors':['physics-light-vacuum','laboratories-measurement-speed-light-metre','physics-ext-refractive-index','physics-earth-escape-velocity'],'reason':'Rounded numerical c differs from vacuum propagation yes/no, identifying defining constant for metre, refractive-index ratio, and Earth escape speed. Correct note recurs as supporting metre fact, but numeric primary prompt is distinct.'},
'physics-heat-spontaneous-direction':{'verdict':'PASS','neighbors':['physics-entropy-isolated-system','physics-wien-law-hotter-body','materials-heat-capacity-water','physics-carnot-efficiency-temperatures','physics-ext-thermal-conductivity','physics-ext-specific-heat','physics-ext-latent-heat','weather-climate-inversion-warmer-above','polar-regions-temperature-inversion-polar'],'reason':'Direction of spontaneous contact heat transfer differs from entropy monotonicity, emission peak shift, heat-capacity definition, conductivity rate, phase heat, Carnot efficiency and inversion recognition. Two source HOLD notes remain separate from this duplicate assessment.'},
'physics-rainbow-color-separation':{'verdict':'PASS','neighbors':['laboratories-measurement-spectroscope-spectrum','physics-ext-refraction-medium','weather-climate-rainbow-refraction'],'reason':'Names wavelength dependence/dispersion, whereas weather names the visible rainbow, instrument card names spectroscope and refraction card names generic boundary direction change. Shared water-drop scenario does not reverse the same dispersion/name predicate.'},
'physics-newton-third-law':{'verdict':'PASS','neighbors':['physics-ext-impulse-force-time','physics-ext-force-interaction','astronomy-space-gravity-orbits'],'reason':'Equal/opposite interaction pair on two bodies differs from naming impulse, force and gravitational orbital cause. No second question tests the third-law pair directly or inversely in reviewed relevant candidates.'},
'physics-current-si-unit':{'verdict':'FIX','neighbors':['physics-ext-electric-current-charge-flow','physics-closed-circuit','physics-metal-conductor','laboratories-measurement-ammeter-current'],'reason':'Current unit→ampere reverses the explicit ampere→current identification in physics-ext-electric-current-charge-flow. Its charge/time cue is supplementary to the same unit/quantity pair; keep one or change the new primary fact through authorized author scope. Circuit/material/instrument questions themselves are distinct.'},
'physics-water-boiling-standard-pressure':{'verdict':'PASS','neighbors':['physics-water-freezing','physics-absolute-zero-celsius','energy-power-bwr-boils-core'],'reason':'Standard-pressure boiling100°C differs from freezing0°C, absolute zero and reactor construction.100°C appearing in the freezing distractor note does not make the keyed freezing question an inverse boiling question.'},
'physics-sound-vacuum':{'verdict':'PASS','neighbors':['physics-light-vacuum','geology-earth-s-wave-solid','geology-earth-p-wave-fast'],'reason':'Asks mechanical-sound carrier absence, not electromagnetic light propagation or liquid outer-core shear transmission/first arriving P waves. Shared medium/wave terminology alone is not direct/inverse semantic duplication.'},
'physics-mass-weight-distinction':{'verdict':'PASS_WITH_CATALOG_TERMINOLOGY_RISK','neighbors':['physics-ext-mass-matter','aviation-weight-down','spaceflight-microgravity-float','laboratories-measurement-tare-container','laboratories-measurement-balance-mass','engineering-machines-counterweight-balance'],'reason':'Formal Russian support-force distinction differs from inertia naming, orbital freefall mechanism and measuring/taring/balancing mass. Aviation card translates English gravity-defined weight; its convention conflicts if generalized across catalog. Current stem explicitly confines school mechanics, so no new second key; coordinator should track terminology consistency separately without rewriting foreign aviation scope.'},
'physics-density-definition':{'verdict':'PASS','neighbors':['physics-ext-density-mass-volume','oceans-seas-density-mass','rivers-lakes-holomictic-mixing','agriculture-23-3','oceans-seas-pycnocline-density','oceans-seas-deep-current','oceans-seas-convection-mix'],'reason':'Reference-relative density numerical conversion differs from naming mass/volume density, water4°C stratification, pore-inclusive soil density, density gradient and ocean circulation. No other reviewed prompt solves the same reference ratio or reverses the same800↔0.8 fact.'}}
noiseReasons={
'cars-road-transport-bumper-low-speed':'Бампер substring contains ампер; car bumper identity has no electric-current/unit predicate.',
'mountains-volcanoes-suture-zone':'Hot/cold volcanic ash phase deposits in engines; not direction of spontaneous contact heat transfer.',
'chemistry-ext-magnesium-flare':'Metal identified by white combustion light; not wavelength-dependent refraction.',
'materials-precipitation-hardening':'Дисперсионное твердение is alloy precipitation mechanism; not optical dispersion.',
'history-china-easy-01b-02':'Весной/массовые are lexical false positives; Beijing protest square identity is unrelated to mass/weight.',
'history-united-kingdom-medium-02b-05':'Массовые protest/tax naming has no mechanical mass/weight concept.',
'motorsport-b3-m06':'Adding ballast to satisfy minimum and distribution of mass; not formal mass versus support-force definition.',
'plants-fungi-xylem-water':'Xylem constituting wood mass is tissue identification; not mechanical mass versus weight.'}
manualNeighbors=[]
for i,c in snap.items():
 assert c==allc[i]
 rel=[qid for qid,v in relations.items() if i in v['neighbors']]
 reason=noiseReasons.get(i) or ('Full current card read; relevant to '+', '.join(rel)+'. See independent relation-level predicate comparison; neighbor quality itself is outside this10-card certification.')
 manualNeighbors.append({'id':i,'fullCurrentCard':c,'wholeCardSha256':sha(compact(c)),'fullLiteralPersonallyRead':True,'relevantScopeIds':rel,'relationReason':reason,'qualityCertificationOfForeignCard':False})
write('catalog-independent-manual-review.json',{'catalogCardCount':11000,'retrievalOnlyAcrossAll11000':True,'all11000ManuallyReviewed':False,'fullCurrentNeighborsRead':len(manualNeighbors),'snapshots':manualNeighbors,'scopeAdjudications':relations,'authorNeighborGradesInherited':False,'currentInverseDuplicate':'physics-current-si-unit ↔ physics-ext-electric-current-charge-flow'})
# Exact context aliases are explicitly resolved, rather than inventing matching source IDs.
aliases={'NIST-meter-definition-light-speed':'NIST-SI-meter-light-speed','NASA-Hubble-rainbow-raw-bytes':'NASA-hubble-raindrop-rainbow','OpenStax-m54131-third-law-p6':'OpenStax-Newton3-pair','OpenStax-m54306-second-law-p12':'OpenStax-SecondLaw-heat-direction','OpenStax-m54306-external-work-p21':'OpenStax-SecondLaw-external-work','OpenStax-m54314-mechanical-p3':'OpenStax-mechanical-waves-medium','OpenStax-m42466-dispersion-p3':'OpenStax-dispersion-definition','OpenStax-m42466-rainbow-p7':'OpenStax-dispersion-raindrops','OpenStax-m58353-specific-gravity-density-p20':'OpenStax-specific-gravity-ratio'}
ids={c['contextId'] for c in ctx['contexts']};author=load(p/'author-adjudication.json');refs=sorted({x for g in author['manualGroups']+author['difficultyAndSourceMetadata'] for x in g.get('proofRefs',[])})
for ref in refs:
 if ref in ids:aliases[ref]=ref
 if 'Russian' in ref:
  for n in [69,93,94]:
   if 'p'+str(n) in ref:aliases[ref]='Russian-p'+str(n)
write('author-proof-alias-resolution.json',{'authorProofRefs':refs,'resolvedAliases':aliases,'unresolved':[x for x in refs if x not in aliases],'method':'Descriptive author aliases resolved by module/page/topic identity against independently read exact raw contexts. No proofRefs changed in original author package.'})
# Add exact base-unit and mixing contexts personally read to close reference specificity.
html=load(o/'contexts/physics-light-speed-vacuum.paragraphs.json');nist=[x for x in html if 'Definitions of SI Base Units' in x['text'] or 'Ampere – Unit of Electric Current' in x['text'] or 'ampere is defined' in x['text']]
s=next(x for x in ctx['rawAssignments'] if 'light-speed-vacuum.html' in x['path']);ctx['contexts'].append({'contextId':'NIST-ampere-base-unit','sourcePath':s['path'],'sourceURL':s['captureURL'],'rawSha256':s['sha256'],'ownFullParagraphs':nist,'normalization':'Own HTMLParser full heading/paragraph text, entities decoded/whitespace collapsed'})
# Precise note proofRefs instead of whole-card omnibus lists.
proofByNote=[
[['BIPM-SI-table4-force-pressure-joule-watt']]*4,
[['NIST-SI-meter-light-speed']]*4,
[['OpenStax-SecondLaw-heat-direction'],['OpenStax-SecondLaw-external-work'],['OpenStax-SecondLaw-heat-direction'],['OpenStax-SecondLaw-heat-direction']],
[['NASA-wave-diffraction-spectrum','OpenStax-dispersion-raindrops'],['NASA-electromagnetic-field-polarization'],['NASA-wave-interference-spectral-signature','OpenStax-dispersion-raindrops'],['OpenStax-dispersion-definition','OpenStax-dispersion-raindrops']],
[['OpenStax-Newton3-pair'],['OpenStax-Newton3-pair'],['OpenStax-Newton3-pair'],['OpenStax-Newton3-pair','Russian-p69']],
[['BIPM-SI-table4-continued-units'],['NIST-ampere-base-unit','BIPM-ampere-definition-p134'],['BIPM-SI-table4-force-pressure-joule-watt'],['BIPM-SI-table4-continued-units']],
[['OpenStax-m42218-phase-diagrams-p7-fresh-capture']]*2+[['OpenStax-m42218-phase-diagrams-p7-fresh-capture','OpenStax-standard-pressure-p14'],['OpenStax-m42218-phase-diagrams-p7-fresh-capture']],
[['OpenStax-mechanical-waves-medium'],['OpenStax-mechanical-waves-medium'],['OpenStax-mechanical-waves-medium','OpenStax-sound-pressure-p4'],['OpenStax-mechanical-waves-medium']],
[['Russian-p69','Russian-p93'],['Russian-p69','Russian-p93'],['Russian-p93'],['Russian-p69','Russian-p93']],
[['OpenStax-specific-gravity-ratio']]*4]
for i,c in enumerate(r['wholeCards']):
 for row in r['manualGroups']:
  if row['questionId']==c['questionId'] and row['group'].startswith('note'):row['independentProofRefs']=proofByNote[i][int(row['group'][-1])]
 for row in r['choiceReviews']:
  if row['questionId']==c['questionId']:row['independentProofRefs']=proofByNote[i][row['index']]
# Source/editorial counts and snapshots are independent; +0 remains until coordinator gate.
r['catalogReview']='catalog-independent-manual-review.json';r['proofContexts']='independent-source-contexts.json';r['proofAliases']='author-proof-alias-resolution.json';r['sourceCoverageHolds']=['physics-heat-spontaneous-direction.note2','physics-heat-spontaneous-direction.note3']
write('independent-source-contexts.json',ctx);write('independent-reader-receipt.json',r)
source=w/'src/content/topics/physics.json';gitb=subprocess.check_output(['git','show','b3cbbc8:src/content/topics/physics.json']);assert source.read_bytes()==gitb
assert len(r['manualGroups'])==60 and len(r['choiceReviews'])==40 and len(r['difficultyAndSourceMetadata'])==20
assert len({(x['questionId'],x['group']) for x in r['manualGroups']})==60
for c in ctx['contexts']:
 if 'rawElementExcerpt' in c:
  b=c['rawElementExcerpt'].encode();assert sha(b)==c['offsetSliceSha256'];x=ET.fromstring(b'<reader xmlns="http://cnx.rice.edu/cnxml" xmlns:m="http://www.w3.org/1998/Math/MathML">'+b+b'</reader>')[0];assert ' '.join(''.join(x.itertext()).split())==c['ownNormalizedFullParagraph']
write('reader-validation-and-cleanup.json',{'actorNativeId':r['actorNativeId'],'actualCompactions':1,'checks':{'60UniqueGroups':True,'40OrderedNotes':True,'20DifficultyMetadata':True,'80AuthorLiteralHashMatches':True,'10RuntimeSnapshotsCurrent':True,'physicsFileDiskEqualsB3cbbc8':True,'physicsFileSHA256':sha(gitb),'raw13AssignmentsDiskGitBodyB3Header4bf':True,'xmlFullParagraphOffsetNormalizationEquality':True,'contextAliasesUnresolved':load(o/'author-proof-alias-resolution.json')['unresolved'],'catalog11000Parsed':True,'manualNeighborCount':len(manualNeighbors)},'gitStatus':subprocess.check_output(['git','status','--short','--untracked-files=all']).decode(),'ignoredStatus':subprocess.check_output(['git','status','--short','--ignored','--untracked-files=normal']).decode(),'foreignResourcesPreserved':['newadvent-rule-benedict.html foreign modification','foreign __pycache__ and node_modules','physics/weather author work'],'ownedProcesses':'All invoked Python/pdftoppm calls completed synchronously. OS-wide ps denied operation not permitted; no foreign-process claims or termination.','ownedOutputPolicy':'All output retained in own /private/tmp as required pending opaque durable Git transport; cleanup debt is exact-copy confirmation then remove only this temp directory. No unique originals duplicated.','remainingGates':['author repair5whole FIX including metadata/inverse duplicate','primary support for2heat note HOLD','fresh exact whole-card independent recheck','coordinator manual adjudication','opaque durable preservation and own temp cleanup'],'testsBuildDeploy':'NotRun, unnecessary for read-only editorial/source audit; none invoked','certifiedCountIncrease':0})
print('validated',len(manualNeighbors),'neighbors; unresolved aliases',load(o/'author-proof-alias-resolution.json')['unresolved'])
