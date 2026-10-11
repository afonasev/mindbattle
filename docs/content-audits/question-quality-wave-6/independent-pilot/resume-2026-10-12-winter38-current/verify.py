"""Mechanical readback only; does not assess claims or change verdicts."""
import json,hashlib,subprocess,runpy,sys
sys.dont_write_bytecode=True
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def gitblob(p):return subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(ROOT))],cwd=ROOT)
def main(name='readback.json'):
 reader=runpy.run_path(str(OUT/'read_originals.py'));Visible=reader['Visible'];PdfReader=reader['PdfReader'];extractions={}
 receipt=json.loads((OUT/'receipt.json').read_bytes());cards={c['id']:c for c in json.loads((ROOT/'src/content/topics/winter-sports.json').read_bytes())['questions']};proof_count=0;mismatches=[]
 assert receipt['agentIdentity']!=receipt['authorIdentity']
 for r in receipt['cards']:
  c=cards[r['questionId']];assert r['cardquestionId']==c['id'];assert sha(canonical(c))==r['cardCanonicalSha256'];assert set(f['field'] for f in r['fields'])=={'prompt-key','note0','note1','note2','note3','explanation'}
  for f in r['fields']:
   value=canonical([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]) if f['field']=='prompt-key' else (c['explanation'] if f['field']=='explanation' else c['answers'][int(f['field'][-1])]['note']).encode()
   assert sha(value)==f['literalSha256'];assert f['literal'].encode()==value;assert f['substantiveRead'] is True;assert f['claimAnalysis'];assert f['proofs']
   for s in f['proofs']:
    p=ROOT/s['rawCapture']
    if str(p) not in extractions:
     if p.suffix=='.pdf':nodes=[page.extract_text() or '' for page in PdfReader(p).pages]
     else:parser=Visible();parser.feed(p.read_bytes().decode('utf-8',errors='replace'));nodes=parser.nodes
     extractions[str(p)]=nodes
    nodes=extractions[str(p)];loc=s['locator'];joiner='\n' if 'newline-joined' in s.get('passageLiteralRecipe','') else ' '
    extracted=nodes[loc['pdfPage']-1] if 'pdfPage' in loc else joiner.join(nodes[loc['textNodeStart']:loc['textNodeEnd']+1]);assert extracted==s['passage'],(c['id'],f['field'],s['locator'])
    assert sha(p.read_bytes())==s['rawCaptureSha256'];assert sha(gitblob(p))==s['rawCaptureSha256'];assert sha(s['passage'].encode())==s['passageSha256'];proof_count+=1
    if not s['independentLocatorMatches']:mismatches.append({'questionId':c['id'],'field':f['field'],'locator':s['locator']})
 for b in receipt['authorBindings']:
  p=ROOT/b['path'];assert sha(p.read_bytes())==b['sha256'];assert sha(gitblob(p))==b['sha256']
 for row in json.loads((OUT/'current-visible-text-readback.json').read_text()):
  p=ROOT/row['currentRawCapture'];assert sha(p.read_bytes())==row['currentRawCaptureSha256'];assert sha(gitblob(p))==row['currentRawCaptureSha256'];assert row['allVisibleNodesEqual'] is True
 p=OUT/'receipt.json';assert p.read_bytes()==gitblob(p)
 result={'kind':'mechanical-git-roundtrip-not-editorial-acceptance','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'cards':len(receipt['cards']),'fields':len(receipt['cards'])*6,'proofs':proof_count,'wholeCardAndLiteralHashesMatch':True,'diskAndGitSourceBytesExact':True,'receiptDiskAndGitExact':True,'authorFrozenReceiptsExact':True,'independentRawSourceExtractionAndPassageSHAExact':True,'locatorMismatches':mismatches,'unreadIds':receipt['unreadIds']}
 (OUT/name).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
 import sys;main(sys.argv[1] if len(sys.argv)>1 else 'readback.json')
