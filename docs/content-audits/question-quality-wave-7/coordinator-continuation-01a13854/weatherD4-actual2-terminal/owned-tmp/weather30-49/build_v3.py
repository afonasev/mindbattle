import json,hashlib,copy
from pathlib import Path
root=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f/weather30-49')
v2p=root/'weather30-49-source-editorial-packet-v2.json'; old=json.loads(v2p.read_bytes())
repo=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7')
alt=repo/'coordinator-continuation-01a13854/capture-only/official-alternatives-54'
# Primary/current official-source registry; records bind full raw body, headers and original retrieval manifest.
source_dirs={
'NASA Aurora':'weather-30','NWS Breeze':'weather-31-breeze','NWS Tropical Cyclone':'weather-32-cyclone','NWS Glossary':'weather-32-33-glossary','NWS Monsoon PDF':'weather-34-monsoon','NWS Fronts/Jets':'weather-35-36-41-fronts','NWS ENSO':'weather-37-38-enso','NOAA CPC NAO':'weather-39-nao','BOM IOD blocked':'weather-40-iod','NOAA OceanService Winds':'weather-42-43-currents','NOAA JetStream Circulations':'weather-42-44-global-circulation'}
source_urls={'NASA Aurora':'https://science.nasa.gov/sun/auroras/','NWS Breeze':'https://forecast.weather.gov/glossary.php?word=breeze','NWS Tropical Cyclone':'https://www.weather.gov/mob/tropical_definitions','NWS Glossary':'https://www.weather.gov/key/glossary','NWS Monsoon PDF':'https://www.weather.gov/media/twc/monsoon/monsoon_whatis.pdf','NWS Fronts/Jets':'https://www.weather.gov/lmk/basic-fronts','NWS ENSO':'https://www.weather.gov/mhx/ensowhat','NOAA CPC NAO':'https://www.cpc.ncep.noaa.gov/data/teledoc/nao.shtml','BOM IOD blocked':'https://www.bom.gov.au/climate/iod/','NOAA OceanService Winds':'https://oceanservice.noaa.gov/education/tutorial_currents/04currents2.html','NOAA JetStream Circulations':'https://www.noaa.gov/jetstream/global/global-atmospheric-circulations'}
receipts=[]
for label,dn in source_dirs.items():
 d=alt/dn
 for fn in (['assembled.body','range-manifest.json','head.headers','head-manifest.json','initial-manifest.json','response.body','response.headers']):
  p=d/fn
  if not p.exists():continue
  raw=p.read_bytes();receipts.append({'source':label,'url':source_urls[label],'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
# Extra primary captures already preserved in the previous author source archive.
extra=[
(repo/'coordinator-continuation-01a13619/capture-only/weather-next10-gaps/trough.body','NWS glossary trough'),
(repo/'coordinator-continuation-01a13619/capture-only/weather-next10-gaps/ridge.body','NWS glossary ridge'),
(repo/'coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-parcel-values.body','SPC parcel values'),
(repo/'coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-parcel-values.headers','SPC parcel values headers'),
(repo/'coordinator-continuation-01a136e6/capture-only/weather20-29-primary/rainbow.body','NWS rainbow glossary'),
(repo/'coordinator-continuation-01a136e6/capture-only/weather20-29-primary/rainbow.headers','NWS rainbow glossary headers'),
(repo/'coordinator-continuation-01a136e6/capture-only/weather20-29-primary/rainbow.manifest.json','NWS rainbow glossary manifest'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/response.body','SPC shear child'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/response.headers','SPC shear child headers'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/manifest.json','SPC shear child manifest'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/17/response.body','NWS precipitation PDF'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/17/response.headers','NWS precipitation PDF headers'),
(repo/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/17/manifest.json','NWS precipitation PDF manifest'),
]
extra_urls={'NWS glossary trough':'https://forecast.weather.gov/glossary.php?word=Trough','NWS glossary ridge':'https://forecast.weather.gov/glossary.php?word=Ridge','SPC parcel values':'https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html','SPC parcel values headers':'https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html','NWS rainbow glossary':'https://forecast.weather.gov/glossary.php?word=Rainbow','NWS rainbow glossary headers':'https://forecast.weather.gov/glossary.php?word=Rainbow','NWS rainbow glossary manifest':'https://forecast.weather.gov/glossary.php?word=Rainbow','SPC shear child':'https://www.spc.noaa.gov/exper/soundings/help/shear.html','SPC shear child headers':'https://www.spc.noaa.gov/exper/soundings/help/shear.html','SPC shear child manifest':'https://www.spc.noaa.gov/exper/soundings/help/shear.html','NWS precipitation PDF':'https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf','NWS precipitation PDF headers':'https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf','NWS precipitation PDF manifest':'https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf'}
for p,label in extra:
 raw=p.read_bytes();receipts.append({'source':label,'url':extra_urls[label],'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
# Provenance for alternative-capture wave and coordinator's byte-preservation receipt.
for p,label in [(alt/'capture-manifest.json','coordinator official capture manifest'),(alt/'coordinator-transport-receipt.json','coordinator transport/readback receipt')]:
 raw=p.read_bytes();receipts.append({'source':label,'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
# Source-specific current factual scopes; all refs point to personally inspected complete captured passages.
facts={
30:'NASA aurora article: auroras are colorful displays produced when energetic particles collide with atoms/molecules in the atmosphere; NASA also describes the solar wind, Earth magnetic shield and auroral activity near polar regions. NWS glossary captures supply lightning, thunder and rainbow option distinctions.',
31:'NWS glossary Sea Breeze entry: daytime wind from cool ocean to adjoining warm land due to differential heating. NOAA/NWS glossary entries supply the hurricane, tornado and monsoon distractor distinctions.',
32:'NWS Mobile tropical definitions: hurricane is a tropical cyclone with maximum sustained surface winds >=74 mph / 64 kt; NWS glossary entries define breeze, tornado and monsoon.',
33:'NWS glossary entry defines tornado by a funnel cloud reaching ground; its separate entries and saved NWS breeze/monsoon source support distractor distinctions. The source does not define an unseen funnel as necessary.',
34:'NWS Monsoon PDF (3 pages, visually inspected): seasonally reversing regional winds, winter NE to summer SW over South Asia, summer rain; the source also explains heating/pressure contrast. NWS glossary supplies other named distractors.',
35:'NWS glossary Trough entry: elongated relatively low-pressure area, usually not associated with closed circulation, opposite of ridge. NWS basic-fronts page shows upper troughs associated with lows/fronts and precipitation ahead. NWS glossary gives bounded cyclone/anticyclone terms.',
36:'NWS glossary Ridge entry: elongated area of relatively high atmospheric pressure, opposite of trough. NWS basic-fronts page describes upper ridge placement; it does not substantiate a general cloudiness reduction. NWS glossary supplies cyclone/anticyclone terms.',
37:'NWS Morehead City ENSO page: ENSO is recurring central/eastern tropical Pacific SST change; El Niño is above-average SST there; easterly equatorial trades weaken or sometimes reverse. The page explains ENSO acronym and impacts.',
38:'Same NWS ENSO page: La Niña is below-average SST in central/eastern tropical Pacific; normal equatorial easterlies strengthen; ENSO has neutral phase between extremes.',
39:'NOAA CPC NAO page: winter NAO is a north-south pressure/height dipole (Greenland and central North Atlantic), phases alter jet/storm track and temperature/precipitation patterns reaching Europe. Other named distractors are supported by captured ENSO pages; IOD definition remains uncaptured.',
40:'The only preserved alternative IOD attempt is a Bureau of Meteorology HTTP 403 block page. No relevant factual passage was read, so the core comparison between Africa and Indonesia, named IOD answer, and phase explanation remain on HOLD.',
41:'NWS basic-fronts page defines jet stream as a relatively high-speed ribbon at roughly 25,000–40,000 ft; its pattern/wind speeds affect surface temperature and precipitation. NWS glossary explicitly says it steers low-pressure storms and high-pressure systems; Flight Environment page says jet streams flow west to east. Other wind terms are covered by official NWS/NOAA captures.',
42:'NOAA OceanService explains trade winds arise in tropical circulation, their hemispheric directions, convergence near the ITCZ and historical use by ships traveling Europe/Americas. NWS/NOAA sources cover the other wind terms.',
43:'NOAA OceanService defines westerlies as prevailing winds continuing poleward from the trade-wind circulation; NOAA JetStream describes the mid-latitude Ferrel cell as surface flow poleward/eastward and westerlies around 35–60° N/S. The source does not claim that many cyclones are carried across Europe.',
44:'NOAA JetStream Global Atmospheric Circulations: surface air moves outward from polar highs, creating east-blowing surface winds called polar easterlies. NWS Flight Environment independently says polar-cell surface winds are easterly. The distractor wind belts have their own captured definitions.'}
cores={
30:'The NASA definition matches the keyed colorful atmospheric glow and particle mechanism. Cross-check the near-polar scope and keep lightning, thunder, and rainbow descriptions separate; each distractor has a captured glossary definition.',
31:'The exact NWS Sea Breeze glossary entry names time of day, direction, and differential heating. The prompt can be clearer that the intended term is daytime sea breeze; the answer currently repeats the key and provides its central distinction.',
32:'The NWS tropical definitions distinguish a hurricane by a 74 mph sustained-wind threshold. Align Atlantic naming scope, answer note, and explanation; use “maximum sustained surface wind” consistently.',
33:'NWS glossary distinguishes a funnel cloud from a tornado by ground contact. Rephrase the stem to focus on contact with the ground and avoid implying that a visible condensation funnel must be present.',
34:'The NWS PDF supports seasonal reversal and South Asian summer rain, while also noting monsoons occur in other regions. Avoid implying that Asian summer rain alone defines every monsoon.',
35:'NWS glossary defines a trough as elongated low pressure usually without closed circulation and opposite to a ridge. That distinction improves the stem against the cyclone option; cut or support the added cloud/precipitation generalization.',
36:'NWS glossary defines a ridge as elongated high pressure opposite a trough. The proposed stem uses that exact distinction; the original claim about cloudiness reduction is not supported by the inspected definition. Its key slot matches #35.',
37:'NWS source explicitly expands ENSO and separates El Niño, La Niña, and neutral phases. Expand the acronym at first use and retain central/eastern tropical Pacific wording; avoid implying only the eastern region.',
38:'NWS source gives La Niña’s cooler central/eastern tropical Pacific and stronger equatorial easterlies. The stem’s simple “opposite phase” is short, but neutral ENSO is a third phase and prevents a strict binary reading.',
39:'CPC source directly supports winter NAO and European/North Atlantic impacts. Rework “especially influences” to specify the dipole or winter teleconnection; the answer currently says “pressure difference” but omits Greenland/35–40N centers.',
40:'The preserved source attempt is a 403 block response, not an IOD source. Keep this card as an independent hold and do not infer its Africa/Indonesia contrast from unrelated ENSO sources.',
41:'NWS sources support the jet definition, vertical layer, west-to-east movement, storm steering, and surface pattern influence. Prompt’s “directing cyclones” is overstrong; the proposed stem asks the directly defined high-speed upper-level ribbon instead.',
42:'NOAA’s account supports historical sailing use but the phrase “торговых судов” leaks the term linguistically. Replace it with the sourced wind direction/ITCZ setting, and explain both hemisphere directions explicitly.',
43:'Official wind-circulation sources support westerlies and midlatitude eastward flow but not the stem’s causal claim about many European cyclones. Ask for the wind belt/direction that sources actually define.',
44:'NOAA directly defines polar easterlies by polar-high surface outflow and easterly direction. State that defining circulation in the explanation; distinguish wind direction “from east” from movement “toward west”.',
45:'SPC defines CINH as integrated negative buoyancy energy from the parcel start to LFC. The current “cap” alias is not in the source; the proposed stem asks for the sourced energy meaning.',
46:'SPC defines LI using parcel and environment temperatures at 500 mb; negative means warmer parcel and instability. State the sign convention without adding unspecified levels.',
47:'SPC shear page supports SRH as storm-inflow streamwise vorticity and a supercell diagnostic. Use the full SRH term to avoid ambiguity with generic helicity.',
48:'NWS PDF distinguishes warm-cloud collision-coalescence from cold-cloud Bergeron. Explain collisions and some drops coalescing; accretion and aggregation notes remain unsupported by this PDF.',
49:'NWS PDF supports Bergeron mechanism and ice-vapor pressure difference, but the prompt’s universal mixed-cloud below-freezing threshold is broader than the passage. Wikipedia is not used.'}
# Per-note mapping to evidence and current-claim limits.
note_source={
30:['NWS glossary: lightning is an electrical discharge from a thunderstorm cloud.','NWS glossary: thunder is the sound of air rapidly expanding after lightning heats it.','NASA aurora source: charged particles energize atmospheric atoms/molecules, producing light; upper-atmosphere mechanism.','NWS rainbow glossary: refraction, reflection and dispersion in water droplets.'],
31:['NWS tropical definitions: hurricane intensity threshold and regional tropical cyclone naming.','NWS glossary: tornado/funnel cloud ground-contact distinction.','NWS breeze glossary: sea breeze direction and daytime differential heating.','NWS monsoon PDF: seasonal wind direction shifts; NWS glossary calls monsoon a persistent seasonal wind/rainfall pattern.'],
32:['NWS breeze glossary: local onshore daytime thermal wind.','NWS glossary: tornado/funnel cloud ground-contact distinction.','NWS Mobile definition: hurricane threshold >=74 mph sustained surface wind.','NWS Monsoon PDF and glossary: seasonal reversal vs tropical cyclone.'],
33:['NWS breeze glossary defines local sea breeze, distinct from a storm-scale rotating column.','NWS tropical definitions give hurricane as a tropical cyclone meeting sustained-wind threshold.','NWS monsoon sources define seasonal regional wind/rain pattern.','NWS glossary calls tornado a funnel cloud reaching ground; current note’s “fast” and thunderstorm wording exceed this short definition.'],
34:['NWS breeze glossary defines a local daytime onshore wind.','NWS tropical definitions define hurricane intensity/geography.','NWS glossary distinguishes tornado via ground contact.','NWS Monsoon PDF documents the seasonal reversal and summer flow; NWS glossary defines monsoon pattern.'],
35:['NWS Trough glossary directly supports.','NWS general glossary calls cyclone a low-pressure weather system; it does not support all updraft/convergence details in this note.','NWS glossary calls anticyclone a high-pressure system and describes clockwise rotation; sinking/diverging details are not in the capture.','NWS Trough glossary says ridge is its opposite; Ridge glossary defines high-pressure elongated region.'],
36:['NWS Ridge glossary directly supports.','NWS glossary gives cyclone low-pressure system and rotation; not all current vertical-motion details.','NWS glossary gives anticyclone high-pressure system and clockwise rotation; not all current vertical-motion details.','NWS Trough glossary directly supports.'],
37:['NWS ENSO source defines La Niña as below-average central/eastern tropical Pacific SST.','NWS ENSO source defines El Niño as above-average SST in the central/eastern tropical Pacific.','NOAA CPC NAO source defines the North Atlantic pressure/height dipole.','No readable IOD primary source in preserved captures; the note comparing western/eastern Indian Ocean remains unverified.'],
38:['NWS ENSO source defines El Niño as above-average central/eastern tropical Pacific SST.','NWS ENSO source defines La Niña as below-average SST and stronger equatorial easterlies.','NOAA CPC source defines NAO pressure/height dipole.','No readable IOD source in captures; this distractor’s asserted Indian Ocean contrast remains unverified.'],
39:['NWS ENSO source defines El Niño.','NOAA CPC NAO source defines the pressure/height dipole; confirm note’s named Azores and Iceland centers are not CPC’s Greenland and 35–40N centers before retaining.','NWS ENSO source defines La Niña.','No readable IOD primary source; note remains unverified.'],
40:['NWS ENSO source supports the El Niño description.','NWS ENSO source supports the La Niña description.','BOM IOD URL returned only 403 denial; core target note is not evidenced.','NOAA CPC NAO source supports the pressure pattern, though confirm note’s Azores/Iceland centers against CPC’s Greenland/central North Atlantic centers.'],
41:['NOAA sources support trade winds and ITCZ relationship.','NOAA sources support midlatitude westerlies and west-to-east flow.','NWS sources support jet stream as high-speed upper-level ribbon and steering storms.','NOAA JetStream supports polar high outflow and polar easterlies.'],
42:['NWS source defines jet stream aloft and west-east.','NOAA sources define westerly midlatitude winds.','NOAA OceanService supports trades and their historic maritime use.','NOAA source supports polar easterlies; the current note’s polar high origin is stated in JetStream.'],
43:['NWS source supports jet stream, but “upper troposphere” is broad relative to its 25–40k-foot range.','NOAA source defines trade-wind belt and direction.','NOAA JetStream defines polar easterlies.','NOAA source supports westerlies; its exact midlatitude range is 35–60 degrees.'],
44:['NWS sources define high-speed jet stream aloft.','NOAA source defines tropical trade winds.','NOAA sources define west-to-east midlatitude westerlies.','NOAA JetStream explicitly defines polar easterlies as east-blowing surface winds from polar highs.'],
45:['SPC parcelvals directly defines CINH energy needed to reach LFC.','SPC parcelvals defines CAPE positive area and relation to updraft strength.','SPC parcelvals defines LI at 500 mb and negative buoyancy convention.','SPC shear defines SRH in storm inflow; it is distinct from inhibition.'],
46:['SPC parcelvals defines CAPE positive area.','SPC parcelvals gives the exact LI formula and negative/warmer/unstable meaning.','SPC parcelvals defines CINH negative area/energy.','SPC shear defines SRH; it is not a thermal stability index.'],
47:['SPC parcelvals defines CAPE positive buoyancy.','SPC shear defines SRH and its supercell diagnostic use.','SPC parcelvals defines CINH inhibition.','SPC parcelvals defines LI at 500 mb.'],
48:['NWS PDF page 2 distinguishes Bergeron as cold-cloud process with ice and supercooled water.','The inspected NWS PDF does not define accretion; this note stays a source gap.','NWS PDF page 3 directly describes collision-coalescence in warm clouds: larger drops collide with smaller, some stick/coalesce.','The PDF does not define aggregation; this note stays a source gap.'],
49:['NWS PDF page 3 describes warm-cloud collision-coalescence.','The NWS PDF does not define accretion; do not claim source support.','The NWS PDF does not define aggregation; do not claim source support.','NWS PDF page 2 directly describes Bergeron mechanism and lower saturation vapor pressure over ice.']}
# Full option labels have their own topical capture groups; group refers to stem plus answer order/key, not notes.
option_cover={
30:'NASA aurora passage plus captured NWS glossary entries for lightning/thunder and rainbow distinguish the keyed phenomenon from all three distractors.',
31:'NWS Sea Breeze entry supports the key; NWS tropical definitions/glossary and monsoon source support the three labels in options.',
32:'NWS Mobile tropical definitions support hurricane; NWS breeze, tornado and monsoon source captures cover distractor concepts.',
33:'NWS glossary supports tornado ground contact; captured breeze, hurricane and monsoon references distinguish the distractors.',
34:'NWS monsoon PDF supports seasonal reversal; official breeze, hurricane and tornado sources distinguish the alternatives.',
35:'NWS glossary entries define trough/ridge/cyclone/anticyclone; the elongated-low/closed-circulation distinction is explicit in the Trough entry.',
36:'NWS glossary entries define ridge/trough/cyclone/anticyclone; the elongated-high/opposite-trough distinction is explicit in the Ridge entry.',
37:'NWS ENSO source supports warm phase; NOAA CPC NAO identifies the North Atlantic pattern; IOD label is present only as a distractor and has not been independently defined in these sources.',
38:'NWS ENSO source supports La Niña/El Niño contrast; CPC distinguishes NAO; IOD remains a label-only distractor pending its own source.',
39:'NOAA CPC supports the keyed winter NAO pattern; NWS ENSO pages distinguish El Niño/La Niña; IOD content not separately sourced.',
40:'HOLD: source capture is 403, so the keyed IOD concept and stem are not established by a usable passage.',
41:'Official NWS sources support the jet, trade, westerly and polar wind labels; the current action phrase about steering is evaluated separately in the explanation group.',
42:'Official NOAA/NWS sources distinguish jet stream, westerlies, trade winds and polar easterlies; NOAA OceanService also supports maritime history but current wording is a cue.',
43:'Official NWS/NOAA sources define all four wind belts; the current Europe/cyclone effect is not established by the captured wind definitions.',
44:'Official NWS/NOAA sources define the four wind belts and their layers/directions; the polar key has a specific NOAA definition.'}

def h(raw):return hashlib.sha256(raw).hexdigest()
def cjson(x,sort=False):return json.dumps(x,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
meta={
30:('NASA Science: Auroras','https://science.nasa.gov/sun/auroras/'),31:('National Weather Service Glossary: Sea Breeze','https://forecast.weather.gov/glossary.php?word=breeze'),32:('National Weather Service Mobile/Pensacola: Tropical Definitions','https://www.weather.gov/mob/tropical_definitions'),33:('National Weather Service Key West: Weather Glossary','https://www.weather.gov/key/glossary'),34:('National Weather Service: What is a Monsoon?','https://www.weather.gov/media/twc/monsoon/monsoon_whatis.pdf'),35:('National Weather Service Glossary: Trough','https://forecast.weather.gov/glossary.php?word=Trough'),36:('National Weather Service Glossary: Ridge','https://forecast.weather.gov/glossary.php?word=Ridge'),37:('National Weather Service Morehead City: What is ENSO?','https://www.weather.gov/mhx/ensowhat'),38:('National Weather Service Morehead City: What is ENSO?','https://www.weather.gov/mhx/ensowhat'),39:('NOAA Climate Prediction Center: North Atlantic Oscillation','https://www.cpc.ncep.noaa.gov/data/teledoc/nao.shtml'),41:('National Weather Service: Pressure Systems, Fronts and Jet Streams','https://www.weather.gov/lmk/basic-fronts'),42:('NOAA Ocean Service: Atmospheric Circulation and Winds','https://oceanservice.noaa.gov/education/tutorial_currents/04currents2.html'),43:('NOAA Ocean Service: Atmospheric Circulation and Winds','https://oceanservice.noaa.gov/education/tutorial_currents/04currents2.html'),44:('NOAA JetStream: Global Atmospheric Circulations','https://www.noaa.gov/jetstream/global/global-atmospheric-circulations'),45:('Storm Prediction Center: Sounding Analysis Help — Parcel Values','https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html'),46:('Storm Prediction Center: Sounding Analysis Help — Parcel Values','https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html'),47:('Storm Prediction Center: Wind Shear — Storm Relative Helicity','https://www.spc.noaa.gov/exper/soundings/help/shear.html'),48:('NOAA/NWS: Clouds and Precipitation, Lesson 10','https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf'),49:('NOAA/NWS: Clouds and Precipitation, Lesson 10','https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf')}
related={30:[27,28,29],31:[34,41,42,43,44],32:[64,65,66,96,97,98,99],33:[18,32,47,76],34:[31,41,42,43,44],35:[18,36],36:[19,35],37:[38],38:[37],39:[37,38],40:[37,38],41:[42,43,44,72,73,74,95],42:[31,34,41,43,44],43:[41,42,44,72,73,74],44:[41,42,43],45:[14,15,16,17,20,21,22,23,24],46:[14,15,20,21,22,23,24],47:[20,21,22,23,24,72,73,74],48:[2,70,71,76,85],49:[2,70,71,76]}
new=[]
for entry in old['entries']:
 i=entry['index']; cur=copy.deepcopy(entry['currentCard']); prop=copy.deepcopy(cur)
 if i in meta: prop['source']={'title':meta[i][0],'url':meta[i][1],'verifiedAt':'2026-10-14'}
 if i==33: prop['prompt']='Как называется воронкообразный вихрь, связанный с грозовым облаком и достигающий земли?'
 if i==35: prop['explanation']='Ложбина — вытянутая область относительно низкого атмосферного давления, обычно без замкнутой циркуляции; этим она отличается от замкнутого минимума.'
 if i==36:
  prop['prompt']='Как называется вытянутая область относительно высокого атмосферного давления, противоположная ложбине?'
  prop['explanation']='Гребень — вытянутая область относительно высокого атмосферного давления, противоположная ложбине.'
 if i in (37,38): prop['prompt']=prop['prompt'].replace('фаза ENSO','фаза Эль-Ниньо — Южного колебания (ENSO)')
 if i==39: prop['prompt']='Как называется зимний режим, представляющий собой противоположные аномалии давления над Гренландией и центральной частью Северной Атлантики и влияющий на погоду Европы?'
 if i==41:
  prop['prompt']='Как называется относительно высокоскоростная лента ветра в верхних слоях атмосферы, влияющая на температуру и осадки у поверхности?'
  prop['explanation']='Струйное течение — узкая высокоскоростная лента ветра примерно на высоте 25 000–40 000 футов; изменения её положения и скорости влияют на приземную температуру и осадки.'
 if i==42:
  prop['prompt']='Какие господствующие ветры в тропиках помогали парусным судам пересекать океаны и сходятся у экваториальной зоны конвергенции?'
  prop['answers'][2]['note']='Пассаты — устойчивые тропические ветры; в Северном полушарии дуют с северо-востока, в Южном — с юго-востока, к зоне конвергенции у экватора.'
  prop['explanation']='Пассаты дуют к экваториальной зоне конвергенции: в Северном полушарии преимущественно с северо-востока, в Южном — с юго-востока. Исторически ими пользовались парусные суда.'
 if i==43:
  prop['prompt']='Какие господствующие ветры в средних широтах дуют с запада на восток?'
  prop['explanation']='Западные ветры — преобладающий пояс средних широт; приземный поток направлен к полюсам и на восток.'
 if i==44:
  prop['answers'][3]['note']='Полярные восточные — приземные ветры, дующие от областей высокого давления у полюсов; их движение направлено преимущественно на запад.'
  prop['explanation']='У полюсов воздух опускается, образуя полярные максимумы; у поверхности он расходится от них и образует восточные ветры, то есть дующие с востока на запад.'
 if i==45:
  prop['prompt']='Какой параметр выражает энергию, необходимую воздушной частице, чтобы достичь уровня свободной конвекции?'
  prop['explanation']='CIN — интегральная отрицательная область от исходного уровня частицы до LFC; её величина выражает энергию, необходимую для достижения LFC.'
 if i==46:
  prop['prompt']='Какой индекс становится более отрицательным, когда поднятая частица на 500 mb теплее окружающей среды?'
  prop['explanation']='LI — температура поднятой частицы минус температура среды на 500 mb. Отрицательный LI означает, что частица теплее среды и плавуча/неустойчива.'
 if i==47:
  prop['answers'][1]['text']='Штормовая относительная спиральность (SRH)'
  prop['answers'][1]['note']='SRH характеризует streamwise vorticity во входящем в шторм слое и зависит от площади между hodograph и движением шторма.'
  prop['explanation']='SRH характеризует streamwise vorticity во входящем в шторм слое. SPC связывает показатель с площадью между hodograph и движением шторма и отмечает его диагностическую пользу для различения торнадических и неторнадических суперячеек.'
 if i==48:
  prop['answers'][2]['note']='В тёплых облаках более крупные капли сталкиваются с мелкими; часть мелких капель слипается с крупными.'
  prop['explanation']='В тёплых облаках более крупные капли падают и сталкиваются с мелкими; часть мелких капель слипается с ними, поэтому капли растут.'
 if i==49:
  prop['answers'][3]['note']='В холодном облаке ледяные кристаллы растут при наличии переохлаждённой жидкой воды; давление насыщенного пара над льдом ниже, чем над водой.'
  prop['explanation']='В холодном облаке ледяные кристаллы растут за счёт облачных капель при наличии переохлаждённой жидкой воды. Давление насыщенного пара над льдом ниже, чем над водой.'
 assert prop['difficulty']==cur['difficulty'] and prop['correctIndex']==cur['correctIndex']
 groups=[]
 vals=[('prompt_ordered_answers_key',{'prompt':cur['prompt'],'answers':[a['text'] for a in cur['answers']],'correctIndex':cur['correctIndex']}),('explanation',cur['explanation'])]+[(f'note{j}',cur['answers'][j]['note']) for j in range(4)]+[('difficulty',cur['difficulty']),('source_metadata',cur['source'])]
 for g,val in vals:
  noteidx=int(g[-1]) if g.startswith('note') else None
  if g=='difficulty': status='EDITORIAL_ONLY_FROZEN_CLASS';sreason=f'Источники по теме не доказывают класс {cur["difficulty"]}; он заморожен и сохраняется. Любое изменение сложности требует отдельного taxonomy решения.'
  elif i==40: status='HOLD_NO_READABLE_IOD_SOURCE';sreason=f'Текущий literal {val!r} не подтверждён: capture BOM вернул 403 blocking page; другие источники в capture относятся к ENSO/NAO и не доказывают диполь Индийского океана. Независимый HOLD карточки 40.'
  elif g=='source_metadata': status='PROPOSED_METADATA_BOUND_TO_READ_PRIMARY';sreason=f'Текущий embedded metadata URL {cur["source"]["url"]}; рекомендуемое verified source: {meta[i][1]}, поскольку его полный body и response headers сохранены, прочитаны и привязаны в sourceReceipts. Для #49 NWS PDF заменяет Wikipedia, которая не использована как доказательство.'
  else:
   if g=='prompt_ordered_answers_key': detail=option_cover.get(i, facts.get(i,''))
   elif g=='explanation': detail=facts.get(i,'')
   elif noteidx is not None: detail=note_source.get(i,['']*4)[noteidx]
   else: detail=facts.get(i,'')
   if i==40: pass
   if i==35 and g=='explanation':detail='NWS glossary and basic-fronts page support elongated low pressure, normally not closed circulation, plus trough/ridge contrast; precipitation can be ahead of upper trough, but “clouds often develop along it” is not directly supported.'
   if i==36 and g=='explanation':detail='NWS glossary supports elongated high pressure/opposite trough; the “often reduced cloudiness” clause is not established by the captured definition.'
   if i==39 and g=='explanation':detail='CPC source supports the dipole, storm track, and European temperature/precipitation effects; note current answer cites Azores/Iceland centers, while CPC specifies Greenland and central North Atlantic (35–40N), so align those centers.'
   if i==41 and g=='explanation':detail='NWS glossary says jet steers low-pressure storms; NWS flight text says west-to-east; this supports the existing clause, while the proposed explanation narrows it to the captured speed/height definition.'
   if i==42 and g=='explanation':detail='NOAA OceanService supports tropical trades, hemisphere directions, ITCZ convergence and historic sailing use; the edited prose removes the lexical answer cue.'
   if i==43 and g=='explanation':detail='NOAA sources define westerlies/eastward midlatitude flow; they do not establish current stem’s specific cyclone-through-Europe causal claim. Proposed stem removes it.'
   if i==44 and g=='explanation':detail='NOAA JetStream defines polar easterlies as east-blowing surface winds from polar highs. Proposed explanation distinguishes wind origin (“from east”) from movement (“toward west”).'
   unsupported=(i==40 or (i==48 and noteidx in (1,3)) or (i==49 and noteidx in (1,2)) or (i in (37,38,39) and noteidx==3) or (i==35 and noteidx in (1,2)) or (i==36 and noteidx in (1,2)))
   status='PARTIAL_PRIMARY_SUPPORT_WITH_LIMIT' if unsupported else 'PRIMARY_PASSAGE_SUPPORT'
   sreason=detail
   if unsupported:sreason+=' This exact note contains a second term/detail not supported by the available passage; retain as an explicit gap or replace only with source-backed text.'
  if g=='prompt_ordered_answers_key' and i in (33,41,43,45,48,49): status='PARTIAL_PRIMARY_SUPPORT_WITH_LIMIT'
  # Explicit, per-literal editorial judgment; source status and pedagogical judgment remain separate.
  if g=='prompt_ordered_answers_key': er=f'{cores[i]} For the entire ordered choice set/key: check one defensible correct option, avoid distractor/wording cues, and preserve the frozen correctIndex {cur["correctIndex"]}.'
  elif g=='explanation': er=f'{cores[i]} Evaluate whether this sentence explains why the answer holds, not simply restates it, and remove causal details beyond the read source.'
  elif noteidx is not None: er=f'{cores[i]} The current note literal {val!r} must help distinguish this particular distractor/key; test its relevance and circularity separately from whether it is factually sourced.'
  elif g=='source_metadata': er=f'{cores[i]} Metadata proposal points to a complete read page actually supporting the card; verifiedAt reflects this evidence review. #40 remains explicitly unverified.'
  else: er=f'{cores[i]} Keep frozen class {cur["difficulty"]}; any mismatch with a short definition/term-recall operation is recorded for a later independent taxonomy decision.'
  refs=[]
  if i==30:refs=['NASA-Auroras','NWS-Glossary-Lighting-Thunder','NWS-Rainbow-Glossary']
  elif i in (31,32,33,34):refs=['NWS-Breeze','NWS-Tropical-Definitions','NWS-Weather-Glossary','NWS-Monsoon-PDF']
  elif i in (35,36):refs=['NWS-Trough/Ridge-Glossary','NWS-Basic-Fronts','NWS-Weather-Glossary']
  elif i in (37,38):refs=['NWS-ENSO']
  elif i==39:refs=['NOAA-CPC-NAO','NWS-ENSO']
  elif i==40:refs=['BOM-IOD-403-only']
  elif i in (41,42,43,44):refs=['NWS-Fronts/Jets','NWS-Flight-Environment','NOAA-OceanService-Winds','NOAA-JetStream-Circulations','NWS-Weather-Glossary']
  elif i in (45,46):refs=['SPC-Parcel-Values']
  elif i==47:refs=['SPC-Shear-SRH']
  elif i in (48,49):refs=['NWS-Precipitation-PDF-pages-2-3']
  groups.append({'group':g,'literal':val,'literalSHA256':h(cjson(val,sort=g=='source_metadata')),'source':{'status':status,'reason':sreason,'evidenceRefs':refs},'editorial':{'status':'ITEM_SPECIFIC_REVIEW','reason':er}})
 new.append({'index':i,'id':cur['id'],'frozenClass':cur['difficulty'],'frozenCorrectIndex':cur['correctIndex'],'currentPreimageSHA256':h(cjson(cur,True)),'currentCard':cur,'proposedCard':prop,'groups':groups,'sourceResolution':'INDEPENDENT_HOLD' if i==40 else 'PRIMARY_SOURCE_READ_WITH_FIELD_LIMITS','qualityCredit':0,'relatedCurrentNeighborIndices':related[i]})
packet={'schema':'mindbattle-weather30-49-source-editorial-packet-v3','authorNativeThreadId':'01a137d4-70e3-74f0-bbe4-0d13e5dca25f','supersedes':str(v2p),'supersedesSHA256':h(v2p.read_bytes()),'scopeTupleSHA256':'66a9cde4368a052113af4a01e9d2f9b8cf16835c61082014d7b962107e1720b5','currentTopicRAW':'b3b48f84d6334f168c0a8a9f800c683dcab2142c4aa2b356b2f3a532ac26fd39','countAsOf':558,'remainingAsOf':1442,'scopeTotal':2000,'qualityCredit':0,'scopeBoundary':'Weather indices 30–49 only. Current full cards and all 80 neighbors are preserved as preimages; proposedCard is a review candidate and was not applied to shared files. Frozen IDs, classes and correct indices are unchanged.','evidencePolicy':'Read complete original bodies and headers before binding claim. HTTP errors and IOD block response are not evidence. PDF text was extracted and all 5 precipitation pages and all 3 monsoon pages visually inspected. NOAA JetStream circulation source assembled from byte ranges after verifying exact entity length/SHA and shared ETag.','entries':new,'currentNeighborSnapshot':old['currentNeighborSnapshot'],'sourceReceipts':receipts,'coordinatorCaptureBatch':{'path':str(alt),'captureManifestSHA256':h((alt/'capture-manifest.json').read_bytes()),'transportReceiptSHA256':h((alt/'coordinator-transport-receipt.json').read_bytes()),'completeOfficialPagesRead':sorted(source_dirs.keys()),'rangeAssembly':{'path':str(alt/'weather-42-44-global-circulation/assembled.body'),'bytes':(alt/'weather-42-44-global-circulation/assembled.body').stat().st_size,'sha256':h((alt/'weather-42-44-global-circulation/assembled.body').read_bytes()),'strongETag':'"1791943788"','rangeCount':13},'iodStatus':'BOM source URL yielded HTTP 403 block body only; #40 remains independent HOLD while other cards reviewed.'}}
out=cjson(packet);dest=root/'weather30-49-source-editorial-packet-v3.json';dest.write_bytes(out)
print(json.dumps({'path':str(dest),'bytes':len(out),'sha256':h(out),'entries':len(new),'groups':sum(len(e['groups']) for e in new),'rationalePairs':sum(2*len(e['groups']) for e in new),'neighborObjects':len(packet['currentNeighborSnapshot']),'rawEvidenceFiles':len(receipts),'qualityCredit':0,'IODhold':[40]},indent=2))
