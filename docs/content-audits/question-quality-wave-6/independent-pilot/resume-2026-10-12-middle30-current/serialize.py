import json,hashlib,subprocess,os
from pathlib import Path
import read_originals as r
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
def write(n,o):(r.OWN/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
a=json.loads((r.AUTHOR/'author-full-scope-receipt.json').read_bytes());qpath=r.ROOT/'src/content/topics/middle-ages.json';qs={q['id']:q for q in json.loads(qpath.read_bytes())['questions']};dec=json.loads((r.OWN/'decisions.json').read_text());head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.ROOT,text=True).strip()
records=[]
for id,d in dec.items():
 q=qs[id]; literals=[[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],*[{'index':i,**v} for i,v in enumerate(q['answers'])],q['explanation']];fields=[]
 for name,lit,status,(source,anchor) in zip(['prompt-key','note0','note1','note2','note3','explanation'],literals,d['status'],d['sources']):
  path=r.AUTHOR/'sources'/source;b=path.read_bytes();text=r.original(source);i=text.find(anchor);assert i>=0,(source,anchor);passage=text[i:i+1400];rel=str(path.relative_to(r.ROOT));blob=subprocess.check_output(['git','show',f'{head}:{rel}'],cwd=r.ROOT)
  assert b==blob
  fields.append({'field':name,'indexedLiteral':lit,'indexedLiteralSha256':sha(canon(lit)),'status':status,'analysis':d.get('fieldReasons',{}).get(name,d['reason']),'sourceClass':'complete institutional/dictionary/primary original capture','originalPath':rel,'fullOriginalRawSha256':sha(b),'gitBlobMatchesWorking':True,'gitFreezeCommit':head,'locator':anchor,'passage':passage,'passageSha256':sha(passage.encode()),'proofDisposition':'supporting passage independently inspected' if status=='PASS' else 'original inspected; this passage does not establish every claim in this field'})
 records.append({'questionId':id,'difficulty':q['difficulty'],'cardCanonicalSha256':sha(canon(q)),'rawTopicFileSha256':sha(qpath.read_bytes()),'currentCard':q,'editorialStatus':d['editorial'],'editorialReason':d['reason'],'status':'FIX' if d['editorial']=='FIX' or 'FIX' in d['status'] else ('HOLD' if 'HOLD' in d['status'] else 'PASS'),'fields':fields})
receipt={'actualReaderIdentity':os.environ['CODEX_THREAD_ID'],'actualAuthorIdentity':'01a12c4e-cd53-7a72-8a54-0ff6ac44fd18','identityProvenance':'Explicit native dispatch author completion cursor c37662e4-6ea8-4c6a-9e9c-1e4c6fe1f110:78; root attaches independent provenance binding. Author receipt omitted identity; bytes retained.','authorReceiptPath':str((r.AUTHOR/'author-full-scope-receipt.json').relative_to(r.ROOT)),'authorReceiptRawSha256':sha((r.AUTHOR/'author-full-scope-receipt.json').read_bytes()),'authorReceiptFreezeCommit':'2e9289c','sourceFreezeCommit':head,'requiredScope':a['scope'],'reviewedScope':list(dec),'unreadScope':[x for x in a['scope'] if x not in dec],'decisionMethod':'Human-like independent substantive reading; decisions.json is manually authored. Scripts only serialize literals, extract explicitly selected locators and check raw Git bytes.','certification':'Independent current-card receipt; not coordinator certification or human acceptance','cards':records}
write('receipt.json',receipt)
print({s:sum(c['status']==s for c in records) for s in ['PASS','FIX','HOLD']})
