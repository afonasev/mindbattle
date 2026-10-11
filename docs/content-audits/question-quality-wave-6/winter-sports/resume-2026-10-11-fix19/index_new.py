import json
from pathlib import Path
from html.parser import HTMLParser
class T(HTMLParser):
 def __init__(self):super().__init__();self.hidden=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.hidden+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.hidden=max(0,self.hidden-1)
 def handle_data(self,s):
  if not self.hidden and s.strip():self.nodes.append(' '.join(s.split()))
b=Path(__file__).resolve().parent;h=json.loads((b/'new-http.json').read_text());i={}
for k,v in h.items():
 t=T();t.feed((b/v['rawCapture']).read_bytes().decode());i[k]={**v,'nodes':t.nodes};print('\n',k,v['curlReadback'])
 for n,s in enumerate(t.nodes):
  if (k in ['plushenko','gretzky'] and any(x in s for x in ['Olympic','Skat','Hockey','2006','2002','Sport','1998','medal'])) or (k not in ['plushenko','gretzky'] and 35<n<83):print(n,s)
(b/'new-index.json').write_text(json.dumps(i,ensure_ascii=False,indent=2)+'\n')
