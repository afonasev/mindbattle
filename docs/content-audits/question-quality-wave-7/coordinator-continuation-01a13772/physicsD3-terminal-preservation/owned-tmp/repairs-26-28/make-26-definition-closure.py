import json,hashlib
from pathlib import Path
b=Path('/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28')
src=b/'current-26-28-source-hard-candidates-v3.json'; out=b/'current-26-28-source-hard-candidates-v4.json'
h=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
d=json.loads(src.read_text()); c=next(x for x in d['candidates'] if x['index']==26)
old=c['proposedRuntimeCard']['prompt']
new='Металл с работой выхода φ и пороговой частотой f₀=φ/h освещают монохроматически: сначала частотой f₁=1,5f₀ и энергетической интенсивностью I₁=I, затем f₂=2,25f₀ и I₂=3I. Площадь освещения и квантовый выход одинаковы. Как изменятся максимальная кинетическая энергия фотоэлектронов и число испущенных электронов в секунду?'
assert len(new)==320
card=c['proposedRuntimeCard']; card['prompt']=new
c['groups']['composite']['proposedGroup']['prompt']=new
c['proposedCanonicalSha256']=h(canon(card))
c['proposedWhole6Sha256']=h(canon([card['prompt'],[a['text'] for a in card['answers']],card['correctIndex'],card['explanation'],*[a['note'] for a in card['answers']]]))
c['groups']['composite']['proposedGroupSha256']=h(canon(c['groups']['composite']['proposedGroup']))
d['edition']='candidate amendment: #26 explicit physical quantities and measured outputs; #28 unchanged'
d['basedOn']={'path':src.name,'sha256':h(src.read_bytes())}
d['amendment']={'targetIndex':26,'targetId':c['id'],'priorPrompt':old,'newPrompt':new,'promptCharacters':len(new),'reason':'Explicitly defines f as frequency and I as energy intensity, names maximum kinetic energy of photoelectrons, and asks for emitted photoelectrons per second; preserves same area and equal quantum yield.'}
out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
old_d=json.loads(src.read_text()); assert next(x for x in old_d['candidates'] if x['index']==28)==next(x for x in d['candidates'] if x['index']==28)
assert len(c['groups'])==8 and len({x['SOURCEreason'] for x in c['groups'].values()})==8 and len({x['EDITORIALreason'] for x in c['groups'].values()})==8
assert c['proposedRuntimeCard']['answers']==next(x for x in old_d['candidates'] if x['index']==26)['proposedRuntimeCard']['answers']
assert c['proposedRuntimeCard']['explanation']==next(x for x in old_d['candidates'] if x['index']==26)['proposedRuntimeCard']['explanation']
print('based_on_sha256',h(src.read_bytes()))
print('packet_bytes',out.stat().st_size)
print('packet_sha256',h(out.read_bytes()))
print('prompt_chars',len(new))
print('card_sha256',c['proposedCanonicalSha256'])
print('whole6_sha256',c['proposedWhole6Sha256'])
print('composite_group_sha256',c['groups']['composite']['proposedGroupSha256'])
print('candidate28_unchanged',True)
