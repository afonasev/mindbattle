import json, pathlib, hashlib, base64, re, copy
from pypdf import PdfReader
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
root=pathlib.Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036')
source=pathlib.Path('/Users/eaafonasev/Documents/Codex/2026-10-14/mindbattle-source-physics-next20/outputs/physics-source20-author-edition3.json')
out=root/'author-original-edition4.json'
d=json.loads(source.read_bytes()); d['edition']=4
d['parentArtifact']={'path':str(source),'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
d['authorNotes']={**d.get('authorNotes',{}),'revision':'edition4: corrected each literal-field source locator to the exact BIPM page or OpenStax claim context supporting that component/option; added BIPM prefix-table page and a precise Newton-force/velocity context; restored the current author read attestation. Prior editions remain immutable.'}
# Add the BIPM full-page extract for the kilo/milli prefix facts used by #32.
pdf=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/physics-force-si-unit.pdf')
pdfbytes=pdf.read_bytes(); reader=PdfReader(str(pdf))
pctx={'binding':{'bytes':len(pdfbytes),'path':str(pdf),'sha256':hashlib.sha256(pdfbytes).hexdigest()},'contextId':'ctx-041','extraction':'pypdf full-page text extraction; PDF page and printed page retained','kind':'pdf_page_full_text','literalExtractedText':reader.pages[144].extract_text() or '','pdfPage':145,'printedPage':143,'source':'BIPM SI Brochure, 9th edition'}
d['primaryContexts'].append(pctx)
# Add the exact §4.4 paragraph explaining what a free-body diagram represents for #37 note 3.
cnxml=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/openstax-m54131-index.cnxml')
raw=cnxml.read_bytes(); tree=ET.fromstring(raw); target=next((x for x in tree.iter() if x.attrib.get('id')=='fs-idm20343184'),None)
if target is None: raise RuntimeError('missing CNXML paragraph fs-idm20343184')
text=' '.join(' '.join(''.join(target.itertext()).split()).split())
old_ctx=next(c for c in d['primaryContexts'] if c.get('elementId')=='fs-idm15080864')
ctx37={'binding':dict(old_ctx['binding']),'contextId':'ctx-042','elementId':'fs-idm20343184','kind':'cnxml_element','literalText':text,'source':'OpenStax Physics §4.4 Newton’s Second Law, free-body diagrams','tag':'para'}
d['primaryContexts'].append(ctx37)
# Add the exact §13.1 summary list that classifies earthquake waves as mechanical.
wave=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/openstax-m54314-index.cnxml')
waveraw=wave.read_bytes(); wtree=ET.fromstring(waveraw); wtarget=next((x for x in wtree.iter() if x.attrib.get('id')=='fs-id1167065033412'),None)
if wtarget is None: raise RuntimeError('missing CNXML summary list fs-id1167065033412')
wtext=' '.join(''.join(wtarget.itertext()).split())
wold=next(c for c in d['primaryContexts'] if c.get('elementId')=='fs-id1167065809902')
ctx45={'binding':dict(wold['binding']),'contextId':'ctx-043','elementId':'fs-id1167065033412','kind':'cnxml_element','literalText':wtext,'source':'OpenStax Physics §13.1 Types of Waves, section summary','tag':'list'}
d['primaryContexts'].append(ctx45)
# Add the additional exact explanatory paragraph to the already bound full §4.2 capture.
cap41=next(c for c in d['primaryContexts'] if c.get('url')=='https://openstax.org/books/physics/pages/4-2-newtons-first-law-of-motion-inertia')
body=pathlib.Path(cap41['fullEntityBinding']['path']).read_text(encoding='utf-8')
class T(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,x):
  if x.strip():self.parts.append(x.strip())
import re
m=re.search(r'<p\b[^>]*\bid=["\']fs-idp76991328["\'][^>]*>.*?</p>',body,re.I|re.S)
if not m: raise RuntimeError('missing §4.2 paragraph fs-idp76991328')
parser=T();parser.feed(m.group(0));txt=' '.join(' '.join(parser.parts).split())
additional={'elementId':'fs-idp76991328','tag':'p','literalText':txt}
if not any(x.get('elementId')==additional['elementId'] for x in cap41['selectedFullParagraphs']): cap41['selectedFullParagraphs'].append(additional)
for prov in d['captureProvenance']:
 ent=prov.get('assembledEntity',{})
 if ent.get('url')==cap41['url']:
  ent['selectedFullParagraphs']=copy.deepcopy(cap41['selectedFullParagraphs'])
# Context reference aliases. These point to exact typed source page/element records, never merely to a URL or chapter label.
C={c['contextId']:c for c in d['primaryContexts']}
def refs(*ids): return list(ids)
M={
30:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-000'),'explanation':refs('ctx-000','ctx-038'),'difficulty':refs('ctx-000'),'sourceMetadata':refs('ctx-000','ctx-038'),'note_0':refs('ctx-000','ctx-038'),'note_1':refs('ctx-000'),'note_2':refs('ctx-000'),'note_3':refs('ctx-000','ctx-037')},
31:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-000','ctx-001','ctx-002'),'explanation':refs('ctx-000'),'difficulty':refs('ctx-000'),'sourceMetadata':refs('ctx-000','ctx-001','ctx-002'),'note_0':refs('ctx-000'),'note_1':refs('ctx-001'),'note_2':refs('ctx-002'),'note_3':refs('ctx-001')},
32:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-000','ctx-002','ctx-020','ctx-021','ctx-038'),'explanation':refs('ctx-000','ctx-021','ctx-041'),'difficulty':refs('ctx-000'),'sourceMetadata':refs('ctx-000','ctx-002','ctx-020','ctx-021','ctx-038','ctx-041'),'note_0':refs('ctx-021'),'note_1':refs('ctx-000','ctx-038'),'note_2':refs('ctx-020'),'note_3':refs('ctx-002')},
33:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-001','ctx-002'),'explanation':refs('ctx-002'),'difficulty':refs('ctx-002'),'sourceMetadata':refs('ctx-001','ctx-002'),'note_0':refs('ctx-002'),'note_1':refs('ctx-001','ctx-002'),'note_2':refs('ctx-002'),'note_3':refs('ctx-001')},
34:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-000','ctx-001','ctx-002','ctx-020'),'explanation':refs('ctx-001'),'difficulty':refs('ctx-001'),'sourceMetadata':refs('ctx-000','ctx-001','ctx-002','ctx-020'),'note_0':refs('ctx-001'),'note_1':refs('ctx-001'),'note_2':refs('ctx-000','ctx-021'),'note_3':refs('ctx-020')},
35:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-000','ctx-001','ctx-002','ctx-037'),'explanation':refs('ctx-001'),'difficulty':refs('ctx-001'),'sourceMetadata':refs('ctx-000','ctx-001','ctx-002','ctx-037'),'note_0':refs('ctx-002'),'note_1':refs('ctx-001'),'note_2':refs('ctx-002'),'note_3':refs('ctx-000','ctx-037')},
36:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-001','ctx-002'),'explanation':refs('ctx-002'),'difficulty':refs('ctx-002'),'sourceMetadata':refs('ctx-002'),'note_0':refs('ctx-002'),'note_1':refs('ctx-001','ctx-002'),'note_2':refs('ctx-002'),'note_3':refs('ctx-001')},
37:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-011'),'explanation':refs('ctx-011'),'difficulty':refs('ctx-011'),'sourceMetadata':refs('ctx-011','ctx-042'),'note_0':refs('ctx-011'),'note_1':refs('ctx-011'),'note_2':refs('ctx-011'),'note_3':refs('ctx-042')},
38:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-019'),'explanation':refs('ctx-019'),'difficulty':refs('ctx-019'),'sourceMetadata':refs('ctx-019'),'note_0':refs('ctx-019'),'note_1':refs('ctx-019'),'note_2':refs('ctx-019'),'note_3':refs('ctx-019')},
39:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-007'),'explanation':refs('ctx-007'),'difficulty':refs('ctx-007'),'sourceMetadata':refs('ctx-007'),'note_0':refs('ctx-007'),'note_1':refs('ctx-007'),'note_2':refs('ctx-007'),'note_3':refs('ctx-007')},
40:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-039'),'explanation':refs('ctx-039'),'difficulty':refs('ctx-039'),'sourceMetadata':refs('ctx-039'),'note_0':refs('ctx-039'),'note_1':refs('ctx-039'),'note_2':refs('ctx-039'),'note_3':refs('ctx-039')},
41:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-040'),'explanation':refs('ctx-040'),'difficulty':refs('ctx-040'),'sourceMetadata':refs('ctx-040'),'note_0':refs('ctx-040'),'note_1':refs('ctx-040'),'note_2':refs('ctx-040'),'note_3':refs('ctx-040')},
42:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-028','ctx-029','ctx-030','ctx-031'),'explanation':refs('ctx-028','ctx-031'),'difficulty':refs('ctx-031'),'sourceMetadata':refs('ctx-028','ctx-029','ctx-030','ctx-031'),'note_0':refs('ctx-031'),'note_1':refs('ctx-031'),'note_2':refs('ctx-028'),'note_3':refs('ctx-029','ctx-030')},
43:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-008','ctx-022'),'explanation':refs('ctx-008','ctx-022'),'difficulty':refs('ctx-022'),'sourceMetadata':refs('ctx-008','ctx-022'),'note_0':refs('ctx-022'),'note_1':refs('ctx-022'),'note_2':refs('ctx-008'),'note_3':refs('ctx-008','ctx-022')},
44:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-028','ctx-030','ctx-031'),'explanation':refs('ctx-028','ctx-031'),'difficulty':refs('ctx-028'),'sourceMetadata':refs('ctx-028','ctx-030','ctx-031'),'note_0':refs('ctx-030'),'note_1':refs('ctx-031'),'note_2':refs('ctx-028'),'note_3':refs('ctx-028','ctx-031')},
45:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-014','ctx-015','ctx-043'),'explanation':refs('ctx-014','ctx-015'),'difficulty':refs('ctx-014'),'sourceMetadata':refs('ctx-014','ctx-015','ctx-043'),'note_0':refs('ctx-014'),'note_1':refs('ctx-015'),'note_2':refs('ctx-043'),'note_3':refs('ctx-014')},
46:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-006','ctx-016','ctx-023'),'explanation':refs('ctx-006','ctx-016'),'difficulty':refs('ctx-006'),'sourceMetadata':refs('ctx-006','ctx-016','ctx-023'),'note_0':refs('ctx-006'),'note_1':refs('ctx-006','ctx-025'),'note_2':refs('ctx-006'),'note_3':refs('ctx-006','ctx-016')},
47:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-017','ctx-025','ctx-027','ctx-036'),'explanation':refs('ctx-025','ctx-027','ctx-036'),'difficulty':refs('ctx-027'),'sourceMetadata':refs('ctx-025','ctx-027','ctx-036'),'note_0':refs('ctx-027','ctx-036'),'note_1':refs('ctx-027'),'note_2':refs('ctx-027','ctx-036'),'note_3':refs('ctx-027')},
48:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-009'),'explanation':refs('ctx-009'),'difficulty':refs('ctx-009'),'sourceMetadata':refs('ctx-009'),'note_0':refs('ctx-009'),'note_1':refs('ctx-009'),'note_2':refs('ctx-009'),'note_3':refs('ctx-009')},
49:{'whole_prompt_all_four_ordered_answers_correctIndex_key':refs('ctx-010'),'explanation':refs('ctx-010'),'difficulty':refs('ctx-010'),'sourceMetadata':refs('ctx-010'),'note_0':refs('ctx-010'),'note_1':refs('ctx-010'),'note_2':refs('ctx-010'),'note_3':refs('ctx-010')}
}
# Fix the #32 explanation/difficulty reason to describe the actual literals, and #37 note3 to the exact CNXML claim.
entries={e['index']:e for e in d['entries']}
entries[32]['componentReasons']['explanation']={'SOURCE':'BIPM SI Brochure Table 2 identifies metre (m) as the base unit of length; the metre definition gives its relation to the speed of light, and Table 7 defines kilo as 10^3, supporting kilometre = 1000 m.','EDITORIAL':'The feedback gives the base-unit symbol and one familiar decimal multiple, keeping both facts after the direct unit question.'}
entries[32]['componentReasons']['difficulty']={'SOURCE':'BIPM SI Brochure Table 2 directly assigns metre (m) to the base quantity length.','EDITORIAL':'The prompt is a one-step match between a named base quantity and its SI unit; no conversion is required.'}
entries[32]['componentReasons']['whole_prompt_all_four_ordered_answers_correctIndex_key']={'SOURCE':'BIPM Table 2 identifies metre (m) as the base length unit. The other listed units are independently identified in the BIPM derived-unit table, accepted-use table, and prefix/periodic-phenomena notes.','EDITORIAL':'The stem asks for the base unit of length. The four options use the frozen order and the metre key remains in slot 0.'}
entries[32]['componentReasons']['sourceMetadata']={'SOURCE':'The BIPM SI Brochure PDF is the official source for the metre definition and the referenced SI unit/prefix tables; the packet maps each exact fact-bearing component to its own page context.','EDITORIAL':'The citation identifies the official brochure while the audit packet carries page-level bindings for each option note and explanation.'}
entries[32]['componentReasons']['note_1']={'SOURCE':'BIPM Table 2 lists kilogram as the base unit of mass, and §3 says mass prefixes attach to gram; the mass-specific exception is on printed p.144.','EDITORIAL':'The note distinguishes the gram distractor from the base length unit by stating its mass-unit role and the SI base-unit exception.'}
entries[37]['card']['answers'][3]['note']='Свободные диаграммы тела показывают действующие силы, а не скорость тела.'
entries[45]['card']['answers'][2]['note']='Волны землетрясений, как и звуковые, относятся к механическим.'
entries[45]['componentReasons']['note_2']={'SOURCE':'OpenStax Physics §13.1 section summary states that sound, water, and earthquake waves are mechanical waves; the same summary says mechanical waves travel through a medium.','EDITORIAL':'This note gives the source’s classification of seismic waves without repeating the keyed light-wave answer.'}
entries[37]['componentReasons']['note_3']={'SOURCE':'OpenStax Physics §4.4 paragraph fs-idm20343184 says a free-body diagram shows only external forces, not acceleration or velocity.','EDITORIAL':'The note separates a force vector from the object’s velocity, addressing the “direction of motion” distractor without repeating the gravity key.'}
# Recompute current literal bindings from exact edition 4 text and the per-field locators above.
def locator(c):
 k=c.get('kind')
 if k=='pdf_page_full_text': return {'type':k,'pdfPage':c.get('pdfPage'),'printedPage':c.get('printedPage'),'source':c.get('source'),'binding':c.get('binding')}
 if k in ('cnxml_element','cnxml-full-element-context','cnxml-element-and-media-alt','cnxml-full-element-context'): return {'type':k,'elementId':c.get('elementId'),'tag':c.get('tag'),'source':c.get('source'),'binding':c.get('binding')}
 if k=='captured_full_html_claim_paragraphs': return {'type':k,'url':c.get('url'),'source':c.get('source'),'fullEntityBinding':c.get('fullEntityBinding')}
 if k=='full-capture-claim-paragraph': return {'type':k,'claim':c.get('claim'),'source':c.get('source'),'fullEntityBinding':c.get('fullEntityBinding')}
 return {'type':k,'source':c.get('source'),'binding':c.get('binding') or c.get('fullEntityBinding')}
def literal(value):
 if isinstance(value,str): b=value.encode('utf-8'); kind='utf8-string'
 else: b=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'); kind='canonical-json-utf8'
 return {'encoding':kind,'utf8ByteLength':len(b),'utf8Base64':base64.b64encode(b).decode(),'sha256':hashlib.sha256(b).hexdigest()}
for e in d['entries']:
 ix=e['index']; c=e['card']; groups=M[ix]
 if set(groups)!=set(e['componentReasons']): raise RuntimeError(f'group map missing {ix}')
 for k,ids in groups.items():
  if not ids or any(cid not in C for cid in ids): raise RuntimeError(f'bad ref {ix} {k} {ids}')
  value={'prompt':c['prompt'],'orderedAnswerText':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'keyText':c['answers'][c['correctIndex']]['text']} if k=='whole_prompt_all_four_ordered_answers_correctIndex_key' else (c['answers'][int(k[-1])]['note'] if k.startswith('note_') else c['explanation'] if k=='explanation' else c['difficulty'] if k=='difficulty' else c['source'])
  e['literalFieldBindings'][k]={'literal':literal(value),'sourceLocatorRefs':[{'contextId':cid,'locator':locator(C[cid])} for cid in ids]}
# Truthful, current author attestation: record what was actually inspected and clearly preserve the independent gate.
d['sourceQualificationAudit']['authorStatus']='edition 4 author source-binding correction; pending independent source/semantic/editorial qualification'
d['readerAttestation']={
 'authorThreadId':d['authorThreadId'],
 'authorIdentity':'01a13841-3085-7ba3-9570-46d16b85c036',
 'editionRead':'4',
 'readMethod':'This same author read the full 100-item Physics inventory and all 80 protected card objects during the edition 2 source/neighbor pass. For edition 4 I personally read all 20 current prompts, ordered answers, keys, difficulties, explanations and notes, and checked each field locator against its specific BIPM page extract or typed OpenStax claim context. The complete 6.2 and 4.2 raw HTML entities and range manifests were checked; I read their exact claim paragraphs and verified each range record against the assembled body hash. BIPM table rows and definition passages relevant to current card claims were checked on the bound page extracts. This remains an author-side attestation.',
 'semanticGuard':'The complete 80 protected objects and 100-ID order are carried unchanged from the prior same-author read. All 20 current card literals were checked; relevant distinctions against protected neighbors were retained from the earlier semantic audit and the current replacements for #44 and #46 were checked against their corresponding concepts.',
 'qualificationCaveat':'No independent coordinator/reader qualification, SOURCE credit, or PASS is claimed. #40/#41 are now sourced proposals, not independently accepted cards.'}
# Canonical UTF-8 JSON. Do not alter prior editions.
rawout=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
out.write_bytes(rawout)
print(json.dumps({'path':str(out),'bytes':len(rawout),'sha256':hashlib.sha256(rawout).hexdigest(),'contexts':len(d['primaryContexts']),'cards':len(d['entries'])},ensure_ascii=False))
