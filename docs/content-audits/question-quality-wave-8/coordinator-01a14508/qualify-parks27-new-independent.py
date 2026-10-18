"""Qualify genuineNEW27 SOURCE after originalgradeHOLD; no quality credit."""
import pathlib,json,re,subprocess,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks27-new-independent';B=D/'qualified-parks27-new-independent';B.mkdir(exist_ok=True);freeze='1e40f8549f22dd42b937179c581696260edad0fe';author='01a1457d-f536-73e0-b097-d540eda34b25';counts={}
for u,date in [(m.O,'16'),(author,'16'),('01a150d1-3383-7d30-ad23-76d70ec18813','19')]:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+u+'.jsonl'));counts[u]=sum(json.loads(l).get('type')=='compacted' for l in j.open());assert counts[u]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
rawCandidate=m.read(R/'candidate.json');entry=rawCandidate['scope'];assert entry['afterHash']=='e67af598d39ce43ffd68f73e1b5f326bf762e0c6ae021d4badbf15c31e0ac53d';candidate={**rawCandidate,'entries':[entry]};sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');g=m.read(R/'global-search.json');assert rawCandidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==author
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);assert m.raw(p)==source['sha256']
 if 'nps.gov' not in source['url']:
  assert source['role'] and source['provenance'];continue # retained historical original27 source, notnewclaimproof
 body=p.read_text();assert {int(n) for n in re.findall(r'\bL([0-9]+):',body)}==set(range(210));pr=source['captureReadProvenance'];native=pathlib.Path(pr['nativeOpenOutput']);assert m.raw(native)==pr['nativeOpenOutputSHA256'];nr=m.read(native)['originalRecord']['payload']['output'];text='\n'.join(v.get('text','') for v in nr);assert body[body.index('L0:'):body.index('L196:')]==text[text.index('L0:'):text.index('L196:')]
cat={}
for p in (C/'src/content/topics').glob('*.json'):
 t=m.read(p)
 for n,c in enumerate(t['questions'],1):cat[c['id']]={'topicId':t['id'],'sourceOrder':n,'card':c}
actual={}
for p in ps['actualCurrentPeers']+ps['fullRelevantCurrentPeers']:
 assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==p['sha256']
 if p['id'] in actual:assert actual[p['id']]['card']==p['card']
 actual[p['id']]=p
read=ps['sameTopicMAINRead'];assert read['count']==len(read['currentPeers'])==100 and m.raw(pathlib.Path(read['path']))==read['rawSHA256'];assert all(r['card']==actual[r['id']]['card'] and m.sha(r['card'])==r['sha256'] for r in read['currentPeers'])
proposals={p['id']:p for p in ps['latestGenuineProposals']}
for p in proposals.values():
 f=pathlib.Path(p['originalCandidatePath']);assert m.raw(f)==p['originalCandidateFileSHA256'];e=next(e for e in m.read(f)['entries'] if e['id']==p['id']);assert e['proposedCard']==p['card'] and e['afterHash']==p['sha256']==m.sha(p['card'])
for pair in ps['bilateralComparisons']:
 p=actual[pair['id']] if pair['kind']=='CURRENT_MAIN' else proposals[pair['id']];assert pair['peerCard']==p['card'] and pair['peerCardSHA256']==p['sha256'];assert all(pair[k] for k in ['candidateToPeer','peerToCandidate','directReverseAssessment']);assert set(pair['candidateERVC'])==set(pair['peerERVC'])=={'entity','relation','value','context'}
base=pathlib.Path(g['base']['path']);assert m.raw(base)==g['base']['rawSHA256'];rows=m.read(base)['cards'];deltaPath,frag=g['delta']['path'].split('#');assert m.raw(pathlib.Path(deltaPath))==g['delta']['snapshotRawSHA256'];dd=m.read(pathlib.Path(deltaPath));
for key in frag.split('.'):dd=dd[key]
overrides={r['id']:r for r in dd};assert len(dd)==14;parks=m.read(pathlib.Path(g['parksOverlay']['path']));assert m.raw(pathlib.Path(g['parksOverlay']['path']))==g['parksOverlay']['rawSHA256']
def main(tid,c):return {'topicId':tid,'id':c['id'],'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']}
for c in parks['questions']:overrides[c['id']]=main(parks['id'],c)
polarBytes=subprocess.check_output(['git','-C',str(C),'show','0d0e115bac0d5a943033fad542a0288f35888603:src/content/topics/polar-regions.json']);import hashlib;assert hashlib.sha256(polarBytes).hexdigest()==g['polarRows']['rawSHA256'];polar=json.loads(polarBytes)
for c in polar['questions']:overrides[c['id']]=main(polar['id'],c)
sourceRows=[overrides.get(r['id'],r) for r in rows];assert len(sourceRows)==11000 and m.sha(sourceRows)==g['canonicalRowsSHA256']=='605913965bd3a84d1c80f448ad7ecc0a273a590954d2eade29c03c6ece53fe3c'
changes=[];currentRows=[]
for old in sourceRows:
 c=cat[old['id']];now=main(c['topicId'],c['card']);currentRows.append(now)
 if old!=now:
  assert old['id'] in ['polar-regions-aurora-charged-particles','polar-regions-permafrost-frozen-ground'];changes.append({'id':old['id'],'SOURCEreadMAIN':old,'actualMAIN':now,'actualFullCard':c['card'],'actualFullCardSHA256':m.sha(c['card'])})
assert len(changes)==2
queries=g['queries'];hits=lambda rr:{r['id'] for r in rr if any(re.search(q,json.dumps(r,ensure_ascii=False),re.I) for q in queries)};assert hits(sourceRows)==hits(currentRows)
ps['actualCurrentPeers']=list(actual.values());ps['ROOTPostSOURCEKnownPolarPromotion']={'SOURCEcanonicalRowsSHA256':g['canonicalRowsSHA256'],'ROOTcurrentCanonicalRowsSHA256':m.sha(currentRows),'changedRows':changes,'ROOTapplyCommit':'11abc1d3e6f155edc3f2ac27c6fdca8fb56845d2','retrievalHitSetUnchangedForAllOriginalQueries':True,'scope':'Exactly2laterROOTpolarpostimages afterSOURCE27snapshot; fullauthorSOURCE27MAINbaseline unchanged, no newgroup/visitor/policyretrievalhit. ROOTtechnicalscope reconciliation notSOURCEclaimtohavepersonallyread laterpostimages. Bothpolarpostimages independentlycertified19562; independent27INITIAL mustfreshCURRENTglobal.'}
for n,x in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
concerns=['GenuinelyNEW27 afterORIGINALSOURCEgradeHOLD5e6 Doñananame/birdmigration atfrozenEASY; originalneverINITIAL/FINAL, originalminimal2b7UNAPPLIED. Actualbeforef132 preserved, newe67 group-sizeorganizationpolicy distinctsourcefact, notrarecluereskin/gradechange/reset. FrozenEASY/key2/topic/order; all6literal4WHOLEvariants/fullprimary/credible4/unique/naturalgrammar/taxonomy/absoluteadultLARGEculturalbasis independentlyrequired.', 'NPScompletecanonical210/nativebyteexact0-195 includescompletearticle20-181; footerunverifiedunused. L38-43planAheadsmallgroups/splitlargecompanieswhenpossible, plusL50-53populartrail/singlefile qualifier. Correctnoteadds recommendationbelongsnamedPrinciple1 PlanAheadAndPrepare beyondwholeprompt/key; independently isthisconcreteusefulownfact versusmerecitation/bookkeepinglabel? Do notinvent a blanketclassification-note ban, but newfactmeaningmustbeassessed. Notes0/1 restatecontrastwithsplitpolicy—assessowntruth/usefulness notautomaticallyencyclopedictriviarequired.', 'All4parallelcredibleorganizationalchoices? Keeponegroup /joinanother /split /spreadacrosstrailwidth; slot3mightbeobviouslyunsuitable/lessparallel ornotecontextpopulartraitnotinprompt. FullpromptgeneralNPSadvice andmodalwhenpossiblekey mustyielduniqueanswerwithoutsmuggledpopularcondition. Prior26FINALHOLD0 poorgrammar/distractorcase separate; do notborrowHOLD orPASS, do notmerelycountsameformatasdefect.', 'SOURCEfull11kMAIN605913 baseline+14delta+100actualparks+100SOURCEpolar snapshot, exactrawhashes reconstructed; SOURCEsnapshotpreceded2laterROOTpolar34/35postimages, ROOTexplicit2rowreconciliation withunchangedallqueryhits/no newvisitor-groupduplicate, bothpolarpostimages independentlycertified19562; sourceall101actualfullbodies+10closest/14bilateral+4genuineproposalbody/sourcefilehashes live. IndependentINITIALfreshGLOBAL/same100MAIN/fullclosestwholebodies/proposals BOTHdirectionsERVC/directreverse. Source1raw1e40pre2/root1/freshreader0/exactaffected19 beforequalitycredit. OneSOURCEfixafterfutureFIRSTINITIAL thenFINAL/unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,author,[27],D/'apply-parks27-new-independent.json',D/'qa-parks27-new-independent.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(sourceRawFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(actual),SOURCEglobalRowsSHA256=g['canonicalRowsSHA256'],ROOTpostSnapshotReconciliation=ps['ROOTPostSOURCEKnownPolarPromotion'],qualityCredit=0)
m.write(D/'qualification-parks27-new-independent.json',r);m.write(B/'normalization-provenance.json',{'owner':m.O,'sourceOriginalPath':str(R.relative_to(C)),'sourceRawFreeze':freeze,'operation':'ExactSOURCEscope wrappedasentries only; originalscope/history retained. Exactsourceproof unchanged. Unionexistingauthoractualfullbodies sameid/hash. ROOTexplicitlater2polarpostimage metadatareconciliation preservesSOURCEold11kbaseline/queries anddoesnotinvent SOURCEreadjudgment; allqueryhitsetsunchanged, independentCURRENTreviewrequired. CanonicalNPSraw reusednofilecopy.','qualityCredit':0});print(m.savecode(list(B.glob('*.json'))+[D/'qualification-parks27-new-independent.json',pathlib.Path(__file__)],'Qualify genuineNEW27 exactsource all6-4 primary livepeers preservingoriginalhold'))
