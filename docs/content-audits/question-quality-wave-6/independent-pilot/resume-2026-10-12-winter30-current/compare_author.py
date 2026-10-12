import json,hashlib,subprocess
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter30-current'
a=json.loads((ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-author30/final-current-author-receipt.json').read_text());qs=json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions']
comp={'authorReceiptIsNotCertification':True,'recipe':'Independent whole-card uses property-order-preserved compactJSON; author hashes independently verified as sort_keys=True compactJSON. Both recipes reported; neither expectedSHA modified. Binding history verbatim, never current proof.','records':[]}
for c in a['cards']:
 q=next(q for q in qs if q['id']==c['questionId']);digest=lambda sort:hashlib.sha256(json.dumps(q,ensure_ascii=False,separators=(',',':'),sort_keys=sort).encode()).hexdigest();assert digest(True)==c['cardCanonicalSha256']
 comp['records'].append({'id':c['questionId'],'currentWholeCardSha256':digest(False),'currentSortedWholeCardSha256':digest(True),'authorSortedWholeCardMatches':True,'authorPromptLiteralOmittedFullOptions':True,'fields':[{'field':f['field'],'authorBindingHistory':f['proofBindings']} for f in c['fields']]})
comp['concreteFindings']=[
'007 prompt-key boot25; note0 binding24 instead ofboot25;note1edge16 instead ofbinding24;note2poles27 instead ofedge16;note3edge16 instead ofpoles27. Whole question reread; no old certificate inherited.',
'023note3 author27 poles; actualbrake25.',
'073note0quoteinterface instead ofbinding;note1quoteedge instead ofinterface;note3page24binding instead ofbrake25. Historical073binding25 failure independently located correct24.',
'076correctnotebearingheight source15; author16standingheight/thickness not complete definition. Historical076note1page25 failure correctly requires24.',
'089note2 author99width notgradient; actual650.3.1physical79. Historical089PASS not inherited; currentwidth40m correctly scopedGS902.1physical104, notminimumallcourses.',
'092historicalnote0page12nationality invalid; current83 supports durations but wrongnote0still leaksfiveyears. note1fouryears must start afterinspection.',
'035authornote0/note1pairs84 does not independently establishdance/singles; oldSkateCanada URL mismatchedpaginatedTbytes. NewfullThrowJumpdirect original used.',
'057/058team pursuit andmassstart needlongtrack97/91 rather than76;058shortgroups need72/75.',
'060explanation needs44forCircle/Line/Wheel requirements in addition to43block.',
'067note0overtime168, note3delayed81;221powerplay alone cannot proveallnotes.',
'082note3author231 isPenalties heading; actualmass234. Olympic2026 raw unavailable remainsHOLD.',
'090note0GS104, note1sum108, note3SG108 rather than109combined.',
'095promptauthor34blocker notcatcher46;note1mask95, note3stick231+blocker34;explanationrequires46+34.'
]
(OUT/'author-locator-comparison.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2)+'\n');print('author sorted hashes 30/30; independent order-preserving hashes retained')
