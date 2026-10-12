from prepare import ROOT,OUT,Nodes,sha
import json,urllib.request,subprocess
from pypdf import PdfReader
manifest=json.loads((OUT/'sources-manifest.json').read_text())
urls={
'fis-current-index.html':'https://www.fis-ski.com/alpine-skiing/documents',
'isu-current-index.html':'https://www.isu.org/en/synchronized-skating-rules',
'isu-current-download.pdf':'https://isudam.blob.core.windows.net/isudamcontainer/2026-SYS-Sports-Rules-FINAL-20260511-as-of-1-June-2026-1780065543-2454.pdf',
'skate-throw-complete.html':'https://info.skatecanada.ca/index.php/en-ca/other-categories/defined-terms/uncategorised/566:throw-jump.html',
'owg2026-biathlon-description.pdf':'https://wmr-static-assets.scd.dgplatform.net/wmr/static/_PDF/OWG2026/BTH/2026-02-02/BTH-------------------------------__N02A_1.0.pdf'
}
for name,url in urls.items():
 if (OUT/'sources'/name).exists():
  data=(OUT/'sources'/name).read_bytes();final=url;headers={'capture-provenance':'Original request URL; first successful complete response preserved, prior acquisition aborted on subsequent DNS error; response headers were not persisted.'}
 else:
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:
    data=response.read();final=response.geturl();headers=dict(response.headers)
  except Exception as exc:
   (OUT/'acquisition-gap.json').write_text(json.dumps({'url':url,'error':str(exc),'verdict':'HOLD for Olympic 2026-specific claims; web-rendered PDF is not a captured raw original'},indent=2)+'\n')
   continue
 (OUT/'sources'/name).write_bytes(data)
 entry={'id':name,'originalUrl':url,'captureUrl':final,'sourceClass':'primary sport federation / official Olympic competition description','rawFormat':'PDF original bytes' if name.endswith('.pdf') else 'HTML original bytes','size':len(data),'sha256':sha(data),'gitBlob':subprocess.check_output(['git','hash-object','--no-filters','--stdin'],input=data,cwd=ROOT).decode().strip(),'path':str((OUT/'sources'/name).relative_to(ROOT)),'httpHeaders':headers}
 if name.endswith('.pdf'):
  pdf=PdfReader(OUT/'sources'/name);entry['pages']=len(pdf.pages);text={'physicalPages1Based':{str(i+1):p.extract_text() for i,p in enumerate(pdf.pages)}}
 else:
  p=Nodes();p.feed(data.decode('utf8',errors='replace'));text={'recipe':'stdlib HTMLParser convert_charrefs=True; strip nonempty data outside script/style; zero based','textNodes':p.nodes};entry['closedHtml']=b'</html>' in data.lower()
 (OUT/'readings'/(name+'.json')).write_text(json.dumps(text,ensure_ascii=False,indent=2)+'\n');manifest.append(entry)
 print(name,len(data),sha(data))
for m in manifest:
 if m['id']=='isu-sys-rules-2026.pdf':
  m['declaredAuthorUrlWasLandingPage']=m['originalUrl'];m['originalUrl']=urls['isu-current-download.pdf'];m['captureUrl']=urls['isu-current-download.pdf'];m['readerResolvedDownload']=True
 if m['id']=='skate-terms180.html':m['usableAsEvidence']=False;m['reason']='Author supplied URL returns STAR requirements; frozen bytes are paginated Defined Terms T slice. No independently verified request provenance. Superseded by full direct Throw Jump HTML.'
(OUT/'sources-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('isu download matches frozen', (OUT/'sources/isu-current-download.pdf').read_bytes()==(OUT/'sources/isu-sys-rules-2026.pdf').read_bytes())
