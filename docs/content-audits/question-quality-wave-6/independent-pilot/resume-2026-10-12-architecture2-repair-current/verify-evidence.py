import json,hashlib,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
r=json.loads((OUT/'independent-receipt.json').read_text());checks=[]
ref=__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'HEAD'
for source in json.loads((OUT/'source-readback.json').read_text())['sources']:
 path=OUT/source['rawCapture'];blob=subprocess.check_output(['git','show',ref+':'+str(path.relative_to(ROOT))],cwd=ROOT)
 assert sha(blob)==source['rawCaptureSha256'] and blob==path.read_bytes()
 original=subprocess.check_output(['git','show',source['frozenRevision']+':'+source['originalPath']],cwd=ROOT)
 assert blob==original
 checks.append({'source':source['rawCapture'],'sha256':sha(blob),'bytes':len(blob),'gitRef':ref,'committedEqualsOriginalAndWorktree':True})
for card in r['cards']:
 assert sha(canonical(card['currentCard']).encode())==card['cardCanonicalSha256']
 for field in card['fields']:
  assert sha(field['literal'].encode())==field['literalSha256']
  for proof in field['proofs']:
   assert sha(proof['passage'].encode())==proof['passageSha256']
   if proof['rawQuotedLiteral'] is not None:
    assert sha(proof['rawQuotedLiteral'].encode())==proof['rawQuotedLiteralSha256']
    assert proof['rawQuotedLiteral'].encode() in (OUT/proof['rawCapture']).read_bytes()
result={'cards':2,'fields':12,'sources':len(checks),'canonicalLiteralAndPassageHashChecks':'PASS','originalToCommittedSourceByteRoundtrip':'PASS','checks':checks,'limits':'Mechanical hash preservation only; manual source/editorial judgments are in independent-receipt.json.'}
(OUT/'git-roundtrip.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
