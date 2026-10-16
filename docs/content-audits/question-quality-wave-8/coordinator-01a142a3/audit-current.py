"""Read-only frozen selection and eligible live-hash audit; stores evidence only."""
import pathlib,importlib.util,subprocess,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('own',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ck=m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');catalog={};positions={};baseline={};bpositions={}
for t in {e['topicId']for e in ck['selectedCards']}:
 current=m.read(C/f'src/content/topics/{t}.json')['questions'];base=__import__('json').loads(subprocess.check_output(['git','-C',str(C),'show',ck['baselineSHA']+f':src/content/topics/{t}.json']))['questions']
 for n,q in enumerate(current):catalog[q['id']]=(t,q);positions[q['id']]=n
 for n,q in enumerate(base):baseline[q['id']]=(t,q);bpositions[q['id']]=n
assert len(ck['selectedCards'])==2000
for e in ck['selectedCards']:
 i=e['questionId'];t,q=catalog[i];bt,b=baseline[i];assert t==bt==e['topicId'];assert b['difficulty']==q['difficulty']==e['difficulty'] and b['correctIndex']==q['correctIndex']==e['correctIndex'];assert m.sha(b)==e['baselineCanonicalSha256'];assert positions[i]==bpositions[i]
ids=ck['currentEligibleCompletedIds'];assert len(ids)==len(set(ids))==len(ck['completedCardHashes'])==828
for e in ck['completedCardHashes']:assert e['questionId']in ids and m.sha(catalog[e['questionId']][1])==e['cardCanonicalSha256']
out=D/'intake828-frozen-live-audit.json';m.write(out,{'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT':828,'remaining':1172,'selectedFrozenVerified':2000,'eligibleCardHashesVerified':828,'mismatches':0,'baseline':ck['baselineSHA'],'pendingAppliedUncertified':['books-publishing-scroll-form','national-parks-nature-002'],'qualityCredit':0,'waveCURRENT':[w['currentSourceEditorialCards']for w in ck['waves']]});print(m.savecode([pathlib.Path(__file__),out],'Verify successor intake828 live hashes and all exact2000 frozen metadata/order'))
