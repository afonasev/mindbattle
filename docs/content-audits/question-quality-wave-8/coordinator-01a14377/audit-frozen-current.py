"""Audit allselected frozen slots and allcredited CURRENT cardhashes, not fulltests."""
import pathlib,importlib.util,subprocess,json,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ck=m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');sel=ck['selectedCards'];assert len(sel)==2000;topics={x['topicId'] for x in sel};current={};base={}
for topic in topics:
 rel=f'src/content/topics/{topic}.json';live=m.read(m.C/rel);old=json.loads(subprocess.check_output(['git','-C',str(m.C),'show',ck['baselineSHA']+':'+rel],text=True));assert live['id']==old['id']==topic;current[topic]=live['questions'];base[topic]=old['questions']
for v in sel:
 topic=v['topicId'];qid=v['questionId'];pos=next(i for i,q in enumerate(base[topic]) if q['id']==qid);old=base[topic][pos];new=current[topic][pos];assert new['id']==qid and m.sha(old)==v['baselineCanonicalSha256'];assert new['difficulty']==old['difficulty']==v['difficulty'];assert new['correctIndex']==old['correctIndex']==v['correctIndex']
ids=ck['currentEligibleCompletedIds'];n=len(ids);assert len(set(ids))==n;h={x['questionId']:x['cardCanonicalSha256'] for x in ck['completedCardHashes']};live={q['id']:q for t in current.values() for q in t}
for qid in ids:assert m.sha(live[qid])==h[qid],qid
assert set(ids).isdisjoint(ck['currentRemainingIds']);assert set(ids)|set(ck['currentRemainingIds'])=={v['questionId'] for v in sel};assert len(ck['currentRemainingIds'])==2000-n
idx={str(r):m.raw(r/m.h.git(r,'rev-parse','--git-path','index')) for r in [m.C,m.P]};expected=m.read(D/'foreign-index-observed-transition.json')['currentForeignIndexSHAs'];assert idx==expected
p=D/f'current{n}-frozen-live-audit.json';m.write(p,{'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fullGoal':2000,'intakeCURRENT':845,'CURRENT':n,'remaining':2000-n,'newlyCertified':n-845,'waveCURRENT':[w['currentSourceEditorialCards'] for w in ck['waves']],'all2000FrozenIDTopicOrderGradeKeyAndBaselineHashesVerified':True,'allCreditedCurrentHashesVerified':n,'baselineSHA':ck['baselineSHA'],'foreignIndexesPreservedSinceObservedTransition':idx,'fullOriginalScopeRemainsActive':True,'notCompletion':n!=2000});print('audit',m.savecode([p,pathlib.Path(__file__)],f'Audit all2000frozencontracts andCURRENT{n} creditedhashes exactlive'));print(n,2000-n)
