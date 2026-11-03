import json,hashlib
from pathlib import Path
p=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original.json');d=json.loads(p.read_bytes())
for e in d['entries']:
 i=e['index']
 if i in (40,41,43):
  e['status']='HOLD_PRIMARY_GAP'; e.pop('card',None); e['componentReasons']={}
  if i==41:
   e['missingEvidence']={'officialURL':'https://openstax.org/books/physics/pages/4-2-newtons-first-law-of-motion-inertia','requiredClaim':'Full §4.2 passage: absent net external force, a body remains at rest or continues uniform straight-line motion; current cited scan p.69 defines mass, not this claim.'}
  elif i==43:
   e['missingEvidence']={'officialURL':'https://openstax.org/books/college-physics-2e/pages/13-2-gas-laws','requiredClaim':'Full section context establishing that a gas has no fixed volume and expands to occupy its available closed-container volume; existing phase-change and entropy sources do not establish this predicate.'}
  else:
   e['missingEvidence']={'officialURL':'https://openstax.org/books/university-physics-volume-1/pages/6-2-friction','requiredClaim':'Full §6.2 passage stating that kinetic friction opposes relative sliding motion; cited raw §4.4 context does not establish it.'}
 if i==36:
  c=e['card'];c['prompt']='Для выражения каких явлений предназначена единица герц в СИ?'
  c['answers']=[
   {'text':'Для отдельных непериодических событий','note':'Герц относится к частоте повторяющихся явлений, а не к единичному событию.'},
   {'text':'Для периодических явлений','note':'В пояснении BIPM герц предписан для периодических явлений.'},
   {'text':'Для активности радионуклида','note':'Активность радионуклида выражают в беккерелях, а не в герцах.'},
   {'text':'Для электрического заряда','note':'Электрический заряд выражают в кулонах.'},
  ];c['correctIndex']=1
  r=e['componentReasons'];r['whole_prompt_all_ordered_answers_correctIndex_key']='BIPM Table 4 note d restricts hertz to periodic phenomena and reserves becquerel for stochastic radionuclide activity. The other choices name one-off events, radioactivity, or charge, each with a different measurement concept; fixed key slot 1 is preserved.'
  r['explanation']='Clarifies the scope of the SI unit: hertz expresses periodic phenomena, while radionuclide activity and charge have different units.'
  r['note_0']='The note distinguishes a single nonrepeating event from the periodic occurrences for which BIPM assigns hertz.'
  r['note_1']='The note states the BIPM use condition that is being tested; it adds scope beyond the bare unit name.'
  r['note_2']='The note uses BIPM’s explicit contrast: becquerel is assigned to stochastic radionuclide activity.'
  r['note_3']='The note distinguishes electric charge, a separate quantity with the SI unit coulomb, from periodic frequency.'
  r['difficulty']='This is direct recognition of the SI table’s short use restriction; no calculation or specialist derivation is needed.'
  r['sourceMetadata']='The official BIPM SI Brochure Table 4 note d directly distinguishes hertz for periodic phenomena from becquerel for stochastic activity; the full PDF and exact page bindings accompany the packet.'
 if i==45:
  c=e['card'];c['prompt']='К какому типу волн относится свет?'
  c['answers']=[
   {'text':'К звуковым механическим волнам','note':'Звуку для распространения нужны колеблющиеся частицы среды.'},
   {'text':'К водным механическим волнам','note':'Водные волны распространяются в материальной среде.'},
   {'text':'К сейсмическим механическим волнам','note':'Сейсмические волны распространяются через вещество Земли.'},
   {'text':'К электромагнитным волнам','note':'Свет — электромагнитная волна; ей не требуется материальная среда.'},
  ];c['correctIndex']=3
  r=e['componentReasons'];r['whole_prompt_all_ordered_answers_correctIndex_key']='OpenStax §13.1 classifies light as electromagnetic radiation; sound, water, and seismic waves are mechanical examples. That tests wave category rather than whether a wave can propagate in vacuum, avoiding protected #7’s inverse predicate; key slot 3 is preserved.'
  r['explanation']='Names light’s wave category and distinguishes it from mechanical waves that require a material medium.'
  r['note_0']='The note identifies the material-medium requirement that makes sound a mechanical-wave example.'
  r['note_1']='The note identifies the material surface/medium used by water waves, supporting their mechanical classification.'
  r['note_2']='The note connects seismic propagation to material Earth, distinguishing it from electromagnetic radiation.'
  r['note_3']='The note supplies the defining wave category for light and its consequence for propagation without a medium.'
  r['difficulty']='The learner chooses among familiar wave categories from one direct classification; no calculation or hidden condition is involved.'
  r['sourceMetadata']='OpenStax Physics §13.1 Types of Waves names light as electromagnetic and contrasts mechanical waves that require a medium; full local CNXML bytes and hash are bound.'
# Correct semantic scope and audit note
pout=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();p.write_bytes(pout)
print(len(pout),hashlib.sha256(pout).hexdigest(),[(e['index'],e['status']) for e in d['entries']])
