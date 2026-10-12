"""Independent byte/literal/locator preservation checks only. No generated quality verdicts."""
import json,hashlib,subprocess,re,gzip
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OWN=Path(__file__).resolve().parent
BASE=ROOT/'docs/content-audits/question-quality-wave-6'
AUTHOR=BASE/'middle-ages/repair2-2026-10-13-native-01a131a7-847b-7073-aa71-27ae12d45778'
SCOPE=BASE/'coordinator-continuation-01a13100/middle2-a6-current-independent-reader-scope.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
H=lambda x:sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
frozen=lambda rev,p:subprocess.check_output(['git','show',rev+':'+str(p.relative_to(ROOT))],cwd=ROOT)
a=json.loads((AUTHOR/'author-source-editorial-review.json').read_text());s=json.loads(SCOPE.read_text());guard=json.loads((BASE/'coordinator-continuation-01a13100/middle2-exact-current-repair-scope.json').read_text())
assert sha((AUTHOR/'author-source-editorial-review.json').read_bytes())==s['authorReceiptSHA256']=='f540570dd9ee40e5ba0a275cf1085af577954046eab1678c66323b5abdfdb798'
assert (AUTHOR/'author-source-editorial-review.json').read_bytes()==frozen('a6f0347',AUTHOR/'author-source-editorial-review.json')
runtime=ROOT/'src/content/topics/middle-ages.json';assert runtime.read_bytes()==frozen('a6f0347',runtime)
cs=json.loads(runtime.read_text())['questions'];cards={c['id']:c for c in cs};assert [c['id'] for c in cs]==guard['order']
for item in guard['protected98']:assert H(cards[item['id']])==item['cardSHA256']
for id,slot in [('middle-ages-crusade',0),('middle-ages-pilgrimage-armed',2)]:assert H(cards[id])==s['candidateWholeCardHashes'][id]==a['wholeCardHashes'][id] and cards[id]['correctIndex']==slot and cards[id]['difficulty']=='medium'
for g in a['groups']:
 c=cards[g['cardId']];name=g['group'];v={'prompt':c['prompt'],'answers':[x['text'] for x in c['answers']],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']} if name=='prompt-answers-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note']
 assert v==g['literal'] and H(v)==g['canonicalSHA256']
reg=json.loads((AUTHOR/'source-register.json').read_text()); rawchecks=[]
for src in reg['sources']:
 path=AUTHOR/src['containerPath'];b=path.read_bytes();raw=gzip.decompress(b) if path.suffix=='.gz' else b;origin=ROOT/src['originalRepositoryPath'];blob=subprocess.check_output(['git','rev-parse',src['originalRepositoryCommit']+':'+src['originalRepositoryPath']],cwd=ROOT,text=True).strip()
 assert raw==frozen(src['originalRepositoryCommit'],origin) and sha(raw)==src['rawSHA256'] and blob==src['originalGitBlob'] and len(raw)==src['rawBytes']
 if src['containerSHA256']:assert sha(b)==src['containerSHA256']
 rawchecks.append({**src,'actualRawSHA256':sha(raw),'actualContainerSHA256':sha(b),'actualBlob':blob,'independentRawCheck':'MATCH'})
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,x):self.parts.append(x)
html=gzip.decompress((AUTHOR/'sources/fulcher-clermont-full-page.html.gz').read_bytes()).decode();parser=Parser();parser.feed(html[html.index('<a name="urban2"'):html.index('<a name="capture"')]);(OWN/'contexts/fulcher-section1.txt').write_text(re.sub(r'\s+',' ',' '.join(parser.parts)).strip())
for source,pages,out in [('glasgow-thesis-complete.pdf',[1,2],'glasgow-cover.txt'),('glasgow-thesis-complete.pdf',[21,22,23],'glasgow-context21-23.txt'),('ucdavis-jihad.pdf',[12],'syed-page12.txt')]:
 pdf=PdfReader(AUTHOR/'sources'/source);(OWN/'contexts'/out).write_text(re.sub(r'\s+',' ','\n\n'.join(pdf.pages[i-1].extract_text() for i in pages)).strip())
cnrtl=json.loads((AUTHOR/'sources/cnrtl-croisade.json').read_text());(OWN/'contexts/cnrtl-full-header.json').write_text(json.dumps(cnrtl['header'],ensure_ascii=False,indent=2)+'\n')
# Bounds selected after direct personal reading of the raw passages. These are NOT verdict generators.
selections=[
 ('fulcher-eastern-aid','fulcher','fulcher-section1.txt','For your brethren who live in the east','Moreover, Christ commands it.',{'type':'html-section','anchor':'urban2','section':1}),
 ('fulcher-seven-battles','fulcher','fulcher-section1.txt','They have occupied more and more','devastated the empire.',{'type':'html-section','anchor':'urban2','section':1}),
 ('fulcher-pilgrim-anathema','fulcher','fulcher-section1.txt','If anyone seizes or robs monks','let him be anathema [that is, cursed].',{'type':'html-section','anchor':'urban2','section':1}),
 ('syed-jihad-duty','syed','syed-page12.txt','We ought to note one important caveat','pray five times a day.39',{'type':'pdf-text','physicalPage':12,'printedPage':146}),
 ('glasgow-ambassador','glasgow','glasgow-context21-23.txt','Robert the Monk’s account of the First Crusade','on the ‘King of Persia.’',{'type':'pdf-main-paragraph','physicalPage':22,'printedPage':14}),
 ('glasgow-shared-shrines','glasgow','glasgow-context21-23.txt','In this thesis, the term','visited and worshiped at the same shrines.',{'type':'pdf-main-paragraph','physicalPage':22,'printedPage':14}),
 ('glasgow-jordan-1119','glasgow','glasgow-context21-23.txt','75 After the Easter ceremonies in 1119','12:33, p. 881.',{'type':'pdf-footnote','physicalPage':22,'printedPage':14,'footnote':75}),
 ('glasgow-armed-warning','glasgow','glasgow-context21-23.txt','However, if they continued on as armed men','they were crusaders.',{'type':'pdf-main-paragraph','physicalPage':22,'printedPage':14}),
 ('glasgow-account-date','glasgow','glasgow-context21-23.txt','Robert the Monk’s account of the First Crusade','how others saw crusaders and pilgrims.',{'type':'pdf-main-paragraph','physicalPage':22,'printedPage':14}),
 ('glasgow-cover-bibliography','glasgow','glasgow-cover.txt','Haberlin, Aoife (2018)','PhD thesis.',{'type':'pdf-cover','physicalPages':[1,2]})]
proofs=[];byid={x['id']:x for x in rawchecks}
for id,sid,file,start,end,loc in selections:
 p=OWN/'contexts'/file;txt=p.read_text();lo=txt.index(start);hi=txt.index(end,lo)+len(end);q=txt[lo:hi];proofs.append(dict(id=id,sourceId=sid,sourceSHA256=byid[sid]['actualRawSHA256'],originURL=byid[sid]['url'],captureURL=byid[sid]['captureURL'],fullOriginalPath=str((AUTHOR/byid[sid]['containerPath']).relative_to(ROOT)),typedLocator=loc,exactSufficientQuote=q,quoteSHA256=sha(q.encode()),offset=lo,endOffset=hi,offsetBasis='zero-based Unicode code points in independent normalized context',contextPath=str(p.relative_to(ROOT)),contextSHA256=sha(p.read_bytes()),recipe='pypdf 6.19.0 extract_text pages joined by two LF then re.sub whitespace to space and strip' if sid!='fulcher' else 'stdlib HTMLParser data from raw HTML anchor urban2 to before capture, join by space, collapse whitespace and strip'))
q=cnrtl['header']['description'];p=OWN/'contexts/cnrtl-full-header.json';t=p.read_text();proofs.append(dict(id='cnrtl-crusade-definition',sourceId='cnrtl-croisade',sourceSHA256=byid['cnrtl-croisade']['actualRawSHA256'],originURL=byid['cnrtl-croisade']['url'],captureURL=byid['cnrtl-croisade']['captureURL'],typedLocator={'type':'json-value','jsonPointer':'/header/description'},exactSufficientQuote=q,quoteSHA256=sha(q.encode()),offset=t.index(q),offsetBasis='Unicode code points in own full-header pretty JSON; canonical field binding is JSON pointer',contextPath=str(p.relative_to(ROOT)),contextSHA256=sha(p.read_bytes()),recipe='json.loads complete API raw; json.dumps(header,ensure_ascii=False,indent=2)+LF'))
q='The Christian conquest of Granada in 1492 marked the beginning of the end of the Muslim population in Spain.';img=OWN/'rendered/lapidus-physical7.png';proofs.append(dict(id='lapidus-granada',sourceId='lapidus',sourceSHA256=byid['lapidus']['actualRawSHA256'],originURL=byid['lapidus']['url'],captureURL=byid['lapidus']['captureURL'],typedLocator={'type':'visual-scan-page','physicalPage':7,'printedPage':319,'column':'right','position':'second paragraph'},exactSufficientQuote=q,quoteSHA256=sha(q.encode()),offset=None,offsetBasis='No character offset: personal visual transcription from own rendered page',renderPath=str(img.relative_to(ROOT)),renderSHA256=sha(img.read_bytes()),recipe='pdftoppm -f 7 -l 7 -scale-to 2000 -png -singlefile; sips -r 90 for upright spread'))
# Fresh author's 12 expected quotes are independently checked in own extracted contexts, expected digests never replaced.
authorchecks=[]
mapfiles={'fulcher':'fulcher-section1.txt','glasgow':'glasgow-context21-23.txt','syed':'syed-page12.txt','cnrtl-croisade':'cnrtl-full-header.json'}
for ev in a['evidence']:
 q=ev['exactSufficientQuote'];sid=ev['sourceId'];expected=ev['quoteSHA256'];assert sha(q.encode())==expected
 if sid=='lapidus':matched=q==next(p['exactSufficientQuote'] for p in proofs if p['id']=='lapidus-granada');offset=None
 else:
  file='glasgow-cover.txt' if ev['id']=='glasgow-cover-bibliography' else mapfiles[sid];text=(OWN/'contexts'/file).read_text();offset=text.find(q);matched=offset>=0
 assert matched
 authorchecks.append(dict(id=ev['id'],expectedQuoteSHA256=expected,actualQuoteSHA256=sha(q.encode()),ownQuoteOffset=offset,matched=True))
historical=[]
paths=[BASE/'middle-ages/repair6-2026-10-12-fresh-writable-author-01a13116/author-review-v3.json']+[BASE/'independent-pilot/resume-2026-10-12-middle-current15-pilot5/middle-current6-f547afe-v4'/name for name in ['reader-receipt.json','independent-source-proofs.json','all-author-bindings-integrity.json']]
for p in paths:
 b=p.read_bytes();assert b==frozen('47d7341',p);historical.append(dict(path=str(p.relative_to(ROOT)),freeze='47d7341',SHA256=sha(b),exactPreserved=True))
(OWN/'independent-source-proofs.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n')
(OWN/'preservation-results.json').write_text(json.dumps(dict(readerNativeId='01a131c5-edfb-7b82-8ddf-bd88a8b95597',purpose='preservation only; quality manually authored separately',runtimeFreeze='a6f0347cd7eca5ecb14db2ea203b353c66fd23e3',authorReceiptSHA256=sha((AUTHOR/'author-source-editorial-review.json').read_bytes()),wholeCardHashes={id:H(cards[id]) for id in s['candidateWholeCardHashes']},groupLiteralChecks=12,protected98Exact=True,orderExact=True,difficultyCounts={d:sum(c['difficulty']==d for c in cs) for d in ['easy','medium','hard']},keyCounts={str(i):sum(c['correctIndex']==i for c in cs) for i in range(4)},sourceOriginals=rawchecks,authorQuoteChecks=authorchecks,historicalPreservation=historical,errors=0),ensure_ascii=False,indent=2)+'\n')
print('Preservation: 12 groups / 5 full raw sources / 12 current quote bindings / protected98/order/classes/keyslots; 0 errors. No quality generated.')
