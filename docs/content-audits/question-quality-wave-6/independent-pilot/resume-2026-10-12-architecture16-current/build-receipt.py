from pathlib import Path
import json, subprocess, hashlib, os, re
from html.parser import HTMLParser
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=Path(__file__).resolve().parent
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip()==str(ROOT)
assert OUT==ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-architecture16-current'
FROZEN='cf60970'; AP='docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-rework21/remainder16/'
def blob(path,rev=FROZEN):return subprocess.check_output(['git','show',rev+':'+path],cwd=ROOT)
def h(x):return hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def save(p,x):(OUT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def rendered(b):
 t=Text();t.feed(b.decode());return re.sub(r'\s+',' ',' '.join(t.parts)).strip()
r=json.loads(blob(AP+'author-receipt.json')); provenance=json.loads(blob(AP+'source-copies-git-roundtrip.json'))
cs=json.loads(blob('src/content/topics/architecture.json'))['questions']; baseline=json.loads(blob('src/content/topics/architecture.json','afef4bf'))['questions']
scope=json.loads(blob('docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12cda/architecture-remaining16-scope.json'))['exactIds']
identity='01a12d07-c52d-77f3-9da9-257547a9970f'
assert identity!=r['agentIdentity']
(OUT/'sources').mkdir(exist_ok=True)
sources={}; prov={x['file']:x for x in provenance['sources']}
for name in sorted({p['rawCapture'] for c in r['cards'] for f in c['fields'] for p in f['proofs']}):
 b=blob(AP+name);(OUT/name).write_bytes(b)
 x=prov[name];actual=next(p for c in r['cards'] for f in c['fields'] for p in f['proofs'] if p['rawCapture']==name)['url']
 decoded=json.loads(b)['results'][0] if name.endswith('.json') else rendered(b)
 sources[name]={'rawCapture':name,'sourceUrl':x['sourceUrl'],'actualCaptureUrl':actual,'originalGitPath':AP+name,'originalCapturePath':x['originalRawCapture'],'originalGitBlob':subprocess.check_output(['git','rev-parse',FROZEN+':'+AP+name],cwd=ROOT).decode().strip(),'rawSha256':h(b),'bytes':len(b),'byteIdenticalToFrozenGit':(OUT/name).read_bytes()==b,'captureFormat':'Complete original HTTP response body bytes; JSON API record' if name.endswith('.json') else 'Complete original HTML response body bytes; decoded as UTF-8 HTML, script/style omitted for reading only','fullOriginalReadBy':identity,'fullOriginalRead':True,'readMethod':'Reader opened frozen Git original, read complete rendered substantive original text, then inspected each locator and current literal. No inherited source or editorial PASS.','decoded':decoded}
save('frozen-cards.json',[c for c in cs if c['id'] in scope])
save('sources-manifest.json',[{k:v for k,v in x.items() if k!='decoded'} for x in sources.values()])
# Rules are copied from the current approved GAME_SPEC, not invented per card.
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text()
rules={
'duplicates':next(s for s in spec.splitlines() if s.startswith('- Ручная калибровка')),'notes':next(s for s in spec.splitlines() if s.startswith('- Каждая справка относится')),
'medium':next(s for s in spec.splitlines() if s.startswith('- Medium-вопрос')),
'hard':next(s for s in spec.splitlines() if s.startswith('- Hard-вопрос')),
'easy':next(s for s in spec.splitlines() if s.startswith('- Easy-вопрос')),
'unique':next(s for s in spec.splitlines() if s.startswith('- Каждый вопрос имеет четыре')),
'russian':next(s for s in spec.splitlines() if s.startswith('- Вопрос и все четыре ответа проверяются')),
'explanation':next(s for s in spec.splitlines() if s.startswith('- Объяснение содержит от двух'))}
save('approved-rules.json',{'source':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','sha256':h(spec),'rules':rules})
manual=json.loads((OUT/'manual-analysis.json').read_text())
records=[]
for ar in r['cards']:
 c=next(x for x in cs if x['id']==ar['questionId']);m=manual[c['id']];fields=[]
 for af in ar['fields']:
  f=af['field']; literal={'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']} if f=='prompt-key' else c['explanation'] if f=='explanation' else c['answers'][int(f[-1])]['note']
  analysis=m['fields'][f];proofs=[]
  for ap in af['proofs']:
   sx=sources[ap['rawCapture']];loc=ap['locator'];raw=blob(AP+ap['rawCapture']);decoded=sx['decoded'];passage=ap.get('decodedPassage',ap['passage'])
   if ap['rawCapture']=='sources/unesco-1485.json' and f=='note3':loc={'jsonPointer':'/results/0/description_en'}
   if ap['rawCapture']=='sources/unesco-1208.json' and f=='note0':passage='Qal’eh Dokhtar (Maiden’s fortress, ca. 7th century)'
   if isinstance(decoded,dict):
    ptr=loc.get('jsonPointer'); target=decoded[ptr.split('/')[-1]] if ptr else canon(decoded);present=passage in target
   else:target=decoded;present=re.sub(r'\s+',' ',passage).strip() in target
   # Locator and quote are reviewed against current claim; presence does not imply support.
   proofs.append({'rawCapture':ap['rawCapture'],'rawCaptureSha256':sx['rawSha256'],'frozenGitBlob':sx['originalGitBlob'],'sourceUrl':sx['sourceUrl'],'actualCaptureUrl':sx['actualCaptureUrl'],'sourceClass':ap['sourceClass'],'captureFormat':sx['captureFormat'],'locator':loc,'quotedPassage':passage,'quotedPassageSha256':h(passage),'passagePresentInCompleteOriginal':present,'nativeReaderIdentity':identity,'originalRead':True,'semanticSupportVerdict':analysis['sourceVerdict'],'semanticAnalysis':analysis['sourceAnalysis'],'authorClaimPassageSha256':ap['passageSha256'],'authorOriginalLocator':ap['locator'],'authorOriginalQuotedPassage':ap['passage']})
  defects=analysis.get('defects',[])
  if f=='explanation' and len(re.findall(r'[.!?](?:$|\s)',c['explanation']))<2:
   defects.append({'class':'explanation-format','rule':'explanation','actualDefect':'В текущем explanation одно предложение; утверждённая спецификация требует 2–4. Это отдельный редакционный дефект, не причина выдумывать техническое наполнение.'})
  fields.append({'field':f,'currentLiteral':literal,'literalSha256':h(canon(literal) if isinstance(literal,dict) else literal),'authorLiteralSha256':af['literalSha256'],'sourceVerdict':analysis['sourceVerdict'],'editorialVerdict':'HOLD' if defects else 'PASS','verdict':'HOLD' if defects or analysis['sourceVerdict']=='HOLD' else 'PASS','manualIndividualAnalysis':analysis['editorialAnalysis'],'defects':[{**d,'approvedRuleQuote':rules[d['rule']]} for d in defects],'proofs':proofs,'nativeReaderIdentity':identity})
  for ff in fields[-1:]:
   if f!='prompt-key':ff['authorLiteralBindingMatchesCurrent']=ff['literalSha256']==af['literalSha256']
 records.append({'questionId':c['id'],'fixedDifficulty':c['difficulty'],'correctIndex':c['correctIndex'],'logicalKey':c['answers'][c['correctIndex']]['text'],'currentCardCanonicalSha256':h(canon(c)),'authorCardCanonicalSha256':ar['cardCanonicalSha256'],'authorCardBindingMatchesCurrent':h(canon(c))==ar['cardCanonicalSha256'],'editorialAnalysis':m['cardAnalysis'],'verdict':'PASS' if all(f['verdict']=='PASS' for f in fields) else 'HOLD','fields':fields})
checks=[]
for old,new in zip(baseline,cs):
 checks.append({'questionId':new['id'],'orderIdUnchanged':old['id']==new['id'],'difficultyUnchanged':old['difficulty']==new['difficulty'],'correctIndexUnchanged':old['correctIndex']==new['correctIndex'],'outsideScopeCanonicalUnchanged':h(canon(old))==h(canon(new)) if new['id'] not in scope else None})
save('invariants.json',{'baseline':'afef4bf','currentFrozen':subprocess.check_output(['git','rev-parse',FROZEN],cwd=ROOT).decode().strip(),'scopeIds':scope,'checks':checks,'allFixedIdOrderDifficultyCorrectIndex':all(x['orderIdUnchanged'] and x['difficultyUnchanged'] and x['correctIndexUnchanged'] for x in checks),'protected84Unchanged':all(x['outsideScopeCanonicalUnchanged'] for x in checks if x['questionId'] not in scope),'logicalKeyPlacement':[{ 'id':c['id'],'index':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text'],'supportedByCurrentPromptKey':next(x for x in records if x['questionId']==c['id'])['fields'][0]['sourceVerdict']} for c in cs if c['id'] in scope]})
save('independent-receipt.json',{'role':'distinct-independent-source-editorial-reader','nativeAgentIdentity':identity,'authorIdentity':r['agentIdentity'],'frozenCommit':subprocess.check_output(['git','rev-parse',FROZEN],cwd=ROOT).decode().strip(),'readDate':'2026-10-12','canonicalRecipe':'Full parsed card JSON, UTF-8, ensure_ascii=False, sort_keys=True, separators=(comma,colon), no trailing newline; SHA-256. Note/explanation literal: exact UTF-8 string. Prompt/key literal: canonical JSON object containing prompt, all four answer texts in order, correctIndex, key.','cards':records,'counts':{'cards':len(records),'pairedFields':sum(len(x['fields']) for x in records),'cardPASS':sum(x['verdict']=='PASS' for x in records),'cardHOLD':sum(x['verdict']=='HOLD' for x in records),'fieldPASS':sum(f['verdict']=='PASS' for x in records for f in x['fields']),'fieldHOLD':sum(f['verdict']=='HOLD' for x in records for f in x['fields']),'sourceFieldPASS':sum(f['sourceVerdict']=='PASS' for x in records for f in x['fields']),'sourceFieldHOLD':sum(f['sourceVerdict']=='HOLD' for x in records for f in x['fields'])},'limits':['Frozen cf60970 only; later source/card changes require a new distinct current binding.','Passage presence and raw hashes do not prove literal support, difficulty or acceptance.','No content edits, no reclassification/exclusion, no protected84 editorial re-audit, no planning/claim edits, no full suite/build/deploy.']})
print(json.dumps(json.loads((OUT/'independent-receipt.json').read_text())['counts']))
