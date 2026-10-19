"""Bind fresh personal SOURCE29 same solecycle1 without changing judgments."""
import pathlib,importlib.util,json,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks29-cycle1-fresh';B=D/'qualified-parks29-cycle1-fresh';freeze='5da5a186e0cb0ee68c5fe538bfefa8703f317504';author='01a152ed-2493-72e0-a195-1c887878e504';A=D/'source-parks29-cycle1-fresh-canonical-context.json'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
assert A.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','b8f508463e240dc92d98b9b027be5dece63290e3:'+str(A.relative_to(C))])
context=m.read(A);assert context['sourceNativeId']==author and context['rawSourceFreeze']==freeze and context['canonicalRoot']==str(m.P)
for doc in context['canonicalDocs']:assert m.raw(pathlib.Path(doc['path']))==doc['sha256'] and doc['personallyReadSections']
for doc in context['protectedPacketFiles']:assert m.raw(pathlib.Path(doc['path']))==doc['sha256BeforeAddendum']
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');assert sp['sourceNativeId']==candidate['sourceNativeId']==ps['sourceNativeId']==author
e=candidate['entries'][0];b=e['beforeCard'];c=e['proposedCard'];assert candidate['cycle']==sp['cycle']==ps['cycle']==1
assert m.sha(b)==e['beforeHash']=='5b6558329af5fa993f6c8ab2f9ac0e7dd1fc90ba425e41975c87bc5b799ae678';assert m.sha(c)==e['afterHash']=='f2fbff276915fceb19ffde3eb5a849ec7dd36ebca7a1f2f8d55c035848b064ee'
assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex','prompt','explanation','source']) and all(b['answers'][k]==c['answers'][k] for k in [0,1,3]) and b['answers'][2]['text']==c['answers'][2]['text']
initial=m.read(D/'independent-parks29-new-initial/receipt.json');assert initial['status']=='FIX' and initial['currentCardCanonicalSHA256']==e['beforeHash'] and candidate['history'][0]['rawInitialFreeze']=='470376f19a34db24739577287e0261cdcb0c22e7'
for source in sp['rawSources']:assert m.raw(pathlib.Path(source['path']))==source['sha256'] and source['personalRead']['sourceNativeId']==author and source['personalRead']['personallyRead'] and source['personalRead']['noPriorVerdictInherited']
rows=[];cat={}
for sf in ps['globalMAIN']['fullCurrentFileInventory']:
 p=pathlib.Path(sf['path']);assert m.raw(p)==sf['rawSHA256'];t=m.read(p);assert len(t['questions'])==sf['rowCount']
 for q in t['questions']:cat[q['id']]={'topicId':t['id'],'card':q};rows.append({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']})
assert len(ps['globalMAIN']['fullCurrentFileInventory'])==110 and len(rows)==ps['globalMAIN']['rowCount']==11000 and m.sha(rows)==ps['globalMAIN']['canonicalRowsSHA256']=='dcbd37b2d6d40d7bf80cc5372679bf4e60e3d79ca427f9ebb00e22c7562d3e97'
actual={}
for p in ps['actualCurrentPeers']:
 digest=p.get('sha256',p.get('canonicalSHA256'));assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==digest;actual[p['id']]={**p,'sha256':digest}
assert len(ps['sameTopicMAIN']['all100FullCurrentPeers'])==100
for pair in ps['bilateralCurrentComparisons']:
 p=pair['currentPeer'];assert p['cardCanonicalSHA256']==actual[p['id']]['sha256'] and pair['candidateSideAssessment'] and pair['peerSideAssessment'] and pair['directReverseReason'] and not pair['directReverse'] and not pair['duplicate'] and not pair['sameEntityRelationValueContext']
# Preserve the SOURCE's reported search limitation. The known original30 input
# has precisely the already personally compared current30 MAIN; do not claim
# the SOURCE read its changed notes or that ROOT adds a semantic verdict.
propPath=D/'source-parks30-first/candidate.json';prop=m.read(propPath)['entries'][0];current30=actual[prop['id']]['card']
main=lambda q:{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']}
assert main(prop['proposedCard'])==main(current30)
ps['knownOriginal30InputPresence']={'path':str(propPath.relative_to(C)),'rawSHA256':m.raw(propPath),'rawFreeze':'4785d350eea499955eab2a84cb6fecf64f5f7f04','cardCanonicalSHA256':m.sha(prop['proposedCard']),'MAINExactSameAsPersonallyReadCurrent30':True,'existingSOURCECurrent30Assessment':next(p for p in ps['bilateralCurrentComparisons'] if p['currentPeer']['id']==prop['id']),'scope':'ROOT technical presence correction only. Original SOURCE did not report reading this separate notes/explanation version. Full current30 with identical MAIN was personally read and compared; no extra semantic or source-quality verdict is added.'}
ps['actualCurrentPeers']=list(actual.values());ps['technicalCanonicalRowShape']={'actualVerifiedRowShape':['topicId','id','prompt','answers:text[]','correctIndex'],'sourceOrder':'Peer positional metadata; excluded from this exact dcbd MAIN digest. Original descriptor preserved verbatim.'}
sp['personalCanonicalContextAddendum']={'path':str(A.relative_to(C)),'rawSHA256':m.raw(A),'freeze':'b8f508463e240dc92d98b9b027be5dece63290e3','originalAuthorAddendum':context,'operation':'Lossless author-owned canonical path correction; no original SOURCE judgment removed or changed.'}
B.mkdir(exist_ok=True)
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
concerns=['GenuineNEW29 FIRSTINITIAL FIX470376 exact5b655 solecycle1 consumed. Old52bd actual2 beforecycle1packet; fresh52ed actual0 personallyall6/4/fullNPS/globalMAIN/31bilaterals raw5da5, notinheritedoldquality. Actualcanonicalroot personalreadaddendum b8f508 resolvesoldlegacy /mindbattle-planning path NotRun; rawcritical3 unchanged. Exactf2fb changesONLYnote2, goodMAIN/4labels/key0/EASY/explanation/notes0/1/3/source preserved. This is FINAL cycle1, unresolvedHOLD0 andnoordinarycycle2/reset.', 'Independent FINAL all6literal groups/4WHOLEvariants FOURseparategrammar/plausibility/unique-key-or-distractor/noteTruthUsefulness judgments. PersonallywholeNPSsubstantive20-181 withinretained210/actualnativeprefix0-195 SHA1161d4; L31-33 stewardship enablesrecreation now/future +staffwaterquality/stewardsandcitizenstrails ownextra. Games/cycling104-117, Passportvirtualcancellations136-143 actualfromanywhere, popular/pristine46-56. Newnote2 attributeshistoricalarticle describedPassport ratherthanclaimsprogramcurrentlyavailable, contrastsarticlepositivebasis notuniversalvirtualvisitsneverhelp conservation. Check allotheruniquecrediblealternatives/absolutescope; directRussiananswerconcept explanation2sentences/note35wordlimit. AbsoluteadultEASY broadcare/recreationreason no narrowUSroute/rareterm required; no arbitrarygenre/math/template/format/crossnotebans.', 'Fresh11000MAIN no-sourceOrder digestdcbd and110filebytes, same100full+31actualclosest bothwaysspecificERVC/directreverse; current39fce6cert887 notesourceonly. Original30rawae1a9 unqualifiedpreINITIAL actualinput exists despite SOURCE searchnotfound; ROOT proves its MAIN exactlysame as fullcurrent30 personallycompared bySOURCE, doesnotpretendownauthorreadchangednotes. ReaderFINAL personallyactualunappliedwhole30 ifrelevant, nootherqualityinheritance; originalsource0credit. Generalparkstewardship->future recreation distinctfromspecifictrail/groups/trash/food/visitorflows/thresholds/resilience/remoteislands/landscapenamefacts. Onlystrictrootbindingafterapply/QA19/FINALPASS cancount887->888, alloldHOLDs retained.']
r=a.apply(B,author,[29],D/'apply-parks29-cycle1-fresh.json',D/'qa-parks29-cycle1-fresh.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='national-parks-nature']},concerns=concerns)
r.update(rawSourceFreeze=freeze,canonicalContextFreeze='b8f508463e240dc92d98b9b027be5dece63290e3',CURRENT=887,remaining=1113,fullGoal=2000,cycle=1,ordinaryCycle2=False,qualityCredit=0)
m.write(D/'qualification-parks29-cycle1-fresh.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-parks29-cycle1-fresh.json',pathlib.Path(__file__)],'Qualify fresh personal SOURCE29 solecycle1 exactnote2 and canonicalcontext without inheritedgrade'))
