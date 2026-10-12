import json, subprocess, re, hashlib
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle23-current'
FROZEN='c6e523bdc7cb3dc06e827c5b6e8d6a877d9173b4'
OLD='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-11-remainder29/sources/'
NEW='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/remainder23/sources/'
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def visible(s):
 h=Parser();h.feed(s);return ' '.join(' '.join(h.out).split())
def raw(path): return subprocess.check_output(['git','show',FROZEN+':'+path],cwd=ROOT)
def text(path):
 b=raw(path)
 if path.endswith('.pdf'):
  import io
  r=PdfReader(io.BytesIO(b));return '\n'.join('\nPDF PAGE '+str(i+1)+'\n'+p.extract_text() for i,p in enumerate(r.pages))
 try:s=b.decode('utf8')
 except UnicodeDecodeError:s=b.decode('cp1252')
 if path.endswith('.json'):
  d=json.loads(s)
  if 'content' not in d:return s
  return visible(' '.join(d['content'][0]['content']))
 return visible(s)
if __name__=='__main__':
 import sys
 p=(NEW if sys.argv[1]=='new' else OLD)+sys.argv[2];s=text(p)
 if len(sys.argv)>3:
  n=int(sys.argv[3]);print(s[n:n+int(sys.argv[4])])
 else:print(s)
