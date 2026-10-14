import json,hashlib
from pathlib import Path
p=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f/author-final.json');d=json.loads(p.read_bytes());out=p
bindings={x['sourceKey']:x for x in d['sourceCaptureBindings']}
uses={
20:[('QUALIFIED-S5','dry unsaturated parcel rate 9.8°C/km'),('CAP-environmental-lapse','environmental rate is decrease of temperature with height, usually measured by radiosonde'),('CAP-stability-glossary','neutral unsaturated air equates environmental and dry adiabatic rates')],
21:[('QUALIFIED-S5','dry and moist parcel rates; moist rate varies with parcel temperature and pressure'),('CAP-spc-parcel-values','LCL marks saturation and corresponds to cloud base in forced ascent')],
22:[('CAP-environmental-lapse','observed environmental lapse rate'),('CAP-stability-glossary','neutral conditions compare observed rate to dry/moist parcel rates'),('QUALIFIED-S5','dry and moist adiabatic rates')],
23:[('CAP-spc-parcel-values','CAPE and CINH integrated areas; LFC, EL, MPL and momentum above EL'),('QUALIFIED-S6','a capping inversion is a warm layer aloft that suppresses/delays storm development')],
24:[('CAP-spc-parcel-values','square-root parcel-theory speed estimate; CAPE/CINH, LFC, EL, MPL and entrainment/water-loading caveat')],
25:[('CAP-noaa-build-weather-station','cup anemometer rpm and diameter conversion to approximate mph'),('CAP-anemometer','anemometer measures wind speed')],
26:[('CAP-noaa-build-weather-station','rain gauge scale and location clear of overhead objects'),('CAP-rain-gauge','rain gauge measures quantity of rain')],
27:[('CAP-lightning','positive cloud-to-ground flash delivers positive charge, contrasts with common negative charge; more frequent in some severe storms')],
28:[('CAP-thunder-jetstream','nearby short bang/crack/snap; distant waves stretch and combine as continuous rumble; temperature inversion refracts sound and amplifies thunder'),('CAP-thunder','glossary thunder/lightning terminology')],
29:[('CAP-rainbow-optics','primary bow one internal reflection; secondary two, reversed colors and ~50° vs ~42°; higher orders uncommon'),('CAP-rainbow','NWS glossary description of refraction, reflection and dispersion')]
}
review=[]
for ix,items in uses.items():
 sources=[]
 for key,focus in items:
  bind=bindings[key]
  body=bind['body']; path=Path(body['path'])
  if not path.is_absolute():path=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')/path
  raw=path.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
  assert len(raw)==body['rawBytes'] and sha==body['rawSHA256'],(key,len(raw),sha,body)
  sources.append({'sourceKey':key,'requestedURL':bind['requestedURL'],'bodyPath':str(path),'bodyBytes':len(raw),'bodySHA256':sha,'completeBodyRawBoundsHalfOpen':[0,len(raw)],'reviewedFact':focus,'typedCompleteContexts':bind.get('typedCompleteContexts',[])})
 review.append({'index':ix,'cardId':d['cards'][ix-20]['id'],'sourcesPersonallyRead':sources})
d['authorReviewedPrimaryContexts']=review
# Correct earlier inherited preflight counts to match this independent revision.
d['authorPreflight']={'candidateCount':10,'contentGroupsPerCard':6,'classMetadataGroupsPerCard':2,'ownReasonStatementsPerCard':8,'ownReasonStatementsTotal':80,'answerRowsAreFourTextNoteObjects':True,'allExplanationsHave2To4MeaningfulSentences':True,'idsTopicClassesAndKeyIndexesMatchFrozenScope':True,'literalGroupsAndHashesRecomputed':True,'completeSourceBodiesAndRawBindingsPresent':True,'currentNeighborsReadFromExactSnapshot':True,'qualificationAndAcceptance':'NOT_CLAIMED'}
d['ownPrimaryContextReview']['allSourceRefsReviewedAgainstExistingCompleteBodies']=True
d['ownPrimaryContextReview']['perCardSourceReadReceipts']=True
# Preserve exact immutable parent identity and report evidence path/hashes for both current and historical packet.
d['authorIdentityAndProvenance']['currentCandidateParentPacketBytes']=Path(d['authorIdentityAndProvenance']['parentCandidatePath']).stat().st_size
d['authorIdentityAndProvenance']['currentCandidateParentPacketSHA256']=hashlib.sha256(Path(d['authorIdentityAndProvenance']['parentCandidatePath']).read_bytes()).hexdigest()
compact=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
for c in d['cards']:
 x=c['proposedCard'];lit=c['literalGroupRecipes']['promptAnswersKey']['literal'];
 assert lit['prompt']==x['prompt'] and lit['orderedAnswerTexts']==[a['text'] for a in x['answers']]
 assert x['correctIndex']==c['frozenCorrectIndex'] and x['difficulty']==c['frozenClass']
 assert len(x['answers'])==4
 assert len(c['ownSourceEditorialReasons'])==6 and len(c['difficultyAndMetadataSourceEditorialReasons'])==2
 assert all(len(v)==1 and v[0] for v in c['ownSourceEditorialReasons'].values())
 assert all(len(v)==1 and v[0] for v in c['difficultyAndMetadataSourceEditorialReasons'].values())
 assert hashlib.sha256(compact(x)).hexdigest()==c['proposedCardCanonicalSHA256']
 assert hashlib.sha256(compact(x['difficulty'])).hexdigest()==c['classSHA256']
 assert hashlib.sha256(compact(x['source'])).hexdigest()==c['metadataSHA256']
# All 80 unique explanation reasons, no generic class/meta templates.
reasons=[v[0] for c in d['cards'] for v in c['ownSourceEditorialReasons'].values()]
reasons += [v[0] for c in d['cards'] for v in c['difficultyAndMetadataSourceEditorialReasons'].values()]
assert len(reasons)==80 and len(set(reasons))==80
out.write_bytes(json.dumps(d,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
print('bytes',len(out.read_bytes()),'sha256',hashlib.sha256(out.read_bytes()).hexdigest(),'own reviewed sources',sum(len(x['sourcesPersonallyRead']) for x in review))
