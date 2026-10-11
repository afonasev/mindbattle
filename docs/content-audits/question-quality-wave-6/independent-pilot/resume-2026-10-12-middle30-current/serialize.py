# Serialization and byte verification only. No editorial verdict inference.
import json,hashlib,subprocess,os,re
from pathlib import Path
import read_originals as r
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
def write(n,o):(r.OWN/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
a=json.loads((r.AUTHOR/'author-full-scope-receipt.json').read_bytes());qpath=r.ROOT/'src/content/topics/middle-ages.json';qs={q['id']:q for q in json.loads(qpath.read_bytes())['questions']};dec=json.loads((r.OWN/'decisions.json').read_text());head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.ROOT,text=True).strip()
rawtext=qpath.read_text();pos=rawtext.index('[',rawtext.index('"questions"'))+1;decoder=json.JSONDecoder();rawcards={}
while True:
 while rawtext[pos].isspace() or rawtext[pos]==',':pos+=1
 if rawtext[pos]==']':break
 card,end=decoder.raw_decode(rawtext,pos);rawcards[card['id']]=rawtext[pos:end];pos=end
metas={}
for card in a['cards']:
 for field in card['fields']:
  for p in field['proofs']:metas[Path(p['rawCapture']).name]={'title':p['title'],'url':p['url']}
for p in (r.AUTHOR/'sources').glob('*.capture.json'):
 meta=json.loads(p.read_text());n=p.name.removesuffix('.capture.json');metas.setdefault(n,{'title':n});metas[n]['url']=meta['url']
# Titles are taken from actual originals, rather than author labels.
for name in list(metas):
 path=r.AUTHOR/'sources'/name
 if not path.exists():continue
 if name.endswith('.json'):
  obj=json.loads(path.read_bytes());form=obj.get('header',{}).get('form')
  if form:metas[name]['title']='CNRTL / TLFi — '+form
 elif name.endswith('.html'):
  raw=path.read_bytes()
  try:html=raw.decode('utf-8')
  except UnicodeDecodeError:html=raw.decode('latin1')
  m=re.search(r'<title[^>]*>(.*?)</title>',html,re.S|re.I)
  if m:metas[name]['title']=' '.join(re.sub('<[^>]+>',' ',m.group(1)).split())
metas['uea-medieval-pilgrimage.pdf']['title']='Michael Schmoelz (2017), Pilgrimage in medieval East Anglia: A regional survey of the shrines and pilgrimages of Norfolk and Suffolk, University of East Anglia PhD thesis'
metas['glasgow-armed-pilgrimage.pdf']['title']='Aoife Haberlin (2018), The infrastructure and mechanics of pilgrimage to the Latin East in the twelfth and thirteenth centuries, University of Glasgow PhD thesis'
manualVisual='The disintegration of the Muslim states in the eleventh century led to the rapid expansion of Christian kingdoms. In the 1080s Alfonso VI, born of the strength of the unified kingdoms of Castile, Leon, and Galicia, conquered Toledo. Thereafter the tiny kingdom of Granada was the last Muslim possession in Spain until 1492.'
def proof(source,anchor,status):
 path=r.AUTHOR/'sources'/source;b=path.read_bytes();rel=str(path.relative_to(r.ROOT));blob=subprocess.check_output(['git','show',f'{head}:{rel}'],cwd=r.ROOT);assert b==blob
 visual=anchor.startswith('VISUAL:')
 if visual:passage=manualVisual;textHash=None;offset=None
 else:
  text=r.original(source);i=text.find(anchor);assert i>=0,(source,anchor);passage=text[i:i+1400];textHash=sha(text.encode());offset=i
 sourceClass=('institutional historical dictionary, complete native CNRTL API response' if source.startswith('cnrtl-') else 'full university thesis PDF' if source in ['uea-medieval-pilgrimage.pdf','glasgow-armed-pilgrimage.pdf'] else 'complete university-hosted seven-page scan excerpt, not full book' if visual else 'publisher abstract page, not full article' if source=='ugr-dowry.html' else 'publisher response displaying page119 of seven-page review, not full review or reviewed thesis' if source=='persee-medieval-jihad.html' else 'complete institutional reference/primary-text web response')
 return {'sourceClass':sourceClass,'title':metas[source]['title'],'url':metas[source]['url'],'sourceURL':metas[source]['url'],'originalPath':rel,'rawCapture':rel,'fullOriginalRawSha256':sha(b),'rawCaptureSha256':sha(b),'gitBlobMatchesWorking':True,'gitFreezeCommit':head,'captureFormat':'complete saved original provider response, exact raw bytes','captureMethod':'Independent visual reading of printed314–315 in own Poppler render; manual transcription' if visual else 'Opened complete original raw capture; parsed native JSON or original HTML, independently read relevant substantive section; no excerpt used as replacement original','locator':anchor,'decodedCharacterOffset':offset,'decodedOriginalTextSha256':textHash,'passage':passage,'passageSha256':sha(passage.encode()),'proofDisposition':'supporting passage independently inspected' if status=='PASS' else 'original inspected; does not establish every claim, or field has recorded editorial defect','visualWitness':str((r.OWN/'lapidus-pages314-315.png').relative_to(r.ROOT)) if visual else None}
extras={('middle-ages-dancing-mania','note2'):[('gutenberg-sweating.html','For sodenly a dedly and burnyng sweate')],('middle-ages-manor','explanation'):[('lancaster-manorial-glossary.html','Reeve: ('),('lancaster-manorial-glossary.html','Steward:')],('middle-ages-relic','explanation'):[('uea-medieval-pilgrimage.pdf','2.3. The cellarer’s account')],('middle-ages-charter','explanation'):[('new-market-gazetteer.html','Generally, these grants')],('middle-ages-toll','prompt-key'):[('new-market-gazetteer.html','to collect from them revenues')],('middle-ages-dowry','explanation'):[('cnrtl-douaire.json',"Droit d'usufruit")],('middle-ages-pilgrimage','explanation'):[('cnrtl-pèlerinage.json','Voyage entrepris dans un esprit'),('cnrtl-pèlerinage.json',"Devoir un pelerinage (à la suite d'un voeu)")]}
records=[]
for id in a['scope']:
 d=dec[id];q=qs[id];literals=[[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],*[{'index':i,**v} for i,v in enumerate(q['answers'])],q['explanation']];fields=[]
 for name,indexed,status,(source,anchor) in zip(['prompt-key','note0','note1','note2','note3','explanation'],literals,d['status'],d['sources']):
  lit=indexed['note'] if name.startswith('note') else indexed
  proofs=[proof(source,anchor,status),*[proof(s,t,status) for s,t in extras.get((id,name),[])]]
  analysis=d.get('fieldReasons',{}).get(name, f"Independent reading of current literal: {d['reason']} Supporting/limiting section: {anchor}.")
  fields.append({'field':name,'literal':lit,'literalSha256':sha(canon(lit)),'indexedLiteral':indexed,'indexedLiteralSha256':sha(canon(indexed)),'status':status,'verdict':status,'analysis':analysis,'claimAnalysis':analysis,'substantiveRead':True,'proofs':proofs})
 status='FIX' if d['editorial']=='FIX' or 'FIX' in d['status'] else ('HOLD' if 'HOLD' in d['status'] else 'PASS')
 records.append({'questionId':id,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':sha(canon(q)),'rawCardSha256':sha(rawcards[id].encode()),'rawTopicFileSha256':sha(qpath.read_bytes()),'cardGitBlobMatchesWorking':qpath.read_bytes()==subprocess.check_output(['git','show',f'2e9289c:src/content/topics/middle-ages.json'],cwd=r.ROOT),'cardFreezeCommit':'2e9289c','currentCard':q,'editorialStatus':d['editorial'],'editorialReason':d['reason'],'editorialAnalysis':d['reason'],'status':status,'verdict':status,'fields':fields})
receipt={'actualReaderIdentity':os.environ['CODEX_THREAD_ID'],'agentIdentity':os.environ['CODEX_THREAD_ID'],'role':'independent','actualAuthorIdentity':'01a12c4e-cd53-7a72-8a54-0ff6ac44fd18','identityProvenance':'Explicit native dispatch author completion cursor c37662e4-6ea8-4c6a-9e9c-1e4c6fe1f110:78; root attaches provenance binding. Author receipt omitted identity; original bytes retained.','authorReceiptPath':str((r.AUTHOR/'author-full-scope-receipt.json').relative_to(r.ROOT)),'authorReceiptRawSha256':sha((r.AUTHOR/'author-full-scope-receipt.json').read_bytes()),'authorReceiptFreezeCommit':'2e9289c','sourceFreezeCommit':head,'requiredScope':a['scope'],'reviewedScope':list(a['scope']),'unreadScope':[],'decisionMethod':'Independent substantive reading; all decisions explicitly authored. Scripts serialize literals, extract manually selected locators and check raw Git bytes. Pilot frozen at1cc32bc, source+Git roundtrip completed before serialization of remaining25 field records. Initial reconnaissance had already inspected remaining literals; this sequence is recorded rather than claimed as strictly delayed reading. No automatic factual/editorial PASS.','certification':'Independent current-card receipt; not coordinator certification or human acceptance','cards':records}
write('receipt.json',receipt);write('raw-card-slices.json',[{'questionId':id,'rawUtf8CardSlice':rawcards[id],'rawSha256':sha(rawcards[id].encode())} for id in a['scope']])
manifest=[]
original33=sorted(set(Path(p['rawCapture']).name for c in a['cards'] for f in c['fields'] for p in f['proofs']))
used=sorted(set(s[0] for d in dec.values() for s in d['sources'])|{s for pairs in extras.values() for s,t in pairs})
for source in sorted(set(original33+used)):
 path=r.AUTHOR/'sources'/source;rel=str(path.relative_to(r.ROOT));b=path.read_bytes();assert b==subprocess.check_output(['git','show',f'{head}:{rel}'],cwd=r.ROOT)
 manifest.append({'path':rel,'fullRawSha256':sha(b),'bytes':len(b),'gitBlobMatchesWorking':True,'freezeCommit':head,'authorBoundOriginal':source in original33,'independentlyUsed':source in used,'originalMetadata':metas[source],'readingScope':'Complete relevant source sections and field claims read, with full raw original retained. Entire long thesis/book not claimed read.','scannedOriginal':source=='texas-reconquista.pdf'})
write('originals-manifest.json',{'authorBoundOriginalCount':len(original33),'additionalUsedCount':len(set(used)-set(original33)),'originals':manifest})
print({s:sum(c['status']==s for c in records) for s in ['PASS','FIX','HOLD']})
