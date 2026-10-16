"""Preserve exact original SOURCE visible primary outputs; alias/source-path transport only."""
import pathlib,importlib.util,json,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S=D.parent/'process-v2-parks13-cycle1-fresh-01a14321/author';B=D/'qualified-parks13-cycle1';B.mkdir(exist_ok=False)
uid='01a14328-322d-71d0-9b8c-3da31158840f';js=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'));assert len(js)==1
wanted={'call_49722fbad48046de85897a08a36184ad','call_fbc18877d26a4d639e985e57c528e96f','call_1a3cb8012f284843b950c181d16c0629'};records=[]
for n,line in enumerate(js[0].open(),1):
 e=json.loads(line);v=e.get('payload',{})
 if e.get('type')=='response_item' and v.get('type')=='custom_tool_call_output' and v.get('call_id') in wanted:records.append({'nativeJournal':str(js[0]),'line':n,'timestamp':e['timestamp'],'callId':v['call_id'],'originalVisibleOutput':v['output']})
assert len(records)==3
raw=D/'source-captures/source28-parks13-original-open-contexts.json';m.write(raw,{'sourceActor':uid,'transport':'Exact original visible SOURCE webopen outputs, no rewritten source prose or invented personal judgment. Full original relevant parsed contexts retained; authored selected excerpts not substituted for raw.','records':records})
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');manual=[r for r in sp['rawSources'] if '/process-v2-parks13-cycle1-fresh-01a14321/' in r['path']];assert len(manual)==3;paths={z['path'] for z in manual};rp=str(raw.relative_to(C));text=raw.read_text();assert all(z['url'] in text for z in manual);assert a['entries'][0]['proposedCard']['source']['url'] in text
sp['rawSources']=[z for z in sp['rawSources'] if z not in manual]+[{'path':rp,'sha256':m.raw(raw),'url':a['entries'][0]['proposedCard']['source']['url'],'additionalURLs':[z['url'] for z in manual],'originalSourceRecords':manual,'locator':'Original SOURCE webopen output: WorldHeritage295/mainL4-L29,L61-L77; multiopen194 LordHoweL211-L233 and CoralSeaL166-L222; Ningaloo308L18-L160. Retain exact pergroup/variant locators.','captureReadProvenance':'Original full webopen contexts personally visible/read by SOURCE28; root transported immutable exactoutputs from nativejournal. Sourceproof semantic judgments unchanged; includes personally opened actual source.url WorldHeritage.'}]
for e in sp['entries']:
 for g in e['literalGroups']:g['sourcePaths']=[rp if p in paths else p for p in g['sourcePaths']]
 for v in e['fourFullPromptAnswerNoteAssessments']:v['sourcePaths']=[rp if p in paths else p for p in v['sourcePaths']]
 if e.get('correctNoteNewFact',{}).get('sourcePaths'):e['correctNoteNewFact']['sourcePaths']=[rp if p in paths else p for p in e['correctNoteNewFact']['sourcePaths']]
for obj in [a,sp,ps]:obj['rootNormalization']={'owner':m.O,'originalPacket':str(S.relative_to(C)),'originalFreeze':'ddd045ca9ee4be0653ca15096f48940d8811af61','transformations':['Manual selected source excerpts replaced by exact original visible primary SOURCE tooloutputs with provenance','Actual author-opened source.url WorldHeritage body preserved in full original context'],'semanticRootEdits':False,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
print('NORMALIZED_FREEZE',m.savecode([pathlib.Path(__file__),raw,*B.glob('*.json')],'Freeze NP13 exactSOURCE cycle1 original fullprimary captures and mechanical transport'))
