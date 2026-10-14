import json,hashlib,os
from html.parser import HTMLParser
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28';root='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
source_rel='docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/capture-only/physics30-49-gaps/49/assembled-original-entity.body'
body=open(root+'/'+source_rel,'rb').read(); body_sha=hashlib.sha256(body).hexdigest()
start,end=106616,107077; raw=body[start:end]; raw_text=raw.decode('utf-8')
class TextNodes(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]
 def handle_data(self,data): self.parts.append(data)
p=TextNodes();p.feed(raw_text); normalized=' '.join(' '.join(p.parts).split())
previous=json.load(open(b+'/current-26-28-source-hard-candidates-v2.json'))
old_literal=previous['candidates'][0]['additionalInferenceSource']['inferenceOnlySupplement']['normalizedLiteral']
assert body_sha=='c4786e44925e83c13eeb8cc1ba8a0d9d6f9c78ee5c72764b0c1670cfb17d91fc'
assert 'sound intensity .' in normalized and 'sound intensity .' not in old_literal
H=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode('utf-8')).hexdigest()
correction={'schema':'mindbattle-26-intensity-source-normalization-correction-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','correctionOnly':True,'bindsPackets':[{'path':'current-26-28-source-hard-candidates-v2.json','sha256':H(open(b+'/current-26-28-source-hard-candidates-v2.json','rb').read())},{'path':'current-26-28-source-hard-candidates.json','sha256':H(open(b+'/current-26-28-source-hard-candidates.json','rb').read())}],'sourceContext':{'title':'OpenStax Physics §14.2 Sound Intensity and Sound Level','url':'https://openstax.org/books/physics/pages/14-2-sound-intensity-and-sound-level','path':source_rel,'capturedBodySha256':body_sha,'paragraphDOMId':'fs-id1167064726893','startByte':start,'endByteExclusive':end,'rawLiteralUtf8':raw_text,'rawSliceSha256':H(raw),'normalizationRecipe':'Parse this exact paragraph fragment with Python html.parser.HTMLParser(convert_charrefs=True); collect each handle_data value in order; join values using one ASCII space; collapse all whitespace runs to one ASCII space; trim leading/trailing whitespace. Preserve punctuation whitespace produced at inline-tag boundaries; do not add punctuation-aware trimming.','correctNormalizedLiteral':normalized,'correctNormalizedLiteralSha256':H(normalized),'priorPunctuationCleanedLiteral':old_literal,'priorPunctuationCleanedLiteralSha256':H(old_literal),'correction':'The prior candidate removed whitespace before the period after “sound intensity”. The exact DOM text-node join retains one space there; that literal is now stated without altering the prior packet bytes.'},'immutability':{'productCardChanged':False,'sourceGroupsChanged':False,'candidateHashesChanged':False,'source2Changed':False,'priorPacketBytesPreserved':True},'qualification':'This is a literal/normalization provenance correction only; it does not change the source inference or assert qualification.'}
out=b+'/physics26-intensity-normalization-correction.json';open(out,'w').write(json.dumps(correction,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print(os.path.getsize(out),H(open(out,'rb').read()),'rawslice',H(raw),'norm',H(normalized),'length',len(normalized))
