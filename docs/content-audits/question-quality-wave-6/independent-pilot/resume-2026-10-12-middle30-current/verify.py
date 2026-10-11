# Focused receipt/schema/current-input and full-original Git-byte proof.
import json,hashlib,subprocess
from pathlib import Path
import read_originals as r
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
receipt=json.loads((r.OWN/'receipt.json').read_text());qs={q['id']:q for q in json.loads((r.ROOT/'src/content/topics/middle-ages.json').read_text())['questions']}
assert receipt['actualReaderIdentity']==receipt['agentIdentity']!=receipt['actualAuthorIdentity']
assert len(receipt['cards'])==30 and len(set(receipt['reviewedScope']))==30 and set(receipt['reviewedScope'])==set(receipt['requiredScope']) and not receipt['unreadScope']
assert sha((r.AUTHOR/'author-full-scope-receipt.json').read_bytes())==receipt['authorReceiptRawSha256']
assert (r.AUTHOR/'author-full-scope-receipt.json').read_bytes()==subprocess.check_output(['git','show','2e9289c:'+receipt['authorReceiptPath']],cwd=r.ROOT)
assert (r.ROOT/'src/content/topics/middle-ages.json').read_bytes()==subprocess.check_output(['git','show','2e9289c:src/content/topics/middle-ages.json'],cwd=r.ROOT)
seen=set()
for c in receipt['cards']:
 q=qs[c['questionId']];assert q==c['currentCard'] and sha(canon(q))==c['cardCanonicalSha256'] and c['cardGitBlobMatchesWorking']
 assert len(c['fields'])==6 and [f['field'] for f in c['fields']]==['prompt-key','note0','note1','note2','note3','explanation']
 literals=[[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],*[v['note'] for v in q['answers']],q['explanation']]
 for f,lit in zip(c['fields'],literals):
  assert f['literal']==lit and sha(canon(lit))==f['literalSha256'] and sha(canon(f['indexedLiteral']))==f['indexedLiteralSha256']
  assert f['substantiveRead'] and f['proofs'] and f['status']==f['verdict']
  for p in f['proofs']:
   assert sha(p['passage'].encode())==p['passageSha256']
   b=(r.ROOT/p['rawCapture']).read_bytes();assert sha(b)==p['rawCaptureSha256']==p['fullOriginalRawSha256'];assert b==subprocess.check_output(['git','show',p['gitFreezeCommit']+':'+p['rawCapture']],cwd=r.ROOT)
   seen.add(p['rawCapture'])
manifest=json.loads((r.OWN/'originals-manifest.json').read_text());assert manifest['authorBoundOriginalCount']==33
for s in manifest['originals']:
 b=(r.ROOT/s['path']).read_bytes();assert sha(b)==s['fullRawSha256'];assert b==subprocess.check_output(['git','show',s['freezeCommit']+':'+s['path']],cwd=r.ROOT)
rawcards=json.loads((r.OWN/'raw-card-slices.json').read_text())
for item,c in zip(rawcards,receipt['cards']):assert item['questionId']==c['questionId'] and sha(item['rawUtf8CardSlice'].encode())==item['rawSha256']==c['rawCardSha256'] and json.loads(item['rawUtf8CardSlice'])==c['currentCard']
result={'checks':'PASS','cardCount':30,'fieldCount':180,'actualDistinctIdentityPair':[receipt['actualAuthorIdentity'],receipt['actualReaderIdentity']],'immutableAuthorReceipt':True,'currentMiddleTopicEquals2e9289c':True,'protectedOther70':'entire topic file byte-identical to author freeze; reader made no changes','allOriginalRawWorkingEqualsFrozenGitBlob':True,'boundOriginalCount':33,'allIndexedLiteralAndRawSliceHashesMatch':True,'unreadRemaining':0,'statusCounts':{s:sum(c['status']==s for c in receipt['cards']) for s in ['PASS','FIX','HOLD']},'scope':'focused serialization/current-input/Git byte checks; no runtime tests, full suite, build, deploy or human acceptance'}
(r.OWN/'focused-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
