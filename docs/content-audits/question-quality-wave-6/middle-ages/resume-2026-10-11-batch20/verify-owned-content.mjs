// Mechanical current-topic validation and exact preservation only; never editorial certification.
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from 'vite';
const here=dirname(fileURLToPath(import.meta.url));
const repo=resolve(here,'../../../../..');
const before=JSON.parse(await readFile(resolve(here,'before.json'),'utf8'));
const topic=JSON.parse(await readFile(resolve(repo,'src/content/topics/middle-ages.json'),'utf8'));
function canonical(value){return JSON.stringify(value, Object.keys(value).sort());}
function sorted(value){if(Array.isArray(value))return value.map(sorted);if(value && typeof value==='object')return Object.fromEntries(Object.keys(value).sort().map(k=>[k,sorted(value[k])]));return value;}
const hash=c=>createHash('sha256').update(JSON.stringify(sorted(c))).digest('hex');
const restored=JSON.parse(JSON.stringify(topic));
const ids=new Set(before.ids),current=new Map(topic.questions.map(c=>[c.id,c]));
const errors=[];
for(const old of before.questions){const c=current.get(old.id);if(!c || c.difficulty!==old.difficulty || c.correctIndex!==old.correctIndex)errors.push(`${old.id}: identity/difficulty/index changed`);}
if(JSON.stringify(topic.questions.map(c=>c.id))!==JSON.stringify(Object.keys(before.allTopicCardHashes)))errors.push('topic question order changed');
const preserved=topic.questions.filter(c=>!ids.has(c.id)).map(c=>({id:c.id,unchanged:hash(c)===before.allTopicCardHashes[c.id]}));
if(preserved.some(c=>!c.unchanged))errors.push('outside-scope card changed');
if(topic.questions.some((c,i)=>hash(c)!==hash(restored.questions[i])))errors.push('roundtrip changed scalar');
const quota={easy:[0,0,0,0],medium:[0,0,0,0],hard:[0,0,0,0]};for(const c of topic.questions)quota[c.difficulty][c.correctIndex]++;
if(JSON.stringify(quota)!==JSON.stringify({easy:[10,10,10,10],medium:[10,10,10,10],hard:[5,5,5,5]}))errors.push('40/40/20 or per-index quota violated');
const server=await createServer({root:repo,configFile:false,appType:'custom',server:{middlewareMode:true},logLevel:'error'});
let validationIssues;
try {const {validateTopicPack}=await server.ssrLoadModule('/src/content/index.ts');validationIssues=validateTopicPack(topic);if(validationIssues.length)errors.push(...validationIssues);} finally{await server.close();}
const report={scope:'current middle-ages topic structure plus exact20 field/identity preservation; no editorial verdicts',cards:topic.questions.length,owned:before.ids.length,unchangedOutsideOwned:preserved.length,preserved,quota,jsonRoundtrip:true,currentCardHashes:Object.fromEntries(before.ids.map(id=>[id,hash(current.get(id))])),validationIssues,errors,passed:errors.length===0,newCertifiedCards:0};
await writeFile(resolve(here,'owned-preservation-current.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({owned:report.owned,unchangedOutsideOwned:report.unchangedOutsideOwned,quota,errors,passed:report.passed,newCertifiedCards:0}));if(errors.length)process.exitCode=1;
