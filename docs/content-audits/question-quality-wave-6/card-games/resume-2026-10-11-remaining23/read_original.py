"""Display original text for actual reader; no editorial judgments."""
import sys,pathlib
from html.parser import HTMLParser
class T(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden:self.parts.append(d)
for name in sys.argv[1:]:
 p=pathlib.Path(__file__).parent/'sources'/name;print('\nSOURCE',name)
 if p.suffix=='.pdf':
  from pypdf import PdfReader
  for i,page in enumerate(PdfReader(p).pages): print('PAGE',i+1,page.extract_text())
 else:
  t=T();t.feed(p.read_text());print(' '.join(' '.join(t.parts).split()))
