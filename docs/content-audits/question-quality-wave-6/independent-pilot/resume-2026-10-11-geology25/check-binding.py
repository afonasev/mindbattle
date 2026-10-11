"""Minimal receipt/source binding and negative checks; no editorial decisions."""
import json,hashlib,subprocess,copy,importlib.util,re,os
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent;R=O.parents[4];A=R/'docs/content-audits/question-quality-wave-6/geology-earth/resume-2026-10-11-remaining25'
def sha(x):return hashlib.sha256(x).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('proof',R/'docs/content-audits/question-quality-wave-6/verify-proof-format.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
receipt=json.loads((O/'independent-current.json').read_text());pilot=json.loads((O/'pilot5-current.json').read_text())
freeze='1e990f2022e83333e249a03632e2d772d8268ec1';topic='src/content/topics/geology-earth.json'
now=json.loads((R/topic).read_text());old=json.loads(subprocess.check_output(['git','show',f'{freeze}:{topic}'],cwd=R));before={c['id']:c for c in old['questions']};current={c['id']:c for c in now['questions']};scope=json.loads((A/'scope.json').read_text())['remainingIds']
assert set(scope)=={x['questionId'] for x in receipt['cards']}
rows=[]
for id in scope:
 c=current[id];h=sha(can(c));row={'questionId':id,'cardCanonicalSha256':h,'freezeCanonicalSha256':sha(can(before[id])),'frozen':c==before[id],'difficulty':c['difficulty'],'correctIndex':c['correctIndex']};rows.append(row);assert row['frozen']
assert all(len(c['fields'])==6 for c in receipt['cards']);assert json.loads(json.dumps(pilot,ensure_ascii=False))==pilot
save('final-hashes.json',{'freezeCommit':freeze,'branch':subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip(),'topicByteSha256':sha((R/topic).read_bytes()),'topicCanonicalSha256':sha(can(now)),'cards':rows,'topicQuota':dict(Counter(c['difficulty'] for c in now['questions'])),'topicAnswerPositions':{d:dict(Counter(c['correctIndex'] for c in now['questions'] if c['difficulty']==d)) for d in ('easy','medium','hard')},'sameTopicBytesAsFreeze':(R/topic).read_bytes()==subprocess.check_output(['git','show',f'{freeze}:{topic}'],cwd=R)})
refs={}
for c in receipt['cards']:
 for f in c['fields']:
  for p in f['proofs']:
   raw=(O/p['rawCapture']).resolve();h=sha(raw.read_bytes());assert h==p['rawCaptureSha256'];key=str(raw.relative_to(R))
   if key not in refs:refs[key]={'path':key,'sha256':h,'bytes':raw.stat().st_size,'format':p['captureFormat'],'url':p['url'],'role':'independent','usedBy':[]}
   refs[key]['usedBy'].append(c['questionId']+'/'+f['field'])
save('source-integrity.json',{'sources':list(refs.values()),'allRawHashesMatch':True,'pilot':{'cards':5,'fields':30,'roundTripEqual':True,'validator':'pilot5-format.json'},'full':{'cards':25,'fields':150,'validator':'full-format.json'},'limits':'Hash equality and passage existence do not create substantive PASS.'})
negative=[]
for label in ('card-hash','literal-hash','raw-hash','passage-hash','absent-passage','missing-field'):
 n=copy.deepcopy(pilot);n['cards']=n['cards'][:1];n['negativeFixture']=True;c=n['cards'][0];f=c['fields'][0];p=f['proofs'][0]
 if label=='card-hash':c['cardCanonicalSha256']='0'*64
 elif label=='literal-hash':f['literalSha256']='0'*64
 elif label=='raw-hash':p['rawCaptureSha256']='0'*64
 elif label=='passage-hash':p['passageSha256']='0'*64
 elif label=='absent-passage':p['passage']='Deliberately nonexistent geological source sentence for negative binding test.';p['passageSha256']=sha(p['passage'].encode())
 elif label=='missing-field':c['fields']=c['fields'][:-1]
 fn='negative-'+label+'.json';save(fn,n);result=v.validate(O/fn,R);assert not result['mechanicallyValid'];save('negative-'+label+'-format.json',result);negative.append({'case':label,'rejected':True,'errors':result['errors'],'fixture':fn})
save('negative-attempt-history.json',{'mechanicalNegativeAttempts':negative,'sourceAttempts':[{'date':'2026-10-11','url':'https://www.open.edu/openlearn/mod/oucontent/view.php?id=20276&section=6.3','command':'curl -fL --max-time40','curlExit':56,'httpStatus':403,'bodySaved':False,'disposition':'Not a source. Existing fully documented full original web extraction retained, read L170–214; no snippet/stitched summary substituted.'},{'date':'2026-10-11','url':'https://pubs.usgs.gov/gip/hawaii/page40.html','httpStatus':200,'bytes':4024,'bodySaved':'raw/usgs-tephra.html','disposition':'Original full body read and bound for tephra notes.'}],'parserWarnings':[{'source':'gsa-zircon.pdf','warning':'fontTools absent for CFF Type1 font; pypdf emitted warning','disposition':'No installation or validator change. Actual page4 text extracted legibly; exact source-passage checks pass. Warning does not create factual PASS.'}],'priorReceiptsPreserved':['pilot5-current.json','pilot5-format.json'],'authorHistoryModified':False})
patterns=[r'боксит|алюмини.*руд|руд.*алюмин',r'руб[иі]н|изумруд|сапфир|берилл|оливин|сингони|Боуэн',r'алмаз|Моос|магнетит|гематит|галит|гипс|обсидиан|пемз',r'фолиац|сланцеват|эпицентр|сейсмограмм|очаг.*землетряс|магм.*земл|земл.*магм',r'циркон|дискордан|конкордан|калий.аргон|рубидий.стронц|уран.свин|свин.*возраст|возраст.*свин']
rx=re.compile('|'.join(patterns),re.I);candidates=[];total=0;files=[]
for file in sorted((R/'src/content/topics').glob('*.json')):
 b=file.read_bytes();files.append({'path':str(file.relative_to(R)),'sha256':sha(b)})
 for q in json.loads(b)['questions']:
  total+=1;t=q['prompt']+' | '+q['answers'][q['correctIndex']]['text']
  if rx.search(t):candidates.append({'questionId':q['id'],'prompt':q['prompt'],'key':q['answers'][q['correctIndex']]['text'],'target':q['id'] in scope})
save('catalog-duplicate-scan.json',{'method':'Full-catalog prompt/key exact and semantic candidate search; explicit topical synonyms. Candidates independently read, not automated PASS. Does not re-audit six fields of certified75.','patterns':patterns,'totalQuestions':total,'catalogSnapshot':files,'candidates':candidates,'confirmed':[{'target':'geology-earth-gypsum-plaster','other':'materials-gypsum-board','relation':'same gypsum-core/drywall link asked in reverse'}],'relatedButDistinct':[{'ids':['geology-earth-diamond-hardness','materials-diamond-hard'],'reason':'Named Mohs upper standard versus cutting tool use; retain as different tested relation.'},{'ids':['geology-earth-carbon14-recent-organic','geology-earth-rubidium-strontium-rocks'],'reason':'Pb-loss causal direction versus terminology for disagreement, not inverse.'},{'ids':['geology-earth-bowen-olivine-first','geology-earth-bowen-pyroxene-second','geology-earth-bowen-amphibole-third','geology-earth-bowen-biotite-last-discontinuous'],'reason':'Different nodes and edges of ordered series; proximity alone does not constitute paraphrase.'}],'limitations':'Lexical search aids human semantic comparison; does not mathematically establish absence of every paraphrase. Other-topic concurrent snapshots are recorded, no mutations.'})
print(json.dumps({'frozenCards':len(rows),'sourceFiles':len(refs),'negativeChecks':len(negative),'cardVerdicts':dict(Counter(c['verdict'] for c in receipt['cards'])),'fieldVerdicts':dict(Counter(f['verdict'] for c in receipt['cards'] for f in c['fields']))},ensure_ascii=False))
