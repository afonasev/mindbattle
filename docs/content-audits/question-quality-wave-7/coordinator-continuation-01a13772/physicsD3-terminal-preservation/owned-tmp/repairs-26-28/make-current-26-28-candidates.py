import json,hashlib,os,math
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'; root='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
receipt=json.load(open(b+'/physics20-29-current.json'))
applyp=root+'/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/physics27-opaque-apply-receipt.json'
apply=json.load(open(applyp)); topic_path=root+'/src/content/topics/physics.json'; topic_raw=open(topic_path,'rb').read(); topic=json.loads(topic_raw)
H=lambda x:hashlib.sha256(x.encode('utf-8') if isinstance(x,str) else x).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
rawsha=H(topic_raw); assert rawsha==apply['topicRawSha256After']=='dc323403f844b3f792a173bedf441d3ecf1fd90e7175adb7ba24055b9121a8d4'
current={q['id']:q for q in topic['questions']}; order=[q['id'] for q in topic['questions']]
assert len(order)==100 and len(set(order))==100 and len(apply['protectedOther99'])==99
# Frozen ID order should equal the order recorded in the pre-apply guard packet.
source2=json.load(open(b+'/repair-packet-26-28-source2.json'))
expected=source2['identityAndPreservation']['fullCurrent100IDOrder']; assert order==expected
# Cross-bind all 99 guards to the post-apply current topic.
for x in apply['protectedOther99']:
 assert x['id'] in current and H(canon(current[x['id']]))==x['canonicalSha256']
assert apply['target']['afterCanonicalSha256']==H(canon(current['physics-meissner-effect']))

def field(i):
 c=next(x for x in receipt['cards'] if x['index']==i)
 actual=current[c['id']]
 assert canon(actual)==canon(c['currentCard'])
 return c,actual
c26,old26=field(26); c28,old28=field(28)
# Source context verification directly uses the immutable e6 receipt ranges.
def verify_contexts(i):
 c=next(x for x in receipt['cards'] if x['index']==i)
 cap=c['primaryEvidence']['sourceCapture']; path=root+'/'+cap['bodyPath']; body=open(path,'rb').read()
 assert H(body)==cap['sha256']
 passages=c['primaryEvidence']['typedPrimaryContextPassages']
 for x in passages: assert body[x['startByte']:x['endByteExclusive']]==x['literalUtf8'].encode()
 return {'capture':cap,'passages':passages}
s26=verify_contexts(26); s28=verify_contexts(28)
# Existing captured general-wave intensity definition, used as an explicitly stated inference premise.
inten_path='docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/capture-only/physics30-49-gaps/49/assembled-original-entity.body'
inten_body=open(root+'/'+inten_path,'rb').read(); assert H(inten_body)=='c4786e44925e83c13eeb8cc1ba8a0d9d6f9c78ee5c72764b0c1670cfb17d91fc'
inten_start,inten_end=106616,107077; inten_raw=inten_body[inten_start:inten_end]
inten_literal='A useful quantity for describing the loudness of sounds is called sound intensity. In general, the intensity of a wave is the power per unit area carried by the wave. Power is the rate at which energy is transferred by the wave. In equation form, intensity I is'
# Extract normalized text using HTML/entity collapse and preserve as exact saved literal record.
import re,html
itxt=html.unescape(re.sub(r'<[^>]+>',' ',inten_raw.decode('utf-8'))); itxt=' '.join(itxt.split()); itxt=re.sub(r'\s+([.,;:!?])',r'\1',itxt); assert itxt==inten_literal

def source_card(title,url): return {'title':title,'url':url,'verifiedAt':'2026-10-14'}
# Candidate #26: two independently necessary ratios, with I/(hf) transparently identified as a derivation, not a quote.
prompt26='Металл имеет работу выхода φ и пороговую частоту f₀=φ/h. Сначала на него падает монохроматический свет частоты 1,5f₀ и энергетической интенсивности I; затем частоты 2,25f₀ и интенсивности 3I. Квантовый выход в обоих режимах одинаков. Как изменятся максимальная кинетическая энергия фотоэлектронов и их число за секунду?'
answers26=[
 {'text':'Kmax возрастёт в 2,5 раза; число электронов за секунду утроится.','note':'Верный расчёт энергии не делает поток фотонов пропорциональным одной лишь I при смене частоты: число фотонов равно энергетическому потоку, делённому на hf.'},
 {'text':'Kmax возрастёт в 2,5 раза; число электронов за секунду удвоится.','note':'При фотоэффекте отдельный поглощённый фотон передаёт свою энергию отдельному электрону; поэтому энергия одного электрона и число событий эмиссии меняются по разным соотношениям.'},
 {'text':'Kmax возрастёт в 3,5 раза; число электронов за секунду удвоится.','note':'Уравнение Kmax=hf−φ требует вычесть работу выхода в обоих режимах: 1,25φ/0,5φ=2,5, а не 3,5.'},
 {'text':'Kmax возрастёт в 3,5 раза; число электронов за секунду утроится.','note':'Здесь смешаны две величины: Kmax зависит от избытка hf над φ, а число фотоэлектронов при постоянном выходе следует за потоком фотонов I/(hf).'}]
exp26='В первом режиме hf=1,5φ, поэтому Kmax=hf−φ=0,5φ; во втором hf=2,25φ и Kmax=1,25φ. Отношение энергий равно 2,5. Для монохроматического пучка интенсивность I — энергия, переносимая за единицу площади и времени; энергия фотона равна hf, поэтому поток фотонов выводится как I/(hf). Его отношение во втором режиме к первому: (3I/(2,25hf₀))/(I/(1,5hf₀))=2. При одинаковом квантовом выходе во столько же раз меняется число электронов за секунду.'
card26={'id':old26['id'],'difficulty':'hard','prompt':prompt26,'answers':answers26,'correctIndex':1,'explanation':exp26,'source':source_card('OpenStax College Physics AP §29.2 The Photoelectric Effect','https://openstax.org/books/college-physics-ap-courses/pages/29-2-the-photoelectric-effect')}
# Candidate #28: no precomputed wavelength, formula, or order cue; requires theoretical chain then an independent diffraction-order check.
prompt28='В опыте Дэвиссона—Джермера электроны начинают из покоя и ускоряются разностью потенциалов 54 В. Их рассеивают на никелевой поверхности с периодом решётки a=2,15 Å; интенсивный максимум наблюдается при угле φ≈50°. Какой порядок максимума согласуется с волновой длиной электрона, предсказанной по ускоряющему напряжению? Используйте mₑ=9,11×10⁻³¹ кг, e=1,60×10⁻¹⁹ Кл и h=6,63×10⁻³⁴ Дж·с.'
answers28=[
 {'text':'Эксперимент согласуется с максимумом второго порядка.','note':'Для второго порядка 2λ должно совпасть с a sinφ; при этих данных расчётная волна близка к a sinφ, поэтому множитель два лишний.'},
 {'text':'Ни один целый порядок не согласуется с экспериментом.','note':'Из напряжения получается λ≈1,67 Å, а геометрическая величина a sin50°≈1,65 Å; их отношение близко к целому, а не к нецелому.'},
 {'text':'Эксперимент согласуется с максимумом третьего порядка.','note':'Для третьего порядка требовалось бы 3λ≈5,0 Å, тогда как измеренная геометрия даёт a sin50°≈1,65 Å.'},
 {'text':'Эксперимент согласуется с максимумом первого порядка.','note':'Опыт Дэвиссона—Джермера на никеле стал первым свидетельством электронных волн; близость теоретической длины волны к независимому дифракционному условию поддержала гипотезу де Бройля.'}]
exp28='Электрон получает кинетическую энергию K=eΔV=8,64×10⁻¹⁸ Дж. Нерелятивистский импульс p=√(2mₑK)≈3,97×10⁻²⁴ кг·м/с, поэтому λ=h/p≈1,67 Å. Независимая геометрия поверхности даёт a sinφ≈2,15 sin50°≈1,65 Å. Из условия поверхностного максимума nλ=a sinφ следует n≈1,65/1,67≈0,99, то есть согласуется первый порядок в пределах округления данных.'
card28={'id':old28['id'],'difficulty':'hard','prompt':prompt28,'answers':answers28,'correctIndex':3,'explanation':exp28,'source':source_card("OpenStax University Physics Volume 3 §6.5 De Broglie's Matter Waves",'https://openstax.org/books/university-physics-volume-3/pages/6-5-de-broglies-matter-waves')}
# Per-group SOURCE/EDITORIAL pairs: individually written reasons, not reusable templates.
R26={
'composite':('§29.2 supplies the threshold relation and KEe=hf−BE; §14.2 defines general wave intensity as power per area, while §29.2 gives photon energy hf. Together these support the two distinct ratios under fixed yield.','All four outcomes combine an energy ratio and a count ratio; the key requires both subtractions and a frequency-adjusted photon-flux comparison.'),
'explanation':('The photoelectric context distinguishes individual-photon energy from emission rate; the supplemental general-wave definition supplies the energy-flux premise for deriving I/(hf).','The solution labels the photon-flux relation as a derivation and makes assumptions and arithmetic visible instead of misattributing a formula to the source.'),
'note0':('At changing frequency, fixed energy intensity does not imply a fixed photon count: each photon carries hf, so the rate is I/(hf).','This note targets the count-only misconception while retaining the distractor’s correct energy ratio.'),
'note1':('The source says an absorbed photon transfers its energy to an individual electron.','The keyed note adds a microscopic mechanism beyond the requested ratios and identifies why Kmax and count can respond differently.'),
'note2':('The source equation is KEe=hf−BE, and BE=φ=hf₀; applying both frequencies yields 0.5φ and 1.25φ.','This note isolates the arithmetic error in the energy clause; its count clause is otherwise correct.'),
'note3':('The source distinguishes the photon energy hf from how many photons arrive; deriving the flux ratio prevents using the energy-intensity multiplier as the count multiplier.','This note addresses both incorrect clauses together and names the two distinct quantities involved.'),
'difficulty':('The problem requires two coupled but independent operations: work-function subtraction at two frequencies and photon-number flux from energy flux divided by hf.','Every option states both results in a parallel structure, so identifying either one alone cannot identify the answer.'),
'sourceMetadata':('The main source is the complete AP §29.2 photoelectric passage; §14.2 is additionally bound only for its explicit general definition of wave intensity.','The metadata distinguishes direct photoelectric facts from the cross-source inference needed for spectral photon flux.')}
R28={
'composite':('§6.5 gives the electron acceleration-energy/momentum relation, λ=h/p, the nickel lattice spacing, and the independent surface condition nλ=a sinφ.','No formula, derived wavelength, or diffraction order is supplied in the stem; the keyed comparison requires both theoretical and geometric results.'),
'explanation':('The primary source’s 54 eV electron example yields a theoretical wavelength near 1.67 Å and compares it with the observed diffraction wavelength near 1.64 Å.','The explanation independently repeats the K→p→λ derivation and then checks the measured angle against the integer-order condition.'),
'note0':('The primary condition includes the order factor n; for the supplied data the ratio a sinφ/λ is near one, not two.','This note names the exact factor-of-two order error in the distractor.'),
'note1':('With approximate inputs, n≈0.99 is the expected first integer order; exact equality is not required of rounded measurements.','This note explains why a small numerical difference does not mean the de Broglie prediction fails.'),
'note2':('Three copies of the predicted wavelength exceed the measured a sinφ value by roughly a factor of three.','The note checks the distractor against the independent geometry rather than relying on an answer-label memory.'),
'note3':('The captured historical paragraph identifies Davisson–Germer as the first evidence of electron waves and reports nickel diffraction maxima.','The keyed note adds historical experimental significance after the calculation, without leaking the order or wavelength in the prompt.'),
'difficulty':('The operation connects electrical work, nonrelativistic momentum, matter wavelength, and a separately measured diffraction constraint.','The options vary only the inferred order/agreement in parallel prose; they contain no computed wavelength shortcut.'),
'sourceMetadata':('The saved §6.5 contexts cover the de Broglie equation, acceleration experiment, nickel spacing, surface diffraction condition, and observed agreement.','The citation supports the complete reasoning chain and the additional first-evidence note from the same primary section.')}

def pack_target(c,card,ctx,reasons,extra_source=None):
 groups={}
 for g in ['composite','explanation','note0','note1','note2','note3','difficulty','sourceMetadata']:
  val={'composite':{'prompt':card['prompt'],'orderedAnswerTexts':[x['text'] for x in card['answers']],'correctIndex':card['correctIndex']},'explanation':card['explanation'],'note0':card['answers'][0]['note'],'note1':card['answers'][1]['note'],'note2':card['answers'][2]['note'],'note3':card['answers'][3]['note'],'difficulty':card['difficulty'],'sourceMetadata':card['source']}[g]
  groups[g]={'proposedGroup':val,'proposedGroupSha256':H(canon(val).encode()),'SOURCEreason':reasons[g][0],'EDITORIALreason':reasons[g][1]}
 return {'index':c['index'],'id':c['id'],'status':'HARD_CANDIDATE_PENDING_COORDINATOR_REVIEW','currentFullCard':c['currentCard'],'currentCanonicalSha256':c['canonicalSha256'],'currentWhole6Sha256':c['authorWhole6Sha256'],'currentClassMeta':{'difficulty':c['currentCard']['difficulty'],'correctIndex':c['currentCard']['correctIndex']},'frozenClassMetaSha256':(lambda z: z['hashBindings'] if 'hashBindings' in z else z['heldPriorDraft']['hashBindings'])(next(x for x in source2['targets'] if x['index']==c['index']))['currentClassMetaSha256'],'proposedRuntimeCard':card,'proposedCanonicalSha256':H(canon(card).encode()),'proposedWhole6Sha256':H(canon([card['prompt'],[x['text'] for x in card['answers']],card['correctIndex'],card['explanation'],*[x['note'] for x in card['answers']]]).encode()),'proposedClassMetaSha256':H(canon({'correctIndex':card['correctIndex'],'difficulty':card['difficulty'],'frozenCorrectIndex':card['correctIndex'],'frozenDifficulty':card['difficulty']}).encode()),'groups':groups,'primaryContexts':ctx,'additionalInferenceSource':extra_source}
source26binding={'primaryCapture':s26['capture'],'primaryContexts':s26['passages'],'inferenceOnlySupplement':{'title':'OpenStax Physics §14.2 Sound Intensity and Sound Level (general wave-intensity definition)','url':'https://openstax.org/books/physics/pages/14-2-sound-intensity-and-sound-level','bodyPath':inten_path,'bodySha256':H(inten_body),'startByte':inten_start,'endByteExclusive':inten_end,'normalizedLiteral':itxt,'scope':'The sentence defines intensity generally for waves and power as energy transfer rate; it does not itself state photon flux for EM radiation.'},'sourceInferenceAndConditions':{'derivedRelation':'photon number flux = energy intensity/(energy per photon) = I/(hf).','assumptions':['monochromatic beam at each frequency','I is energy flux per area-time, not photon-number flux','same illuminated area and no frequency-dependent losses between comparisons','constant electron-per-incident-photon quantum yield as stated in the prompt'],'directSourceClaims':['§29.2 identifies photon energy hf and Kmax=hf−BE','§29.2 says individual photons transfer energy to individual electrons','§29.2 treats emission rate as intensity-dependent and maximum electron energy as intensity-independent'],'caveat':'The §29.2 paragraph does not explicitly print I/(hf); it also phrases the rate result as proportional to intensity and no other characteristic in its property list. This packet treats the cross-frequency I/(hf) ratio as an inference from energy flux and hf under the stated assumptions, not as a direct quotation. Coordinator must review this interpretation; source qualification and quality credit are not asserted.'}}
# 28 direct passages from saved capture only; no new fetch.
protected98=[{'index':i,'id':qid,'canonicalSha256':H(canon(current[qid]).encode())} for i,qid in enumerate(order) if qid not in {'physics-photoelectric-threshold-frequency','physics-debroglie-wavelength'}]
# correct identifier spelling is physics-de-broglie-wavelength
protected98=[{'index':i,'id':qid,'canonicalSha256':H(canon(current[qid]).encode())} for i,qid in enumerate(order) if qid not in {'physics-photoelectric-threshold-frequency','physics-de-broglie-wavelength'}]
protected98=[x for x in protected98 if x['id']!='physics-de-broglie-wavelength']
assert len(protected98)==98 and {x['id'] for x in protected98}==set(order)-{'physics-photoelectric-threshold-frequency','physics-de-broglie-wavelength'}
# Include current 27 applied card and accepted seven in protected register, proving new guard baseline.
accepted7=[]
for i in (20,21,22,23,24,25,29):
 c=next(x for x in receipt['cards'] if x['index']==i); actual=current[c['id']]
 accepted7.append({'index':i,'id':c['id'],'canonicalSha256':H(canon(actual).encode()),'fullCurrentCard':actual})
assert next(x for x in protected98 if x['id']=='physics-meissner-effect')['canonicalSha256']==apply['target']['afterCanonicalSha256']
# Bind source bodies at exact pinned byte ranges.
verifyAll={'photoelectric':s26,'deBroglie':s28,'supportIntensity':{'path':inten_path,'bodySha256':H(inten_body),'range':[inten_start,inten_end]}}

t26=pack_target(c26,card26,s26,R26,source26binding)
t28=pack_target(c28,card28,s28,R28,None)
packet={'schema':'mindbattle-source-hard-candidates-current-26-28-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','scope':'Only current physics #26 and #28. Source-only proposals in owned TMP; no repo/runtime/QA/Git changes. #27 remains applied and protected, no wording change.','currentBaseline':{'commit':'8af9d4df1a859e46e120908033a423869441fc55','currentHEAD':'8af9d4df1a859e46e120908033a423869441fc55','topicPath':'src/content/topics/physics.json','topicBytes':len(topic_raw),'topicRawSha256':rawsha,'opaqueApplyReceiptPath':'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/physics27-opaque-apply-receipt.json','opaqueApplyReceiptSha256':H(open(applyp,'rb').read()),'full100IDOrder':order,'full100IDOrderSha256':apply['full100IDOrderSha256'],'protectedOther98ForTwoTargetScope':protected98,'protectedOther98Count':len(protected98),'applied27':{'id':'physics-meissner-effect','canonicalSha256':apply['target']['afterCanonicalSha256'],'fullCurrentCard':current['physics-meissner-effect']},'acceptedSevenCards':accepted7,'source2AndPriorPacketsRemainImmutable':[{'path':'repair-packet-26-28-source2.json','sha256':H(open(b+'/repair-packet-26-28-source2.json','rb').read())},{'path':'physics27-current-neighbor-binding-addendum.json','sha256':H(open(b+'/physics27-current-neighbor-binding-addendum.json','rb').read())},{'path':'physics27-provenance-dedup-correction.json','sha256':H(open(b+'/physics27-provenance-dedup-correction.json','rb').read())},{'path':'physics27-protected-guard-correction.json','sha256':H(open(b+'/physics27-protected-guard-correction.json','rb').read())},{'path':'physics27-provenance-origin-correction.json','sha256':H(open(b+'/physics27-provenance-origin-correction.json','rb').read())}]},'sourceBodyIntegrity':verifyAll,'candidates':[t26,t28],'decisionStatus':{'26':'HARD_SOURCE_CANDIDATE; photon-flux source inference expressly disclosed and requires coordinator review; source status not qualified.','28':'HARD_SOURCE_CANDIDATE; requires full energy→momentum→wavelength→diffraction comparison; source status not qualified.','currentCount':557,'remaining':1443,'qualityCredit':0,'humanAcceptance':'NOT_PERFORMED','productionApply':'NOT_PERFORMED'}}
# exact metadata hashes and pair cardinality
assert len(t26['groups'])==8 and len(t28['groups'])==8
for t in packet['candidates']:
 assert len({g['SOURCEreason'] for g in t['groups'].values()})==8 and len({g['EDITORIALreason'] for g in t['groups'].values()})==8
 assert set(t['proposedRuntimeCard'])=={'id','difficulty','prompt','answers','correctIndex','explanation','source'}
 assert all(set(a)=={'text','note'} for a in t['proposedRuntimeCard']['answers'])
for ix in (26,28):
 c=next(x for x in receipt['cards'] if x['index']==ix); assert c['currentCard']['difficulty']=='hard'
 assert c['currentCard']['correctIndex']==(1 if ix==26 else 3)
# reproduce proposed answers' numerical checks as arithmetic integrity, not product test
k1=1.5-1;k2=2.25-1
rate=(3/2.25)/(1/1.5)
K=54*1.60e-19;p=math.sqrt(2*9.11e-31*K);lam=6.63e-34/p/1e-10;n=(2.15*math.sin(math.radians(50)))/lam
assert abs(k2/k1-2.5)<1e-12 and abs(rate-2)<1e-12 and abs(n-1)<0.02
out=b+'/current-26-28-source-hard-candidates.json';open(out,'w').write(json.dumps(packet,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',H(open(out,'rb').read()),'targets',[(x['index'],len(x['groups'])) for x in packet['candidates']],'protected98',len(protected98),'27',packet['currentBaseline']['applied27']['canonicalSha256'],'flux ratio',rate,'n',n)
