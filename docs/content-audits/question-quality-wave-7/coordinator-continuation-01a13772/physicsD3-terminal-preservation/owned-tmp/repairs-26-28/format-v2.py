import json,hashlib,os
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'
src=b+'/current-26-28-source-hard-candidates.json'; old=json.load(open(src)); d=json.loads(json.dumps(old,ensure_ascii=False))
H=lambda x:hashlib.sha256(x.encode('utf-8') if isinstance(x,str) else x).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
d['schema']='mindbattle-source-hard-candidates-current-26-28-v2'
d['edition']='v2-format-only'
d['basedOn']={'path':'current-26-28-source-hard-candidates.json','sha256':H(open(src,'rb').read()),'preservedUnchanged':True}
t26=next(x for x in d['candidates'] if x['index']==26); t28=next(x for x in d['candidates'] if x['index']==28)
# Condense to 3 meaningful sentences; all premises and inference conditions remain explicit.
exp26='Поскольку f₀=φ/h, в двух режимах Kmax=hf−φ равны 0,5φ и 1,25φ, то есть отношение составляет 2,5. Интенсивность — энергия на площадь за время; каждый фотон несёт hf, поэтому поток фотонов выводится как I/(hf), а его отношение (3I/(2,25hf₀))/(I/(1,5hf₀)) равно 2. При одинаковом квантовом выходе число электронов за секунду также удваивается.'
prompt28='В опыте Дэвиссона—Джермера электроны из покоя ускоряют напряжением 54 В и рассеивают на никеле с периодом решётки 2,15 Å. Интенсивный максимум наблюдается при φ≈50°. Какой порядок максимума согласуется с волновой длиной электрона, предсказанной по напряжению? Даны mₑ=9,11×10⁻³¹ кг, e=1,60×10⁻¹⁹ Кл, h=6,63×10⁻³⁴ Дж·с.'
t26['proposedRuntimeCard']['explanation']=exp26
t28['proposedRuntimeCard']['prompt']=prompt28
# Update group literals/hashes and exact card hashes for affected fields/cards only.
for t in (t26,t28):
 card=t['proposedRuntimeCard']; cidx=t['index']
 for g,v in t['groups'].items():
  if cidx==26 and g=='explanation': value=exp26
  elif cidx==28 and g=='composite': value={'prompt':prompt28,'orderedAnswerTexts':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']}
  else: continue
  v['proposedGroup']=value;v['proposedGroupSha256']=H(canon(value))
 t['proposedCanonicalSha256']=H(canon(card))
 t['proposedWhole6Sha256']=H(canon([card['prompt'],[a['text'] for a in card['answers']],card['correctIndex'],card['explanation'],*[a['note'] for a in card['answers']]]))
# Verify format and preservation invariants.
assert len(prompt28)<320,len(prompt28)
assert len(exp26.split())<=70,len(exp26.split())
assert 2<=sum(1 for ch in exp26 if ch=='.')<=4
assert old['currentBaseline']['topicRawSha256']==d['currentBaseline']['topicRawSha256']
assert old['currentBaseline']['protectedOther98ForTwoTargetScope']==d['currentBaseline']['protectedOther98ForTwoTargetScope']
assert old['currentBaseline']['applied27']==d['currentBaseline']['applied27']
assert old['candidates'][0]['currentCanonicalSha256']==t26['currentCanonicalSha256'] and old['candidates'][1]['currentCanonicalSha256']==t28['currentCanonicalSha256']
out=b+'/current-26-28-source-hard-candidates-v2.json';open(out,'w').write(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',H(open(out,'rb').read()),'stem28 chars',len(prompt28),'ex26 words',len(exp26.split()),'ex26 sentences',exp26.count('.') )
