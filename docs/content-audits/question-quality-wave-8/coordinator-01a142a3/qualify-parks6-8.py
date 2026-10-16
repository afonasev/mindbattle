"""Attach exact SOURCE mutual ERVC addendum without changing any card, claim or judgment."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-parks6-15-sourceb7-corrected-01a142a3/author';B=D/'qualified-parks6-8-sourceb7';B.mkdir(exist_ok=False);ad=S/'mutual-ervc-confirmation.json';add=m.read(ad);assert add['owner']=='01a142b7-50b2-7d11-8dd8-0585e2e11218';a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');proposals={e['id']:e['proposedCard']for e in a['entries']}
for p in add['proposals']:assert p['card']==proposals[p['id']]and m.sha(p['card'])==p['canonicalSHA256']
assert len(add['mutualProposedPairs'])==3
for pair in add['mutualProposedPairs']:
 for side in ['left','right']:assert pair[side+'Card']==proposals[pair[side+'Id']]and m.sha(pair[side+'Card'])==pair[side+'CanonicalSHA256']
 assert pair['leftToRight']and pair['rightToLeft']and pair['result']=='DISTINCT'
ps['relevantProposedPairs']=add['mutualProposedPairs'];ps['sourceMutualMainAddendum']={'path':str(ad.relative_to(C)),'rawSHA256':m.raw(ad),'owner':add['owner'],'wordingUnchanged':True}
for x in [a,sp,ps]:x['rootNormalization']={'coordinator':m.O,'sourceOriginalPacket':str(S.relative_to(C)),'sourceOriginalFreeze':'b7733d6845161a7a8411d25d3627485d0fbfd6f2','SOURCEAddendum':str(ad.relative_to(C)),'SOURCEAddendumRawSHA256':m.raw(ad),'transformation':'SOURCE-provided exact fullcards/hash and three bilateral mutual comparisons replace wrong country-as-entity prose; no root semantic judgment or card edit.','qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P;r=app.apply(B,add['owner'],[6,7,8],D/'apply-parks6-8.json',D/'qa-parks6-8.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']});m.write(D/'qualification-parks6-8.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'sourceMutualMainAddendum':ps['sourceMutualMainAddendum'],'mutualFullCardPairs':3,'qualityCredit':0});print('SOURCEFreeze',m.savecode([pathlib.Path(__file__),ad,D/'qualification-parks6-8.json']+list(B.iterdir()),'Freeze fullyqualified SOURCE parks6-8 exact literal countries and SOURCE confirmed mutual ERVC; quality0'))
