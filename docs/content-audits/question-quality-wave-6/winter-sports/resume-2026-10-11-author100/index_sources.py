import json,hashlib
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden and d.strip():self.parts.append(' '.join(d.split()))
if __name__=='__main__':
 index={}
 for raw in sorted((ROOT/'sources').glob('*.html')):
  if 'failed-partial' in raw.name or not raw.with_suffix('.http.json').exists():continue
  parser=Text();parser.feed(raw.read_text());index[raw.stem]={'rawCapture':'sources/'+raw.name,'rawCaptureSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'http':json.loads(raw.with_suffix('.http.json').read_text()),'extraction':'HTMLParser visible text nodes excluding script/style, whitespace collapsed in each node; node index is zero-based; full raw HTML retained','nodes':parser.parts}
 from pypdf import PdfReader
 for raw in sorted((ROOT/'sources').glob('*.pdf')):
  if 'failed-partial' in raw.name:continue
  index[raw.stem]={'rawCapture':'sources/'+raw.name,'rawCaptureSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'http':json.loads(raw.with_suffix('.http.json').read_text()),'extraction':'pypdf extract_text per page unchanged; node index is zero-based PDF page','format':'pdf','nodes':[p.extract_text() for p in PdfReader(raw).pages]}
 (ROOT/'source-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
