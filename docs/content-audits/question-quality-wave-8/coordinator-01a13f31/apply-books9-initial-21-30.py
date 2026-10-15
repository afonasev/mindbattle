"""Decode author's exact JSON-object literal containers, apply qualified9 only."""
import pathlib,json,copy,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
def rd(p):return json.loads(pathlib.Path(p).read_text())
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('m',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books21-30-01a13f31/author';B=D/'normalized-books9-initial-21-30';B.mkdir(exist_ok=True);a=rd(A/'candidate.json');sp=rd(A/'sourceproof.json');p=rd(A/'peer-snapshot.json');ready={e['id']:e for e in a['entries'] if e['status']=='READY_FOR_INDEPENDENT_REVIEW'};assert len(ready)==9;changed=[]
for e in sp['entries']:
 if e['id'] not in ready:continue
 for g in e['literalGroups']:
  if g['group']=='prompt_ordered_answers_key' and isinstance(g['literal'],str):
   old=g['literal'];obj=json.loads(old);c=ready[e['id']]['proposedCard'];assert obj=={'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']} and m.sha(obj)==g['literalSHA256']==ready[e['id']]['fieldGroups'][g['group']]['afterCanonicalSHA256'];g['literal']=obj;g['originalSerializedLiteral']=old;g['technicalNormalization']='JSONdecodeexactauthorobject; existingcorrectobjectcanonicaldigestunchanged';changed.append(e['id'])
assert len(changed)==9;catalog={}
for t in {e['topicId'] for e in p['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for e in p['actualCurrentPeers']:assert e['card']==catalog[e['id']] and m.sha(e['card'])==e['sha256']
for n,v in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',p)]:wr(B/n,v)
wr(B/'normalization-manifest.json',{'originalAuthor':str(A.relative_to(C)),'only9KeyGroupSerializedJSONDecoded':changed,'existingCanonicalObjectDigestsPreserved':True,'allPrimaryGroundsAndFourVariantJudgmentsUnchanged':True,'currentPeers135Bound':True,'excludedHOLD27':'SeparateINITIALSOURCEcompletion running; nochange/noqualitycredit for27.','qualityCredit':0})
orders=[e['sourceOrder'] for e in ready.values()];same={'actualCurrentPeers':[e for e in p['actualCurrentPeers'] if e['topicId']=='books-publishing']};r=m.apply(B,'01a13fb8-287d-7753-8f8f-a92c6dac33c0',orders,None,None,None,qualifyOnly=True,peerSnapshot=same);assert len(r['applied'])==9
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);files=[A/n for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]+[C/s['path'] for s in sp['rawSources']]+[p for p in B.iterdir() if p.is_file()]+[pathlib.Path(__file__)];files=list(dict.fromkeys(str(p.relative_to(C)) for p in files));print('SOURCE9freeze',h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Preserve qualifiedSOURCEbook21–30 READY9 with literalcontainer-only normalization',m.raw(C/h.git(C,'rev-parse','--git-path','index'))))
m.apply(B,'01a13fb8-287d-7753-8f8f-a92c6dac33c0',orders,D/'apply-books9-initial-21-30.json',D/'qa-books9-initial-21-30.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['INITIALonly9 orders21–26/28–30; SOURCEHOLD27 excluded, completingseparately.','Canonicalprimary sourcefacts/individualfrozenlevels mustbepersonallyjudgedincludingrarebookterms21–25, designerrole26 andspecificHalifaxloanpolicyconditions28–30. No inheritedAUTHORPASS.','135actualfullpeers35cross verifiedandfullproposedMAINpairsretained; sourcekeygroupliteralserializedJSONdecodedwithoutcontentordigestchange.','ParallelSOURCEsolefix12/15/17/18drafts notyetREADY; beforefinalcredit compareactualcurrentandrelevantnewqualifiedproposals iftheyappear.'])
