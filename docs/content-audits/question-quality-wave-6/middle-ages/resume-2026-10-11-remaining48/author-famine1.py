"""One explicit source-based author read; no automated substantive certification."""
import importlib.util,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('p',R/'pilot-authored.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
URL='https://sourcebooks.web.fordham.edu/source/famin1315a.asp'
raw=R/'sources/fordham-famine1315.html';parser=p.Text();parser.feed(raw.read_text());txt=' '.join(' '.join(parser.parts).split())
quotes={
 'rain':'The summer rains were so heavy that grain could not ripen.',
 'drying':'It could hardly be gathered and used to bake bread down to the said feast day unless it was first put in vessels to dry.',
 'warmth':'Bread did not have its usual nourishing power and strength because the grain was not nourished by the warmth of summer sunshine.',
 'livestock':'Meat and eggs began to run out, capons and fowl could hardly be found, animals died of pest, swine could not be fed because of the excessive price of fodder.',
 'royal':'The land was so oppressed with want that whe the king came to St. Albans on the feast of St. Laurence [August 10] it was hardly possible to find bread on sale to supply his immediate household.'}
for quote in quotes.values():assert quote in txt,quote
edit={'prompt':'С каким бедствием хронист Иоанн де Трокелоу связывал нехватку зрелого зерна в Англии во время голода 1315 года?','answers':[{'text':'С гибелью озимых от зимних морозов','note':'В этом рассказе зерну не хватало летнего солнечного тепла для созревания; гибель озимых от мороза не названа причиной.'},{'text':'С засухой, лишившей поля влаги','note':'Хронист описывает избыток влаги: собранное зерно сначала приходилось сушить в сосудах, чтобы использовать для хлеба.'},{'text':'С нашествием саранчи на посевы','note':'Упомянутая в хронике животная беда — падёж скота от мора; препятствием созреванию зерна названы дожди.'},{'text':'С чрезмерно обильными летними дождями','note':'По рассказу хрониста, даже для королевского двора в Сент-Олбансе было трудно найти хлеб в продаже.'}],'explanation':'Хронист связывал плохое созревание зерна с сильными летними дождями. Даже собранное зерно приходилось предварительно сушить, прежде чем печь из него хлеб.','source':{'title':'Johannes de Trokelowe — Famine of 1315, Internet Medieval Sourcebook','url':URL,'verifiedAt':'2026-10-11'}}
reads=[
 ('prompt-key','PASS',True,'The chronicle explicitly states summer rains so heavy grain could not ripen. Вопрос атрибутирован конкретному хронисту, а не выдаёт его суждения за полный современный климатический анализ. Обильные летние дожди и нехватка зрелого зерна1315 прямо подтверждены.',['rain']),
 ('note0','PASS',True,'Warmth passage states insufficient summer sunshine. Note corrects the precise misplaced season/cause in the false winter-frost statement, not an empty does-not-fit label. It does not assert that no frost occurred anywhere.',['warmth','rain']),
 ('note1','PASS',True,'Heavy rain plus requirement to put grain in vessels to dry directly support excess moisture and specified drying. This corrects drought by a concrete, source-bound opposite process.',['rain','drying']),
 ('note2','PASS',True,'Chronicle reports animal pest and separately rains preventing ripening. Note identifies the actual animal calamity rather than attributing locust damage without evidence; no modern pathogen diagnosis added.',['livestock','rain']),
 ('note3','PASS',True,'Royal household at StAlbans could hardly find bread on sale. Атрибуция хронисту retained; additional food-supply episode distinct from main weather cause. Not claimed that king starved.',['royal']),
 ('explanation','PASS',True,'Two sentences combine explicit rains/ripening and drying-before-bread. No unsupported temperatures or Europe-wide generalization.',['rain','drying'])]
def emit():
 topic=json.loads(p.TOPIC.read_text());c=next(q for q in topic['questions'] if q['id']=='middle-ages-great-famine');c.update(edit)
 rec={'questionId':c['id'],'cardCanonicalSha256':p.digest(p.canon(c)),'verdict':'PASS','editorialAnalysis':'Medium: известный изучающим позднесредневековую Европу кризис1315–1317, вопрос о характере аграрного бедствия, а не случайной цене или дате. Четыре сопоставимых причины неурожая, все реальные угрозы аграрному хозяйству; ключ не повторяет слово голод. Зимний мороз, засуха и насекомые правдоподобны до знания конкретного эпизода. Все четыре конструкции с + творительный падеж прочитаны вместе с вопросом. Correct-note добавляет случай с королевским снабжением.','literalSnapshot':c,'grammarSubstitutions':[c['prompt']+' — '+a['text']+'.' for a in c['answers']],'fields':[]}
 for name,v,read,analysis,refs in reads:
  lit=[c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note'];f={'field':name,'verdict':v,'substantiveRead':read,'claimAnalysis':analysis,'literal':lit,'literalSha256':p.digest(p.canon(lit) if isinstance(lit,list) else lit.encode()),'proofs':[]}
  for ref in refs:
   quote=quotes[ref];f['proofs'].append({'proofId':ref,'sourceClass':'Medieval primary chronicle: Johannes de Trokelowe, Annales; Brian Tierney translation reproduced by Internet Medieval Sourcebook','title':'Famine of 1315','url':URL,'rawCapture':'sources/'+raw.name,'rawCaptureSha256':p.digest(raw.read_bytes()),'captureFormat':'HTML original bytes','captureMethod':'Complete HTTP200 curl --compressed response; original full chronicle excerpt, not search snippet. Original spelling including whe retained.','locator':'Translated chronicle paragraph containing '+quote[:65],'passage':quote,'passageSha256':p.digest(quote.encode())})
  rec['fields'].append(f)
 receipt={'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'status':'AUTHOR_CANDIDATE_ONLY; not independent certification','cards':[rec]};p.TOPIC.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n');(R/'author-famine1.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(R/'famine1-candidate.json').write_text(json.dumps([c],ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':emit()
