"""Apply qualified solecycle1 SOURCE2 after priorCURRENT27 review completed."""
import pathlib,json,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('m',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books26-28-cycle1-and-locator3-01a13f31/author';p=m.read(A/'peer-snapshot.json');cat={}
for t in {x['topicId'] for x in p['actualCurrentPeers']}:cat.update({q['id']:q for q in m.read(C/f'src/content/topics/{t}.json')['questions']})
for x in p['actualCurrentPeers']:assert x['card']==cat[x['id']] and m.sha(x['card'])==x['sha256']
same={'actualCurrentPeers':[x for x in p['actualCurrentPeers'] if x['topicId']=='books-publishing']};r=m.apply(A,'01a13fc7-e37f-7822-9f37-2f69122dc2fe',[26,28],None,None,None,qualifyOnly=True,peerSnapshot=same);assert len(r['applied'])==2
m.apply(A,'01a13fc7-e37f-7822-9f37-2f69122dc2fe',[26,28],D/'apply-books26-28-cycle1.json',D/'qa-books26-28-cycle1.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['SOLEcycle1 INITIALFIX26/28: copyeditorRussianroleterm, Halifax60capHomeDeliveryexemption andrenewalperiodscope. Preserve60/conditions; no generalizationoutsideHalifax.','FullSOURCE6/4 andsourceCURRENT135peers includingnew27 readbyAUTHOR. NEWFINALmustpersonallyreadall2/currentprimarylimits/notes, notinheritSOURCEPASS.','SOURCElocator3 repairfor22/23/30 isproof-onlyseparatealreadycertified; thosecardtextsnotmodified. Canonicalwrongnotefactpoolallowed.'])
