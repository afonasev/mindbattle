import json,hashlib
from pathlib import Path
base=Path('/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28')
src=base/'current-26-28-source-hard-candidates-v2.json'
out=base/'current-26-28-source-hard-candidates-v3.json'
add=base/'physics26-intensity-normalization-correction.json'
d=json.loads(src.read_text())
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
h=lambda b:hashlib.sha256(b if isinstance(b,bytes) else b.encode('utf-8')).hexdigest()
c=next(x for x in d['candidates'] if x['index']==26)
old_prompt=c['proposedRuntimeCard']['prompt']
new_prompt='Металл с работой выхода φ и f₀=φ/h освещают монохроматически: сначала f₁=1,5f₀, I₁=I, затем f₂=2,25f₀, I₂=3I. Освещённая площадь и квантовый выход одинаковы. Как изменятся Kmax и общее число электронов в секунду?'
assert len(new_prompt)<=320, len(new_prompt)
c['proposedRuntimeCard']['prompt']=new_prompt
c['groups']['composite']['proposedGroup']['prompt']=new_prompt
supp=c['additionalInferenceSource']['inferenceOnlySupplement']
cor=json.loads(add.read_text())
supp['normalizedLiteral']=cor['sourceContext']['correctNormalizedLiteral']
supp['normalizationCorrection']={'path':add.name,'sha256':h(add.read_bytes()),'normalizedLiteralSha256':cor['sourceContext']['correctNormalizedLiteralSha256']}
card=c['proposedRuntimeCard']
c['proposedCanonicalSha256']=h(canon(card))
c['proposedWhole6Sha256']=h(canon([card['prompt'],[a['text'] for a in card['answers']],card['correctIndex'],card['explanation'],*[a['note'] for a in card['answers']]]))
c['groups']['composite']['proposedGroupSha256']=h(canon(c['groups']['composite']['proposedGroup']))
# Keep a compact amendment record, binding the exact previous packet and normalization addendum.
d['edition']='candidate amendment: #26 fixed-area condition and exact normalized source literal; #28 unchanged'
d['basedOn']={'path':src.name,'sha256':h(src.read_bytes())}
d['amendment']={'targetIndex':26,'targetId':c['id'],'priorPrompt':old_prompt,'newPrompt':new_prompt,'promptCharacters':len(new_prompt),'reason':'Fix identical illuminated area so I/(hf) photon number flux density yields the compared total electron rate under the already-fixed equal quantum yield.','normalizationAddendum':{'path':add.name,'sha256':h(add.read_bytes())}}
out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Structural integrity: only target #26 prompt/literal/hash-bindings and packet amendment metadata changed.
old=json.loads(src.read_text()); old26=next(x for x in old['candidates'] if x['index']==26); new26=c
old28=next(x for x in old['candidates'] if x['index']==28); new28=next(x for x in d['candidates'] if x['index']==28)
assert old28==new28
assert len(new26['groups'])==8 and len(set(g['SOURCEreason'] for g in new26['groups'].values()))==8 and len(set(g['EDITORIALreason'] for g in new26['groups'].values()))==8
assert new26['groups']['composite']['proposedGroup']['prompt']==new_prompt
print('prompt_chars',len(new_prompt))
print('prior_packet_sha256',h(src.read_bytes()))
print('normalization_addendum_sha256',h(add.read_bytes()))
print('new_candidate_packet_bytes',out.stat().st_size)
print('new_candidate_packet_sha256',h(out.read_bytes()))
print('new_card_sha256',c['proposedCanonicalSha256'])
print('new_whole6_sha256',c['proposedWhole6Sha256'])
print('new_composite_group_sha256',c['groups']['composite']['proposedGroupSha256'])
print('corrected_literal_sha256',supp['normalizationCorrection']['normalizedLiteralSha256'])
print('candidate28_unchanged',old28==new28)
