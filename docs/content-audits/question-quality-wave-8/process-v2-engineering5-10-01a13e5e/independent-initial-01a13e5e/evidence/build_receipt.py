import json, hashlib, subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path.cwd()
PACKET=Path('docs/content-audits/question-quality-wave-8/process-v2-engineering5-10-01a13e5e')
OUT=PACKET/'independent-initial-01a13e5e'
def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sha(v): return hashlib.sha256(canonical(v)).hexdigest()
def raw(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
apply=json.loads((PACKET/'apply-initial7-8.json').read_text())
proof=json.loads((PACKET/'author/sourceproof.json').read_text())
author=json.loads((PACKET/'author/candidate.json').read_text())
snapshot=json.loads((PACKET/'author/peer-snapshot.json').read_text())
catalogPath=Path('src/content/topics/engineering-machines.json')
catalog=json.loads(catalogPath.read_text())
questions=catalog['questions']; byid={c['id']:c for c in questions}
ids=[x['id'] for x in apply['applied']]
short=lambda s:'engineering-machines-'+s
norms=[]
for n in apply['technicalCanonicalRepresentationNormalizations']:
 if 'authorLiteral' in n:
  assert sha(n['authorLiteral'])==n['authorRepresentationSHA256']
  assert {**n['authorLiteral'],'answers':[a['text'] for a in n['authorLiteral']['answers']]}==n['canonicalProcessLiteral']
 else:
  assert hashlib.sha256(n['canonicalProcessLiteral'].encode('utf-8')).hexdigest()==n['authorRawStringSHA256']
 assert sha(n['canonicalProcessLiteral'])==n['canonicalProcessSHA256']
 cardProof=next(x for x in proof['cards'] if x['id']==n['id'])
 g=next(x for x in cardProof['sixLiteralGroups'] if x['group']==n['group'])
 assert g['afterLiteral']==n.get('authorLiteral',n['canonicalProcessLiteral'])
 assert g.get('afterCanonicalSHA256',g.get('afterSHA256'))==n.get('authorRepresentationSHA256',n.get('authorRawStringSHA256'))
 norms.append({**n,'independentlyVerified':True,'semanticChanges':False})
sources={}
for key,s in proof['sources'].items():
 p=Path(s['capturedPath']) if key=='NASA_RP1228' else PACKET/'author'/s['capturedPath']
 t=Path(s['fullTextPath']) if key=='NASA_RP1228' else PACKET/'author'/s['fullTextPath']
 assert raw(p)==s['rawSHA256'] and raw(t)==s['fullTextSHA256']
 reader=PdfReader(p);assert len(reader.pages)==s['pages']
 pages=[5,11,30,31] if key=='NASA_RP1228' else [383]
 sources[key]={'path':str(p),'rawSHA256':raw(p),'bytes':p.stat().st_size,'fullTextPath':str(t),'fullTextSHA256':raw(t),'PDFPageCount':len(reader.pages),'personallyReadFullPages':pages,'personallyInspectedRenderedPages':pages,'url':s['url'],'refetched':False,'readScope':'Relevant full pages only, including both columns, figures, captions, table and footnotes; not all pages of either book.'}
RP=sources['NASA_RP1228'];FAQ=sources['NASA_FAQ']
def loc(k,n,detail):
 s=sources[k]
 return {'sourcePath':s['path'],'rawSHA256':s['rawSHA256'],'PDFPage':n,'printedPage':{5:'1',11:'7',30:'26',31:'27',383:'21-7'}[n],'context':detail,'fullPageTextEvidence':str(OUT/'evidence'/f'{k}-page-{n}.txt'),'fullPageRenderEvidence':str(OUT/'evidence'/f'{k}-page-{n}.png')}
materials=loc('NASA_RP1228',5,'Fastener Materials, first paragraph; page read through Cadmium Plating and numbered precautions.')
nylon=loc('NASA_RP1228',11,'Nylok pellet paragraph and figure 4; contrasted with deformed-thread fig.3, collar fig.5, castellated fig.6 and Nylok footnote 8.')
rivet=loc('NASA_RP1228',30,'Rivets: permanent installation and drilling removal; Solid rivets shop head, Table IX including reference 21 and Briles footnote 13.')
rivet2=loc('NASA_RP1228',31,'Fig.34 head types, fig.35, fig.36 setting sequence and Tubular rivets final paragraph describing hollow end formed into field head.')
faq=loc('NASA_FAQ',383,'Q10/A10 entire page: four proposed bolt/screw distinctions, none universally acceptable, final instruction to specify geometry or part number.')
notes={
 'Заклёпка':{'status':'PASS','sourceClaims':'RP p.30 explicitly treats rivets as permanent fasteners and drilling as removal. The Russian usually is weaker than the manual categorical wording and does not claim drilling is the only conceivable operation.','usefulness':'Adds the practical cost of dismantling: drilling out the fastener; this is absent from the head-forming question and is more than a reworded definition.','grammar':'Complete natural two-clause Russian sentence; крепёж refers to the rivet being removed.','sources':[rivet]},
 'Болт':{'status':'PASS','sourceClaims':'RP p.5 explicitly says most bolts are carbon, alloy or stainless steel. Большинство preserves the qualifier and allows titanium/aluminium exceptions; the card makes no unsupported strength/corrosion claim.','usefulness':'Adds material selection information rather than repeating the question or an external-thread definition.','grammar':'Three parallel material adjectives share стали; изготавливают из is idiomatic.','sources':[materials]},
 'Гайка':{'status':'PASS','sourceClaims':'RP p.11 Nylok paragraph and fig.4 support projection, mating-thread compression and locking contact. This is a statement about a named nylon insert, not an assertion that every nut contains it. Nut-card explanation explicitly says Некоторые гайки; rivet-card note likewise has no universal quantifier. More explicit subtype wording would improve standalone clarity but the actual sentence does not claim all nuts have nylon.','usefulness':'Explains how one locking element works, beyond the internal-thread definition; a player learns a real mechanical effect.','grammar':'Two technical but complete clauses; сопряжённая резьба сжимает его clearly refers to the insert. No grammatical implication of universal possession.','sources':[nylon]},
 'Винт':{'status':'PASS','sourceClaims':'FAQ p.383 explicitly rejects a universally acceptable distinction and concludes with geometry or corresponding part number. NASA is the publishing organisation; the card accurately attributes its advice without turning a local distinction into an absolute rule.','usefulness':'Warns why a label alone is insufficient for selecting a part and names two practical alternatives. It does not simply repeat the screw definition.','grammar':'Граница ... не универсальна is a comprehensible concise paraphrase; parallel geometry/part-number complement is clear.','sources':[faq]}}
variants=[];groups=[];cards=[]
for item in apply['applied']:
 c=byid[item['id']]; old=item['beforeCard']; assert c==item['proposedCard'] and sha(c)==item['proposedSHA256']
 assert next(x for x in author['entries'] if x['id']==c['id'])['proposedCard']==c
 assert all(c[k]==old[k] for k in ['id','difficulty','correctIndex'])
 assert [a['text'] for a in c['answers']]==[a['text'] for a in old['answers']]
 isNut=c['id']==short('nut-fastener')
 literal={'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']}
 six=[('prompt_ordered_answers_key',literal),('explanation',c['explanation'])]+[(f'note{i}',a['note']) for i,a in enumerate(c['answers'])]
 for name,value in six:
  expected=next(g for g in apply['finalGroups12'] if g['id']==c['id'] and g['group']==name)
  assert value==expected['literal'] and sha(value)==expected['canonicalSHA256']
  if name=='prompt_ordered_answers_key':
   ground=('Internal receiving thread and being screwed onto a bolt isolate nut among these four. Bolt and screw have external threaded bodies; a rivet does not receive the bolt in an internal thread. FAQ overlap of bolt/screw labels does not create another correct choice here.' if isNut else 'The described upset/formed closing head is rivet installation. Merely having a hole does not suffice: bolt, screw and nut are normally tightened by thread engagement, not set by upsetting their protruding end. The stem describes a class instance and does not assert every blind rivet is hammer-bucked.')
   sr=[nylon,faq] if isNut else [rivet,rivet2]
  elif name=='explanation':
   ground=('RP fig.3/4/5 show the internal female thread receiving the bolt and different locking mechanisms. Некоторые is correctly limited: locknuts are a subtype, not all nuts. Resistance to unscrewing is the stated locking function.' if isNut else 'RP p.30 solid-rivet paragraph and p.31 tubular-rivet paragraph support forming the protruding end into a shop/field head. RP p.30 supports permanent setting and drilling for removal. Nothing says every rivet design uses identical installation tools.')
   sr=[nylon] if isNut else [rivet,rivet2]
  else:
   d=notes[c['answers'][int(name[4:])]['text']];ground=d['sourceClaims']+' '+d['usefulness'];sr=d['sources']
  groups.append({'id':c['id'],'group':name,'literal':value,'canonicalSHA256':sha(value),'status':'PASS','grounds':ground,'sources':sr})
 for slot,a in enumerate(c['answers']):
  d=notes[a['text']]
  if isNut:
   grounds={0:'Rivet is a real neighbouring fastener and plausible to a novice, but its body is set by deformation rather than screwed onto a bolt using a female thread.',1:'Bolt is a plausible paired component familiar from гайка и болт, but its outer thread is the received member, not the internally threaded receiving part.',2:'Nut alone has the female threaded receiving body in the described bolt joint; key 2 remains unique.',3:'Screw is a plausible neighbouring threaded fastener, but externally threaded rather than the female receiving part. The bolt/screw terminology overlap cannot turn it into a nut.'}[slot]
  else:
   grounds={0:'Bolt can be inserted through a hole and has a head, making it a plausible competing fastener; formation of a closing head by upsetting is not its normal threaded installation.',1:'Screw belongs to the same practical fastening vocabulary and has a head, but it is threaded into a receiving material or thread, not set by upsetting a protruding end.',2:'Rivet alone is set by forming a closing head in this description; this remains true despite the source covering additional blind-rivet mechanisms. Key 2 is unique.',3:'Nut is a familiar component in the same fastening family, but it is screwed onto a male thread rather than inserted through a hole and upset into a head.'}[slot]
  triple={'prompt':c['prompt'],'answer':a['text'],'note':a['note']}
  expected=next(x for x in apply['finalVariants8'] if x['id']==c['id'] and x['slot']==slot)
  assert all(triple[k]==expected[k] for k in triple)
  assert sha(triple)==expected['bindingCanonicalSHA256']
  variants.append({'id':c['id'],'slot':slot,**triple,'bindingCanonicalSHA256':expected['bindingCanonicalSHA256'],'status':'PASS','answerGrammar':'All four answer labels are nominative noun phrases answering Как называется деталь or Какой крепёж; no gender/case or sentence-completion cue excludes a distractor.','plausibilityAndKeyGrounds':grounds,'noteGrammar':d['grammar'],'allNoteClaims':d['sourceClaims'],'individualUsefulness':d['usefulness'],'correctNoteBeyondPrompt':(d['usefulness'] if slot==2 else None),'sources':d['sources']})
 cards.append({'id':c['id'],'fullCard':c,'canonicalSHA256':sha(c),'sourceOrder':item['sourceOrder'],'frozenInvariantStatus':'PASS','correctIndex':2,'difficulty':{'status':'PASS','level':'easy','specPath':'/Users/eaafonasev/Projects/mindbattle-planning/openspec/specs/question-catalog/spec.md','specLines':'21-33','grounds':('Nut receiving a bolt is familiar to broad adult household/DIY users without specialist study. All labels are real fasteners, and internal versus external thread is everyday recognition, not a quota-driven difficulty choice.' if isNut else 'Recognising a rivet by a formed closing head is common to a broad DIY/repair/craft group; specialist material or aerospace detail is not required. Расклёпывают also supplies an accessible linguistic cue. This is an absolute easy judgement, not a comparison against the other catalog questions.')},'sixGroupsStatus':'PASS','eightSubstitutionRelevantSlotsStatus':'PASS','catalogContextStatus':'FIX','status':'FIX','defectIds':['CURRENT-PEER-ANSWER-LEAKAGE'],'nextAction':'Coordinator must reconcile the currently unqualified 5/6 peers or explicitly adjudicate their answer leakage, then rebind the affected comparison against actual CURRENT. No catalog changes made by reviewer.'})
# Personally read complete current cards for direct fasteners and neighbouring joint/drilling context.
peerSuffix=['bolt-fastener','screw-fastener','nut-fastener','rivet-fastener','lap-joint','butt-joint','drilling-hole','welding-join']
peerCards=[{'id':short(x),'fullCard':byid[short(x)],'canonicalSHA256':sha(byid[short(x)]),'readScope':'Entire prompt, all four answer labels/notes, key, explanation and source'} for x in peerSuffix]
pairs=[]
for target in ['nut-fastener','rivet-fastener']:
 for peer in ['bolt-fastener','screw-fastener']:
  t=byid[short(target)];p=byid[short(peer)];text='Гайка' if target=='nut-fastener' else 'Заклёпка';pa=next(a for a in p['answers'] if a['text']==text)
  forward={'from':p['id'],'to':t['id'],'peerQuote':pa['note'],'targetQuote':t['prompt'],'verdict':'DIRECT_ANSWER_LEAKAGE','grounds':('The peer explicitly labels Гайка as the internally threaded component joined with a bolt, reproducing the target discriminator.' if target=='nut-fastener' else 'The peer explicitly labels Заклёпка as the fastener inserted into holes with a second head formed; this gives the same discriminating installation operation as the target closing-head stem.')}
  ta=next(a for a in t['answers'] if a['text']==('Болт' if peer=='bolt-fastener' else 'Винт'))
  reverse={'from':t['id'],'to':p['id'],'peerTargetQuote':p['prompt'],'fromNoteQuote':ta['note'],'fromExplanationQuote':t['explanation'],'verdict':('RELATIONSHIP_CUE' if target=='nut-fastener' and peer=='bolt-fastener' else 'NO_DIRECT_ANSWER_LEAKAGE'),'grounds':('Nut explanation identifies the bolt/nut threaded pairing and therefore cues peer5 usually working with a nut. Materials alone do not provide this answer.' if target=='nut-fastener' and peer=='bolt-fastener' else 'The changed note supplies material information or cautions about terminology. It does not state the peer prompt definition, unlike the unchanged peer-to-target direction. No artificial symmetric defect is asserted.')}
  pairs.append({'leftId':t['id'],'leftCanonicalSHA256':sha(t),'rightId':p['id'],'rightCanonicalSHA256':sha(p),'directions':[forward,reverse],'status':'FIX','ownership':'Peer5/6 are not reviewed as INITIAL ready: this is an actual-CURRENT dependency finding only.'})
n=byid[short('nut-fastener')];r=byid[short('rivet-fastener')]
pairs.append({'leftId':n['id'],'leftCanonicalSHA256':sha(n),'rightId':r['id'],'rightCanonicalSHA256':sha(r),'status':'PASS','directions':[{'from':n['id'],'to':r['id'],'fromQuote':n['answers'][0]['note'],'targetQuote':r['prompt'],'verdict':'NO_DIRECT_ANSWER_LEAKAGE','grounds':'Permanent setting/removal by drilling does not state the head-forming operation; the latter distinguishes the rivet stem. This is a neighbouring fact, not the original repeated definition.'},{'from':r['id'],'to':n['id'],'fromQuote':r['answers'][3]['note'],'targetQuote':n['prompt'],'verdict':'NO_DIRECT_ANSWER_LEAKAGE','grounds':'Insert locking mechanism does not state the internal-thread receiving definition. It is a scoped mechanism example; it does not assert every nut has such an insert.'}],'sharedNotes':'All four term notes are identical across the two cards, transparently retained. Repetition of a term fact is not itself a second same-answer stem or a direct defining cue.'})
for suffix in ['lap-joint','butt-joint','drilling-hole','welding-join']:
 p=byid[short(suffix)]
 for t in [n,r]:
  pairs.append({'leftId':t['id'],'leftCanonicalSHA256':sha(t),'rightId':p['id'],'rightCanonicalSHA256':sha(p),'status':'PASS','directions':[{'from':p['id'],'to':t['id'],'fromQuote':p['explanation'],'targetQuote':t['prompt'],'verdict':'NO_DIRECT_ANSWER_LEAKAGE','grounds':'This peer identifies joint geometry, a machining process or welding. It does not label the internal-thread component or the formed-head fastener.'},{'from':t['id'],'to':p['id'],'fromQuote':t['explanation'],'targetQuote':p['prompt'],'verdict':'NO_DIRECT_ANSWER_LEAKAGE','grounds':'The fastener explanation does not name the target joint geometry or describe the target process discriminator. Rivet removal by drilling mentions drilling but does not reproduce the drilling question definition of a round hole made by a rotating drill.'}]})
old={x['id']:x['card'] for x in snapshot['currentCards']}
changed=[c['id'] for c in questions if old[c['id']]!=c];assert set(changed)==set(ids)
sourceEvidence={'sources':sources,'independentClaimReviews':notes,'sourceHashAssertionsPassed':True,'readAndRenderedPages':{'NASA_RP1228':[5,11,30,31],'NASA_FAQ':[383]},'pageContextRemarks':['RP p.5 was read including limitations, numbered precautions and cadmium discussion; none is silently extended to every bolt.','RP p.11 figures distinguish multiple locknut types; Nylok is not treated as generic anatomy of all nuts. Footnote 8 is a trade-name attribution, not another mechanism.','RP p.30 table IX and footnote 13 were read; neither changes the permanent/drilling statements.','RP p.31 includes multiple blind-rivet mechanisms and tubular rivets; the question describes a valid formed-head type, not all installation methods.','FAQ p.383 was read in full including all four proposed definitions and concluding qualification; the claim is appropriately non-universal.']}
save(OUT/'evidence/source-review.json',sourceEvidence)
save(OUT/'evidence/six-groups12.json',groups)
save(OUT/'evidence/full-substitutions8.json',variants)
save(OUT/'evidence/normalizations-verified.json',norms)
save(OUT/'evidence/current-peers-full.json',{'catalogPath':str(catalogPath),'catalogRawSHA256':raw(catalogPath),'all100PromptInventoryRead':[{'sourceOrder':i+1,'id':c['id'],'prompt':c['prompt']} for i,c in enumerate(questions)],'fullRelevantCards':peerCards,'fullCardHashConvention':'SHA256 of UTF-8 canonical JSON: sort_keys=True, separators comma/colon, ensure_ascii=False','authorSnapshotDriftOnlyIds':changed,'authorSnapshotOtherwiseMatchesCurrent':True,'comparisons':pairs,'qualification':'5/6 remain qualification; 9/10 HOLD are outside ready review. No inheritance of author/QA PASS.'})
save(OUT/'evidence/current-cards2.json',cards)
root={'cards':[{'id':c['id'],'canonicalSHA256':c['canonicalSHA256']} for c in cards],'groups':[{'id':g['id'],'group':g['group'],'literal':g['literal'],'canonicalSHA256':g['canonicalSHA256']} for g in groups],'variants':[{'id':v['id'],'slot':v['slot'],'prompt':v['prompt'],'answer':v['answer'],'note':v['note'],'bindingCanonicalSHA256':v['bindingCanonicalSHA256']} for v in variants]}
save(OUT/'evidence/root-binding.json',root)
evidenceFiles=sorted(x for x in (OUT/'evidence').iterdir() if x.is_file())
receipt={'schema':'independent-initial-current-review-v2','reviewerThread':'01a13ee0-350c-7d62-b433-efc497addb2c','stage':'INITIALCURRENT2','date':'2026-10-15','worktree':str(ROOT),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'applyCommit':'0d6a3feabf7aabbfdc1973aef3ee74708286436d','referencedAffectedQACommit':'1ed86742c3731779facd0a192cba03f34a4f0ba1','observedHEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'processReadAtCommit':'12e5581b','scope':ids,'qualityCredit':0,'rootBindingCanonicalSHA256':sha(root),'rootBindingPath':str(OUT/'evidence/root-binding.json'),'groups12RootCanonicalSHA256':sha(root['groups']),'canonicalHashContract':'SHA256 UTF-8 json.dumps(sort_keys=True,ensure_ascii=False,separators=(comma,colon)); JSON strings include quotes, unlike original author raw string SHA. Full cards include all fields/source.','status':'FIX','cards':[{'id':c['id'],'canonicalSHA256':c['canonicalSHA256'],'status':c['status'],'localSixGroups':'PASS','absoluteEasy':'PASS','correctIndex':2,'defects':c['defectIds']} for c in cards],'findings':[{'id':'CURRENT-PEER-ANSWER-LEAKAGE','status':'FIX','affectedIds':ids,'summary':'Unchanged actual CURRENT bolt5/screw6 answer notes explicitly supply the target definitions for nut7/rivet8. New 7/8 no longer repeat those definitions themselves, but old peers still defeat current catalog independence.','evidence':str(OUT/'evidence/current-peers-full.json'),'requestedAction':'Coordinator adjudicates and reconciles 5/6 as dependencies before crediting 7/8 CURRENT. Do not automatically accept unqualified proposals for 5/6. No requested edit of 9/10.'}],'nylonJudgement':{'status':'PASS','grounds':'The named insert mechanism is supported by RP p.11; the actual sentence does not say all nuts contain it, and nut explanation explicitly limits locking elements to some nuts. A subtype phrase could improve standalone clarity but no false universal claim is imputed.'},'rivetCorrectNoteJudgement':{'status':'PASS','grounds':'Adds removal by drilling, a useful practical fact absent from the formed-head stem; not mere definition repetition.'},'independence':'Personally read the exact CURRENT two full cards, 12 groups, eight full triples, saved full source pages and renders, actual relevant peer full cards and both directions of final self-pair. No inherited quality conclusions.','checks':{'type':'Evidence structure/hash/preimage comparison only, not a test/runtime run','catalogMatchesExactAppliedCards':True,'all12GroupsRecomputed':True,'all8BindingsRecomputed':True,'all12AuthorNormalizationFormsVerifiedAgainstOriginalSourceproof':True,'fullSourceRawAndTextSHAAndPageCountsVerified':True,'snapshotDriftOnly7and8':True,'frozenIdTopicDifficultyAnswerOrderKey':True,'testsRuntimeBuild':'Not run: explicitly excluded and unnecessary for independent content reading. Referenced QA is context, not inherited evidence of quality.','GitMutation':'None: no commit, staging, index, branch, claim or planning mutation authorized.'},'evidenceManifest':[{'path':str(x),'rawSHA256':raw(x),'bytes':x.stat().st_size} for x in evidenceFiles],'preservation':{'state':'Files persisted in requested worktree output folder; not committed by this reviewer per explicit instruction.','nextOwner':'Source coordinator','nextAction':'Read/adjudicate FIX and save receipt/evidence in Git with branch+commit before archiving this chat.','ownProcesses':'All reviewer commands synchronous and completed; no runtime, browser, test, render server or background jobs started.','temporaryFiles':'None outside allowed evidence folder. Five PNGs and five full-page texts retained as required primary-reading evidence.','mainIntegration':'Not claimed; no Git integration performed.'}}
save(OUT/'receipt.json',receipt)
print(json.dumps({'status':receipt['status'],'cards':receipt['cards'],'rootSHA':sha(root),'evidenceFiles':len(evidenceFiles)},ensure_ascii=False))
