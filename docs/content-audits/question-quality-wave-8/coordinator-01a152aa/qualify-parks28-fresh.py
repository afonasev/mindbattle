"""Qualify fresh native full SOURCE28 without inheriting exhausted source approval."""
import pathlib,importlib.util,json,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks28-fresh-native';B=D/'qualified-parks28-fresh';B.mkdir(exist_ok=True);freeze='65edbd33dd006d03674b20db396ab65ede4ca2ad';author='01a152bd-e34b-7243-bd49-74e543b38229'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');assert sp['sourceNativeId']==candidate['sourceNativeId']==author
e=candidate['entries'][0];b=e['beforeCard'];c=e['proposedCard'];assert m.sha(c)==e['afterHash']=='b9faf23b4d4c8b4718a7076ee1d953ac19fa25793616666deb762173bfdd448a';assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex','prompt','explanation']);assert all(b['answers'][k]==c['answers'][k] for k in [1,3])
for source in sp['rawSources']:assert m.raw(pathlib.Path(source['path']))==source['sha256'] and source['personalCurrentRead']
rows=[];cat={}
for sf in ps['globalMAIN']['files']:
 p=pathlib.Path(sf['path']);assert m.raw(p)==sf['rawSHA256'];t=m.read(p);assert len(t['questions'])==sf['rowCount']
 for n,q in enumerate(t['questions'],1):cat[q['id']]={'topicId':t['id'],'card':q};rows.append({'topicId':t['id'],'id':q['id'],'sourceOrder':n,'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']})
assert len(ps['globalMAIN']['files'])==110 and len(rows)==ps['globalMAIN']['rowCount']==11000 and m.sha(rows)==ps['globalMAIN']['canonicalRowsSHA256']
actual={}
for p in ps['sameTopicMAIN']['all100FullCurrentPeers']+ps['fullClosestCurrentPeers']:
 digest=p.get('sha256',p.get('canonicalSHA256',p.get('fullCardCanonicalSHA256')))
 assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==digest;actual[p['id']]={**p,'sha256':digest}
assert len(ps['sameTopicMAIN']['all100FullCurrentPeers'])==100
for p in ps['globalLiteralRetrievalOnlyHits']:assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==p['fullCardCanonicalSHA256'] and p['relevanceAssessment']
for pair in ps['bilateralCurrentComparisons']:assert actual[pair['peerId']]['sha256']==pair['peerFullCardSHA256'] and pair['candidateToPeer'] and pair['peerToCandidate'] and pair['directReverseAssessment']
for pair in ps['genuineProposalPairs']:
 path=pathlib.Path(pair['packetPath']);assert m.raw(path)==pair['packetRawSHA256'];entry=next(x for x in m.read(path)['entries'] if x['id']==pair['proposalId']);assert entry['proposedCard']==pair['proposalCard'] and entry['afterHash']==pair['proposalCanonicalSHA256']==m.sha(pair['proposalCard']);assert pair['candidateToQ28'] and pair['q28ToCandidate'] and pair['directReverseAssessment']
ps['actualCurrentPeers']=list(actual.values());ps['technicalNormalization']={'rawSourceDirectory':str(R.relative_to(C)),'rawSourceFreeze':freeze,'operation':'Exact SOURCE candidate/sourceproof unchanged. Lossless actual100+6closest union only; original per-pair grounds and full literal retrieval bodies preserved. Historical un-applied first37proposal1ff remains separate from actual9907; no current or SOURCE grade inherited. No source download, semantic judgment or peer body added.'}
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
concerns=['Original28 FIRSTINITIAL not yet reviewed. Old7d rawfa555 exhaustedactual2 incomplete; newnative01a152bd actual0 personallyestablishes complete6/4/full6primary contexts, not inheritedSOURCEapproval. Newexactb9faf changesonlynote0singularhighestmountain/note2Guadalquivirestuary/sourceverifieddate; originalMAIN/4labels/key3/EASY/explanation/goodnotes1+3 preserved. Oldcandidate6db80 historicalminimumproposal notfrozen.', 'Independent all6literal/4WHOLEvariants withfour separate judgments, wholeofficialLakefacts/geology, CinqueTerreofficial+UNESCO826, DonanaUNESCO685, BialowiezaUNESCO33 fullretainedscientificcontexts+actualcoverage. BialowiezaUNESCO explicitly iconicEuropeanbison/largestfree-roamingpopulation/borderPolandBelarus/oldgrowthlowlandforest; ownkeynote borderextra beyondwholeprompt/key. Otherparks true ownnotes; independently whycredible choices/uniquekey undergeneral especiallyknown prompt, no inventedabsoluteabsenceofbison. Donanaestuariumnotdelta; singularmountain sourcebound. AudienceEASY broadadult/LARGEculturalassociation must independentlyjudge actualbison-place association, songvisibilityalone notproof and no blanketpropernameban; no arbitrarymath/format/crossnoteban.', 'Authorfresh11000 fullMAIN shape includes sourceOrder (hash526e2) unlike reader rows393c withoutsourceOrder; both explicitdifferentrepresentations, all110filebytes exact. Same100fullcurrent+6closest+5literalhits; Q25sameanswerpool/notes butWindermereRomanticpoets->LakeDistrict differsfrombison->Bialowieza, bilateralERVC/directreverse. Music author/performer andMoldovaRiversdistinct, no notevsMAINban. HistoricalSOURCE37first1ff is realunappliedoldproposal, actual37now9907; SOURCE38proposal4c44 transportHOLD/unqualified notqualitycredit. ReaderfreshCURRENT/global/nearest/genuineproposals needed, onlyrootstrictbinding afterapply/QA19/INITIAL can count.']
r=a.apply(B,author,[28],D/'apply-parks28-fresh.json',D/'qa-parks28-fresh.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='national-parks-nature']},concerns=concerns)
r.update(rawSourceFreeze=freeze,sourceNativeCompactions=0,CURRENT=884,remaining=1116,fullGoal=2000,qualityCredit=0)
m.write(D/'qualification-parks28-fresh.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-parks28-fresh.json',pathlib.Path(__file__)],'Qualify fresh personal native0 SOURCE28 all6/4 currentglobal and minimalnotes'))
