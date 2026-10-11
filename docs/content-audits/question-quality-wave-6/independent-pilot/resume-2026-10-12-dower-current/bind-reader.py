#!/usr/bin/env python3
"""Bind this reader's manual decisions to frozen committed source/card bytes."""
import hashlib,json,os,subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
REL=ROOT.relative_to(Path.cwd()).as_posix()
FROZEN='40568e60a28a1eb780077a037e9541028d6285e9'
AUTHOR='d91e19a8882816d83471cb8d321ce85496d597a7'
TOPIC='src/content/topics/middle-ages.json'
BASE='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/'
IDENTITY='01a12ce5-7826-7822-8c4e-1125ff7cee9b'
def git(*args):return subprocess.check_output(['git',*args])
def raw(p,rev=FROZEN):return git('show',rev+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):
  if s.strip():self.parts.append(s.strip())
def plain(s):
 p=Text();p.feed(s);return ' '.join(p.parts)
qs=json.loads(raw(TOPIC))['questions'];card=next(q for q in qs if q['id']=='middle-ages-dower')
assert sha(canon(card))=='783df1e6cf9b5bdb99adbf34b491054874003f2f2092e954f2e0a26db835f57e'
assert os.environ.get('CODEX_THREAD_ID')==IDENTITY
assert git('branch','--show-current').decode().strip()=='codex/question-quality-wave-6'
originals=[]; texts={}
for name in ['cnrtl-douaire.json','cnrtl-dot.json','ugr-dowry.html']:
 p=BASE+'sources/'+name;b=raw(p);dest=ROOT/'originals'/name;dest.write_bytes(b)
 assert raw(p,AUTHOR)==b==Path(p).read_bytes()
 if name.endswith('.json'):
  d=json.loads(b);lines=['HEADER '+json.dumps(d['header'],ensure_ascii=False)]
  for s in d['content']:
   value=s['content'];lines.append('SECTION '+s['id'])
   lines.extend(plain(x) for x in value) if isinstance(value,list) and all(isinstance(x,str) for x in value) else lines.append(json.dumps(value,ensure_ascii=False))
  t='\n'.join(lines)
 else:t=plain(b.decode('iso-8859-1'))
 texts[name]=t;(ROOT/(name+'.reader-text.txt')).write_text(t+'\n')
 originals.append({'originalPath':p,'readerRawCopy':REL+'/originals/'+name,'rawSha256':sha(b),'byteCount':len(b),'gitBlob':git('rev-parse',FROZEN+':'+p).decode().strip(),'captureFormat':'complete native CNRTL API JSON response bytes' if name.endswith('.json') else 'complete publisher HTML response bytes, ISO-8859-1; abstract, not full article','readerMethod':'Read entire preserved committed native response independently, all dictionary sections and metadata; rendered HTML fragments to text only for reading. No fabricated recapture, no excerpt-only original. Raw copy unchanged.'})
(ROOT/'originals' / '.gitattributes').write_text('*.json -text -diff\n*.html -text -diff\n')
def proof(name,url,loc,passage,kind,title):
 assert passage in texts[name],(name,passage)
 o=next(o for o in originals if o['originalPath'].endswith('/'+name))
 return {'sourceClass':kind,'title':title,'url':url,'locator':loc,'rawCapture':o['readerRawCopy'],'rawCaptureSha256':o['rawSha256'],'originalPath':o['originalPath'],'gitBlob':o['gitBlob'],'frozenCommit':FROZEN,'captureFormat':o['captureFormat'],'passage':passage,'passageSha256':sha(passage.encode()),'passageEncoding':'UTF-8, text after HTML entity decoding and whitespace join; original response bytes retained separately'}
douaire=proof('cnrtl-douaire.json','https://www.cnrtl.fr/definition/douaire',{'entry':'DOUAIRE','jsonSectionId':'tlfi','section':'DR. ANC.'},"Droit d'usufruit sur ses biens qu'un mari assignait à sa femme par son mariage et dont elle jouissait si elle lui survivait.",'institutional historical dictionary / CNRTL-TLFi','CNRTL — DOUAIRE, TLFi')
dot=proof('cnrtl-dot.json','https://www.cnrtl.fr/definition/dot',{'entry':'DOT','jsonSectionId':'tlfi','section':'A.'},"Bien qu'apporte une femme en se mariant.",'institutional historical dictionary / CNRTL-TLFi','CNRTL — DOT, TLFi')
alternate=proof('cnrtl-dot.json','https://www.cnrtl.fr/definition/dot',{'entry':'DOT','jsonSectionId':'dmf','section':'definition and Cartul. Laval 1350 example'},'DOT substantif masculin [GDC : dot ; FEW (III, 148a) : dos ; TLF (VII, 445b) : dot ] Douaire . ...sauf du dot fait au mariage de luy et de feue dame Ysabel de Bretaigne, sa première compaigne, et sauf l’entérimance de cest apointement.'.replace('l’entérimance','l\'entérimance'),'institutional Middle French dictionary / CNRTL-DMF','CNRTL — DOT, DMF')
price=proof('ugr-dowry.html','https://www.ugr.es/~arenal/articulo.php?id=80',{'section':'English Abstract, opening sentence'},'This study traces the long term evolution of dowry systems, which can go from brideprice to dowry (the idea of purchase, exchange price, or the value of the bride for that of the dowry).','university journal publisher page; abstract, not full article','Arenal — From Brideprice to Dowry in Mediterranean Europe, Diane Owen Hughes')
gift=proof('ugr-dowry.html','https://www.ugr.es/~arenal/articulo.php?id=80',{'section':'English Abstract, second sentence'},'The author discusses the existence and development of two types of dowry: that which is given by the bride’s parents and that which is given by the groom in exchange for the bride (propter wedding donation).','university journal publisher page; abstract, not full article','Arenal — From Brideprice to Dowry in Mediterranean Europe, Diane Owen Hughes')
keywords=proof('ugr-dowry.html','https://www.ugr.es/~arenal/articulo.php?id=80',{'section':'Spanish Palabras clave / English Keywords'},'donatio propter nupcias o antefactum.','university journal publisher page; abstract, not full article','Arenal — original historical name in keywords')
fields=[]
def field(name,text,editorial,analysis,proofs):fields.append({'field':name,'literalText':text,'literalSha256':sha(canon(text)) if isinstance(text,list) else sha(text.encode()),'sourceVerdict':'PASS','editorialVerdict':editorial,'verdict':editorial,'substantiveRead':True,'individualReaderAnalysis':analysis,'proofs':proofs})
field('prompt-key',[card['prompt'],card['correctIndex'],card['answers'][0]['text']],'FIX','SOURCE PASS: the chosen key matches the TLFi DR. ANC. usufruct definition. The former parenthetical semantic self-cue is resolved: no answer repeats the requested definition. EDITORIAL FIX: the unqualified wording «в старом праве» does not specify the lexicographic sense/tradition. The complete native DOT original includes DMF defining medieval DOT as Douaire, with a 1350 marriage example; answer1 therefore cannot be certified uniquely wrong across the historical scope stated. This is a concrete uniqueness concern, not a claim that every use of dot is usufruct. In the intended TLFi contrast the four alternatives are all marriage-property concepts, but the bare French Douaire/Dot, English Brideprice and hybrid Propter wedding donation form an uneven language/register set. The latter is the publisher abstract’s translation, while the same original supplies donatio propter nupcias. For actual medium, term recognition is legitimate only with clear historical scope and plausible parallel names; removing glosses alone does not establish that boundary or general Russian accessibility. Preserve medium/key0 and repair scope/parallel presentation without reinstating definitional cues.',[douaire,dot,alternate,gift,keywords])
field('note0',card['answers'][0]['note'],'PASS','Assignment by husband and usufruct conditional on outliving him are explicitly supported in TLFi and corroborated by Académie and DMF. The survival condition adds a useful fact absent from prompt/key. This note is Russian prose with the named term and a correct legal loanword. It passes the approved rule even if this fact is also used in an explanation; no invented novelty requirement.',[douaire])
field('note1',card['answers'][1]['note'],'PASS','The TLFi A sense explicitly is property a woman brings into marriage. This is a useful definition about Dot, not merely the question/key repeated. It is concise Russian prose. The fact passes within that named sense; this note does not erase the separate DMF historical synonym issue in the unconstrained question.',[dot])
field('note2',card['answers'][2]['note'],'PASS','The complete publisher HTML abstract explicitly frames brideprice through purchase and exchange price. The note attributes the interpretation to Hughes and does not pretend the full paper was read. It provides a useful fact about the named option in intelligible Russian surrounding the source term/author name. No clue to the key is supplied.',[price])
field('note3',card['answers'][3]['note'],'FIX','SOURCE PASS: the English abstract explicitly identifies a groom-given marriage transfer in exchange for the bride; the Spanish resumen and original Latin keyword confirm which transfer is meant. The fact belongs to option3 and is useful. EDITORIAL FIX for Russian readability and explicit reference: «вид dowry» leaves the essential category untranslated and the note refers only to an unnamed abstract, while the answer is a hybrid English translation. Express this source-attributed fact in clear Russian about the named gift; this is a language repair, not a demand for a new fact.',[gift,keywords])
field('explanation',card['explanation'],'PASS','Two short Russian sentences state the supported TLFi definition and contrast it with property brought into marriage and other transfers. This explains the intended key within the TLFi sense; it does not prove historical answer uniqueness. Douaire is the term being explained. Reading time is below 30 seconds. No requirement that the explanation or correct note contain mutually novel facts is imposed.',[douaire,dot,gift])
protected=[{'questionId':q['id'],'canonicalSha256':sha(canon(q))} for q in qs if q['id']!='middle-ages-dower']
assert len(protected)==99
old='docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle4-current/reader-receipt.json'
receipts=[]
for p,rev in [(BASE+'author-dower-repair-receipt.json',FROZEN),(BASE+'dower-repair-git-roundtrip.json',FROZEN),(old,'d13ff9f')]:
 receipts.append({'path':p,'commit':rev,'sha256':sha(raw(p,rev)),'gitBlob':git('rev-parse',rev+':'+p).decode().strip()})
record={'schemaVersion':1,'role':'independent-reader','readerIdentity':IDENTITY,'actualCODEX_THREAD_ID':IDENTITY,'authorIdentity':'01a12ca5-97a5-7860-9e4a-789a3f6bdcab','independentIdentities':True,'frozenContentCommit':AUTHOR,'frozenEvidenceCommit':FROZEN,'scope':['middle-ages-dower'],'decisionOrigin':'Independent manual reading of current committed card and complete originals, not copied verdicts or automatic author PASS. Script binds manually written analysis to exact bytes.','topicWitness':{'path':TOPIC,'gitBlob':git('rev-parse',FROZEN+':'+TOPIC).decode().strip(),'sha256':sha(raw(TOPIC))},'inputReceipts':receipts,'approvedRules':{'specPath':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','specSha256':sha(Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_bytes()),'correctNote':'Useful supported definition/additional fact allowed, overlap with main explanation permitted; only bare prompt/key repetition fails.','medium':'A person familiar with topic should solve it; no obvious nonsense alternatives.','uniqueKey':'Exactly one correct answer, four distinct plausible alternatives.'},'cards':[{'questionId':card['id'],'difficulty':card['difficulty'],'correctIndex':card['correctIndex'],'currentCard':card,'cardCanonicalSha256':sha(canon(card)),'sourceVerdict':'PASS','editorialVerdict':'FIX','verdict':'FIX','fields':fields,'resolvedPriorFinding':'Old answer0 parenthetical semantic definition cue removed; verified on current literals, no remaining direct definitional cue.','remainingFindings':['Unqualified old-law scope overlaps native DOT DMF synonym Douaire; certify a single key only after narrowing source tradition or repairing the alternative.','Parallel Russian presentation of historical options and note3 needs repair without defining the answer in the options.']}],'sourceOriginals':originals,'counts':{'cardsRead':1,'fieldsRead':6,'sourcePASS':6,'sourceFIX':0,'editorialPASS':4,'editorialFIX':2,'cardPASS':0,'cardFIX':1},'protected':{'count':99,'method':'Only machine hash inventory; no substantive reread/review or certification of these cards. Content and planning untouched.','cards':protected},'history':'Previous HOLD/FIX receipts and original bytes preserved without edits; prior verdict not promoted automatically.','qaScope':{'commands':['python3 '+REL+'/bind-reader.py','python3 '+REL+'/verify-reader.py','git diff --cached --check','git show <own-evidence-commit>:<owned-path> compared byte-for-byte'],'reason':'Evidence-only change: exact provenance, per-field binding, scope preservation and Git roundtrip are affected contracts. No runtime, content, tooling route or configuration change.','fullSuite':'NotRun; not authorized or needed','build':'NotRun','deploy':'NotRun'}}
save(ROOT/'reader-receipt.json',record)
save(ROOT/'frozen-card.json',card)
print(json.dumps({'frozen':FROZEN,'cardSha':sha(canon(card)),'counts':record['counts']},indent=2))
