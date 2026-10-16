"""Reject retained web headers with no visible page body; no semantic PASS."""
import pathlib,re,json,hashlib
def inspect_packet(C,B):
 result=[]
 for source in json.loads((B/'sourceproof.json').read_text())['rawSources']:
  p=C/source['path'];body=p.read_text();digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest==source['sha256']
  headerOnly='Total lines:' in body and re.search(r'\bL[0-9]+:',body) is None
  result.append({'path':str(p.relative_to(C)),'rawSHA256':digest,'headerOnlyNoVisiblePageBody':headerOnly})
 return result
