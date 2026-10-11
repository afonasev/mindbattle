"""Serialize written manual decisions only; assertions never create editorial PASS."""
import json,hashlib,os
from pathlib import Path
OUT=Path(__file__).resolve().parent
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(x.encode()).hexdigest()
def sourceclass(url):
 if 'olympic.ca' in url:return 'Canadian Olympic Committee — primary national Olympic institution'
 if 'hockeycanada.ca' in url:return 'Hockey Canada — primary national hockey governing institution'
 if 'iihf.com' in url:return 'IIHF — primary international hockey governing institution'
 if 'fis-ski.com' in url:return 'FIS — primary international ski governing institution'
 if 'skatecanada.ca' in url:return 'Skate Canada — primary national skating governing institution'
 if 'biathlonworld.com' in url:return 'IBU — primary international biathlon governing institution'
 if 'bobsleighcanadaskeleton.ca' in url:return 'Bobsleigh Canada Skeleton — primary national sport governing institution'
 if 'wtgf.org' in url:return 'World Transplant Games Federation — primary event sporting institution'
 if 'maine.gov' in url:return 'Maine Legislature — primary statute publisher'
 if 'isudam.' in url:return 'ISU — primary international skating governing institution'
 raise ValueError(url)
def main():
 original=json.loads((OUT/'originals-and-bindings.json').read_text());byid={r['card']['id']:r for r in original['cards']};decisions=json.loads((OUT/'decisions.json').read_text());cards=[]
 for d in decisions['cards']:
  r=byid[d['questionId']];c=r['card'];fmap={f['field']:f for f in r['fields']};fields=[];assert len(d['fields'])==6
  for f in d['fields']:
   assert f['verdict'] in ('PASS','FIX_REQUIRED','HOLD');assert f['claimAnalysis']
   orig=fmap[f['field']];literal=canonical([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]) if f['field']=='prompt-key' else orig['literal'];proofs=[]
   for p in orig['proofs']:
    p=dict(p);p['sourceClass']=sourceclass(p['url']);p.pop('independentExtractedPassage');proofs.append(p)
   fields.append({**f,'literal':literal,'literalSha256':sha(literal),'substantiveRead':True,'proofs':proofs})
  cards.append({'cardquestionId':c['id'],'questionId':c['id'],'cardCanonicalSha256':r['cardCanonicalSha256'],'verdict':d['verdict'],'editorialAnalysis':d['editorialAnalysis'],'authorReceipt':r['authorReceipt'],'fields':fields})
 result={'role':'distinct-independent-current-reader','agentIdentity':os.environ['CODEX_THREAD_ID'],'authorIdentity':original['authorIdentity'],'sourceSnapshotCommit':original['snapshotCommit'],'literalRecipe':{'prompt-key':'UTF-8 canonical JSON array [prompt,correctIndex,keytext]; ensure_ascii=False sort_keys=True separators=(comma,colon)','note0..note3/explanation':'UTF-8 exact literal string','wholeCard':'UTF-8 canonical JSON object ensure_ascii=False sort_keys=True separators=(comma,colon)'},'authorBindings':original['authorBindings'],'cards':cards,'unreadIds':[r['card']['id'] for r in original['cards'] if r['card']['id'] not in {c['questionId'] for c in cards}]}
 (OUT/'receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(len(cards),'cards',len(cards)*6,'manually decided fields; UNREAD',len(result['unreadIds']))
if __name__=='__main__':main()
