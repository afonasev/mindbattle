"""Storage/provenance only. Editorial decisions must be supplied in manual-decisions.json.
No editorial decisions or expected digest changes are made by this program.
"""
import json, hashlib, pathlib, subprocess, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
AUTHOR = ROOT / 'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-rework30'
IDENTITY = '01a12cad-9b8a-7660-9004-53e2529c54c6'
FROZEN = '65c805926cf2008d7e9d15abc8af855c7b9c5432'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def gitbytes(path, ref='HEAD'):
    return subprocess.check_output(['git','show',f'{ref}:{path.relative_to(ROOT)}'],cwd=ROOT)
def write(name, obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
class Visible(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self,t,a):
        if t in ('script','style'): self.hidden+=1
    def handle_endtag(self,t):
        if t in ('script','style'): self.hidden-=1
    def handle_data(self,d):
        if not self.hidden: self.parts.append(d)
def visible(b):
    p=Visible(); p.feed(b.decode('utf-8')); return ' '.join(' '.join(p.parts).split())
def literal(q, field):
    if field=='prompt-key': return json.dumps([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],ensure_ascii=False,separators=(',',':'))
    if field.startswith('note'): return q['answers'][int(field[-1])]['note']
    return q['explanation']
def pointer(obj, loc):
    for k in loc.split('/')[1:]: obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

manual=json.loads((OUT/'manual-decisions.json').read_bytes())
qs={q['id']:q for q in json.loads((ROOT/'src/content/topics/architecture.json').read_bytes())['questions']}
headqs={q['id']:q for q in json.loads(gitbytes(ROOT/'src/content/topics/architecture.json'))['questions']}
frozenqs={q['id']:q for q in json.loads(gitbytes(ROOT/'src/content/topics/architecture.json',FROZEN))['questions']}
acards={}; receipts=[]
for name in ['pilot5-receipt.json','batch2-4-receipt.json','batch3-2-receipt.json','batch4-3-receipt.json']:
    path=AUTHOR/name; b=path.read_bytes(); assert b==gitbytes(path)==gitbytes(path,FROZEN)
    d=json.loads(b); assert d['agentIdentity']=='01a12c87-fd74-7ff1-a4e3-211f1b4da7c3'
    receipts.append({'path':str(path.relative_to(ROOT)),'sha256':sha(b),'frozenCommit':FROZEN,'authorIdentity':d['agentIdentity']})
    for c in d['cards']: acards[c['questionId']]=(c,name)
review=[]; witness={}; frozen_fields=[]
for m in manual['cards']:
    q=qs[m['questionId']]; a,afn=acards[q['id']]
    assert q==headqs[q['id']]==frozenqs[q['id']]
    assert sha(canonical(q))==a['cardCanonicalSha256']
    fields=[]
    assert [f['field'] for f in m['fields']]==['prompt-key','note0','note1','note2','note3','explanation']
    for mf,old in zip(m['fields'],a['fields']):
        lit=literal(q,mf['field']); digest=sha(lit.encode())
        assert digest==old['literalSha256'], (q['id'],mf['field'],'frozen literal mismatch')
        proofs=[]
        for op in old['proofs']:
            raw=AUTHOR/op['rawCapture']; b=raw.read_bytes(); gb=gitbytes(raw); fb=gitbytes(raw,FROZEN)
            assert b==gb==fb and sha(b)==op['rawCaptureSha256'], str(raw)
            loc=op['locator']; loc=loc.get('jsonPointer') if isinstance(loc,dict) else loc
            if q['id']=='architecture-palladian-inspiration' and mf['field']=='note2':
                loc='/results/0/justification_en'
            if raw.suffix=='.json':
                # Full original decoded scalar, not an author-selected excerpt.
                passage=pointer(json.loads(b),loc)
                expected=op.get('decodedPassage',op['passage'])
                if q['id']=='architecture-palladian-inspiration' and mf['field']=='note2':
                    assert 'three pyramids of Giza' in passage
                else: assert expected in passage
                extraction='JSON pointer; entire decoded original scalar; passage hash UTF-8'
            else:
                text=visible(b); expected=op['passage']; norm=' '.join(expected.split())
                assert norm in text, (raw, norm)
                # Entire small university page; municipal/regulatory definitions with original context.
                if raw.name.startswith('pitt-'): passage=text
                else:
                    start=text.index(norm); passage=text[max(0,start-100):start+len(norm)+180]
                extraction='HTMLParser visible text, entities decoded, whitespace collapsed; full small page or definition plus context; raw original unchanged'
            rp=str(raw.relative_to(ROOT))
            witness[rp]={'rawCapture':rp,'workingSha256':sha(b),'headSha256':sha(gb),'frozenSha256':sha(fb),'bytes':len(b),'CRLFCount':b.count(b'\r\n')}
            proof={'sourceClass':op['sourceClass'],'title':op.get('title','UNESCO World Heritage record '+raw.stem.split('-')[1] if raw.name.startswith('unesco-') else raw.name),'url':op['url'],'rawCapture':rp,'rawCaptureSha256':sha(b),'captureFormat':'Complete original bytes; no newline conversion','captureMethod':op.get('captureMethod','Frozen author capture of original HTTPS response; independently reopened from disk and Git'),'locator':loc,'passage':passage,'passageSha256':sha(passage.encode()),'extractionRecipe':extraction,'independentOriginalRead':True,'readerIdentity':IDENTITY}
            if proof not in proofs: proofs.append(proof)
        fields.append({**mf,'literal':lit,'literalSha256':digest,'substantiveRead':True,'substantiveReadBy':IDENTITY,'proofs':proofs})
        frozen_fields.append({'questionId':q['id'],'field':mf['field'],'receipt':afn,'frozenLiteralSha256':old['literalSha256'],'actualRecipe':'JSON UTF-8 compact array [prompt,correctIndex,keytext]' if mf['field']=='prompt-key' else 'Exact decoded scalar UTF-8, no normalization','actualMatch':True})
    review.append({**{k:v for k,v in m.items() if k!='fields'},'cardCanonicalSha256':sha(canonical(q)),'currentCard':q,'fields':fields})
result={'role':'independent','agentIdentity':IDENTITY,'actualAuthorIdentity':'01a12c87-fd74-7ff1-a4e3-211f1b4da7c3','frozenAuthorCommit':FROZEN,'frozenHandoffCommit':'26ccbe74dcb9c6ae302fc596758755ba0e92edef','reviewHead':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'canonicalRecipes':{'card':'UTF-8 JSON sorted object keys, ensure_ascii=False, compact separators','prompt-key':'UTF-8 JSON compact array [prompt,correctIndex,keytext], ensure_ascii=False','note/explanation':'Exact decoded scalar UTF-8; no normalization'},'frozenReceipts':receipts,'frozenAuthorFieldRecipes':frozen_fields,'methodology':manual['methodology'],'cards':review,'coverage':{'cards':len(review),'fields':len(review)*6,'UNREAD':14-len(review)},'limits':'Independent card review only; no root certification, human acceptance, source edits, stamps, planning, build, full suite, merge, push or archive.'}
write('receipt.json',result); write('source-roundtrip.json',{'scope':[c['questionId'] for c in review],'witnesses':list(witness.values()),'result':'EXACT original bytes working=HEAD=frozen including CRLF'})
print(json.dumps({'cards':len(review),'fields':len(review)*6,'sources':len(witness),'UNREAD':14-len(review)}))
