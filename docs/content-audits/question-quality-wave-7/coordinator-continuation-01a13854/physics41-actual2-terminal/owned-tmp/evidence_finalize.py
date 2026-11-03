import json,hashlib
from pathlib import Path
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
P=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original-edition2.json');d=json.loads(P.read_bytes());by={e['index']:e for e in d['entries']}
# Change #48 to exactly the directly sourced lever definition, preserving key slot.
c=by[48]['card'];c['prompt']='Как называется простой механизм, поворачивающийся вокруг точки опоры?';c['answers'][3]['text']='Рычаг';
r=by[48]['componentReasons'];r['whole_prompt_all_four_ordered_answers_correctIndex_key']['EDITORIAL']='The stem now describes a lever by its defining pivot, directly matching the cited passage; the distractors remain other named simple machines. The frozen key stays in slot 3.'
r['whole_prompt_all_four_ordered_answers_correctIndex_key']['SOURCE']='OpenStax §9.3 says the lever pivots around a fulcrum and defines effort/resistance arms. This establishes the answer “Рычаг” directly, without relying on an uncited seesaw example.'
# Make #47 notes distinguish different metallic-current consequences.
c=by[47]['card'];c['answers'][0]['note']='В металле свободные электроны перемещаются между атомами кристаллической решётки.';c['answers'][1]['note']='В обычном проводнике для поддержания тока требуется постоянный источник энергии; сверхпроводник указан как исключение.';c['answers'][2]['note']='Столкновения электронов передают энергию атомам; это может повысить температуру проводника.';c['answers'][3]['note']='Электроны дрейфуют медленно, хотя их хаотическое движение намного быстрее.'
# Replace distractor #42 with a true phase-equilibrium concept explicitly covered in §13.5.
c=by[42]['card'];c['answers'][3]={'text':'Сосуществование жидкости и газа','note':'В закрытом контейнере при температуре кипения жидкая и газовая фазы могут находиться в равновесии.'}
# Add specific editorial comments for the corrected #47/#48/#42 options.
for i,arr in {42:['The liquid note distinguishes shape from phase while retaining volume.','The gas note makes the vapor option distinct from liquid and solid.','Pressure-dependent melting adds a source-supported property beyond identifying ice as solid.','The equilibrium option draws on the same chapter’s two-phase description, not an unrelated advanced state.'],47:['Free-electron motion among atoms is distinct from energy leaving the wire.','The continuous-power note adds the ordinary-conductor/superconductor contrast.','This note links collision to heat without copying the answer’s full energy-transfer wording.','The drift/random-motion distinction expands on the carrier mechanism without repeating protected #5.'],48:['The wedge is described as an inclined-plane machine.','OpenStax explicitly relates a screw to a circular inclined plane.','A pulley and rope change force direction in the source examples.','This correct choice uses the pivot definition stated in the stem.']} .items():
 for j,s in enumerate(arr): by[i]['componentReasons'][f'note_{j}']['EDITORIAL']=s
# Bind all HTTP response evidence used by these source contexts, including headers/range parts and complete capture manifests.
WT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');root=WT/'docs/content-audits/question-quality-wave-7'; base=root/'coordinator-continuation-01a13772'; orig=root/'physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals'
def filebind(f):
 b=f.read_bytes();return {'path':str(f),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'gitBlobSha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
# Original primary download headers for every local CNXML/PDF/html body used.
for f in list(orig.glob('openstax-m54131*'))+list(orig.glob('openstax-m42218*'))+list(orig.glob('openstax-m42341*'))+list(orig.glob('openstax-m54314*'))+list(orig.glob('physics-force-si-unit.*'))+list(orig.glob('physics-water-boiling-standard-pressure.*')):
 if f.is_file():
  b=filebind(f)
  if b not in d['evidenceBindings']:d['evidenceBindings'].append(b)
# Full transport objects for all capture sources used in proposed claims.
captureDirs=[base/'capture-only'/f'physics30-49-gaps/{i}' for i in (39,43,48,49)]
captureDirs += [root/'coordinator-continuation-01a136e6/capture-only/physics-next20-29/23']
for dr in captureDirs:
 for f in [dr/'full-range-manifest.json',dr/'initial-manifest.json',dr/'initial.body',dr/'initial.headers',dr/'initial-0-8191.body',dr/'initial-0-8191.headers']:
  if f.exists():
   b=filebind(f)
   if b not in d['evidenceBindings']:d['evidenceBindings'].append(b)
 manifest=dr/'full-range-manifest.json'
 if manifest.exists():
  m=json.loads(manifest.read_text())
  for rec in m.get('records',[]):
   for field in ('bodyPath','headersPath'):
    path=rec.get(field)
    if path:
     f=WT/path
     if f.exists():
      b=filebind(f)
      if b not in d['evidenceBindings']:d['evidenceBindings'].append(b)
# Preserve explicit HTTP transport provenance manifests and reconstructed entity identities.
d['captureProvenance']=[{'manifest':filebind(dr/'full-range-manifest.json'),'initialHeaders':filebind(next(f for f in [dr/'initial.headers',dr/'initial-0-8191.headers'] if f.exists())),'assembledEntity':next((x for x in d['primaryContexts'] if x.get('fullEntityBinding',{}).get('path')==str(dr/'assembled-original-entity.body')),None)} for dr in captureDirs if (dr/'full-range-manifest.json').exists()]
# Full typed figure/caption contexts: add source alt attributes separately; #46's closed-path caption is decisive.
cn=orig/'openstax-m42341-index.cnxml'; tree=ET.parse(cn).getroot()
for ident in ('import-auto-id2931325','import-auto-id2670391','import-auto-id2446845','fs-id2616778','import-auto-id2691415'):
 for el in tree.iter():
  if el.attrib.get('id')==ident:
   ctx={'kind':'cnxml-full-element-context','source':'OpenStax College Physics 2e §20.1 Current','elementId':ident,'tag':el.tag.split('}')[-1],'literalText':' '.join(''.join(el.itertext()).split()),'mediaAlt':[x.attrib.get('alt') for x in el.iter() if x.tag.split('}')[-1]=='media' and x.attrib.get('alt')],'binding':filebind(cn)}
   if not any(x.get('elementId')==ident and x.get('kind')=='cnxml-full-element-context' for x in d['primaryContexts']):d['primaryContexts'].append(ctx)
   break
# Full source page water phase extra locator details, include the full raw section bytes hash already bound.
cn=orig/'openstax-m42218-index.cnxml';tree=ET.parse(cn).getroot()
for ident in ('import-auto-id1848208','import-auto-id1518525','import-auto-id1358200'):
 for el in tree.iter():
  if el.attrib.get('id')==ident:
   ctx={'kind':'cnxml-full-element-context','source':'OpenStax College Physics 2e §13.5 Phase Changes','elementId':ident,'tag':el.tag.split('}')[-1],'literalText':' '.join(''.join(el.itertext()).split()),'mediaAlt':[x.attrib.get('alt') for x in el.iter() if x.tag.split('}')[-1]=='media' and x.attrib.get('alt')],'binding':filebind(cn)}
   if not any(x.get('elementId')==ident and x.get('source')==ctx['source'] for x in d['primaryContexts']):d['primaryContexts'].append(ctx)
   break
# Canonical hashes and invariant/coverage checks.
for i,e in by.items():
 if 'card' in e:
  c=e['card'];assert c['id']==d['scope']['ids'][i-30] and c['difficulty']=='easy' and c['correctIndex']==d['scope']['keySlots'][i-30]
  assert len(c['answers'])==4 and len(e['componentReasons'])==8
  assert all(set(x)=={'SOURCE','EDITORIAL'} for x in e['componentReasons'].values())
# Detach parent authorNotes to exact current revision.
d['authorNotes']['revision']='edition2: 18 proposals + 2 holds; independent reader pending. Fixed key notes, explanations and every option note; updated per-field source/editorial reasons; changed unsupported #48 example to directly sourced lever definition; restored full #43 punctured-tire paragraph; added raw headers/range provenance and context byte/Git-blob hashes.'
b=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();P.write_bytes(b)
print('bytes',len(b),'sha256',hashlib.sha256(b).hexdigest(),'contexts',len(d['primaryContexts']),'bindings',len(d['evidenceBindings']),'captures',len(d['captureProvenance']))
