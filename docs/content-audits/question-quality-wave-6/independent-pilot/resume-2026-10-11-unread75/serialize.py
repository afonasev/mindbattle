"""Serialize explicit independent manual decisions; assert hashes and six-field shape."""
import json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
label=sys.argv[1];base=ROOT/label
b=json.loads((base/'bindings.json').read_text());d=json.loads((base/'decisions.json').read_text());by={x['questionId']:x for x in b['cards']};rows=[]
for x in d['cards']:
 row=by[x['questionId']];assert len(x['fields'])==6
 fields=[]
 for bound,manual in zip(row['fields'],x['fields']):
  verdict,analysis=manual;assert verdict in ['PASS','HOLD','FIX_REQUIRED'] and analysis
  fields.append({**bound,'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis})
 rows.append({**row,'verdict':x['verdict'],'editorialAnalysis':x['editorialAnalysis'],'fields':fields})
assert set(by)=={x['questionId'] for x in rows}
out={k:v for k,v in b.items() if k not in ['cards','mechanicalOnly']};out.update({'decisionSource':'decisions.json; manual independent source and editorial reading','cards':rows,'independentPass':sum(x['verdict']=='PASS' for x in rows),'independentFixRequired':sum(x['verdict']=='FIX_REQUIRED' for x in rows),'independentHold':sum(x['verdict']=='HOLD' for x in rows),'fieldsRead':6*len(rows),'humanAcceptance':False})
(base/'receipt.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(label,len(rows),out['independentPass'],out['independentFixRequired'],out['independentHold'])
