"""Transport exact full original SOURCE USNO glossary output, no semantic edits."""
import pathlib,importlib.util,json
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S=D.parent/'process-v2-polar5-6-8-10-fresh-01a14321/author/polar5-cycle1/proof-completion';B=D/'qualified-polar5-cycle1';B.mkdir(exist_ok=False);uid='01a14327-fb48-70e1-8d55-3db044c2d83b';js=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'));assert len(js)==1;records=[]
for n,line in enumerate(js[0].open(),1):
 e=json.loads(line);d=e.get('payload',{})
 if e.get('type')=='response_item' and d.get('type')=='custom_tool_call_output' and d.get('call_id')=='call_3aff2627ea2e4346a746bae8ef15f399':records.append({'nativeJournal':str(js[0]),'line':n,'timestamp':e['timestamp'],'callId':d['call_id'],'originalVisibleOutput':d['output']})
assert len(records)==1;raw=D/'source-captures/source27-usno-glossary-original-open.json';m.write(raw,{'sourceActor':uid,'transport':'Exact full original SOURCE visible webopen USNO glossary context, no manual selected excerpt.','records':records});a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');old=next(s for s in sp['rawSources'] if s['url']=='https://aa.usno.navy.mil/faq/asa_glossary');oldpath=old['path'];rp=str(raw.relative_to(C));assert old['url'] in raw.read_text();sp['rawSources']=[s for s in sp['rawSources'] if s is not old]+[{'path':rp,'url':old['url'],'sha256':m.raw(raw),'originalSourceRecord':old,'locator':'Original SOURCE USNO glossary webopen native line458, complete original glossary context; month entriesL384-L387. Preserve original pergroup/variant locators.','captureReadProvenance':'Exact personally opened SOURCE27 original full visible context, mechanically transported by root; no new authorjudgment.'}]
for e in sp['entries']:
 for g in e['literalGroups']:g['sourcePaths']=[rp if p==oldpath else p for p in g['sourcePaths']]
 for v in e['fourFullPromptAnswerNoteAssessments']:v['sourcePaths']=[rp if p==oldpath else p for p in v['sourcePaths']]
for o in [a,sp,ps]:o['rootNormalization']={'owner':m.O,'originalPacket':str(S.relative_to(C)),'originalFreeze':'ad230fc10f9a7a72636535254ed334e554540ac5','transformations':['Manual USNO quote capture replaced by exact original SOURCE full glossary output; paths/hash only'],'semanticRootEdits':False,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
print(m.savecode([pathlib.Path(__file__),raw,*B.glob('*.json')],'Freeze polar5 SOURCEcycle1 fulloriginal USNO context mechanicaltransport beforesecond'))
