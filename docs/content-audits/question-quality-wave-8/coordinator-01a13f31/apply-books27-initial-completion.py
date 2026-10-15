"""Finish original SOURCE10 with qualified27 and exact personallyread peer4 delta."""
import pathlib,json,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
def rd(p):return json.loads(pathlib.Path(p).read_text())
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('m',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books21-30-01a13f31/author';B=A/'source27-completion';cand=rd(B/'candidate.json')['entries'][0];current=rd(C/'src/content/topics/books-publishing.json')['questions'];cm={q['id']:q for q in current};delta={};files=[B/'same-original-source9-peer-refresh-after-fix4.json',B/'newtwo-peer15-18-completion.json']
for fp in files:
 j=rd(fp);pr=j['source27Proposal'];assert any(pr.get(k)==cand['proposedCard'] for k in ['card','proposedCard'])
 for e in j['actualCurrentCards']:
  assert e['card']==cm[e['id']] and m.sha(e['card'])==e['sha256'];delta[e['id']]=e
ids=[current[o-1]['id'] for o in [12,15,17,18]];assert all(i in delta for i in ids)
dp=D/'SOURCE27-personally-read-current-peer4-delta.json';wr(dp,{'actualCurrentPeers':[delta[i] for i in ids],'authorPersonalReadEvidence':[str(p.relative_to(C)) for p in files],'scope':'SOURCEoriginal9/27 same-slice peercompletion, fresh4 CURRENT cards andbilateralMAIN grounds retained. No targetSOURCEliteralchangedbyROOT.'})
ps=rd(B/'peer-snapshot.json');cat={}
for t in {p['topicId'] for p in ps['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in ps['actualCurrentPeers']:
 p=delta.get(p['id'],p);assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
same={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='books-publishing']};rr=m.apply(B,'01a13fb8-287d-7753-8f8f-a92c6dac33c0',[27],None,None,None,qualifyOnly=True,peerAddendum=dp,peerSnapshot=same);assert len(rr['applied'])==1
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);allfiles=[p for p in A.rglob('*') if p.is_file()]+[dp,pathlib.Path(__file__),D/'planning-certification-guard.py',D/'verify-planning-certification-guard.py',D/'planning-certification-guard-verification.json'];print('SOURCE10completeFreeze',h.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in allfiles],'Preserve completeoriginalSOURCEbooks21–30 and exactfreshpeer4/guard evidence noqualitycredit',m.raw(C/h.git(C,'rev-parse','--git-path','index'))))
m.apply(B,'01a13fb8-287d-7753-8f8f-a92c6dac33c0',[27],D/'apply-books27-initial-completion.json',D/'qa-books27-initial-completion.json',pathlib.Path(__file__),peerAddendum=dp,peerSnapshot=same,concerns=['OriginalSOURCEHOLD27 termtypesettertoo-specialforEASY replacedgenuinepracticalbookgutterproblem usingnewKDPprimary; remainsINITIAL no priorOTHERreview27. Frozen5unchanged.','Fourrealprintlayoutparameters, exactprimaryscopeKDP externalmargin/bleed/trimsize andpagecountgutterlimits. FreshOTHERjudgeEASY/plausibility/onekey/ownextra andCURRENTbooks+design MAINglobalneighbors.','OriginalSOURCE9targets unchanged byall4previouspeerupdatesandnew27; SOURCEsameauthorpersonallyreadnew4, SOURCE27 authored/comparedwithCURRENT9. ActiveINITIAL9review needsonlynewpeer27 freshcomparison/newlatestQA snapshot.'])
