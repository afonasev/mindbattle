"""Sequential exact apply SOURCE10 then SOURCE3; no QA until both apply succeed."""
import pathlib,json,hashlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('ap',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
B=D/'normalized-books11-20-initial';S=C/'docs/content-audits/question-quality-wave-8/process-v2-books-titlepage3-newprimary-01a13f31/author/finalpacket';cand=rd(B/'candidate.json');c3=rd(S/'candidate.json')['entries'][0];a3=rd(S/'simultaneous-books11-20-addendum.json');a10=rd(C/'docs/content-audits/question-quality-wave-8/process-v2-books11-20-01a13f31/author/initial-source-completion/cross-proposed-titlepage3.json')
assert a3['source3FinalCard']==c3['proposedCard'] and a3['source3FinalCanonicalSHA256']==sha(c3['proposedCard'])
props={e['id']:e for e in a3['finalProposals11to20']}
for e in cand['entries']:assert props[e['id']]['card']==e['proposedCard'] and props[e['id']]['canonicalSHA256']==e['afterHash']
# Author10 compared SOURCE3 before its solely note/verso wording correction.
cross3=a10['titlepage3'];crosscard=cross3['card'] if 'card' in cross3 else cross3['proposedCard'];main=lambda q:{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']};assert main(crosscard)==main(c3['proposedCard'])
ps=rd(B/'peer-snapshot.json');catalog={}
for t in {p['topicId'] for p in ps['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in ps['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['sha256']
m.apply(B,'01a13f93-17b0-7893-8955-26059d806d41',list(range(11,21)),D/'apply-books10-initial.json',D/'qa-books11-combined.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='books-publishing']},concerns=['Exact finalversions only:12base;11/13/14finaladdendum;15/16fullstandardfinal15-16;17–20printing. All originalhistoryretained.','FreshINITIALmustjudge actualadultMEDIUM andplausibility, fullsources+notes, entity/relation/value/context acrossallrelevantCURRENTcrosscatalog, especially crafts-perfect-glue16finishingresult and15case-laminatevsjacketed sourcecondition.','SOURCE3versocorrected MAIN hash equalauthor10 personallycompared SOURCE3v1; SOURCE3authorpersonallyreadall10latestfullproposals. Source3 FINAL andthese10INITIAL areseparatestages.'])
current={q['id']:q for q in rd(C/'src/content/topics/books-publishing.json')['questions']};delta=[]
for e in a3['finalProposals11to20']:
 assert e['card']==current[e['id']] and sha(e['card'])==e['canonicalSHA256'];delta.append({'id':e['id'],'topicId':'books-publishing','sourceOrder':e['sourceOrder'],'card':e['card'],'sha256':e['canonicalSHA256']})
dp=D/'SOURCE3-actual-current10-peer-state-delta.json';wr(dp,{'actualCurrentPeers':delta,'sourceAuthorPersonalRead':str((S/'simultaneous-books11-20-addendum.json').relative_to(C)),'meaning':'Exactsame fullcards personallyreadasNOTCURRENT proposalsnowapplied; state/path metadata rebind only, no newsemanticgrounds.'})
sp=rd(S/'peer-snapshot.json');othercat={}
for t in {p['topicId'] for p in sp['actualCurrentPeers']}:othercat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
dm={e['id']:e for e in delta}
for p in sp['actualCurrentPeers']:
 p=dm.get(p['id'],p);assert p['card']==othercat[p['id']] and sha(p['card'])==p['sha256']
m.apply(S,'01a13f98-8be4-7fd3-a70f-dc0ea9b54b27',[3],D/'apply-books3-newprimary.json',D/'qa-books11-combined.json',pathlib.Path(__file__),peerAddendum=dp,peerSnapshot={'actualCurrentPeers':[p for p in sp['actualCurrentPeers'] if p['topicId']=='books-publishing']},concerns=['GenuinenewPeaceCorps primarysolution afterSOURCEHOLD3; originalindependentINITIALFIX thenSOURCEcycle1HOLD, nowconcrete newsource notunchangedautomaticcycle2. PerentryreviewstageFINAL.','Verso relationcorrectedtoafter/onreverse, notsimultaneousleft-facingpage; primary usually/traditionally limits retained. Owncorrectnote relationmustaddownfact beyondprompt+key.','FreshMAIN actualnew11–20 plusanime-tobira culturalterm mustbedistinguished personally, canonicalwrongnotesallowed.'])
