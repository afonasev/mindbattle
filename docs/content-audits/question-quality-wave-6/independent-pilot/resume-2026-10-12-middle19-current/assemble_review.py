import csv,json,pathlib,hashlib,subprocess,os,sys,re
from read_sources import extract,visible
ROOT=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert pathlib.Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())==ROOT
BASE=pathlib.Path('docs/content-audits/question-quality-wave-6'); OUT=BASE/'independent-pilot/resume-2026-10-12-middle19-current'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d,sort=False:json.dumps(d,ensure_ascii=False,separators=(',',':'),sort_keys=sort).encode()
write=lambda n,d:(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
paths=[BASE/'middle-ages/resume-2026-10-12-fresh-rework19'/n for n in ['author-pass-01-first3.json','author-pass-02-interdict-melee-chivalry.json','author-pass-03-relic-shrine-indulgence.json']]+[BASE/'middle-ages/resume-2026-10-12-fresh-unreviewed10/author-pass-current10.json']
author={}; meta={}
for idx,p in enumerate(paths):
 d=json.loads(p.read_text())
 for c in d['cards']:
  author[c['questionId']]={'path':str(p),'record':c,'sort':idx<3,'identity':'01a12e9a-ded0-7130-b6cb-ff9f08c6ea6d' if idx<3 else '01a12ebd-42bd-7ab3-a8dd-638984bcefce'}
  for f in c['fields']:
   for pr in f['proofs']:meta[pathlib.Path(pr['fullCapturePath']).name]=pr
scope=json.loads((BASE/'coordinator-continuation-01a12cda/middle-ages-remaining19-scope.json').read_text())['exactIds']
assert len(scope)==len(author)==19 and set(scope)==set(author)
topic=pathlib.Path('src/content/topics/middle-ages.json');disk=topic.read_bytes();frozen=subprocess.check_output(['git','show','08e4ee3:src/content/topics/middle-ages.json']);assert disk==frozen
cards={c['id']:c for c in json.loads(disk)['questions']}
for id in scope:assert sha(canon(cards[id],author[id]['sort']))==author[id]['record']['cardCanonicalSha256'],id
rows={('middle-ages-'+r['id'],r['field']):r for r in csv.DictReader((OUT/'manual-analysis.tsv').open(),delimiter='\t')};assert len(rows)==114
# Each selector is a reader-chosen passage, not an inherited verdict.
selectors={
'fief':('cnrtl-fief.json','Terre, plus rarement',550),
'homage':('fordham-homage.html','When a Freeman shall do Homage',420),
'fealty':('fordham-homage.html','When a Freeman shall do fealty',380),
'tournoi':('cnrtl-tournoi.json','Joute guerrière',600),
'joute':('cnrtl-joute.json','Combat de parade',440),
'melee':('cnrtl-mêlée.json','Combat confus',270),
'duel':('cnrtl-duel-api.json','Combat singulier entre',430),
'duel-general':('cnrtl-duel-api.json','Combat singulier dans',180),
'chevalerie':('cnrtl-chevalerie.json','Institution militaire',560),
'mail':('armour.html','Mail was a very good defence',420),
'axes-maces':('armour.html','The Battle of Rosebeke',475),
'interdict':('new-interdict.html','A general local interdict is one',700),
'interdict-contrast':('new-interdict.html','Interdict differs from excommunication',430),
'interdict1909':('new-interdict.html','A quite recent example',1200),
'indulgence':('cnrtl-indulgence.json','Rémission totale',380),
'excommunication':('cnrtl-excommunication.json','Sanction qui retranche',430),
'penance':('newadvent-penance-virtue.html','Penance ( poenitentia )',680),
'courtoisie':('cnrtl-courtoisie.json','COURTOISIE substantif féminin',660),
'vassal':('cnrtl-vassal.json','Dans la société franque',470),
'monastere':('cnrtl-monastere.json','Institution chrétienne',550),
'relique':('cnrtl-relique.json','Ce qui reste',500),
'icone':('cnrtl-icone.json',"Dans l'Église d'Orient",400),
'reliquaire':('cnrtl-reliquaire.json','Sorte de coffret',500),
'crucifix':('cnrtl-crucifix.json','Objet de dévotion',390),
'cathedrale':('cnrtl-cathedrale.json','Église principale',220),
'eglise':('cnrtl-eglise.json','Ca 1050',300),
'repentir':('cnrtl-repentir-api.json','Regret douloureux',360),
'confession':('cnrtl-confession-api.json',"Déclaration que l'on fait",260),
'market':('new-market-gazetteer.html','Markets and fairs were trading events',1550),
'fair':('new-market-gazetteer.html','A fair was held once a year',1600),
'fair-place':('new-market-gazetteer.html','Fairs were sometimes held outside',640),
'market-inference':('new-market-gazetteer.html','An important indication of whether each place',1100),
'mint':('new-market-gazetteer.html','A second indication of the early urban',950),
'market-charter':('new-market-gazetteer.html','In England royal grants of markets and fairs',650),
'market-tolls':('new-market-gazetteer.html','By their grants monarchs conveyed',440),
'peage':('cnrtl-péage.json','Droit dont devaient',600),
'douane':('cnrtl-douane.json','Administration qui organise',580),
'charte':('cnrtl-charte.json','Acte authentique',600),
'registre':('cnrtl-registre.json','Cahier, livre',500),
'proces-verbal':('cnrtl-proces-verbal.json','Acte de procédure',440),
'london':('london-archives-william-charter.html',"The 'William Charter'",1000),
'london-rights':('london-archives-william-charter.html','William the king, friendly salutes',830),
'croisade':('cnrtl-croisade.json','Expédition dont',1200),
'persee':('persee-medieval-jihad.html','Un tableau historique du djihâd',1600),
'hecker':('hecker-dancing-1374.html','The Dancing Mania of the year 1374',1150),
'boccaccio':('ucdavis-black-death.html','In the year of our Lord 1348',1000),
'famine':('fordham-famine-1315.html','In the year of our Lord 1315',1300),
'webb':('gutenberg-sweating.html','We may preface our historical',1200),
'webb-symptoms':('gutenberg-sweating.html','For sodenly a dedly',1000),
'webb-spread':('gutenberg-sweating.html','The English sweat is stated by Caius',2300),
'shrine':('uea-medieval-pilgrimage.pdf',17, None),
'pilgrim':('glasgow-armed-pilgrimage.pdf',22,None),
'pilgrim-general':('glasgow-armed-pilgrimage.pdf',9,None),
'pilgrim-merchants':('glasgow-armed-pilgrimage.pdf',51,None),
}
scans={
'lapidus1149':('Physical PDF page5, left column, printed314, The Reconquista; paragraph The Christian advance', 'The Almohads, who took Marrakesh in 1147, unhesitatingly accepted the concept of a Moroccan empire which included Spain. In turn, they took Seville and Cordova in 1149, and the rest of Muslim Spain by 1172.'),
'lapidus1085':('Physical PDF page5, left column, printed314, second paragraph','In 1085 Alfonso VI, with the strength of the unified kingdoms of Castile, Leon, and Galicia, conquered Toledo.'),
'lapidus1236':('Physical PDF page5, left column, printed314, final paragraph','The union of Castile and Leon in 1230 opened the way for the conquest of Cordova in 1236 and Seville in 1248.'),
'lapidus1492':('Physical PDF page5, right column, printed315, first paragraph','Christian rulers gave no priority to the conquest of Granada until the union of Castile and Aragon opened the way for the final conquest of the last Muslim possession in Spain in 1492.'),
}
registry={}; proofs={};texts={}
for key,(name,anchor,length) in selectors.items():
 p=meta[name]; path=p['fullCapturePath'];raw=pathlib.Path(path).read_bytes(); blob=subprocess.check_output(['git','hash-object','--no-filters',path],text=True).strip();committed=subprocess.check_output(['git','show','HEAD:'+path]);indexed=subprocess.check_output(['git','show',':'+path]);assert raw==committed==indexed,(path,'raw roundtrip')
 registry[path]={'path':path,'originalUrl':p['originalUrl'],'captureUrl':p.get('captureUrl',p['originalUrl']),'sourceClass':p['sourceClass'],'format':p['captureFormat'],'nativeBytes':len(raw),'sha256':sha(raw),'gitBlob':blob,'diskIndexCommittedBytesEqual':True,'encoding':('PDF binary' if name.endswith('.pdf') else 'utf8 or cp1252 according to original response'),'readExtent':'Relevant complete definition and neighbouring context in the committed original; no claim that the entire dictionary corpus or thesis was read.'}
 if path not in texts:texts[path]=extract(path)
 s=texts[path]
 if isinstance(anchor,int):
  q=dict(s)[anchor]; loc=f'Physical PDF page{anchor}; printed page'+('17' if key=='shrine' else '14' if key=='pilgrim' else '1' if key=='pilgrim-general' else '43')+'; full physical page extracted from original PDF'
 else:
  i=s.find(anchor);assert i>=0,(key,anchor);q=s[i:i+length];loc=f'Reader extract visible offset{i}; begins {anchor!r}. JSON extraction uses full original JSON then HTMLParser; locator in content component corrected in analysis when relevant.'
 proofs[key]={'sourceRef':path,'locator':loc,'quote':q,'quoteSha256':sha(q.encode()),'quoteRecipe':'SHA256(UTF8 exact stored quote); HTML whitespace collapse only in derived quotation, never in original capture','verification':'Checked against actual raw original extraction with neighbouring context; metadata hashes do not establish reading.'}
path=meta['texas-reconquista.pdf']['fullCapturePath'];p=meta['texas-reconquista.pdf'];raw=pathlib.Path(path).read_bytes();assert raw==subprocess.check_output(['git','show','HEAD:'+path])==subprocess.check_output(['git','show',':'+path]);registry[path]={'path':path,'originalUrl':p['originalUrl'],'captureUrl':p.get('captureUrl',p['originalUrl']),'sourceClass':'Scanned book excerpt, NOT complete book or complete chapter','format':'Original scanned PDF bytes','nativeBytes':len(raw),'sha256':sha(raw),'gitBlob':subprocess.check_output(['git','hash-object','--no-filters',path],text=True).strip(),'diskIndexCommittedBytesEqual':True,'physicalPages':7,'scopeLimitation':'Only printed309-319 excerpt; all linked source fields HOLD under complete-original requirement. Specific passages are visually confirmed independently.','readExtent':'Printed312-315 and318-319 visually inspected; key passages on314/315 and319.'}
for key,(loc,q) in scans.items():proofs[key]={'sourceRef':path,'locator':loc,'quote':q,'quoteSha256':sha(q.encode()),'quoteRecipe':'SHA256(UTF8 exact manual transcription; line wraps/hyphenation joined in derived quotation only)','verification':'Direct visual inspection of scanned physical5 rendered as lapidus-1.png; physical7 as lapidus-2.png. Full-original completeness HOLD.'}
# Six explicitly selected bindings in prompt-key,note0,note1,note2,note3,explanation order.
bindings={
'homage':['fief','fief','fief','fief','homage','fief+fealty'],
 'tournament':['tournoi','joute','melee','duel-general+tournoi','tournoi','tournoi+joute+melee'],
 'joust':['joute','mail','axes-maces','axes-maces','joute','joute+mail+axes-maces'],
 'interdict':['interdict','indulgence','excommunication','interdict1909','penance','interdict+interdict-contrast+indulgence+penance'],
 'melee':['melee','tournoi+melee','tournoi','joute','duel-general+duel','melee+joute+duel'],
 'chivalry':['chevalerie+courtoisie','chevalerie','courtoisie','vassal','monastere','chevalerie+courtoisie'],
 'relic':['relique','icone','relique','reliquaire','crucifix','relique+icone+reliquaire+crucifix'],
 'shrine':['shrine','monastere','shrine','cathedrale','eglise','shrine'],
 'indulgence':['indulgence','repentir','confession','indulgence','penance','indulgence+confession+repentir+penance'],
 'market-town':['market','fair+market-inference','market-charter','market+market-inference','mint','market+fair'],
 'fair':['fair','market','market','market','fair-place','fair+market'],
 'toll':['peage','douane','market-tolls','market-tolls','peage','peage+douane+market-tolls'],
 'charter':['charte+london','registre','registre','proces-verbal','london','london-rights+london'],
 'crusade':['croisade','croisade','lapidus1492','persee','pilgrim-general+pilgrim','croisade+pilgrim'],
 'reconquista':['lapidus1149','lapidus1085','lapidus1149','lapidus1236','lapidus1492','lapidus1149+lapidus1236'],
 'jihad':['persee','croisade','persee','lapidus1492','pilgrim','persee'],
 'pilgrimage-armed':['pilgrim','croisade','market+pilgrim-merchants','pilgrim+pilgrim-general','monastere','pilgrim'],
 'dancing-mania':['hecker','boccaccio','famine','webb-symptoms','hecker','hecker'],
 'sweating-sickness':['webb','boccaccio','famine','hecker','webb-spread','webb+boccaccio+famine+hecker']}
fields=['prompt-key','note0','note1','note2','note3','explanation'];result=[]
for id in scope:
 c=cards[id];a=author[id];fs=[]
 for i,f in enumerate(fields):
  r=rows[id,f];literal={'prompt':c['prompt'],'answers':c['answers'],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']} if f=='prompt-key' else c['explanation'] if f=='explanation' else {'answer':c['answers'][i-1]['text'],'note':c['answers'][i-1]['note']}
  fs.append({'field':f,'currentLiteral':literal,'literalSha256':sha(canon(literal)),'sourceVerdict':r['sourceVerdict'],'editorialVerdict':r['editorialVerdict'],'sourceAnalysis':r['sourceAnalysis'],'editorialAnalysis':r['editorialAnalysis'],'proofs':[proofs[k] for k in bindings[id.removeprefix('middle-ages-')][i].split('+')],'verdict':('HOLD' if 'HOLD' in [r['sourceVerdict'],r['editorialVerdict']] else 'FIX' if 'FIX' in [r['sourceVerdict'],r['editorialVerdict']] else 'PASS'),'independentReaderRead':True})
 aggregate=lambda vs:'HOLD' if 'HOLD' in vs else 'FIX' if 'FIX' in vs else 'PASS'
 sv=aggregate([f['sourceVerdict'] for f in fs]);ev=aggregate([f['editorialVerdict'] for f in fs])
 result.append({'questionId':id,'authorThreadId':a['identity'],'authorRecordPath':a['path'],'authorRecordCardSha256':a['record']['cardCanonicalSha256'],'authorCanonicalRecipe':'sort_keys=True' if a['sort'] else 'sort_keys=False; insertion order','currentCard':c,'currentCanonicalSha256':sha(canon(c)),'readerCanonicalRecipe':'UTF8 json.dumps ensure_ascii=False,separators=(comma,colon),sort_keys=False; insertion order','sourceVerdict':sv,'editorialVerdict':ev,'verdict':aggregate([sv,ev]),'fields':fs,'historicalAuthorAssessments':a['record'],'historyPolicy':'Historical author verdicts included as attributed immutable context; NOT independent verdicts and NOT inherited.'})
from collections import Counter
counts={'cards':19,'fields':114,'cardVerdicts':dict(Counter(c['verdict'] for c in result)),'cardSourceVerdicts':dict(Counter(c['sourceVerdict'] for c in result)),'cardEditorialVerdicts':dict(Counter(c['editorialVerdict'] for c in result)),'fieldSourceVerdicts':dict(Counter(f['sourceVerdict'] for c in result for f in c['fields'])),'fieldEditorialVerdicts':dict(Counter(f['editorialVerdict'] for c in result for f in c['fields']))}
counts['fieldCombinedVerdicts']=dict(Counter(f['verdict'] for c in result for f in c['fields']))
write('source-index.json',{'readerThreadId':os.environ['CODEX_THREAD_ID'],'originals':list(registry.values()),'originalBytePolicy':'No source originals rewritten/copied/normalized. Every referenced disk/index/HEAD original verified byte-identical. New failed capture evidence uses scoped -text.','readingLimit':'Personally reviewed all114 current fields. Read the actual cited definitions, contextual passages and relevant PDF pages from complete saved captures. Did NOT read entire316/271-page theses, all dictionary concordances, or entire historical books. Incomplete original captures remain explicitly HOLD.','excluded':'newadvent-rule-benedict.html is foreign WIP/incomplete and was neither used nor changed.'})
write('reader-receipt.json',{'role':'Independent substantive reader; source/editorial judgments authored in this reader session','readerThreadId':os.environ['CODEX_THREAD_ID'],'frozenCommit':'08e4ee3','gitRoot':str(ROOT),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'frozenTopicSha256':sha(disk),'exactIds':scope,'scopeUnionAndFrozenBytesVerified':True,'protectedOtherCardCount':81,'canonicalRecipe':'UTF8 json.dumps ensure_ascii=False,separators=(comma,colon),sort_keys=False; insertion order. SHA256 of exact UTF8. First9 author comparison separately sort_keys=True; last10 False. Prompt-key literal includes all4 answers and notes plus key/index.','quoteRecipe':'As stored on each proof; no original byte normalization.','verdictAggregation':'HOLD if any source/editorial HOLD, otherwise FIX if any FIX, otherwise PASS. Independent source and editorial verdicts remain separately visible.','counts':counts,'cards':result,'humanAcceptance':False,'pairCertification':'Coordinator01a12cda owns pair certification; no certification or message sent here.'})
print(json.dumps(counts));print('Sources',len(registry))
