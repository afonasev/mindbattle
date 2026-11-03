import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
p=Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036/author-original.json');d=json.loads(p.read_bytes())
WT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');base=WT/'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772';phys=WT/'docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals'
def bind(path):
 b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
contexts=[]
# BIPM full extracted pages that contain the base and derived SI-unit definitions used by 30-36.
pdf=phys/'physics-force-si-unit.pdf';reader=PdfReader(str(pdf))
for n in (132,139,140):
 text=reader.pages[n-1].extract_text() or ''
 contexts.append({'kind':'pdf_page_full_text','source':'BIPM SI Brochure','pdfPage':n,'printedPage':n-2,'binding':bind(pdf),'literalExtractedText':text,'extraction':'pypdf 6.x; no punctuation normalization'})
# Full typed CNXML para and caption elements, preserving parsed text plus exact raw source bytes by SHA.
cnxml=phys/'openstax-m42341-index.cnxml';root=ET.parse(cnxml).getroot()
for tag in ['import-auto-id2670391','import-auto-id2446845','fs-id2616778','import-auto-id2931325']:
 for el in root.iter():
  if el.attrib.get('id')==tag:
   contexts.append({'kind':'cnxml_element','source':'OpenStax College Physics 2e §20.1','elementId':tag,'tag':el.tag.split('}')[-1],'literalText':' '.join(''.join(el.itertext()).split()),'binding':bind(cnxml)});break
# Exact claim-bearing contexts from complete captured OpenStax HTML pages.
class H(HTMLParser):
 def __init__(self):super().__init__();self.p=0;self.buf=[];self.blocks=[];self.title=False;self.t=[]
 def handle_starttag(self,t,a):
  if t=='title':self.title=True
  if t in ('p','h2','h3'): self.p+=1;self.buf=[]
 def handle_endtag(self,t):
  if t=='title':self.title=False
  if t in ('p','h2','h3') and self.p:self.blocks.append((t,' '.join(''.join(self.buf).split())));self.p-=1
 def handle_data(self,x):
  if self.title:self.t.append(x)
  if self.p:self.buf.append(x)
criteria={39:['law of reflection states','mirror images make objects appear'],43:['not even theoretically possible for engines to be 100 percent efficient','not possible to use the entire available energy'],48:['simple machines make work easier','a lever is a rigid'],49:['intensity of a sound is proportional to its amplitude squared','perception of frequency is called pitch']}
for i,terms in criteria.items():
 f=base/f'capture-only/physics30-49-gaps/{i}/assembled-original-entity.body'; raw=f.read_bytes();h=H();h.feed(raw.decode('utf-8','replace'))
 selected=[]
 for typ,txt in h.blocks:
  if any(t in txt.lower() for t in terms):selected.append({'tag':typ,'literalText':txt})
 contexts.append({'kind':'captured_full_html_claim_paragraphs','source':{39:'OpenStax Physics §16.1 Reflection',43:'OpenStax Physics §12.3 Entropy (reviewed as a rejected replacement)',48:'OpenStax Physics §9.3 Simple Machines',49:'OpenStax Physics §14.2 Sound Intensity and Sound Level'}[i],'url':{39:'https://openstax.org/books/physics/pages/16-1-reflection',43:'https://openstax.org/books/physics/pages/12-3-entropy',48:'https://openstax.org/books/physics/pages/9-3-simple-machines',49:'https://openstax.org/books/physics/pages/14-2-sound-intensity-and-sound-level'}[i],'pageTitle':' '.join(h.t),'fullEntityBinding':bind(f),'selectedFullParagraphs':selected})
# CNXML fact contexts previously read from complete saved source bytes.
fileIds={37:('openstax-m54131-index.cnxml',['fs-idm15080864']),42:('openstax-m42218-index.cnxml',['import-auto-id1848208']),44:('openstax-m42218-index.cnxml',['import-auto-id1848208']),45:('openstax-m54314-index.cnxml',['fs-id1167065809902','fs-id1167065854785']),46:('openstax-m42341-index.cnxml',['import-auto-id2931325']),47:('openstax-m42341-index.cnxml',['import-auto-id2446845','fs-id2616778'])}
for i,(fname,ids) in fileIds.items():
 f=phys/fname; root=ET.parse(f).getroot()
 for id in ids:
  for el in root.iter():
   if el.attrib.get('id')==id:
    contexts.append({'kind':'cnxml_element','source':next(e['card']['source']['title'] for e in d['entries'] if e.get('index')==i and e.get('card')),'elementId':id,'tag':el.tag.split('}')[-1],'literalText':' '.join(''.join(el.itertext()).split()),'binding':bind(f)});break
# Magnet complete paragraph raw byte-range embedded in its full captured entity.
f=base/'../coordinator-continuation-01a136e6/capture-only/physics-next20-29/23/assembled-original-entity.body';f=f.resolve();b=f.read_bytes();contexts.append({'kind':'full_entity_byte_range','source':'OpenStax Physics §20.1 magnetic fields','elementId':'fs-id1167065911660','byteStart':107616,'byteEnd':108513,'rawLiteralUtf8':b[107616:108513].decode('utf-8'),'fullEntityBinding':bind(f)})
d['primaryContexts']=contexts
out=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();p.write_bytes(out);print(len(contexts),len(out),hashlib.sha256(out).hexdigest())
