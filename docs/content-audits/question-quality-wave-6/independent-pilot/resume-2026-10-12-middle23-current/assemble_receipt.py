"""Packages handwritten per-field decisions; no source/editorial verdict is computed."""
import json, hashlib, subprocess, os, io, collections
from urllib.parse import quote
from pathlib import Path
from read_sources import ROOT,OUT,OLD,NEW,FROZEN,raw,text,visible
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()=='codex/question-quality-wave-6'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode('utf8')
def write(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
scopepath='docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12cda/middle-remaining23-scope.json'
authorpath='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/remainder23/author-remainder23-receipt.json'
scope=json.loads(raw(scopepath));author=json.loads(raw(authorpath));topic=json.loads(raw('src/content/topics/middle-ages.json'));byid={q['id']:q for q in topic['questions']}
oldurls={p['rawCapture']:p['url'] for c in author['cards'] for f in c['fields'] for p in f['proofs']}
# Exact quote locations below were selected during source reading, not from author verdicts.
defs={
'FA':(OLD,'fordham-famine-1315.html','The land was so oppressed',1600),
'HM':(OLD,'fordham-homage.html','When a Freeman shall do Homage',2000),
'FF':(OLD,'cnrtl-fief.json','Terre, plus rarement',650),
'VS':(OLD,'cnrtl-vassal.json','Dans la société franque',1800),
'TO':(OLD,'cnrtl-tournoi.json','Joute guerrière',750),
'JO':(OLD,'cnrtl-joute.json','Combat de parade',1400),
'ME':(OLD,'cnrtl-mêlée.json','Confusion de combattants',900),
'CH':(OLD,'cnrtl-chevalerie.json','Institution militaire',900),
'EX':(OLD,'cnrtl-excommunication.json','Sanction qui retranche',1800),
'IN':(OLD,'cnrtl-indulgence.json','Rémission totale',1800),
'PL':(OLD,'cnrtl-pèlerinage.json','Voyage individuel',850),
'RE':(OLD,'cnrtl-relique.json','Ce qui reste',600),
'CT':(OLD,'cnrtl-charte.json','Acte authentique',1200),
'PE':(OLD,'cnrtl-péage.json','Droit dont devaient',900),
'CS':(OLD,'cnrtl-croisade.json','Expédition dont',1500),
'ID':(OLD,'new-interdict.html','An interdict is a censure',4700),
'YK':(OLD,'new-shrine-york.html','Place pilgrimage is a fundamental',1250),
'GA':(OLD,'new-market-gazetteer.html','Markets and fairs were trading events',6500),
'JI':(OLD,'persee-medieval-jihad.html',"Un tableau historique du djihâd",1650),
'BD':(OLD,'ucdavis-black-death.html','In the year of our Lord 1348',2500),
'DM':(OLD,'hecker-dancing-1374.html','The Dancing Mania of the year 1374',2000),
'SS':(OLD,'gutenberg-sweating.html','We may preface our historical',1800),
'FR':(NEW,'fao-frost-cereals.pdf','EUROPE:',1100),
'DR':(NEW,'fao-drought.html','Drought is a slow-onset',1250),
'LC':(NEW,'fao-locust-crops.html','During infestations and outbreaks',900),
'PN':(NEW,'newadvent-penance-virtue.html','Penance ( poenitentia )',1200),
'CB':(NEW,'cambridge-homage.html','Summary The French historian',1000),
'IC':(NEW,'cnrtl-icone.json',"Dans l'Église d'Orient",750),
'RQ':(NEW,'cnrtl-reliquaire.json','Sorte de coffret',600),
'CR':(NEW,'cnrtl-crucifix.json','Objet de dévotion',650),
'MO':(NEW,'cnrtl-monastere.json','Institution chrétienne',850),
'CA':(NEW,'cnrtl-cathedrale.json',"Église principale",600),
'EG':(NEW,'cnrtl-eglise.json','II. — P. méton.',750),
'CO':(NEW,'cnrtl-courtoisie.json',"[P. réf.",1300),
'RG':(NEW,'cnrtl-registre.json','Cahier, livre',2500),
'PV':(NEW,'cnrtl-proces-verbal.json','Acte de procédure',750),
'TX':(NEW,'cnrtl-taxe.json','Dans les fin. locales',1900),
'DU':(NEW,'cnrtl-douane.json','Administration qui organise',2200),
'GP':(OLD,'glasgow-armed-pilgrimage.pdf','Approaches',4300),
'RC':(OLD,'texas-reconquista.pdf',None,0),
}
newurls={
'FR':'https://www.fao.org/4/J2254e/J2254e00.pdf',
'DR':'https://www.fao.org/land-water/water/drought/drought',
'LC':'https://www.fao.org/locusts-cca/bioecology/en',
'PN':'https://www.newadvent.org/cathen/11618b.htm',
'CB':'https://www.cambridge.org/core/books/abs/peacemaking-in-the-middle-ages/homage-fealty-and-gestures-of-submission/B787F01B922BBE1043C52B00A8A393AD',
'IC':'https://www.cnrtl.fr/api/word/ic%C3%B4ne/',
'CA':'https://www.cnrtl.fr/api/word/cath%C3%A9drale/',
'MO':'https://www.cnrtl.fr/api/word/monastere/',
'EG':'https://www.cnrtl.fr/api/word/eglise/',
'PV':'https://www.cnrtl.fr/api/word/proc%C3%A8s-verbal/',
}
entries={}
for sid,(base,name,anchor,length) in defs.items():
 path=base+name;b=raw(path);u=oldurls.get(path) or newurls.get(sid)
 if not u:
  term={'RQ':'reliquaire','CR':'crucifix','CO':'courtoisie','RG':'registre','TX':'taxe','DU':'douane'}[sid];u='https://www.cnrtl.fr/api/word/'+term+'/'
 sourceurl=u
 if name.startswith('cnrtl-'):
  j=json.loads(b);sourceurl='https://www.cnrtl.fr/definition/'+quote(j['header']['full_form'].split(',')[0].lower())
  cls='CNRTL/TLFi full lexical API response; TLFi entry read from original JSON'
  fmt='JSON lexical API payload, not HTML definition page or search result'
 elif name.endswith('.pdf'):
  cls='complete captured PDF document'
  fmt='PDF original bytes'
 elif sid=='CB':cls='publisher chapter Summary/abstract only; no full chapter';fmt='HTML publisher response with access gate'
 elif sid=='JI':cls='review web page with transcription of printed119 only; NOT full119–125 article or Morabia thesis';fmt='HTML bibliographic page and first-page transcription'
 else:cls='complete captured institutional/reference or primary-text web response';fmt='HTML original response bytes'
 passages=[]
 if sid=='RC':
  cls='scanned11-page extract of Lapidus, A History of Islamic Societies,2nd ed.; captured7 PDF pages incl cover/fragment'
  passages=[{'locator':'PDF5 left, printed314, The Reconquista','passage':'The disintegration of the Muslim states in the eleventh century allowed for the rapid expansion of the various Christian kingdoms.'}, {'locator':'PDF5 right, printed315, paragraph before Hispano-Arabic civilization','passage':'final conquest of the last Muslim possession in Spain in 1492.'}, {'locator':'PDF7 right, printed319','passage':'The Christian conquest of Granada in 1492 marked the beginning of the end of the Muslim population in Spain.'}]
  method='All7 original scanned pages visually inspected via extracted original page images; quotations manually transcribed. No text layer exists; no OCR/snippet substitute.'
 else:
  s=text(path);i=s.find(anchor);assert i>=0,(sid,anchor);passages=[{'locator':anchor+'; visible text offset '+str(i),'passage':s[i:i+length]}]
  method='Complete raw capture loaded from frozen Git blob; relevant substantive entry/sections read in source. No claim entire271-page thesis or every unrelated chapter was read.'
  extras={'GA':[('An important indication of whether each place',2200),('A second indication of the early urban',800),('It cannot be assumed that such places also had a fair',200)],'SS':[('For sodenly a dedly and burnyng sweate',1000)],'YK':[('Miracle collections associated with particular shrines',450)],'GP':[('The efforts of the',1000),('For the purposes of this thesis',1800),('Pilgrimage is a religious or spiritual',700),('penitential pilgrimages',750),('Substitute pilgrims also appear',650)]}
  for term,n in extras.get(sid,[]):
   k=s.find(term);assert k>=0,(sid,term);passages.append({'locator':term+'; visible text offset '+str(k),'passage':s[k:k+n]})
 for p in passages:p['passageSha256']=sha(p['passage'].encode())
 attrs=subprocess.check_output(['git','check-attr','text','--',path],cwd=ROOT).decode().strip()
 local=(ROOT/path).read_bytes();assert local==b,path
 entries[sid]={'sourceId':sid,'rawCapture':path,'rawCaptureSha256':sha(b),'rawBytes':len(b),'frozenGitCommit':FROZEN,'frozenGitBlob':subprocess.check_output(['git','rev-parse',FROZEN+':'+path],cwd=ROOT).decode().strip(),'sourceURL':sourceurl,'actualCaptureURL':u,'captureURLProvenance':'original author receipt / native author capture command inspected; no new fetch claimed','sourceClass':cls,'captureFormat':fmt,'readingMethod':method,'gitAttribute':attrs,'currentEqualsFrozenGitBytes':True,'quotedPassages':passages}
# Fixed source manifests preserve raw failures, which must not count as proof.
manifest=json.loads(raw('docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/remainder23/source-manifest.json'))
excluded=[x for x in manifest['files'] if x['captureStatus']=='failed-or-unusable']
for x in excluded:
 b=raw(x['path']);x.update({'independentExcluded':True,'actualRawSha256':sha(b),'reason':'failed/unusable original capture; not evidence regardless extension'})
rows=[]
for line in (OUT/'manual-analysis.tsv').read_text().splitlines():
 if not line or line.startswith('#'):continue
 parts=line.split('|');assert len(parts)==7,parts
 rows.append(parts)
assert len(rows)==138
fields=['prompt-key','note0','note1','note2','note3','explanation'];cards=[]
for qid in scope['exactIds']:
 q=byid[qid];cr=[x for x in rows if x[0]==qid];assert [x[1] for x in cr]==fields
 frows=[]
 for _,field,pids,sv,ev,sa,ea in cr:
  literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if field=='prompt-key' else q['explanation'] if field=='explanation' else q['answers'][int(field[-1])]['note']
  proofs=[entries[x] for x in pids.split(',')]
  frows.append({'field':field,'literal':literal,'literalSha256':sha(canonical(literal)),'sourceVerdict':sv,'editorialVerdict':ev,'verdict':'PASS' if sv==ev=='PASS' else 'FIX','sourceAnalysis':sa,'editorialAnalysis':ea,'proofs':proofs,'manualIndividualAnalysis':True})
 ac=next(c for c in author['cards'] if c['questionId']==qid);assert sha(canonical(q))==ac['cardCanonicalSha256'],qid
 cards.append({'questionId':qid,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':sha(canonical(q)),'cardLiteral':q,'verdict':'PASS' if all(f['verdict']=='PASS' for f in frows) else 'FIX','fields':frows})
assert len(cards)==23
stats={'cards':dict(collections.Counter(c['verdict'] for c in cards)),'fields':dict(collections.Counter(f['verdict'] for c in cards for f in c['fields'])),'sourceFields':dict(collections.Counter(f['sourceVerdict'] for c in cards for f in c['fields'])),'editorialFields':dict(collections.Counter(f['editorialVerdict'] for c in cards for f in c['fields']))}
# Compare protected literals without editorial reread.
canonpath=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');spec=canonpath.read_text();rules=[]
for phrase in ['Easy-вопрос проверяет','Medium-вопрос, скорее всего','Каждая справка относится','Прямой и обратный вопросы']:
 for i,line in enumerate(spec.splitlines(),1):
  if phrase in line:rules.append({'path':str(canonpath),'line':i,'quotedRule':line,'ruleSha256':sha(line.encode())});break
protected=[]
for p in scope['protected77']:
 qid=p['questionId'];actual=sha(json.dumps(byid[qid],ensure_ascii=False,separators=(',',':'),sort_keys=True).encode());assert actual==p['cardCanonicalSha256'],qid;protected.append({'questionId':qid,'cardCanonicalSha256':actual})
assert len(protected)==77
partnerpath='src/content/topics/history-spain.json';partner=next(q for q in json.loads(raw(partnerpath))['questions'] if q['id']=='history-spain-easy-01-04')
receipt={'role':'distinct independent current source and editorial reader; not author acceptance or human acceptance','actualNativeAgentIdentity':{'CODEX_THREAD_ID':os.environ['CODEX_THREAD_ID'],'sourceCoordinatorThread':'01a12cda-2625-7c23-afec-132db866c172','actualAuthorThread':'01a12ca5-97a5-7860-9e4a-789a3f6bdcab','distinctFromAuthor':os.environ['CODEX_THREAD_ID']!='01a12ca5-97a5-7860-9e4a-789a3f6bdcab'},'reviewedDate':'2026-10-12','frozenAuthorContentCommit':'c20daf0a1af4d706daf8750bf4fd0a7d7365e0f5','frozenReviewCommit':FROZEN,'authorReceiptPath':authorpath,'authorReceiptSha256':sha(raw(authorpath)),'scopePath':scopepath,'scopeSha256':sha(raw(scopepath)),'exactIdsInScopeOrder':scope['exactIds'],'pairedFieldCount':138,'counts':stats,'overallVerdict':'FIX','canonicalRecipe':"UTF8(json.dumps(parsed object, ensure_ascii=False, separators=(',',':'), sort_keys=False)); preserve parsed field insertion order; SHA256 bytes. Same recipe for every field literal incl JSON strings and prompt/key list.",'passageRecipe':'HTML: standard HTMLParser data, skip script/style, collapse whitespace. CNRTL: first complete TLFi content entry from full raw JSON then same parser. PDF text: pypdf full page extraction incl page markers, quotes retain extracted text. Texas: manual visual transcription from complete scanned page. SHA256 of quoted passage UTF8 exactly as stored; raw SHA always original Git blob bytes.','rubric':{'correctNote':'Useful standalone definition/fact accepted; may overlap main fact and explanation. No invented novelty rule beyond bare prompt/key repetition.','wrongNote':'Own useful fact suffices; explaining wrongness is not mandatory.','holds':'No HOLD issued; difficulty defects explicitly FIX within unchanged level/slot. No reclassification/exclusion/content edit.'},'approvedRules':rules,'approvedSpecSha256':sha(canonpath.read_bytes()),'cards':cards,'duplicateFinding':{'reviewedQuestionId':'middle-ages-reconquista','verdict':'FIX','partnerPath':partnerpath,'partnerLiteral':partner,'partnerCanonicalSha256':sha(canonical(partner)),'partnerGitBlob':subprocess.check_output(['git','rev-parse',FROZEN+':'+partnerpath],cwd=ROOT).decode().strip(),'testedFactReadInBothCards':'Name of multi-century expansion of Christian Iberian kingdoms against Muslim states; same relation, same answer Reconquista.','resolutionRequired':'Replace tested fact of reviewed middle-ages-reconquista with independent medium fact preserving ID/key1/order. Partner unchanged; recording alone does not close duplicate.'},'protected77CanonicalRecipe':'Scope protected77 uses UTF8 JSON ensure_ascii=False compact separators sort_keys=True; distinct from author current-card recipe; protected hash comparisons use scope recipe.', 'protected77HashReadOnlyCheck':protected,'sourceLimits':'Original complete raw captures read and relevant full sections/pages inspected; publisher summary and first-page review are limited evidence honestly classified. A file extension or receipt never establishes completeness. Long theses were not read cover-to-cover and are not claimed to be.','excludedCaptures':excluded,'failedNetworkAttemptsExcluded':manifest['failedNetworkAttempts'],'scopeBoundary':'Only independent reader folder written. No cards, planning, claims, primary Local, or outside2000 edited; other actors preserved. No fullsuite/build/deploy.'}
write('reader-receipt.json',receipt);write('source-inventory.json',{'frozenGitCommit':FROZEN,'sources':list(entries.values()),'excludedCaptures':excluded,'sourceCounts':{'usedRawOriginals':len(entries),'excludedRawCaptures':len(excluded)},'normalizationOnlyForQuotedPassages':True})
print(json.dumps(stats));print('reader',os.environ['CODEX_THREAD_ID'],'raw sources',len(entries),'protected',len(protected))
