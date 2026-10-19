"""Qualify genuineNEW29 full source plus author-owned concrete peer completion."""
import pathlib,importlib.util,json,subprocess,hashlib
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks29-new-complete';B=D/'qualified-parks29-new';B.mkdir(exist_ok=True);freeze='60a6b92dcba8f3f0a712f2f9818de01116a9658a';author='01a152bd-e34b-7243-bd49-74e543b38229';A=D/'source-parks29-new-peer-complete/peer-completion.json'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
assert A.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','9e616fa65331b6904b6f0df990d5c45c19e600a5:'+str(A.relative_to(C))])
add=m.read(A)
for ref in add['baseReferences']:assert m.raw(pathlib.Path(ref['path']))==ref['sha256']
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');assert sp['sourceNativeId']==candidate['sourceNativeId']==add['sourceNativeId']==author
e=candidate['entries'][0];b=e['beforeCard'];c=e['proposedCard'];assert m.sha(c)==e['afterHash']=='5b6558329af5fa993f6c8ab2f9ac0e7dd1fc90ba425e41975c87bc5b799ae678';assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex'])
triple_aliases=[]
for variant in sp['entries'][0]['fourFullPromptAnswerNoteAssessments']:
 legacy={'fullPrompt':variant['fullPrompt'],'answer':variant['answer'],'note':variant['note']}
 assert variant['tripleSHA256']==m.sha(legacy)
 canonical={'prompt':variant['fullPrompt'],'answer':variant['answer'],'note':variant['note']}
 triple_aliases.append({'slot':variant['slot'],'originalFullPromptKeySHA256':variant['tripleSHA256'],'canonicalPromptKeySHA256':m.sha(canonical)})
 variant['originalFullPromptKeyTripleSHA256']=variant['tripleSHA256'];variant['tripleSHA256']=m.sha(canonical)
sp['technicalHashNormalization']={'operation':'Exact author triple strings unchanged. All four original hashes proven to be compact sorted JSON of {fullPrompt,answer,note}; protocol canonical hash uses {prompt,answer,note}. Original hashes preserved, canonical hashes recomputed mechanically; no semantic judgment added and core checks unchanged.','bindings':triple_aliases,'rawSourceFreeze':freeze}
for source in sp['rawSources']:assert m.raw(pathlib.Path(source['path']))==source['sha256'] and source['personalRead']
rows=[];cat={};drift=[]
for sf in ps['globalMAIN']['files']:
 p=pathlib.Path(sf['path']);t=m.read(p)
 if m.raw(p)!=sf['rawSHA256']:
  assert t['id']=='polar-regions';oldbytes=subprocess.check_output(['git','-C',str(C),'show','145c49fd1f207c524b1da2a97ccdd63b9e6a598f:src/content/topics/polar-regions.json']);assert hashlib.sha256(oldbytes).hexdigest()==sf['rawSHA256'];old=json.loads(oldbytes);changes=[(x,y) for x,y in zip(old['questions'],t['questions']) if x!=y];app=m.read(D/'apply-polar38-complete.json')['applied'][0];assert changes==[(app['beforeCard'],app['proposedCard'])];assert all(app['beforeCard'][k]==app['proposedCard'][k] for k in ['id','difficulty','correctIndex','prompt','explanation']);assert [x['text'] for x in app['beforeCard']['answers']]==[x['text'] for x in app['proposedCard']['answers']]
  drift.append({'path':str(p.relative_to(C)),'historicalSOURCEFileSHA256':sf['rawSHA256'],'currentFileSHA256':m.raw(p),'onlyChange':'Exact38 correctnote/source postimage ac70bd; allMAINunchanged. Historical snapshot metadata not labeledcurrent.'})
 for n,q in enumerate(t['questions'],1):cat[q['id']]={'topicId':t['id'],'card':q};rows.append({'topicId':t['id'],'id':q['id'],'sourceOrder':n,'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']})
assert len(ps['globalMAIN']['files'])==110 and len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['canonicalRowsSHA256']==add['globalSearch']['canonicalRowsSHA256']
closest={p['id']:p for p in ps['fullClosestCurrentPeers']}
comparisons=[]
for pair in add['bilateralCurrentComparisons']:
 assert pair['peerFullCard']==closest[pair['peerId']]['card'] and m.sha(pair['peerFullCard'])==pair['peerFullCardSHA256'];comparisons.append(pair)
for pair in add['globalSemanticConservationComparisons']:
 assert pair['peerFullCard']==cat[pair['id']]['card'] and m.sha(pair['peerFullCard'])==pair['peerFullCardSHA256'];closest[pair['id']]={'id':pair['id'],'topicId':pair['topicId'],'sourceOrder':pair['sourceOrder'],'card':pair['peerFullCard'],'sha256':pair['peerFullCardSHA256']};comparisons.append({**pair,'peerId':pair['id']})
actual={}
for p in ps['sameTopicMAIN']['all100FullCurrentPeers']+list(closest.values()):
 digest=p.get('sha256',p.get('canonicalSHA256'));assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==digest;actual[p['id']]={**p,'sha256':digest}
assert len(ps['sameTopicMAIN']['all100FullCurrentPeers'])==100 and len(comparisons)==26
for pair in comparisons:
 assert actual[pair['peerId']]['sha256']==pair['peerFullCardSHA256'];assert pair['candidateToPeer'] and pair['peerToCandidate'] and pair['directReverseAssessment'];assert set(pair['peerERVC'])==set(pair['candidateERVC'])=={'entity','relation','value','context'}
for pair in add['genuineProposalPairs']:
 p=pathlib.Path(pair['packetPath']);assert m.raw(p)==pair['packetRawSHA256'];entry=next(x for x in m.read(p)['entries'] if x['id']==pair['proposalId']);assert entry['proposedCard']==pair['proposalCard'] and m.sha(pair['proposalCard'])==entry['afterHash']==pair['proposalCanonicalSHA256'];assert pair['candidateToProposal'] and pair['proposalToCandidate'] and pair['directReverseAssessment']
ps.update(actualCurrentPeers=list(actual.values()),fullClosestCurrentPeers=list(closest.values()),bilateralCurrentComparisons=comparisons,genuineProposalPairs=add['genuineProposalPairs'],ROOTPostSOURCEFileOnlyChanges=drift,authorPersonalPeerCompletion={'path':str(A.relative_to(C)),'rawSHA256':m.raw(A),'rawFreeze':'9e616fa65331b6904b6f0df990d5c45c19e600a5','operation':'Exact author-owned22+4 meaningfulbilateral/fullbody evidence replaces generic scaffold; basecandidate/sourceproof unchanged. NoROOTsemanticjudgmentsadded.'})
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
concerns=['GenuineNEW29 SOURCE afteroriginalTheNarrows->Zion absoluteEASY SOURCEHOLD937a51/cb6cd; thosehistoryrawretained/unapplied/noINITIAL ever29. Newfullmutabletextsolution5b655 conservesfrozenID/topic/order/EASY/key0, meaningchangedtoNPSstewardship->present/futurerecreation. Completepersonalnative01a152bd1 rawsource60a6 +ownconcretepeer9e616 combinedlosslessly; no inheritedold7d orrawgradeverdict. No INITIALfixcycle consumed.', 'Independent6literal/4WHOLEvariants fourseparate judgments/fullNPSarticle20-181 insidecanonical210nativeprefix0-195byteexact. Allclaimswholeprimary: stewardship/trails/citizens/waterquality31-33, popular/pristine46-56, actualrecreationgames/cycling101-117/158-160, virtualPassport136-143. Correctnote ownextra stewards/citizens contribution totrails beyondbroadcareprompt/key; overlapexplanationallowed. Key0generalcare vsentertainment/virtualsubstitution/equippedsitesonly independentlyjudgeunique/credible/plausible/parallel/naturalRussian/noteowntruthusefulness, no universalvirtualvisitsneverhelp/onlyoneparkusepolicy invented. Explanation stewardship termtranslatedascare anddirectanswernaming/2sentence/bounds required. AbsoluteadultEASY broadconservationreason editorinference notsurveyorUSrouteknowledge; no arbitrarymath/genre/format/crossnoteban.', 'Fresh11000MAIN sourceOrder-includedhash526e2/same100/currentfull26nearby and26authorconcretebidirectionalERVC/directreverse. Broadparkcareenablesfuture recreation distinctfromanimalfood9/firefuel14/foundobjects15/firepit16/dogwaste17/leash18/closure20/bootseeds22/dishes24/trailcourtesy26/groups27/siteidentities/tourismrefill/staytrail/trash; crossprotected-area label/nativegarden/corridor/remoteisland96 differentmechanisms/relations, notgenericcontext-onlyclaim. Historical38file note/sourceonly transition verified noMAINchange, actual38cert4c44. RealSOURCE39unappliedfce6 literalbody comparedbothways only; its SOURCEproofslot0/1 alignmentpending/no39qualityapproval. ReaderfreshCURRENTglobal/nearest/proposals required. Onlyrootstrictbinding afterapply/QA19/independentINITIAL cancount; oldHOLDs retained.']
r=a.apply(B,author,[29],D/'apply-parks29-new.json',D/'qa-parks29-new.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(rawSourceFreeze=freeze,rawPeerCompletionFreeze='9e616fa65331b6904b6f0df990d5c45c19e600a5',sourceNativeCompactions=1,qualityCredit=0,CURRENT=886,remaining=1114,fullGoal=2000,ROOTPostSOURCEFileOnlyChanges=drift)
m.write(D/'qualification-parks29-new.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-parks29-new.json',pathlib.Path(__file__)],'Qualify genuineNEW29 wholeSOURCE and meaningful26peer fullbindings no originalgradeinheritance'))
