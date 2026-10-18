"""Qualify minimal original36 correction with exactcanonical6/4 evidence; no credit."""
import pathlib,json,re,subprocess,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar36-bindings-complete';B=D/'qualified-polar36-minimal';B.mkdir(exist_ok=True);freeze='5e72695ed2026cd1bd79c1239abc62813fab9792';author='01a150be-8a21-7a73-a0c7-6358f1abe716';counts={}
for u,date in [(m.O,'16'),(author,'19'),('01a150d1-3383-7d30-ad23-76d70ec18813','19')]:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+u+'.jsonl'));counts[u]=sum(json.loads(l).get('type')=='compacted' for l in j.open());assert counts[u]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-evidence.json');e=candidate['entries'][0];before=e['beforeCard'];after=e['proposedCard'];assert e['afterHash']=='7f68c0c2efb27de276ce3f1d748887fbac8e5bb9007baa9934a0ae54d2727769' and m.sha(after)==e['afterHash'];assert all(after[k]==before[k] for k in ['id','difficulty','correctIndex','prompt','explanation','source']);assert before['difficulty']=='medium' and before['correctIndex']==0;assert all(after['answers'][k]==before['answers'][k] for k in [0,1,3]);assert after['answers'][2]['text']==before['answers'][2]['text'] and after['answers'][2]['note']!=before['answers'][2]['note'];contexts=[]
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);assert m.raw(p)==source['sha256'];doc=m.read(p)
 if 'fullOriginalToolOutput' in doc:body=doc['fullOriginalToolOutput']
 else:
  assert doc['sourceNativeId']==author and doc['nativeJournalLine']==836;body='\n'.join(v.get('text','') for v in doc['originalRecord']['payload']['output'] if 'Total lines:' in v.get('text',''))
 declared=[int(n) for n in re.findall('Total lines: ([0-9]+)',body)];ids={int(n) for n in re.findall('L([0-9]+):',body)};assert len(declared)==1 and ids==set(range(declared[0]));contexts.append({'path':str(p.relative_to(C)),'rawSHA256':m.raw(p),'url':source['url'],'declaredPageLines':declared[0],'actualVisibleLineIds':len(ids),'wholeRetainedPageCaptured':True})
assert sorted(x['actualVisibleLineIds'] for x in contexts)==[199,358,367,376,385]
cat={}
for p in (C/'src/content/topics').glob('*.json'):
 t=m.read(p)
 for n,c in enumerate(t['questions'],1):cat[c['id']]={'topicId':t['id'],'sourceOrder':n,'card':c}
base=ps['globalMainBaselineReference'];bp=pathlib.Path(base['path']);assert m.raw(bp)==base['fileSHA256'] and m.sha(m.read(bp))==base['canonicalSHA256'];baseRows=m.read(bp)['rows'];assert len(baseRows)==11000;deltas=ps['globalMainDelta']+ps['additionalPostSnapshotGlobalMainDelta'];assert {d['id'] for d in deltas}=={'national-parks-nature-026','national-parks-nature-027','polar-regions-aurora-charged-particles','polar-regions-permafrost-frozen-ground'};dd={d['id']:d for d in deltas}
for d in deltas:
 assert d['currentFullCard']==cat[d['id']]['card'];assert m.sha(d['currentFullCard'])==d.get('currentFullCardSHA256',d.get('currentWholeCardSHA256'));assert m.sha(d['currentMain'])==d['currentMainSHA256']
rows=[]
for old in baseRows:
 r=dict(old)
 if r['id'] in dd:r.update(main=dd[r['id']]['currentMain'],mainSHA256=m.sha(dd[r['id']]['currentMain']))
 c=cat[r['id']]['card'];assert r['main']=={'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']};assert m.sha(r['main'])==r['mainSHA256'];rows.append(r)
assert m.sha({'catalogBaseline':base['reconciledCurrentCatalogCommit'],'rowCount':len(rows),'rows':rows})==base['reconciledCurrentCanonicalSHA256']=='7c195d19fc1c7aeb765c6003e4be34e673425664752b4fbe43aa1a4535e7bad3'
for group in ps['globalSearch']['patterns']:
 rx=re.compile(group['pattern']['regex'],re.I);hits={r['id'] for r in rows if rx.search(' '.join([r['main']['prompt'],*r['main']['answers']]))};assert hits=={r['id'] for r in group['hits']} and len(hits)==group['hitCount']
ref=ps['sameTopicSnapshotReference'];prior=pathlib.Path(ref['peerSnapshotPath']);assert m.raw(prior)==ref['peerSnapshotSHA256'];rp=pathlib.Path(ref['readReceiptsPath']);assert m.raw(rp)==ref['readReceiptsSHA256'];assert ref['personalReadNativeId']==author and ref['sameTopicCount']==100;actual={}
for p in m.read(prior)['actualCurrentPeers']:
 if p['topicId']!='polar-regions':continue
 c=p['card']
 if c!=cat[p['id']]['card']:
  assert p['id'] in dd and dd[p['id']]['currentFullCard']==cat[p['id']]['card'];c=dd[p['id']]['currentFullCard']
 assert c==cat[p['id']]['card'];actual[p['id']]={'id':p['id'],'topicId':'polar-regions','sourceOrder':cat[p['id']]['sourceOrder'],'card':c,'sha256':m.sha(c)}
assert len(actual)==100
for p in ps['closestWholeCardPeers']:assert p['fullCard']==cat[p['id']]['card'] and m.sha(p['fullCard'])==p['wholeCardSHA256']
for p in ps['previousGenuineProposals']:
 path=pathlib.Path(p['candidatePath']);assert m.raw(path)==p['candidateFileSHA256'];entry=next(e for e in m.read(path)['entries'] if e['id']==p['id']);assert entry['proposedCard']==p['fullProposedCard'] and entry['afterHash']==p['postimageHash']==m.sha(p['fullProposedCard']);assert p['fullProposedCard']==cat[p['id']]['card']
pairs={}
for pair in ps['pairwiseBilateralERVCandDirectReverse']:
 assert pair['basis'] and pair['ERVC'] and pair['directReverse'];pairs.setdefault((pair['peerId'],pair['peerType']),set()).add(pair['direction'])
assert len(pairs)==6 and all(v=={'candidate36_to_peer','peer_to_candidate36'} for v in pairs.values())
ps['actualCurrentPeers']=list(actual.values());ps['ROOTCurrentBodyBinding']={'sourceOwnReadSnapshot':str(prior),'originalReadSnapshotSHA256':m.raw(prior),'currentTopicRawSHA256':m.raw(C/'src/content/topics/polar-regions.json'),'knownOwnPostimages34_35Applied':True,'operation':'SOURCEoriginalsame100snapshot hasolder34/35 bodies, alreadyfullyauthoredsamebe postimages fromexplicitglobalDelta+certificate replaceexactversions only. Source unchangedFromPrior/currentRaw6fba retainedashistoricalreference, notassertedcurrentwholefile. No newSOURCEreadjudgment invented.'}
for name,doc in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/name,doc)
concerns=['Original36 FIRSTINITIAL no previousreview/fixcycle. Beforeexpansive099f proposalwasUNAPPLIED; preINITIALminimalreconciliation946 thencompletecanonical6/4bindings5e726. Exact7f68 content changesONLYnote2Larsenpasttense topreciseLarsenA1995/LarsenBpartial2002, oldvalidMAIN/explanation/correctnotePrydzBay+East/notes1and3/key0/MEDIUM/source preserved. All6literal4wholevariants andownnoteextra independentlyrequired, no gratuitousrewrites/nocrossnoteban.', 'Fivefullretainedprimarycontexts actual385NASAAmery/science266-270,376AAPiceShelves/fullarticleAmery315-317,199BASRonnegeo151-158,367NASAGetz255+263-265,358AAPLarsenFULLarticle298-319/claims305-306. OriginalLarsenwebresult hadpathnull, ROOThaswholeoriginalnativeSOURCEbejournal836 originalrecordall358labels storedcanonicalSHA9991; authorpersonallyconfirmed/rebound, notnewfetch/manualselectedquotes. Keepallfullscopequalifiers, sourceNASA385supportsMAINLambertflow, AAP376PrydzBay/East+largeLambertbasinexplanation, BASsouthernWeddell, NASAMarieByrdcoastalcontext, AAPLarsenspecificsections/years. Do not inferentireLarsengone.', 'FrozenMEDIUMnotROOTearliergenericEASYwarning. IndependentlyassessabsoluteadultMEDIUM fornamedLambert→Ameryregionalfact, notmerelyrelativeice-shelfexpertise/onlynotEASY orsourcepagepresence; all4crediblecomparableice-shelfnames/unique/naturalgrammar/polartaxonomy. CorrectnotePrydzBay/Eastadditionalbeyondwholeprompt/key; qualitativeoneoflargestEastAntglaciersystems inoriginalexplanation needsfullprimaryscope, notunboundedrankinginvented.', 'Sourcefull11kBASE76fd/wholeDOC45890+4explicitcurrentdeltas26/27/34/35, currentreconstruction7c195 is canonical {catalogBaseline:83d592,rowCount,rows} withBASEmetadata rows andupdatedmain/mainSHA; eachMAIN exactlyCURRENTchecked. Do notmislabelSOURCEBASEoldrawSourceSHA metadataascurrenttopicfile; SOURCECURRENTbody/deltas separatelychecked. Sameauthor100MAINownpriorread+ownalreadyauthored34/35postimages reusescanonicalreceipts, source-old6fba refhistorical; nearest19/20/37/100fullbodies+34/35genuinebothwayERVC/directreverse, noMAINinverse/formatban or notevsMAINcollisionban. New27actuale67awaitsonlyslot3SOURCEfix (notduplicateAmeryroute), 26FINALHOLD0retaineduncounted. IndependentCURRENTglobal/same100/fullclosest/proposals needed. OneSOURCEfixafterINITIAL thenFINAL/unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,author,[36],D/'apply-polar36-minimal.json',D/'qa-polar36-minimal.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':list(actual.values())},concerns=concerns);r.update(sourceRawFreeze=freeze,sourceMinimalPreservationFreeze='9462776ac5944b445cfeb7c7ce6f57265c2ae819',nativeCompactions=counts,primaryContexts=contexts,allActualSameTopicBodiesVerified=100,sourceGlobalProjectionSHA256=base['reconciledCurrentCanonicalSHA256'],SOURCEbilateralBothDirections=6,qualityCredit=0)
m.write(D/'qualification-polar36-minimal.json',r);m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operation':'Candidate/sourceproofexactunchanged, originalsourcepeer-evidence retainedasnormalizedpeer-snapshot. Existingauthorhistoricalfull100snapshot andexactownknowncurrent34/35postimages union givesactual100bodyhashes; originalSOURCE referencefields remainhistorical. WHOLEcanonicalprimarycaptures reused, noSourcebody/semanticjudgment invented.','globalHashProjection':'{catalogBaseline:83d592,rowCount,rows} withupdated main/mainSHA only; BASE rowmetadata historical, exactCURRENTdeltas separate.','qualityCredit':0});print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar36-minimal.json',pathlib.Path(__file__)],'Qualify exactminimal36 canonical6-4 fullfiveprimarycontexts andlivepeer bindings'))
