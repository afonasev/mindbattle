"""Serialize explicit reader decisions; only existence/hash/quote mechanics, no verdict creation."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).parent
REPO=ROOT.parents[4]
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def run(name):
 decisions=json.loads((ROOT/(name+'-decisions.json')).read_text());index=json.loads((ROOT/'source-index.json').read_text());path=REPO/'src/content/topics/winter-sports.json';topic=json.loads(path.read_text());byid={c['id']:c for c in topic['questions']};rows=[]
 for d in decisions['cards']:
  c=byid[d['questionId']];fields=d['fields'];assert len(fields)==6
  c['prompt']=d['prompt'];c['answers']=[{'text':t,'note':fields[i+1]['literal']} for i,t in enumerate(d['answers'])];c['explanation']=fields[5]['literal'];key=fields[0]['proofRefs'][0][0];c['source']={'title':d['sourceTitle'],'url':index[key]['http']['url'],'verifiedAt':'2026-10-11'}
  frows=[]
  for i,f in enumerate(fields):
   assert f['verdict'] in ('PASS','HOLD','FIX_REQUIRED') and f['substantiveRead'] is True
   namefield=['prompt-key','note0','note1','note2','note3','explanation'][i];literal=canonical([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]) if i==0 else f['literal'].encode();proofs=[]
   for src,first,last in f['proofRefs']:
    s=index[src];passage=s['nodes'][first] if s.get('format')=='pdf' else ' '.join(s['nodes'][first:last+1]);assert passage
    proofs.append({'sourceClass':'primary sports governing institution','title':src+' — institutional original','url':s['http']['url'],'rawCapture':s['rawCapture'],'rawCaptureSha256':s['rawCaptureSha256'],'captureFormat':'pdf original bytes with pdfPage locator' if s.get('format')=='pdf' else 'html original bytes','captureMethod':s['http']['method']+'; text locator uses '+s['extraction'],'locator':{'pdfPage':first+1} if s.get('format')=='pdf' else {'textNodeStart':first,'textNodeEnd':last,'index':'source-index.json/'+src},'passage':passage,'passageSha256':sha(passage.encode())})
   frows.append({'field':namefield,'literalSha256':sha(literal),'verdict':f['verdict'],'substantiveRead':f['substantiveRead'],'claimAnalysis':f['claimAnalysis'],'proofs':proofs})
  rows.append({'questionId':c['id'],'cardCanonicalSha256':sha(canonical(c)),'verdict':d['verdict'],'editorialAnalysis':d['editorialAnalysis'],'fields':frows})
 path.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n')
 (ROOT/(name+'-receipt.json')).write_text(json.dumps({'role':'author','agentIdentity':'01a12ba2-6af8-79b3-96c4-14a4e60812b6','decisionSource':name+'-decisions.json','cards':rows},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
