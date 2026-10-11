"""Reassemble entire numbered original responses; refuse gaps/conflicting overlap. No summary."""
from pathlib import Path
import re,json,hashlib
P=Path(__file__).resolve().parent/'sources'
for target,url,total,names in [('lehman','https://www.lehman.edu/public-art-bronx/glossary/',766,['web-glossaries-original-response.txt','lehman-mid-web-original.txt','lehman-end-web-original.txt','lehman-tail-web-original.txt']),('dob','https://www.nyc.gov/site/buildings/dob/dob-glossary1.page',363,['web-glossaries-original-response.txt','dob-full-web-original.txt'])]:
 lines={};used=[]
 for n in names:
  f=P/n;s=f.read_text();used.append({'path':n,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
  for part in s.split('--------------------------------------------------------------------------------'):
   if url not in part[:200]:continue
   matches=list(re.finditer(r'L(\d+): ',part))
   for i,m in enumerate(matches):
    num=int(m.group(1));value=part[m.end():matches[i+1].start() if i+1<len(matches) else len(part)].rstrip('\n')
    # Tool display changes internal citation ids between calls. Normalize only citation wrappers, retain visible original text.
    value=re.sub(r'\ue200cite\ue202\d+†([^†\ue201]+)(?:†[^\ue201]+)?\ue201',r'\1',value).strip()
    if num in lines and lines[num]!=value:raise ValueError((target,num,lines[num],value))
    lines[num]=value
 missing=[i for i in range(total) if i not in lines];print(target,'missing',missing)
 if missing:continue
 text='\n'.join(f'L{i}: {lines[i]}' for i in range(total))+'\n';(P/(target+'-complete-extracted.txt')).write_text(text)
 (P/(target+'-complete-extracted.txt.http.json')).write_text(json.dumps({'url':url,'status':'EXTRACTED_ORIGINAL_COMPLETE','exitCode':0,'completeOriginalExtract':True,'totalNumberedLines':total,'captureMethod':'Complete web.run original rendered extraction; all original line numbers present in order, overlaps checked; only tool citation wrappers removed, visible text unchanged. No claim selection or summary.','sourceResponses':used},ensure_ascii=False,indent=2)+'\n')
