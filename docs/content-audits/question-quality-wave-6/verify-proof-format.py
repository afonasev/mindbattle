"""Mechanical identity/capture checks only. Never creates editorial PASS or coverage."""
import argparse, hashlib, json, re
from pathlib import Path
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)

def digest(value): return hashlib.sha256(value).hexdigest()
def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def norm(value): return ' '.join(value.split())

def validate(receipt_path, repo):
    receipt_path=Path(receipt_path).resolve(); repo=repo.resolve(); receipt=json.loads(receipt_path.read_text())
    errors=[]; checks=[]
    if receipt.get('role') not in ('author','independent'): errors.append('Missing explicit role')
    if not receipt.get('agentIdentity'): errors.append('Missing explicit reader identity')
    catalog={c['id']:c for p in (repo/'src/content/topics').glob('*.json') for c in json.loads(p.read_text())['questions']}
    for row in receipt.get('cards',[]):
        qid=row.get('questionId'); card=catalog.get(qid)
        if card is None: errors.append(f'{qid}: unknown ID'); continue
        if row.get('cardCanonicalSha256')!=digest(canonical(card)): errors.append(f'{qid}: current card hash mismatch')
        expected={'prompt-key':canonical([card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']]),'explanation':card['explanation'].encode(),**{f'note{i}':a['note'].encode() for i,a in enumerate(card['answers'])}}
        fields=row.get('fields',[])
        if sorted(f.get('field','') for f in fields)!=sorted(expected): errors.append(f'{qid}: six-field shape mismatch')
        for f in fields:
            name=f.get('field'); label=f'{qid}/{name}'
            if name not in expected: continue
            if f.get('literalSha256')!=digest(expected[name]): errors.append(f'{label}: current literal hash mismatch')
            if not f.get('claimAnalysis'): errors.append(f'{label}: missing claim analysis')
            if f.get('verdict')=='PASS' and (f.get('substantiveRead') is not True or not f.get('proofs')): errors.append(f'{label}: PASS missing actual receipt/proof')
            for proof in f.get('proofs',[]):
                for key in ('sourceClass','title','url','captureFormat','captureMethod','locator','passage','passageSha256'):
                    if not proof.get(key): errors.append(f'{label}: missing {key}')
                raw=receipt_path.parent/proof.get('rawCapture','INVALID'); quote=proof.get('passage','')
                if not raw.is_file(): errors.append(f'{label}: missing raw {raw}'); continue
                body=raw.read_bytes()
                if digest(body)!=proof.get('rawCaptureSha256'): errors.append(f'{label}: original raw hash mismatch')
                if digest(quote.encode())!=proof.get('passageSha256'): errors.append(f'{label}: passage hash mismatch')
                locator=proof.get('locator'); matched=False; mode=''
                if quote.startswith('VISUAL OBSERVATION'):
                    matched=bool(locator) and (raw.suffix.lower() in ('.jpg','.jpeg','.png') or isinstance(locator,dict) and locator.get('pdfPage') and locator.get('figure'))
                    mode='manual visual source receipt; no automated factual certification'
                elif raw.suffix.lower()=='.pdf':
                    from pypdf import PdfReader
                    page=locator.get('pdfPage') if isinstance(locator,dict) else None
                    if page:
                        extracted=PdfReader(raw).pages[page-1].extract_text(); matched=quote in extracted; mode='exact PDF page extracted scalar'
                    else: errors.append(f'{label}: missing PDF page locator')
                else:
                    extracted=body.decode('utf-8')
                    if raw.suffix.lower() in ('.html','.htm'):
                        parser=Text();parser.feed(extracted);extracted=' '.join(parser.parts)
                    matched=quote in extracted
                    mode='exact original extracted text scalar'
                    if not matched and norm(quote) in norm(extracted):
                        matched=True; mode='declared whitespace-only rendered-text match'
                if not matched: errors.append(f'{label}: passage not found in bound original capture')
                checks.append({'field':label,'rawCapture':str(raw.relative_to(repo)),'sourceMatch':matched,'mode':mode})
    return {'receipt':str(receipt_path.relative_to(repo)),'role':receipt.get('role'),'agentIdentity':receipt.get('agentIdentity'),'cardRecords':len(receipt.get('cards',[])),'mechanicalChecks':checks,'errors':errors,'mechanicallyValid':not errors,'newSubstantiveVerdictsCreated':0,'newCompletedCards':0,'limits':['Only hashes, source byte identity and quoted-passage existence are mechanically checked.','Image/figure claims retain explicit actual visual receipt; this script does not read or certify them.','Human editorial/source judgments and independent full-card decisions are separate.']}

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('receipt');cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--output',type=Path,required=True);args=cli.parse_args();result=validate(args.receipt,args.repo);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='mechanicalChecks'},ensure_ascii=False));raise SystemExit(0 if result['mechanicallyValid'] else 1)
