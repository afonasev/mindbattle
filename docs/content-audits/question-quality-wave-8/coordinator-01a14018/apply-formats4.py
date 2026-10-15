"""Compose existing SOURCE evidence containers, then apply exact four proposals."""
import pathlib,json,importlib.util,copy
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books51-70-01a14018/author/source-completion';F=A/'qualification-completion4';B=D/'qualified-formats4';B.mkdir(exist_ok=True)
candidate=m.read(A/'candidate.json');candidate['entries']=[e for e in candidate['entries'] if e['sourceOrder'] in [65,66,67,68]]
assert len(candidate['entries'])==4
proof=m.read(A/'sourceproof.json');proof['entries']=[e for e in proof['entries'] if e['sourceOrder'] in [65,66,67,68]]
supp=m.read(F/'sourceproof.json');peer=m.read(F/'peer-snapshot.json');items={e['id']:e for e in supp['items']};cards={e['id']:e for e in candidate['entries']};pathByName={pathlib.Path(x['path']).name:str(pathlib.Path(x['path']).relative_to(C)) for x in proof['rawSources']}
def normpath(p):
 pp=pathlib.Path(p)
 if pp.is_absolute():return str(pp.relative_to(C))
 if (C/pp).is_file():return str(pp)
 assert pp.name in pathByName,p
 return pathByName[pp.name]
for raw in proof['rawSources']:
 raw['path']=normpath(raw['path']);assert m.raw(C/raw['path'])==raw['sha256']==supp['sourceHashes'][pathlib.Path(raw['path']).name]
 if raw.get('readPath'):assert m.raw(pathlib.Path(raw['readPath']))==raw['readTextSHA256']
for e in proof['entries']:
 c=cards[e['id']]['proposedCard'];q=items[e['id']];assert q['prompt']==c['prompt'] and q['proposedCardHash']==m.sha(c)
 assert len(q['variantAssessments'])==4
 for g in e['literalGroups']:g['sourcePaths']=[normpath(p) for p in g['sourcePaths']]
 for v in e['fourFullPromptAnswerNoteAssessments']:
  k=v['slot'];extra=next(x for x in q['variantAssessments'] if x['answerIndex']==k);tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']}
  assert extra['answer']==tr['answer'] and extra['note']==tr['note'] and extra['isKey']==(k==c['correctIndex'])
  assert m.sha(tr)==extra['variantTripleSHA256']==v['tripleSHA256']
  v['originalAuthorAssessment']=copy.deepcopy({x:v[x] for x in ['plausibilityUniqueKeyAndNoteTruthUsefulness','locator','sourcePaths']})
  v['plausibilityUniqueKeyAndNoteTruthUsefulness']=extra['variantGround']+'\n'+extra['promptAndNoteAssessment']
  v['sourcePaths']=list(dict.fromkeys([normpath(p) for p in v['sourcePaths']]+[normpath(extra['sourcePath'])]))
  v['locator']=v['locator']+'; individual qualification: '+extra['locator']
  v['technicalComposition']='Verbatim SOURCE completion grounds composed into standard original variant container; no new root semantic judgment.'
 e['correctNoteNewFact']['sourcePaths']=[normpath(p) for p in e['correctNoteNewFact']['sourcePaths']]
actual=[]
for p in peer['sameTopicSnapshot']['cards']:actual.append({'id':p['id'],'topicId':'books-publishing','sourceOrder':p['index']+1,'card':p['card'],'sha256':p['sha256']})
for p in peer['crossTopicRetrieval']['hits']:actual.append({'id':p['id'],'topicId':p['topicId'],'sourceOrder':p['index']+1,'card':p['card'],'sha256':p['sha256'],'retrievalDisposition':p['retrievalDisposition'],'dispositionReason':p['dispositionReason']})
cat={}
for t in {x['topicId'] for x in actual}:cat.update({q['id']:q for q in m.read(C/f'src/content/topics/{t}.json')['questions']})
for p in actual:assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
for p in peer['targetProposals']:assert p['proposedCard']==cards[p['id']]['proposedCard'] and m.sha(p['proposedCard'])==p['afterHash']
assert len(peer['meaningfulPairgrounds'])==11
for p in peer['meaningfulPairgrounds']:assert p['a'] in cards and p['b'] in (set(cards)|set(cat)) and p['ground']
peer['actualCurrentPeers']=actual;peer['sourceCompletionPath']=str(F.relative_to(C));peer['rootTechnicalComposition']='Only standard snapshot container/path aliases; SOURCE fullcards/grounds retained verbatim. Incidental token hits remain explicitly non-relevant.'
m.write(B/'candidate.json',candidate);m.write(B/'sourceproof.json',proof);m.write(B/'peer-snapshot.json',peer)
same={'actualCurrentPeers':[p for p in actual if p['topicId']=='books-publishing']}
qualified=m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[65,66,67,68],None,None,None,qualifyOnly=True,peerSnapshot=same)
m.write(D/'qualification-formats4.json',{'stage':'SOURCE_QUALIFIED_NOT_INDEPENDENT_CERTIFIED','sourceCandidate':str((A/'candidate.json').relative_to(C)),'sourceQualificationCompletion':str(F.relative_to(C)),'technicalComposition':'Exact original six groups/extra/level plus verbatim source qualification sixteen individual variant grounds, normalized path aliases; all card/group/triple/source/actualpeer hashes verified. No semantic ground authored by root.','verified':{'cards':4,'literalGroups':24,'individualVariants':16,'actualPeers':len(actual),'meaningfulPairs':11,'crossTopicHits':len(peer['crossTopicRetrieval']['hits'])},'qualification':qualified,'qualityCredit':0})
m.apply(B,'01a1402b-4c6a-7453-8992-25b45d34795e',[65,66,67,68],D/'apply-formats4.json',D/'qa-formats4.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['SOURCE4 format layout/accessibility/historical file class; full official primary bodies retained; personally read W3C/Adobe756pagePDF relevant complete sections,DAISYarticle,Kindle89pageguide relevant sections.','Independent must personally judge fullCURRENT6/4, ONEkey/actualMEDIUM/plausibility/notes/ownextra/precise sources. Preserve EPUB fixed-layout and PDF TaggedPDF optionalreflow, DAISY noaudio and historicKindleDRM conditions.','SOURCE qualification completion4 supplies sixteen option-specific grounds and global110topic retrieval with109fullcurrentcards,11meaningful selected pairs. Explicitly assess relevant computer Adobe-origin neighbor; wrongnote canonical reuse allowed.','Original SOURCE31-50 sixteen drafts remain UNQUALIFIED/UNAPPLIED; first5 proof/text correction pending. Do not certify proposal or same-topic token matching alone.'])
