import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
P=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original-edition2.json');d=json.loads(P.read_bytes());by={e['index']:e for e in d['entries']}
# Direct URLs from the complete capture manifests, correcting the 12.3 slug.
by[43]['card']['source']['url']='https://openstax.org/books/physics/pages/12-3-second-law-of-thermodynamics-entropy'
# Phase notes rely only on facts stated in the cited §13.5 text, not a borrowed plasma definition.
c=by[42]['card'];c['answers']=[
 {'text':'Газообразное','note':'В §13.5 реальный газ при понижении температуры может конденсироваться в жидкость.'},
 {'text':'Жидкое','note':'Повышение давления при постоянной температуре может перевести лёд в жидкую воду.'},
 {'text':'Твёрдое','note':'При границе плавления твёрдая и жидкая фазы воды находятся в равновесии.'},
 {'text':'Сосуществование жидкости и газа','note':'В закрытом контейнере при температуре кипения жидкая и газовая фазы могут быть в равновесии.'},
];c['correctIndex']=2
# Tailor source/evidence narratives to the exact claim and source locator for each ready ID.
sourceMeta={
30:'BIPM SI Brochure Table 2 (PDF p.132) gives kilogram/kg as mass unit; Table 3 and PDF p.35 establish decimal prefixes and the gram exception.',
31:'BIPM SI Brochure Table 2 and the second-definition passage on PDF p.132 give the unit and the Cs-133 frequency definition.',
32:'BIPM Table 2 and the metre definition on PDF pp.132–133 support m; PDF p.35 (printed p.33) supports litre, and Table 4 supports Hz.',
33:'BIPM SI Brochure Table 4 on PDF p.140 lists volt V, its base-unit expression, pascal, tesla and joule.',
34:'BIPM Table 4 on PDF p.140 gives watt W = J/s and the SI units for charge; Table 2 gives metre and Table 8 discusses degree.',
35:'BIPM Table 4 on PDF p.139 gives joule J = N·m alongside ohm, lumen and ampere.',
36:'BIPM Table 4 note d on PDF p.139 explicitly reserves hertz for periodic phenomena and becquerel for stochastic radionuclide activity.',
37:'OpenStax Physics §4.4 raw CNXML paragraph fs-idm15080864 states Earth-centre gravity and the outward normal force; the exact full CNXML and HTTP sidecar are bound.',
38:'OpenStax Physics §20.1 complete assembled entity, paragraph fs-id1167065911660, bytes 107616–108513; full ranges, response headers and manifest are bound.',
39:'OpenStax Physics §16.1 complete 391961-byte assembled body; selected full reflection-law and plane-mirror paragraphs are separately typed and hashed.',
42:'OpenStax College Physics 2e §13.5 raw CNXML elements import-auto-id1860596, import-auto-id1848208, import-auto-id1358200; these establish gas condensation, ice/liquid boundary and liquid-gas equilibrium.',
43:'OpenStax Physics §12.3 complete 343448-byte assembled body; the exact full punctured-tire paragraph says air disperses in all directions and connects dispersal with entropy.',
44:'OpenStax College Physics 2e §13.5 raw CNXML paragraph import-auto-id1848208 gives 0 ºC at 1.00 atm; the boiling-water paragraph in the same full section gives 100 ºC at 1.00 atm.',
45:'OpenStax Physics §13.1 raw CNXML paragraphs fs-id1167065809902 and fs-id1167065854785 distinguish mechanical waves from light and list wave characteristics.',
46:'OpenStax College Physics 2e §20.1 raw Figure 20.1 subtree/caption and media alt state the closed path from battery through load to the other terminal.',
47:'OpenStax College Physics 2e §20.1 raw paragraphs import-auto-id2446845 and import-auto-id2691415 explain free-electron collisions, lattice heating and continuous power input.',
48:'OpenStax Physics §9.3 complete 364089-byte body, paragraph fs-id1167066791981, defines lever arms and fulcrum; no unsupported seesaw claim remains.',
49:'OpenStax Physics §14.2 complete 367070-byte body; full paragraphs give intensity proportional to pressure-amplitude squared and distinguish pitch from loudness perception.'}
for i,desc in sourceMeta.items():
 c=by[i]['card']; c['source']['title']=c['source']['title']
 r=by[i]['componentReasons']['sourceMetadata'];r['SOURCE']=desc+' Primary byte bindings, typed context, relevant original headers, and Git blob SHA-1 are included in the packet.'
# Reflect revised #42 answer facts in component reasons.
by[42]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['SOURCE']='OpenStax §13.5 identifies ice as solid water, describes gas condensing to liquid, pressure-driven ice melting, and gas-liquid equilibrium in a closed vessel. Only the solid state answers the prompt; key slot 2 is preserved.'
by[42]['componentReasons']['note_0']['SOURCE']='§13.5 describes real gases condensing to liquid as temperature falls; the note states this transition rather than an unsupported universal claim about gas volume.'
by[42]['componentReasons']['note_3']['SOURCE']='The same section says liquid and gas are in equilibrium at the boiling temperature in a closed container.'
by[42]['componentReasons']['note_3']['EDITORIAL']='The equilibrium option is a source-based distractor about two coexisting phases; its note explains the condition without implying ordinary ice is that mixture.'
by[42]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='The answer set contrasts gas, liquid, solid, and a two-phase equilibrium. The three phase descriptions are parallel, and the final condition is explicitly tied to boiling in a closed vessel.'
by[43]['componentReasons']['sourceMetadata']['SOURCE']=sourceMeta[43]+' The exact manifest URL is https://openstax.org/books/physics/pages/12-3-second-law-of-thermodynamics-entropy.'
by[48]['componentReasons']['sourceMetadata']['SOURCE']=sourceMeta[48]+' The stem now asks the chapter’s directly defined mechanism, not an unmentioned seesaw example.'
# Exclude an empty JS-shell mirror from the source evidence set; full §13.5 CNXML proves the boiling contrast.
for ctx in list(d['primaryContexts']):
 if ctx.get('kind')=='neighbor-source-claim-context' and ctx.get('neighborIndex')==6:
  d['primaryContexts'].remove(ctx)
  path=ctx.get('fullEntityBinding',{}).get('path')
  d['evidenceBindings']=[b for b in d['evidenceBindings'] if b.get('path')!=path and b.get('path')!=path.replace('.html','.headers.txt')]
# Add exact water-boiling paragraph and 100 °C value from full primary CNXML.
WT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');cn=WT/'docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/openstax-m42218-index.cnxml';root=ET.parse(cn).getroot()
def binding(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'gitBlobSha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
for el in root.iter():
 txt=' '.join(''.join(el.itertext()).split())
 if 'boiling point of water is' in txt and '100' in txt:
  d['primaryContexts'].append({'kind':'cnxml-full-element-context','source':'OpenStax College Physics 2e §13.5','elementId':el.attrib.get('id'),'tag':el.tag.split('}')[-1],'literalText':txt,'binding':binding(cn)});break
# Adjust #44 note-source pair to explicitly bind the section itself, not an incomplete wrapper.
by[44]['componentReasons']['note_0']['SOURCE']='The same §13.5 raw phase-diagram paragraph gives water’s boiling point as 100 ºC at 1.00 atm; therefore this distractor names the other standard transition.'
# canonical output
b=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();P.write_bytes(b);print(len(b),hashlib.sha256(b).hexdigest(),'ctx',len(d['primaryContexts']),'bind',len(d['evidenceBindings']))
