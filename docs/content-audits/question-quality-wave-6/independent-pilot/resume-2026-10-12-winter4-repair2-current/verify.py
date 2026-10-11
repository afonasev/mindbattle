import os,json,hashlib,subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
OUT=Path(__file__).resolve().parent
ROOT=Path.cwd()
sha=lambda b:hashlib.sha256(b).hexdigest()
compact=lambda x,sorted=False:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=sorted)
class Visible(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.hidden=0;self.nodes=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'): self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  s=' '.join(d.split())
  if s and not self.hidden:self.nodes.append(s)
rpath=Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/followup2/author-current-repair-receipt.json')
r=json.loads(rpath.read_text()); (OUT/'author-receipt-frozen.json').write_bytes(rpath.read_bytes())
qs=json.loads(Path('src/content/topics/winter-sports.json').read_text())['questions'];cards=[q for q in qs if q['id'] in [c['questionId'] for c in r['cards']]]
(OUT/'current-cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
raws={};texts={}; checks=[]
for p in {p['rawCapture'] for c in r['cards'] for f in c['fields'] for p in f['proofs']}:
 b=Path(p).read_bytes();gb=subprocess.check_output(['git','show','54fbf71:'+p]);pdf=b.startswith(b'%PDF-')
 if pdf: parts=[page.extract_text() for page in PdfReader(p).pages];text='\n'.join(f'\nPAGE {i+1}\n{v}' for i,v in enumerate(parts))
 else:parser=Visible();parser.feed(b.decode());parts=parser.nodes;text='\n'.join(f'NODE {i}: {v}' for i,v in enumerate(parts))
 texts[p]=parts
 name=Path(p).name+'.txt';(OUT/name).write_text(text)
 raws[p]={'sha256':sha(b),'bytes':len(b),'git54fbf71Roundtrip':b==gb,'pdf':pdf,'partCount':len(parts),'extractedText':name,'extractedTextSha256':sha(text.encode())}
for c,q in zip(r['cards'],cards):
 # lookup rather than relying on ordering
 q=next(q for q in cards if q['id']==c['questionId'])
 row={'questionId':q['id'],'cardCanonicalSha256':sha(compact(q).encode()),'sortedCardSha256':sha(compact(q,True).encode()),'fields':[]}
 row['authorCanonicalMatch']=row['cardCanonicalSha256']==c['cardCanonicalSha256'];row['authorSortedMatch']=row['sortedCardSha256']==c['sortedCardSha256']
 for f in c['fields']:
  k=f['field'];literal=compact([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]) if k=='prompt-key' else q['explanation'] if k=='explanation' else q['answers'][int(k[-1])]['note']
  fr={'field':k,'literal':literal,'literalSha256':sha(literal.encode()),'authorLiteralMatch':literal==f['literal'] and sha(literal.encode())==f['literalSha256'],'proofs':[]}
  for p in f['proofs']:
   loc=p['locator'];parts=texts[p['rawCapture']]
   if 'textNodeStart' in loc: passage=' '.join(parts[loc['textNodeStart']:loc['textNodeEnd']+1])
   else:page=loc.get('pdfPage',loc.get('physicalPdfPage'));passage=parts[page-1]
   fr['proofs'].append({'url':p['url'],'rawCapture':p['rawCapture'],'rawSHAmatch':raws[p['rawCapture']]['sha256']==p['rawCaptureSha256'],'locator':loc,'passageSHAdeclaredMatch':sha(p['passage'].encode())==p['passageSha256'],'actualLocatedPassage':passage,'locatorLiteralMatch':passage==p['passage'],'declaredPassageSha256':p['passageSha256'],'actualPassageSha256':sha(passage.encode())})
  row['fields'].append(fr)
 checks.append(row)
report={'readerIdentity':os.environ['CODEX_THREAD_ID'],'authorIdentity':r['agentIdentity'],'authorRevision':subprocess.check_output(['git','rev-parse','54fbf71']).decode().strip(),'frozenAtHead':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'authorReceiptSha256':sha(rpath.read_bytes()),'raws':raws,'cards':checks}
(OUT/'proof-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('RAW',len(raws),'cards',len(checks),'fields',sum(len(c['fields']) for c in checks))
for c in checks:
 print(c['questionId'],'canonical',c['authorCanonicalMatch'],'sorted',c['authorSortedMatch'])
 for f in c['fields']:
  print(f['field'],'literal',f['authorLiteralMatch'],'proof',[{k:p[k] for k in ['rawSHAmatch','passageSHAdeclaredMatch','locatorLiteralMatch']} for p in f['proofs']])
