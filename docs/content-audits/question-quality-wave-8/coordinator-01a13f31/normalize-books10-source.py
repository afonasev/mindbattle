"""Merge author's original10 SOURCE versions; only paths/schema/hash containers normalized."""
import pathlib,json,hashlib,copy,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books11-20-01a13f31/author/initial-source-completion';B=D/'normalized-books11-20-initial';B.mkdir(exist_ok=True)
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def gs(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
def paths(x,mp):
 if isinstance(x,dict):return {k:paths(v,mp) for k,v in x.items()}
 if isinstance(x,list):return [paths(v,mp) for v in x]
 return mp.get(x,x) if isinstance(x,str) else x
versions=[(A,[12]),(A/'addenda/final-11-13-14',[11,13,14]),(A/'printing-15-20',[17,18,19,20]),(A/'cross-primary-qualification/final15-16',[15,16])];ce={};se={};sources={};origins={};cross=rd(A/'cross-primary-qualification/qualification-addendum.json');replacement={e['sourceOrder']:e for e in cross['entries']}
for V,orders in versions:
 cand=rd(V/'candidate.json');proof=rd(V/'sourceproof.json');mp={}
 for s in proof['rawSources']:
  p=C/s['path']
  if not p.is_file():p=V/s['path']
  if not p.is_file():p=A/s['path']
  assert p.is_file(),s['path'];new=str(p.resolve().relative_to(C));assert raw(p)==s['sha256'],(s['path'],'raw source changed')
  mp[s['path']]=new;ns={**s,'path':new}
  if new in sources:assert sources[new]['sha256']==ns['sha256']
  else:sources[new]=ns
 for e in cand['entries']:
  o=e['sourceOrder']
  if o not in orders:continue
  e=copy.deepcopy(e)
  assert sha(e['proposedCard'])==e['afterHash'];assert e['status']=='READY_FOR_INDEPENDENT_REVIEW';ce[o]=e;origins[o]={'candidate':str((V/'candidate.json').relative_to(C)),'sourceproof':str((V/'sourceproof.json').relative_to(C)),'latestReplacement':e.get('technicalLatestVersionSource')}
 for e in proof['entries']:
  o=e['sourceOrder']
  if o in orders:se[o]=paths(copy.deepcopy(e),mp)
assert set(ce)==set(se)==set(range(11,21))
for o,e in ce.items():
 q=e['proposedCard'];sg=gs(q);pe=se[o];assert len(pe['literalGroups'])==6 and len(pe['fourFullPromptAnswerNoteAssessments'])==4
 for g in pe['literalGroups']:assert g['literal']==sg[g['group']] and sha(g['literal'])==g['literalSHA256'],(o,g['group'],'SOURCE literal not latest authorcard')
 for v in pe['fourFullPromptAnswerNoteAssessments']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and sha(tr)==v['tripleSHA256']
peers=rd(A/'printing-15-20/peer-snapshot.json');ps=peers['actualCurrentPeers'];catalog={}
crosspeers=[]
for p in cross['actualCurrentCrossCatalogPeers']:
 np=copy.deepcopy(p);np['topicId']=pathlib.Path(np.pop('topicFile')).stem;crosspeers.append(np)
for t in {p['topicId'] for p in ps+crosspeers}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in ps+crosspeers:assert p['card']==catalog[p['id']] and sha(p['card'])==p['sha256'],('stale peer',p['id'])
wr(B/'candidate.json',{'owner':'01a13f31-9224-7dd1-90e0-e5b0ea2e94a9','author':'01a13f93-17b0-7893-8955-26059d806d41','entries':[ce[o] for o in range(11,21)],'qualityCredit':0})
wr(B/'sourceproof.json',{'rawSources':list(sources.values()),'entries':[se[o] for o in range(11,21)],'normalization':'Only paths/versioncontainers changed. Latest15/16 usefullauthorstandardfinalpacket withACTUALcurrentpreimage andexactSOURCE6/4, nosemanticgrounds inventedbyROOT.'})
wr(B/'peer-snapshot.json',{'actualCurrentPeers':ps+crosspeers,'sameTopicAuthorEvidence':str((A/'printing-15-20/peer-snapshot.json').relative_to(C)),'crossAuthorEvidence':str((A/'cross-primary-qualification/qualification-addendum.json').relative_to(C)),'earlierVersionHistoryPreserved':True,'proposedCards':[{'id':e['id'],'sourceOrder':o,'card':e['proposedCard'],'sha256':sha(e['proposedCard'])} for o,e in sorted(ce.items())]})
wr(B/'normalization-manifest.json',{'purpose':'Technical latest-version merge and C-relative sourcepath repair. Originalqualification15/16intermediatesUNAPPLIED; latestfullstandardfinal15-16 packet usesACTUALCURRENTpreimage andexact6/4. Noqualitycredit','origins':origins,'originalRawSourcesVerified':len(sources),'literalGroups':60,'wholeVariants':40,'currentSameTopicPeers':len(ps),'currentCrossTopicPeers':len(crosspeers),'crossSOURCEFullOriginalRetained':str((A/'cross-primary-qualification/qualification-addendum.json').relative_to(C)),'qualityCredit':0})
s=importlib.util.spec_from_file_location('ap',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
rr=m.apply(B,'01a13f93-17b0-7893-8955-26059d806d41',list(range(11,21)),None,None,None,qualifyOnly=True,peerSnapshot={'actualCurrentPeers':ps});assert len(rr['applied'])==10
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);files=[p for p in A.rglob('*') if p.is_file()]+[p for p in B.rglob('*') if p.is_file()]+[pathlib.Path(__file__)];print('QUALIFIED10',h.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in files],'Preserve SOURCEoriginalbooks11–20 final10 and exactliteralversionmerge noqualitycredit',raw(C/h.git(C,'rev-parse','--git-path','index'))))
