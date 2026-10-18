"""Qualify soleSOURCEcycle1 onlyslot3 repair; retain allINITIAL/sourcegradeHOLDhistory."""
import pathlib,json,re,subprocess,importlib.util,hashlib
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks27-new-cycle1';B=D/'qualified-parks27-cycle1';B.mkdir(exist_ok=True);freeze='9d8d4efe2d84fbfd8729964a1e0045a112aea0f6';author='01a1457d-f536-73e0-b097-d540eda34b25';counts={}
for u,date in [(m.O,'16'),(author,'16'),('01a150d1-3383-7d30-ad23-76d70ec18813','19')]:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+u+'.jsonl'));counts[u]=sum(json.loads(l).get('type')=='compacted' for l in j.open());assert counts[u]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');e=candidate['entries'][0];assert candidate['scope']==e and e['afterHash']=='3e0fbc22db5d2d7f050000aa06e07c2fc3ddfcd1c3cf090cbb6f6b78c83f62b7';b=e['beforeCard'];c=e['proposedCard'];assert e['beforeHash']=='e67af598d39ce43ffd68f73e1b5f326bf762e0c6ae021d4badbf15c31e0ac53d';assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex','prompt','explanation','source']);assert all(b['answers'][k]==c['answers'][k] for k in [0,1,2]);assert b['answers'][3]!=c['answers'][3]
for s in sp['rawSources']:
 p=pathlib.Path(s['path']);assert m.raw(p)==s['sha256']
 if 'nps.gov' in s['url']:
  body=p.read_text();assert {int(n) for n in re.findall('L([0-9]+):',body)}==set(range(210));pr=s['captureReadProvenance'];f=pathlib.Path(pr['nativeOpenOutput']);assert m.raw(f)==pr['nativeOpenOutputSHA256'];nr=m.read(f)['originalRecord']['payload']['output'];nt='\n'.join(x.get('text','') for x in nr);assert body[body.index('L0:'):body.index('L196:')]==nt[nt.index('L0:'):nt.index('L196:')]
 else:assert s['role']=='Original 027 source HOLD history only; not used to ground the new candidate'
cat={};rows=[];fileDrift=[]
for sf in ps['globalMAIN']['sourceFiles']:
 p=pathlib.Path(sf['path']);topic=m.read(p)
 if m.raw(p)!=sf['rawSHA256']:
  assert topic['id']=='polar-regions';oldBytes=subprocess.check_output(['git','-C',str(C),'show','11abc1d3e6f155edc3f2ac27c6fdca8fb56845d2:src/content/topics/polar-regions.json']);assert hashlib.sha256(oldBytes).hexdigest()==sf['rawSHA256'];old=json.loads(oldBytes);changed=[]
  for x,y in zip(old['questions'],topic['questions']):
   if x!=y:
    assert x['id']==y['id']=='polar-regions-amery-east-antarctica';assert all(x[k]==y[k] for k in ['id','difficulty','correctIndex','prompt','explanation','source']);assert all(x['answers'][k]==y['answers'][k] for k in [0,1,3]);assert x['answers'][2]['text']==y['answers'][2]['text'];assert m.sha(y)=='7f68c0c2efb27de276ce3f1d748887fbac8e5bb9007baa9934a0ae54d2727769';changed.append(x['id'])
  assert changed==['polar-regions-amery-east-antarctica'];fileDrift.append({'path':str(p.relative_to(C)),'SOURCEsnapshotRawSHA256':sf['rawSHA256'],'currentRawSHA256':m.raw(p),'noteOnly36Change':'ROOT172940 onlynote2, noMASTER MAINdiff','scope':'HistoricalSOURCEfilehash retained; currentMAINprojection all11000exact checked below, actualclosestbodyhashes unchanged.'})
 for n,q in enumerate(topic['questions'],1):cat[q['id']]={'topicId':topic['id'],'sourceOrder':n,'card':q};rows.append({'topicId':topic['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']})
assert len(ps['globalMAIN']['sourceFiles'])==110 and len(rows)==ps['globalMAIN']['cardCount']==11000 and m.sha(rows)==ps['globalMAIN']['canonicalRowsSHA256']=='1be7210a3432364e7dc416d608e800aa3ffce1b5caed6b0649e4b0636c0f8f73'
actual={}
for p in ps['sameTopicMAIN']['actualCurrentPeers']+ps['fullClosestActualPeers']:
 assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==p['sha256']
 if p['id'] in actual:assert p['card']==actual[p['id']]['card']
 actual[p['id']]=p
assert ps['sameTopicMAIN']['count']==len(ps['sameTopicMAIN']['actualCurrentPeers'])==100
for p in ps['bilateralCurrentPairs']+ps['genuineProposalPairs']:
 assert p['candidateCard']==c and p['candidateFullCardSHA256']==m.sha(c);assert m.sha(p['peerCard'])==p['peerFullCardSHA256'];f=pathlib.Path(p['peerSourcePath'])
 if m.raw(f)!=p['peerSourceRawSHA256']:
  assert f==C/'src/content/topics/polar-regions.json';historical=subprocess.check_output(['git','-C',str(C),'show','11abc1d3e6f155edc3f2ac27c6fdca8fb56845d2:src/content/topics/polar-regions.json']);assert hashlib.sha256(historical).hexdigest()==p['peerSourceRawSHA256'];assert next(q for q in json.loads(historical)['questions'] if q['id']==p['peerId'])==p['peerCard']==cat[p['peerId']]['card']
 assert p['candidateToPeer'] and p['peerToCandidate'] and p['directReverse']
 if p in ps['bilateralCurrentPairs']:assert p['peerCard']==cat[p['peerId']]['card']
 else:
  data=m.read(f);entry=next(v for v in data['entries'] if v['id']==p['peerId']);assert entry['proposedCard']==p['peerCard'] and entry['afterHash']==p['peerFullCardSHA256']
ps['actualCurrentPeers']=list(actual.values());ps['ROOTPostSOURCEFileOnlyChange']={'differences':fileDrift,'all11000MAINRowsStillByteCanonicalEqualSOURCEHash':True,'noActualClosestPeerBodyDrift':True,'noSOURCEnewReadJudgmentsInvented':True}
for n,doc in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,doc)
concerns=['SOLE SOURCEcycle1 aftergenuine27FIRSTINITIALFIX65e54/ROOTconsume8c7f315. ChangesONLYslot3text/note: newaction splitscompanyinto2groups thatremainlarge; oldwidth-walking/duplicatewholegroup0 removed. Main/good0,1/key2/EASY/PlanAheadcorrectnote/explanation/source untouched. ReaderFIRSTINITIALconfirmedclassificationnoteadditionalfact; do notgratuitouslyreplaceorbannoteclass. OriginalDoñanaSOURCEgradeHOLD5e6 andnewindependentfacthistory preserved, notnewINITIAL/cycle2/reset.', 'Independent FINAL needsall6literal4WHOLEvariants/absoluteadultEASY/4credibleparallelunique/grammar/taxonomy/ownnoteextra; isnew3meaningfuldistinctcompromise versuskey? FULLNPSL43 says visitinsmallgroupswhenpossible andconsidersplittinglargerintosmallergroups. Do notinventnumericalmaximum/two-groupsban, oracceptuniquenessmerelybecauseslot3wordlarge/numeral2. Checkwhether2stilllargecanpartlyfulfillsmallergroupsclause andmodalsundergeneralprompt, withoutsourceoverstatement orarbitrarymath. Wrongnote3explainsgoalnotmeresplit, SOURCEtraceground mustsupportfullreading. UnresolvedFINALHOLD0/noordinary2.', 'CanonicalNPSfull210/sourcebody0-195nativebyteexact COMPLETEarticle20-181, unusedfooterunverified; allclaimsNPSnewcase only. UNESCO685historicaloriginalHOLDsource retainedrawhash butnotnewclaimproof. Sourcefresh110file/direct11kMAIN1be721+same100/full15closest+6genuinewholebodies/bilateralERVC/directreverse. RootlaterchangedONLYpolar36note2 noMAINdiff; historicSOURCE188fffilehash verifiedagainst11abc, actualMASTERMAINhashsamecurrent, allactualclosestbodiesunchanged. No SOURCEclaimednewprimaryread/inheritedQA. ReaderfreshCURRENTglobalrequired. SOURCE1/raw9d8pre2/root1/reader<2/affected19 thenFINAL only.']
r=a.apply(B,author,[27],D/'apply-parks27-cycle1.json',D/'qa-parks27-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(sourceRawFreeze=freeze,nativeCompactions=counts,actualFullBodies=len(actual),sourceGlobalMAINHash=ps['globalMAIN']['canonicalRowsSHA256'],ROOTPostSOURCEFileOnlyChange=ps['ROOTPostSOURCEFileOnlyChange'],sameSoleCycle=1,qualityCredit=0)
m.write(D/'qualification-parks27-cycle1.json',r);m.write(B/'normalization-provenance.json',{'owner':m.O,'sourceOriginalPath':str(R.relative_to(C)),'sourceRawFreeze':freeze,'operation':'ExactSOURCEcandidate/sourceproof unchanged; existingfullsame100+15closest rowunion. NoteonlyROOT36filemetadata transition recordsoriginalSOURCErawhash notcurrent butall11000MAINprojection exactlySOURCEhash; no unseen actualclosestbody change/newSOURCEjudgment. Canonicalprimaryreusedwithoutcopies, originalHOLD/INITIALFIX history intact.','qualityCredit':0});print(m.savecode(list(B.glob('*.json'))+[D/'qualification-parks27-cycle1.json',pathlib.Path(__file__)],'Qualify soleSOURCE27cycle1 exactslot3repair fullSOURCEbindings no reset'))
