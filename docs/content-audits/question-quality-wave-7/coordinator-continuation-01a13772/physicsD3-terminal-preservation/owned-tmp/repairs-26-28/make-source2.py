import json,hashlib,os,copy
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'
src=b+'/repair-packet-26-28-edition2.json'; out=b+'/repair-packet-26-28-source2.json'
d=json.load(open(src)); H=lambda x:hashlib.sha256(x.encode()).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
# New independent edition; preserve all predecessors byte-for-byte.
d['schema']='mindbattle-independent-source2-26-27-with-28-hold-v1'
d['edition']='source2'; d['producerNativeThreadId']='01a137d3-c9ba-7260-be2b-42f25ee03ab6'
d['revisionNote']='Source2 independently fixes the Meissner option-note bindings; #26 uses same-frequency intensity change to keep flux I/(hf) source-consistent; #28 is retained as explicit HOLD because the latest numeric substitution does not meet frozen Hard.'
t26=next(t for t in d['targets'] if t['index']==26)
t27=next(t for t in d['targets'] if t['index']==27)
t28=next(t for t in d['targets'] if t['index']==28)
# #26 consistent with the captured primary's fixed-frequency proportionality; both clauses are necessary.
t26['prompt']='Металл имеет работу выхода φ и пороговую частоту f₀=φ/h. На него падает свет частоты 1,5f₀; затем интенсивность удваивают, сохраняя ту же частоту. Как изменятся максимальная кинетическая энергия фотоэлектронов и их число за единицу времени?'
t26['opts']=['Kmax удвоится до φ; число электронов за секунду удвоится.','Kmax останется 0,5φ; число электронов за секунду удвоится.','Kmax удвоится до φ; число электронов за секунду не изменится.','Kmax останется 0,5φ; число электронов за секунду не изменится.']
t26['key']=1;t26['correctIndex']=1
t26['exp']='Энергия фотона равна hf=1,5φ, поэтому Kmax=hf−φ=0,5φ; она не меняется при удвоении интенсивности, поскольку частота та же. Поток фотонов при фиксированной энергии каждого фотона равен I/(hf), поэтому удвоение I удваивает поток. При неизменном квантовом выходе число фотоэлектронов за секунду также удваивается.'
t26['notes']=['При постоянной частоте энергия каждого фотона hf не меняется; удвоение интенсивности увеличивает число фотонов, а не энергию каждого электрона.','В модели источника отдельный фотон поглощается отдельным электроном и передаёт ему свою энергию; это объясняет, почему Kmax остаётся прежней, хотя событий эмиссии становится больше.','Максимальная энергия определяется hf−φ, а не интенсивностью: при 1,5f₀ она равна 0,5φ, не φ.','При неизменной частоте и квантовом выходе поток фотонов и число выбитых электронов пропорциональны интенсивности; удвоение интенсивности не оставляет скорость эмиссии прежней.']
# replace card and group literals + individualized pair reasons
r26={
'composite':('The captured §29.2 passage gives f₀=φ/h and KEe=hf−BE; substituting f=1.5f₀ and BE=φ yields 0.5φ in both trials.','The four choices form a 2×2 outcome grid: unchanged/doubled Kmax crossed with unchanged/doubled count, so both requested results are needed to identify index 1.'),
'explanation':('The capture says Kmax is independent of intensity and electron emission rate is proportional to intensity; for fixed f each photon has energy hf, so photon flux scales as I/(hf).','The derivation states the fixed-frequency condition before applying the two different response rules, preventing the rate argument from being confused with per-electron energy.'),
'note0':('The source says increasing intensity yields more electrons of the same energy; it does not raise the energy of each emitted electron.','This note diagnoses the single mistaken energy clause while preserving the distractor’s correct count clause.'),
'note1':('The primary passage states that individual photons are absorbed by individual electrons and the electron gains the photon’s energy.','The correct note contributes the microscopic interaction fact, beyond the numerical outcome in stem and answer.'),
'note2':('At fixed f the source relation KEe=hf−BE is unchanged, whereas the emission rate follows intensity; this option reverses both outcomes.','This rationale maps separately to each clause of the distractor instead of giving a generic rejection.'),
'note3':('OpenStax identifies maximum kinetic energy as independent of intensity and electron count per unit time as proportional to intensity.','This note explains why an unchanged rate is incompatible with the stated doubled intensity.'),
'difficulty':('To select the key, the solver must apply work-function subtraction to determine Kmax and independently use photon flux/count scaling at fixed frequency.','Each option states both observables in parallel and has a comparable length; neither response alone marks the keyed pair.'),
'sourceMetadata':('The complete pinned AP §29.2 paragraph contains threshold, one-photon/one-electron behavior, intensity-rate dependence, and the Einstein energy equation.','This single exact primary passage supports the coupled prompt and the additional correct-note fact.')}
# #27 correct notes: each distractor's actual false clause is named explicitly.
t27['notes']=[
'Сверхпроводник вытесняет магнитное поле при переходе. Нулевое сопротивление идеального проводника само по себе такого вытеснения не требует.',
'При нулевом сопротивлении E=0, поэтому уже существующий магнитный поток идеального проводника сохраняется; вытеснение требует свойства сверхпроводника.',
'В слабом внешнем поле сверхпроводник является идеальным диамагнетиком: результирующее магнитное поле внутри его объёма равно нулю.',
'Идеальный проводник может сохранить исходный поток, но сверхпроводник вытесняет поле при переходе ниже критической температуры.'
]
r27={
'composite':('The pinned §9.8 passage says normal-state field lines are expelled at the superconducting transition, while its E=0 derivation prevents prior flux change in an ideal conductor.','Each option names both materials in the same order; the keyed pairing is selected by evaluating both clauses, not by length or extra precision.'),
'explanation':('The source separates the observed Meissner expulsion from Faraday flux conservation when E=0; these are distinct material behaviors.','The explanation follows those two claims in order and connects them to the pre-existing-field condition in the stem.'),
'note0':('The superconducting sample expels its prior normal-state field on transition; the option’s claim that it retains that field is the false clause.','This note identifies the SC-history error in option 0 directly, without incorrectly characterizing the ideal conductor.'),
'note1':('When E=0 the source derives dΦm/dt=0, so an ideal conductor does not have to expel its pre-existing flux.','Option 1 gets the superconducting clause right; this note isolates its erroneous claim about the ideal conductor.'),
'note2':('The source describes perfect diamagnetism: under an applied weak field the net internal magnetic field in the superconductor is zero.','This keyed note adds a useful primary-source property beyond the two cooling histories stated in the prompt and answer.'),
'note3':('The Meissner passage says field is expelled when the normal sample becomes superconducting; retaining the initial SC field is the false clause.','Option 3 correctly allows ideal-conductor flux retention, so the note targets only its mistaken superconducting behavior.'),
'difficulty':('The distinction depends on transition history: one model expels pre-existing field, while zero resistance alone preserves flux.','The options remain matched two-clause histories of similar length, so neither the wording nor the correct ideal-conductor clause singles out the key.'),
'sourceMetadata':('The three pinned §9.8 contexts cover Meissner expulsion, perfect diamagnetism, and the E=0/Faraday argument.','The exact source location jointly supports the keyed comparison and the additional fact in note 2.')}
# update target/card/group hashes and reasons
for t,r,notes in [(t26,r26,t26['notes']),(t27,r27,t27['notes'])]:
 i=t['index']; card=t['proposedRuntimeCard']; card['prompt']=t['prompt'];card['explanation']=t['exp'];card['answers']=[{'text':a,'note':n} for a,n in zip(t['opts'],t['notes'])]
 for g in ('composite','explanation','note0','note1','note2','note3','difficulty','sourceMetadata'):
  value={'composite':{'prompt':t['prompt'],'orderedAnswerTexts':t['opts'],'correctIndex':t['correctIndex']},'explanation':t['exp'],'note0':t['notes'][0],'note1':t['notes'][1],'note2':t['notes'][2],'note3':t['notes'][3],'difficulty':'hard','sourceMetadata':card['source']}[g]
  t['groups'][g].update({'proposedGroup':value,'proposedGroupSha256':H(canon(value)),'SOURCEreason':r[g][0],'EDITORIALreason':r[g][1]})
 t['hashBindings'].update({'proposedCanonicalSha256':H(canon(card)),'proposedWhole8Sha256':H(canon([t['prompt'],t['opts'],t['correctIndex'],t['exp'],*t['notes']])),'proposedClassMetaSha256':H(canon({'correctIndex':t['correctIndex'],'difficulty':'hard','frozenCorrectIndex':t['correctIndex'],'frozenDifficulty':'hard'})),'proposedSourceMetadataSha256':H(canon(card['source'])),'proposedRuntimeFieldSha256':{k:H(canon(v)) for k,v in card.items()}})
# Evidence binding: raw byte range and normalized complete source facts.
t26['sourceBinding']={'captureCommit':'8a7522ee69dea7abd4ccbe17f4ecff95d7d599e5','capturedSourcePath':'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/physics-cd-next10-pages/photon-full-ranges/assembled-original-entity.body','bodySha256':'9161ce4769d0aae0d22de1f96bbec576ef85e2670c4b1b8ab963f7753c877fac','startByte':115543,'endByteExclusive':129730,'domLocator':'p#import-auto-id1495207','normalizedLiteral':t26['sourceContextPassages'][0]['normalizedText'],'factsUsed':['photon energy hf','threshold f0=φ/h','electron rate proportional to intensity','maximum kinetic energy independent of intensity','KEe=hf−BE','individual photon transfers energy to individual electron'],'fluxDerivation':'For monochromatic light at fixed frequency, each photon carries hf. Intensity is energy flux per area; photon number flux is therefore I/(hf). With unchanged f, doubling I doubles photon flux. The captured source separately states electron rate proportional to intensity; unchanged quantum yield carries that ratio to electron emission.'}
t27['sourceBinding']={'captureCommit':'8a7522ee69dea7abd4ccbe17f4ecff95d7d599e5','capturedSourcePath':'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/capture-only/physics20-29-current.json#cards[index=27].primaryEvidence.typedPrimaryContextPassages','bodySha256':'ac895716acb670d984a58a4009502d3b3839d1d8699ad4d80f40f545f4221de1','ranges':[{'startByte':103644,'endByteExclusive':103917,'domLocator':'p#fs-id1172101758770'},{'startByte':107352,'endByteExclusive':107351,'domLocator':'p#fs-id1172099559884'},{'startByte':108003,'endByteExclusive':109002,'domLocator':'p#fs-id1172102116006'}],'factsUsed':['normal-state field lines are expelled on transition','superconductors have perfect diamagnetism and zero net internal field','if E=0 magnetic flux cannot change','zero resistance alone does not imply Meissner effect'],'normalizedLiteralSourceContexts':t27['sourceContextPassages']}
# Correct byte ranges from immutable source context records, not guessed offsets.
for r in t27['sourceContextPassages']:
 if r.get('domNodeType')=='paragraph':
  if 'normal state' in r.get('normalizedText',''): t27['sourceBinding']['ranges'][0]={'startByte':r['startByte'],'endByteExclusive':r['endByteExclusive'],'domLocator':'p#fs-id1172101758770'}
  elif 'interesting' in r.get('normalizedText','').lower(): t27['sourceBinding']['ranges'][1]={'startByte':r['startByte'],'endByteExclusive':r['endByteExclusive'],'domLocator':'p#fs-id1172099559884'}
  elif 'If E is zero' in r.get('normalizedText',''): t27['sourceBinding']['ranges'][2]={'startByte':r['startByte'],'endByteExclusive':r['endByteExclusive'],'domLocator':'p#fs-id1172102116006'}
# #28 explicit hold: candidate gets archived, no proposed runtime output or new rationale claims.
t28['targetState']='HOLD'
t28['holdReasons']=['The prior revision is mostly substitution into three supplied formulas and does not establish a meaningful Hard operation.','The previous answer set exposed λ≈1.67 Å in three options and included a wavelength/geometry shortcut; no new prompt or answer set is proposed here.','Frozen Hard remains unchanged. Human/coordinator review is required before a new design is authored.']
t28['heldPriorDraft']={'proposedRuntimeCard':t28.pop('proposedRuntimeCard'),'groups':t28.pop('groups'),'hashBindings':t28.pop('hashBindings'),'previousDraftSha256':'842a8cb3b38863e3c232440312884a480413d1cf2ddd61de198a47e4e8c76b4f'}
t28['proposedRuntimeCard']=None
t28['sourceEditorialPairs']=None
t28['qualification']='HOLD; no new candidate or source qualification asserted.'
d['targetStatuses']={'26':'CANDIDATE_FOR_COORDINATOR_REVIEW','27':'CANDIDATE_FOR_COORDINATOR_REVIEW','28':'HOLD'}
d['identityAndPreservation']['countBefore']=550;d['identityAndPreservation']['countAfterCoordinatorUpdate']=557;d['identityAndPreservation']['remainingBefore']=1450;d['identityAndPreservation']['remainingAfterCoordinatorUpdate']=1443;d['identityAndPreservation']['repairQualityCredit']=0;d['identityAndPreservation']['humanAcceptance']='NOT_PERFORMED'
# Full/current preimages, ID order, protected97 and neighbors are preserved from the prior verified bundle.
assert len(d['identityAndPreservation']['fullCurrent100IDOrder'])==100 and len(d['identityAndPreservation']['protected97Records'])==97
assert t26['correctIndex']==1 and t27['correctIndex']==2 and t26['difficulty']==t27['difficulty']=='hard'
assert all(len(t['groups'])==8 for t in (t26,t27))
open(out,'w').write(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print(os.path.getsize(out),hashlib.sha256(open(out,'rb').read()).hexdigest())
for t in (t26,t27): print(t['index'],'groups',len(t['groups']),'unique source reasons',len({g['SOURCEreason'] for g in t['groups'].values()}),'unique editorial reasons',len({g['EDITORIALreason'] for g in t['groups'].values()}),'answers', [len(x['text']) for x in t['proposedRuntimeCard']['answers']])
print('28',t28['targetState'],t28['proposedRuntimeCard'])
