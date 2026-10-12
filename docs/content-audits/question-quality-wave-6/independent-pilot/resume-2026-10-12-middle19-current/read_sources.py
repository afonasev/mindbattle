import json,re,html,pathlib,sys
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def visible(s):
 p=Text();p.feed(s);return re.sub(r'\s+',' ',' '.join(p.parts)).strip()
def extract(path):
 b=pathlib.Path(path).read_bytes()
 if path.endswith('.pdf'):
  from pypdf import PdfReader
  return [(i+1,p.extract_text()) for i,p in enumerate(PdfReader(path).pages)]
 try:s=b.decode('utf8')
 except UnicodeDecodeError:s=b.decode('cp1252')
 if path.endswith('.json'):
  d=json.loads(s)
  def strings(v):
   if isinstance(v,str):return [v]
   if isinstance(v,list):return [s for x in v for s in strings(x)]
   if isinstance(v,dict):return [s for x in v.values() for s in strings(x)]
   return []
  return visible(' '.join(strings(d['content'])))
 return visible(s)
if __name__=='__main__':
 for path in sys.argv[1:]:print('SOURCE',path,'\n',extract(path))
