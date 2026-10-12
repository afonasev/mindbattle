from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as ET,subprocess,collections
w=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');assert Path.cwd()==w
out=Path('/private/tmp/mindbattle-physics-reader-01a131c5-current-b3cbbc8')
p=w/'docs/content-audits/question-quality-wave-7/physics/first10-successor-native-01a13237-776c-7242-a52b-fff331e038f5'
load=lambda f:json.loads(f.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()
write=lambda name,d:(out/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sc=load(p/'current-cards.json')['cards']; author=load(p/'author-adjudication.json'); prov=load(p/'source-provenance.json'); raw=load(out/'raw-original-checks.json')
# Reasons below are independent manual judgments, not copied author grades.
manual=[
[
'Four real SI units are distinct; only newton measures force. The stem needs no unstated model and key3 is unique.',
'N=kg·m/s² agrees with Table4. Applying F=ma to1kg gives the stated acceleration; concise relation adds substance beyond the unit name.',
'Joule belongs to work/energy. Work of1N through1m along its direction implements J=N·m, and the direction qualification avoids a misleading general formula.',
'Pascal belongs to pressure; Pa=N/m² is a useful positive fact about this chosen unit rather than a bare rejection.',
'Watt belongs to power; W=J/s differentiates this plausible SI-unit distractor with its own fact.',
'Correct note adds the derived-unit classification and operational1kg acceleration relation, absent from the stem/key.'
],
[
'Vacuum and nearest1000km/s are explicit.299792.458km/s rounds to300000; the other orders of magnitude are wrong and comparable.',
'Exact299792458m/s converts to the rounded answer and the metre-definition fact is confirmed by NIST; two concise sentences.',
'Correct note adds exact SI value and its defining-constant status, beyond the rounded key.',
'30000/299792.458≈0.100069; approximately one tenth is accurate. This diagnoses the chosen order-of-magnitude error.',
'3000/299792.458≈0.0100069; approximately one hundredth is accurate. The subsequent100-times language is understood at the same stated approximation.',
'3000000/299792.458≈10.0069; approximately tenfold above c is accurate. It need not assert an unrelated material medium.'
],
[
'Initial spontaneous flow is controlled by temperature difference, not mass or heat capacity. The refrigerator caveat concerns nonspontaneous work, so no second key.',
'OpenStax explains spontaneous hot-to-cold transfer and external work for reverse transfer. Equilibrium is the standard two-body contact endpoint; read paragraphs13–15 also describe mixing/equal-temperature endpoint.',
'Correct note supplies isolation and cessation at equal temperatures, a new endpoint fact beyond the initial direction requested.',
'Refrigerator and external work are specifically discussed in paragraph21; this is a positive case for the reverse-direction option.',
'The direction clause is supported by paragraph12. The added claim that mass governs the temperature change needs a primary Q=mcΔT or equivalent context; the supplied second-law module does not establish it for this group. Scientifically plausible, source coverage incomplete.',
'The direction clause is supported. The added heat-capacity/temperature-change relation needs a primary definition or Q=CΔT context; an authored neighbor note is not primary proof. Scientifically plausible, source coverage incomplete.'
],
[
'The stem specifies wavelength dependence of refraction within a water drop, isolating dispersion. Diffraction/interference can separate colours in other instruments, but are not additional keys to this mechanism.',
'OpenStax paragraph7 distinguishes entry/exit refraction from internal reflection and wavelength-dependent index. Explanation accurately names the mechanism without saying reflection itself causes dispersion.',
'NASA full paragraphs describe diffraction/gratings separating wavelengths; OpenStax attributes droplet colour separation to wavelength-dependent refraction. This is a distinct instrument fact for the chosen option.',
'NASA polarization paragraph defines electromagnetic-field alignment; this is an informative positive property, appropriately distinguished from droplet colour separation.',
'FIX: NASA says gratings/slits separate wavelengths via diffraction and subsequent interference, then energy peaks are detected/recorded; the next paragraph identifies emission lines from substances. It does not support interference forming spectral-energy peaks. Current causal wording conflates instrumental separation with the source spectrum.',
'Factual support PASS: water index varies with wavelength and rays refract at different angles. Editorial FIX: both dependency and resulting colour separation already appear in the current stem; replacing refraction with index does not add an independent learning fact beyond the prompt/key.'
],
[
'The pair is equal in magnitude, opposite in direction, and acts on different bodies. Wrong alternatives each change a defining condition, so key1 is unique.',
'OpenStax paragraphs5–8 specify the action/reaction pair and separate objects. Forces on different objects do not cancel in the free-body sum for one object; useful follow-through.',
'Opposite directions are positively supplied for the same pair; different bodies alone do not make same-direction answer correct.',
'Correct note adds why the pair does not cancel in a single-body force sum, beyond the selected equal/opposite/different-body conditions.',
'Correctly redirects the pair to different bodies, while allowing sums of other forces on a single body. It does not claim that all opposed forces must be a third-law pair.',
'Equal interaction forces do not depend on unequal masses; mass changes acceleration under the same force. OpenStax pair plus Russian textbook69 F/a=mass supports the inference.'
],
[
'Source fact PASS: ampere is the SI current unit. Editorial FIX for inverse duplicate: physics-ext-electric-current-charge-flow asks which quantity is measured in amperes and carries charge per time, keyed to current. This new stem reverses its already tested current↔ampere association, without a distinct primary fact. Q/t clue in the neighbor does not erase its explicit amperes cue.',
'BIPM134 states SI ampere and C=A·s; hence1A=1C/s. The charge-rate relation adds content beyond unit recognition.',
'Volt is potential difference; BIPM continued Table4 directly identifies it. This is a substantive fact about the wrong option.',
'Correct note adds base-unit classification beyond the requested unit name. Classification is corroborated by the SI base-unit context, not historical two-wire ampere definition.',
'Coulomb is electric charge and C=A·s. This specifically explains this distractor, rather than denying it is an ampere.',
'Ohm is resistance and Ω=V/A. Ratio relation is independently useful and directly in continued Table4.'
],
[
'Clean water, standard atmospheric pressure and approximate Celsius value are explicit;100°C is the unique key. All numeric options are boiling-temperature candidates.',
'Fresh m42218 paragraph7 states100°C at1atm and rising boiling temperature with pressure; altitude/lower pressure explains the other direction. No use of partial failed capture.',
'90°C can occur at reduced pressure; the altitude example is consistent with lower atmospheric pressure. It supplies conditions for the chosen numeric alternative.',
'110°C needs pressure above standard; the pressure-cooker example is directly supported by the phase-diagram paragraph and is useful for this option.',
'Correct note adds the pressure conversion≈101.3kPa, beyond the phrase standard atmosphere and key. Own full m58353 paragraph14 explicitly states standard pressure101.3kPa; this collateral primary context is added without modifying author proofRefs.',
'120°C requires elevated pressure and cannot be the equilibrium boiling point in an open vessel at standard pressure. This is a positive conditional fact about120, not solely a negative key. Similar pressure dependence in110 note is not itself a duplicate question or reason to reject;120 note supplies the open-vessel contrast.'
],
[
'Ideal vacuum lacks a material medium. Mechanical versus electromagnetic propagation gives a single key2. Wrong options expose absorption, field-kind and material/speed misconceptions; the faster-than-light story is weak but does not create ambiguity.',
'OpenStax paragraphs3–4 establishes material medium for sound, particle/pressure transmission, and light in vacuum. Explanation connects mechanism and contrast in three brief sentences.',
'Absorption requires a medium; absence of a material carrier is the vacuum issue. Note positively differentiates these mechanisms.',
'Sound is mechanical; light/radio are electromagnetic and can traverse vacuum. The note gives the wrong option its actual contrasting wave class.',
'Correct note adds pressure variation in gases and transmission through solid/liquid media, beyond the stem/key requirement for particles.',
'Ideal vacuum means absent material carrier, not merely too few particles or a slower allowed speed. This targets the chosen sparse-medium misconception.'
],
[
'School mechanics is explicitly specified, making Russian support/suspension definition applicable. Mass/inertia versus support force is a unique key3; English aviation weight convention is not imported as a second definition.',
'Russian69 defines mass via response to force;93 distinguishes force on body from weight on support and gives P=mg without acceleration;94 gives P=m(g−a), implying P=0 for free fall a=g while gravity persists. Earth/Moon comparison follows same mass and different g.',
'Mass is not changed merely by local gravitational acceleration; weight acts on support/suspension rather than being volume. This positively corrects both parts of the chosen option.',
'The note correctly distinguishes mass from force and specifies gravity acts on the body; it does not confuse the support force with gravity.',
'Intended P=mg relation is source supported, but editorial FIX: antecedent of их численные значения is килограмм и ньютон, names of units. Units do not have body-dependent numeric values linked through g. State mass in kg and weight in N explicitly, under the current rest/support condition.',
'Correct note adds quantitative P=mg at rest beyond the conceptual keyed distinction. The support condition is retained, avoiding applying mg to accelerating/free-falling weight.'
],
[
'The reference water temperature, pressure and density are given; relative density0.8 is dimensionless.ρ=0.8×1000=800kg/m³; unitless, decimal-factor and addition alternatives are distinct and wrong.',
'Own original MathML equation defines ratio to water; solving for density and multiplying gives800. Explanation states dimensional distinction and exact computation concisely.',
'0.8 is the unitless ratio, not density inkg/m³. Multiplication by reference density is a specific positive correction for this option.',
'8000 gives ratio8 rather than0.8; the note identifies a tenfold arithmetic/decimal error, independently relevant to this choice.',
'1000.8 treats a ratio as an additive density increment; the source ratio equation implies multiplication. This notes the actual operation error.',
'Source fact PASS:ρ=relative density×water density is exactly derived from the primary equation. Editorial FIX: current note only repeats the calculation already asked and solved by the key; it adds no fact beyond current prompt/key. A dimensionless/unit-invariant ratio fact from following paragraph21 is available as a repair, but no edit is made.'
]]
assert len(manual)==10 and all(len(x)==6 for x in manual)
source_overrides={(2,4):'HOLD',(2,5):'HOLD',(3,4):'FIX'}
editorial_overrides={(3,4):'FIX',(3,5):'FIX',(5,0):'FIX',(8,4):'FIX',(9,5):'FIX'}
diffReasons=[
'Easy: widely taught SI force-unit recognition; neighboring real SI units are plausible confusions, no calculation required.',
'Easy: widely known rounded300000km/s; specified rounding prevents requiring specialist exact-value recall.',
'Easy: ordinary hot/cold-contact intuition; mass/heat capacity options test common confusion without thermodynamic formalism.',
'Easy retained with caution: basic school optics vocabulary, not numerical Snell-law calculation. Spectrum/drop mechanism makes dispersion distinguishable from adjacent terms. No difficulty promotion merely to rebalance quota; note defects remain separate.',
'Easy: widely taught action/reaction rule, with different-body condition explicitly among options.',
'Easy: school unit recognition; inverse duplicate is an editorial problem, not grounds to change difficulty.',
'Easy: familiar water-boiling100°C with standard pressure explicit; no phase-diagram calculation required.',
'Easy: familiar sound-in-space contrast; mechanism is specified in options. Weak faster-than-light distractor is noted as a style risk, not a new factual ambiguity.',
'Medium: demands a formal Russian mass/weight/support distinction rather than colloquial weight-as-mass; multiple force definitions must be discriminated.',
'Medium: uses reference-relative density and dimensional conversion. Arithmetic is simple, but the tested concept is ratio-to-reference density rather than common name/definition recognition.'
]
# Individual factual support references are resolved to exact original contexts below; inherited grades never used.
proofs=[['BIPM-SI-table4-force-pressure-joule-watt'],['NIST-SI-meter-light-speed'],['OpenStax-SecondLaw-heat-direction','OpenStax-SecondLaw-external-work'],['OpenStax-dispersion-definition','OpenStax-dispersion-raindrops','NASA-wave-diffraction-spectrum','NASA-wave-interference-spectral-signature','NASA-electromagnetic-field-polarization'],['OpenStax-Newton3-pair','Russian-p69'],['BIPM-ampere-definition-p134','BIPM-SI-table4-continued-units','BIPM-SI-table4-force-pressure-joule-watt'],['OpenStax-m42218-phase-diagrams-p7-fresh-capture','OpenStax-standard-pressure-p14'],['OpenStax-mechanical-waves-medium','OpenStax-sound-pressure-p4'],['Russian-p69','Russian-p93','Russian-p94'],['OpenStax-specific-gravity-ratio','OpenStax-specific-gravity-unit-invariance-p21']]
groups=[];choices=[];metadata=[];whole=[]
for i,c in enumerate(sc):
 ag=[g for g in author['manualGroups'] if g['questionId']==c['id']];assert len(ag)==6
 for j,g in enumerate(ag):
  lit=g['exactCurrentLiteral'];actual={'prompt':c['prompt'],'orderedAnswerTextStrings':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']} if j==0 else c['explanation'] if j==1 else c['answers'][j-2]['note']
  assert lit==actual; encoded=compact(lit) if isinstance(lit,dict) else lit.encode();assert sha(encoded)==g['literalSha256']
  row={'questionId':c['id'],'group':g['group'],'exactCurrentLiteral':lit,'literalSha256':sha(encoded),'literalRecipe':'Scalar exact UTF-8; composite compact JSON preserving declared insertion order','authorProofRefsPreserved':g.get('proofRefs',[]),'independentProofRefs':proofs[i],'sourceVerdict':source_overrides.get((i,j),'PASS'),'editorialVerdict':editorial_overrides.get((i,j),'PASS'),'reason':manual[i][j],'independentlyJudged':True}
  row['verdict']='FIX' if 'FIX' in [row['sourceVerdict'],row['editorialVerdict']] else 'HOLD' if 'HOLD' in [row['sourceVerdict'],row['editorialVerdict']] else 'PASS';groups.append(row)
  if j>=2:choices.append({'questionId':c['id'],'variant':g['group'],'index':j-2,'isKey':j-2==c['correctIndex'],'currentAnswerText':c['answers'][j-2]['text'],'currentNote':lit,'noteSha256':row['literalSha256'],'sourceVerdict':row['sourceVerdict'],'editorialVerdict':row['editorialVerdict'],'verdict':row['verdict'],'individualReason':manual[i][j]})
 for g in [x for x in author['difficultyAndSourceMetadata'] if x['questionId']==c['id']]:
  lit=c['difficulty'] if g['group']=='difficulty' else c['source'];assert lit==g['exactCurrentLiteral'];encoded=compact(lit) if isinstance(lit,dict) else lit.encode();assert sha(encoded)==g['literalSha256']
  if g['group']=='difficulty':reason=diffReasons[i];v='PASS'
  else:
   reason='Captured primary work, public URL, title identity and verification date align with this current source. Git-pinned XML originals establish chapter identity; normalization is explicitly recorded. Verification date is capture provenance, not a claim of fresh network access during this reader turn.';v='PASS'
   if i==0:reason='Primary BIPM brochure and URL are correct, but historical definitions of units describes neither the visible work title nor the current Table4 evidence used for this card. Use the current9th-edition brochure title, as the current-unit card already does. This is a metadata wording defect, not invalid raw proof.';v='FIX'
   if i==8:reason='Personally viewed cover/title page: Г.Я.Мякишев, М.А.Петрова, Физика10класс, базовый уровень, Москва2019; printed69/93/94 confirm§§14/19 and definitions. Filename11 is not used to infer grade. Current source metadata matches the visible work.'
  metadata.append({'questionId':c['id'],'group':g['group'],'exactCurrentLiteral':lit,'literalSha256':sha(encoded),'literalRecipe':'Scalar exact UTF-8 or insertion-order compact JSON','verdict':v,'reason':reason,'authorProofRefsPreserved':g.get('proofRefs',[])})
 cg=[x for x in groups if x['questionId']==c['id']];cm=[x for x in metadata if x['questionId']==c['id']]
 verdict='FIX' if any(x['verdict']=='FIX' for x in cg+cm) else 'HOLD' if any(x['verdict']=='HOLD' for x in cg+cm) else 'PASS'
 composite={'prompt':c['prompt'],'orderedAnswerTextStrings':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'explicitKey':c['answers'][c['correctIndex']]['text']}
 whole.append({'questionId':c['id'],'verdict':verdict,'wholeCard':c,'wholeCardSha256':sha(compact(c)),'wholeCardHashRecipe':'Compact UTF-8 JSON preserving current runtime field order','explicitKeyComposite':composite,'explicitKeyCompositeSha256':sha(compact(composite)),'explicitKeyCompositeRecipe':'Compact UTF-8 JSON in declared prompt/orderedAnswerTextStrings/correctIndex/explicitKey order; intentionally distinct from author three-field composite','blockingGroups':[x['group'] for x in cg+cm if x['verdict']!='PASS']})
# Contexts independently reconstructed from original raw bytes, not author paraphrases.
contexts=[];aliases={}
for ac in prov['contexts']:
 f=next((w/s['path'] for s in prov['sources'] if Path(s['path']).name==ac['sourceFile']),None);assert f
 rawbytes=f.read_bytes();loc=ac['locator'];r={'contextId':ac['contextId'],'sourcePath':str(f.relative_to(w)),'rawSha256':sha(rawbytes),'rawBytes':len(rawbytes),'sourceURL':ac['sourceUrl'],'locator':loc,'authorContextLiteralPreserved':ac['literal']}
 if f.suffix=='.cnxml':
  paras=list(ET.fromstring(rawbytes).iter('{http://cnx.rice.edu/cnxml}para'));n=loc['paragraphOrdinal'];para=paras[n-1];text=' '.join(''.join(para.itertext()).split());r['ownNormalizedFullParagraph']=text;r['normalization']='ElementTree descendant text, XML entities decoded, whitespace collapsed; empty cross-reference labels retained as omissions, not reconstructed'
  start,end=loc['rawByteStart'],loc['rawByteEnd'];r['rawElementExcerpt']=rawbytes[start:end].decode();r['offsetSliceSha256']=sha(rawbytes[start:end]);ET.fromstring(b'<reader xmlns="http://cnx.rice.edu/cnxml" xmlns:m="http://www.w3.org/1998/Math/MathML">'+rawbytes[start:end]+b'</reader>')
  if ac['contextId']=='OpenStax-specific-gravity-ratio':
   r['followingEquationExactRaw']=rawbytes[loc['equationRawByteStart']:loc['equationRawByteEnd']].decode();r['followingParagraphOwnText']=' '.join(''.join(paras[n].itertext()).split());r['authorLiteralIsSynthesisNotVerbatimQuote']=True
 elif f.suffix=='.html':
  own=next(x for x in load(out/'html-original-readback.json') if x['path']==str(f.relative_to(w)));r['ownFullParagraphs']=own['paragraphsRead'];r['normalization']=own['normalization'];start,end=loc['rawByteStart'],loc['rawByteEnd'];r['originalOffsetSlice']=rawbytes[start:end].decode();r['offsetSliceSha256']=sha(rawbytes[start:end])
 else:
  txt=out/'contexts'/('bipm-physical'+str(loc['pdfPage'])+'.txt');r['ownFullPageText']=txt.read_text();r['normalization']='Own pypdf full-page extraction; Table4 pixels also personally inspected at PDF139/140 = printed137/138';r['pixelEvidence']=str(out/'rendered'/('bipm-table-'+str(loc['pdfPage'])+'.png')) if loc['pdfPage'] in [139,140] else None
 contexts.append(r)
# Collateral primary paragraphs needed by groups and not in author17.
for name,module,n in [('OpenStax-standard-pressure-p14','m58353',14),('OpenStax-specific-gravity-unit-invariance-p21','m58353',21),('OpenStax-sound-pressure-p4','m54314',4)]:
 s=next(s for s in prov['sources'] if module in s['path']);f=w/s['path'];b=f.read_bytes();matches=list(re.finditer(rb'<para\b[^>]*>.*?</para>',b,re.S));m=matches[n-1];root=ET.fromstring(b);para=list(root.iter('{http://cnx.rice.edu/cnxml}para'))[n-1]
 contexts.append({'contextId':name,'sourcePath':s['path'],'sourceURL':s['captureURL'],'rawSha256':sha(b),'rawBytes':len(b),'locator':{'module':module,'paragraphOrdinal':n,'rawByteStart':m.start(),'rawByteEnd':m.end()},'ownNormalizedFullParagraph':' '.join(''.join(para.itertext()).split()),'rawElementExcerpt':m.group().decode(),'offsetSliceSha256':sha(m.group()),'normalization':'Own original ElementTree full paragraph; whitespace collapsed'})
for n in [69,93,94]:
 f=p/('russian-physics-p'+str(n)+'-'+str(n).zfill(3)+'.png');s=next(x for x in prov['sources'] if 'russian-physics' in x['path']);contexts.append({'contextId':'Russian-p'+str(n),'sourcePath':s['path'],'sourceURL':s['captureURL'],'rawSha256':s['sha256'],'rawBytes':s['bytes'],'locator':{'pdfPhysicalPage':n,'printedPagePersonallyVisible':n,'section':14 if n==69 else 19},'renderPath':str(f.relative_to(w)),'renderSha256':sha(f.read_bytes()),'personallyReadPixels':True,'normalization':'Manual visual reading of printed Russian page; equations preserved in receipt reasoning, no English weight convention substituted'})
write('independent-source-contexts.json',{'contexts':contexts,'rawAssignments':raw,'excludedFailedSources':{'cloudFront403':prov['failedCloudFrontRainbowBody'],'optionalPartialCapture':prov['unusedFailedOptionalCapture']},'captureQualification':'05d3fbc mechanical intake; no substantive PASS inferred','oldHeaderExpectedNotRewritten':True,'bodyFreeze':'b3cbbc8','headerRestorationFreeze':'4bf45d0'})
write('independent-reader-receipt.json',{'schema':'physics-first10-independent-reader-v1','actorNativeId':'01a131c5-edfb-7b82-8ddf-bd88a8b95597','actualNativeIdentitySource':'Current reader native chat, not a label substituted for another actor','authorNativeId':'01a13237-776c-7242-a52b-fff331e038f5','actualCompactions':1,'authorReceiptFreeze':'92672c0','runtimeAndRawFreeze':'b3cbbc8','qualifiedIntake':'05d3fbc','headerRestoration':'4bf45d0','scopeIds':[c['id'] for c in sc],'status':'INDEPENDENT_FIX_AND_SOURCE_HOLD','method':'Personally read all10 current whole cards,17 primary contexts with own original extraction, collateral primary paragraphs, Russian/BIPM pixels and full catalog neighbors. Manual reasons below were authored independently. No AUTHOR_PASS inherited. Mechanical hashing checks only identity. No runtime mutation/test/build/deploy.','manualGroups':groups,'choiceReviews':choices,'difficultyAndSourceMetadata':metadata,'wholeCards':whole,'counts':{'groups':len(groups),'choices':len(choices),'difficultyMetadata':len(metadata),'groupVerdicts':dict(collections.Counter(x['verdict'] for x in groups)),'sourceVerdicts':dict(collections.Counter(x['sourceVerdict'] for x in groups)),'editorialVerdicts':dict(collections.Counter(x['editorialVerdict'] for x in groups)),'wholeVerdicts':dict(collections.Counter(x['verdict'] for x in whole))},'certifiedCountIncrease':0,'coordinatorManualGate':'Required after repairs/current whole-card recheck; this receipt never credits cards itself','preservation':'Only own permitted /private/tmp output. Coordinator must opaque-copy all bytes into durable Git; then reader may clean only own temp. No shared index/code/source-original/planning mutation.'})
print('counts',dict(collections.Counter(x['verdict'] for x in whole)),dict(collections.Counter(x['verdict'] for x in groups)))
