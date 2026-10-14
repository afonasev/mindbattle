import json,hashlib,copy
from pathlib import Path
ROOT=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f')
basep=ROOT/'author-correction-2.json';oldpairp=ROOT/'weather-good7-source-editorial-pairs.json'
basebytes=basep.read_bytes();oldpairbytes=oldpairp.read_bytes()
assert hashlib.sha256(basebytes).hexdigest()=='358782192fd2aa06a3b5ed22c32a753e1acad11a4b8f6b128c152648d312d1f0'
assert hashlib.sha256(oldpairbytes).hexdigest()=='6a3edb93249018505d41bfb99c155be1aa96afdae0e5e9a2fa6f16acefa4fc02'
compact=lambda o,sort=False:json.dumps(o,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode('utf-8')
# New complete source candidate, derived from 358; one authored answer note literal changes on #20.
candidate=json.loads(basebytes); c20=next(c for c in candidate['cards'] if c['index']==20); x=c20['proposedCard']
old_note=x['answers'][3]['note']
new_note='Во втором слое температурное преимущество порции перед средой уменьшается на 1,8 °C на каждый километр; остаток 0,2 °C исчезает примерно за 0,11 км, поэтому температуры сравниваются около 1,11 км.'
x['answers'][3]['note']=new_note
c20['ownSourceEditorialReasons']['note3']=['При разности градиентов 1,8 °C/км температурное преимущество 0,2 °C уменьшается до нуля примерно за 0,11 км.']
lit={'prompt':x['prompt'],'orderedAnswerTexts':[a['text'] for a in x['answers']],'correctIndex':x['correctIndex'],'correctAnswerText':x['answers'][x['correctIndex']]['text']}
c20['literalGroupRecipes']['promptAnswersKey']['literal']=lit
c20['sixGroupSHA256']['promptAnswersKey']=hashlib.sha256(compact(lit)).hexdigest()
c20['sixGroupSHA256']['note3']=hashlib.sha256(new_note.encode('utf-8')).hexdigest()
c20['proposedCardCanonicalSHA256']=hashlib.sha256(compact(x,True)).hexdigest()
newcandp=ROOT/'author-correction-3.json';newcandbytes=compact(candidate)+b'\n';newcandp.write_bytes(newcandbytes)
newcandsha=hashlib.sha256(newcandbytes).hexdigest()
# Correct pair addendum as a separate additive file; original 6a is never overwritten.
add=json.loads(oldpairbytes); add['supersedesAddendum']={'path':str(oldpairp),'bytes':len(oldpairbytes),'sha256':hashlib.sha256(oldpairbytes).hexdigest(),'preserveImmutable':True}
add['boundCandidate']={'path':str(newcandp),'bytes':len(newcandbytes),'sha256':newcandsha,'parentCandidatePath':str(basep),'parentCandidateSHA256':hashlib.sha256(basebytes).hexdigest(),'immutability':'only #20 note3 authored literal changed; all other proposed card fields and card objects retained'}
add['sourceCorrections']=[
 {'index':28,'group':'note0','kind':'SOURCE rationale only','oldReason':'В контексте распространения в источнике говорит, что ударная волна теряет высокочастотные компоненты и растягивается при удалении; текст о дальнем звуке связывает это с рокотом.','newReason':'Точный контекст источника говорит, что при распространении ударная волна растягивается, ослабевает и становится протяжённой; на большом расстоянии сочетание волн даёт непрерывный рокот. Источник не утверждает о потере высокочастотных компонентов.','contextRefs':['81fa7aa8300c2d58ea52ea6479802524f6f57a066f5c6a14040d98d1dfdb8300','95ddfc24be1516b7f648f307169a782606d828876f484e69b4460699e657cf01']},
 {'index':21,'group':'note0','kind':'SOURCE rationale only','newReason':'В полном первичном контексте SPC определение уровня конденсации при подъёме (LCL) прямо говорит, что при вынужденном подъёме его высота соответствует высоте основания облака; это непосредственно подтверждает заметку.','contextRefs':['2115926e4d9e16b3507613f38e0fc237a26edb68658a6249d108bdd638f2b411']},
 {'index':20,'group':'note3','kind':'one product note literal + matching author reason/hash rebinding','oldLiteral':old_note,'newLiteral':new_note,'newSourceReason':'Глоссарий определяет адиабатическое изменение как изменение температуры без теплообмена с окружающим воздухом, а сухой градиент задаёт 9,8 °C/км. Вместе с градиентом среды 8 °C/км из стема это означает уменьшение температурного преимущества на 1,8 °C на километр, а не потерю тепловой энергии.','contextRefs':['37f05c5b4930cc332c0c5c9638ab45b8a07206f8705549c4d4f3a2392f9ac12c','d354db08c526baffe169f0a69a72353d33d0be94877ba20c18b45d2281157073','f55f6e999cd2e16a3f72bd24ccb4ac67ba5ce7b99685fe6459ff49ff4feb78bd']}]
entries={e['index']:e for e in add['cards']}
# #20 new product literals require the parent-card and literal-group hashes to be rebound.
e20=entries[20];e20['proposedCardCanonicalSHA256']=c20['proposedCardCanonicalSHA256'];g20=e20['groups']['note3'];g20['literal']=new_note;g20['exactGroupSHA256']=c20['sixGroupSHA256']['note3'];g20['SOURCE']['reason']=add['sourceCorrections'][2]['newSourceReason']
# Correct only source rationales for #21 and #28; their candidate/runtime literals remain identical.
e21=entries[21];e21['groups']['note0']['SOURCE']['reason']=add['sourceCorrections'][1]['newReason']
spc={'label':'SPC LCL definition exact byte slice','sourceRef':'CAP-spc-parcel-values','contextSHA256':'2115926e4d9e16b3507613f38e0fc237a26edb68658a6249d108bdd638f2b411','bodySHA256':'fc6ee69c1ea46c620c867bb2c35294597803563d64b9a57f6ed7b572c0226917','bodyBytes':2386,'rawBoundsHalfOpen':[1052,1242],'path':'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-parcel-values.body','receiptKind':'locally-read exact source slice from existing capture; no new capture or network access'}
e21['primaryContextRefs'].append(spc)
e21['groups']['note0']['SOURCE']['primaryContextRefs'].append(spc['contextSHA256'])
e28=entries[28];e28['groups']['note0']['SOURCE']['reason']=add['sourceCorrections'][0]['newReason']
add['effectiveStatus']='SOURCE_CORRECTION_ADDITIVE; qualification and credit remain coordinator-owned'
newpairp=ROOT/'weather-good7-source-editorial-pairs-correction-1.json';newpairbytes=compact(add)+b'\n';newpairp.write_bytes(newpairbytes)
newpairsha=hashlib.sha256(newpairbytes).hexdigest()
# Final independent bindings and exact-delta audit.
assert hashlib.sha256(basep.read_bytes()).hexdigest()=='358782192fd2aa06a3b5ed22c32a753e1acad11a4b8f6b128c152648d312d1f0'
assert hashlib.sha256(oldpairp.read_bytes()).hexdigest()=='6a3edb93249018505d41bfb99c155be1aa96afdae0e5e9a2fa6f16acefa4fc02'
assert [c['index'] for c in candidate['cards']]==[c['index'] for c in json.loads(basebytes)['cards']]
# only intended proposedCard literal differs across source packet; same card/source metadata set and other indices byte-equivalent as objects.
base=json.loads(basebytes)
for old,new in zip(base['cards'],candidate['cards']):
 if old['index']==20:
  ox=copy.deepcopy(old['proposedCard']);nx=copy.deepcopy(new['proposedCard']);ox['answers'][3]['note']=nx['answers'][3]['note'];assert ox==nx
 else: assert old==new
# write manifests
m1={'schema':'mindbattle-bounded-source-correction-v1','sourceCandidatePath':str(basep),'sourceCandidateBytes':len(basebytes),'sourceCandidateSHA256':hashlib.sha256(basebytes).hexdigest(),'effectiveCandidatePath':str(newcandp),'effectiveCandidateBytes':len(newcandbytes),'effectiveCandidateSHA256':newcandsha,'previousPairedAddendumPath':str(oldpairp),'previousPairedAddendumBytes':len(oldpairbytes),'previousPairedAddendumSHA256':hashlib.sha256(oldpairbytes).hexdigest(),'effectivePairedAddendumPath':str(newpairp),'effectivePairedAddendumBytes':len(newpairbytes),'effectivePairedAddendumSHA256':newpairsha,'productLiteralDelta':['index 20 / note3 only'],'sourceRationaleOnlyDeltas':['index 21 / note0','index 28 / note0'],'scopeIndices':[20,21,25,26,27,28,29],'holdsExcluded':[22,23,24],'pairCount':56,'reasonCount':112,'sourceCredit':0,'qualification':'NOT_QUALIFIED; coordinator qualification required','noCaptureRuntimeQAOrGit':True}
mp=ROOT/'source-correction-1-manifest.json';mb=json.dumps(m1,ensure_ascii=False,indent=2).encode()+b'\n';mp.write_bytes(mb)
print('candidate3',len(newcandbytes),newcandsha)
print('pairs correction',len(newpairbytes),newpairsha)
print('manifest',len(mb),hashlib.sha256(mb).hexdigest())
print('Only candidate product literal changed: #20 note3; source-only pairs changed: #21 note0 and #28 note0; immutable 358/6a preserved.')
