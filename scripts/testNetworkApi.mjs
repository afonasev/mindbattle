import assert from "node:assert/strict";
const origin=process.env.MINDBATTLE_TEST_ORIGIN??"http://127.0.0.1:4185";
async function post(path,body,credential){const response=await fetch(`${origin}/api/network/${path}${credential?`?code=${credential.code}`:""}`,{method:"POST",headers:{"content-type":"application/json",...(credential?{authorization:`Bearer ${credential.token}`}:{})},body:JSON.stringify(body)});return {response,value:await response.json()};}
async function connect(credential){
 const abort=new AbortController();const response=await fetch(`${origin}/api/network/stream?code=${credential.code}`,{headers:{authorization:`Bearer ${credential.token}`},signal:abort.signal});assert.equal(response.status,200);
 const reader=response.body.getReader();const decoder=new TextDecoder();let buffer="";
 return {abort,async next(){while(!buffer.includes("\n\n")){const {value,done}=await reader.read();if(done)return null;buffer+=decoder.decode(value,{stream:true});}const end=buffer.indexOf("\n\n");const event=buffer.slice(0,end);buffer=buffer.slice(end+2);return event;}};
}
const streams=[];
try{
 const {response,value:display}=await post("create",{});assert.equal(response.status,201);assert.match(display.code,/^\d{4}$/);
 const first=await connect(display);streams.push(first);assert.match(await first.next(),/event: connected/);let snapshot=JSON.parse((await first.next()).slice(6));assert.equal(snapshot.phase,"lobby");
 const second=await connect(display);streams.push(second);let replaced=false;for(let i=0;i<5;i++){const event=await first.next();if(event?.includes("event: replaced")){replaced=true;break;}}assert.equal(replaced,true,"old stream must be explicitly replaced");
 assert.match(await second.next(),/event: connected/);snapshot=JSON.parse((await second.next()).slice(6));
 const forged=await post("command",{commandId:"forged",epoch:snapshot.epoch,phaseRevision:snapshot.phaseRevision,action:{type:"close"}},{...display,token:"not-the-token"});assert.equal(forged.response.status,403);
 const result=await post("command",{commandId:crypto.randomUUID(),epoch:snapshot.epoch,phaseRevision:snapshot.phaseRevision,action:{type:"close"}},display);assert.equal(result.response.status,200);assert.equal(result.value.closed,true);
 let expired=false;for(let i=0;i<8;i++){const event=await second.next();if(event===null)break;if(event.includes("event: expired"))expired=true;}assert.equal(expired,true);
 await new Promise(r=>setTimeout(r,350));const after=await post("command",{},display);assert.equal(after.response.status,404);
 console.log("PASS: production API code, authorization, stream replacement, close acknowledgement, stream cleanup and room removal");
}finally{for(const stream of streams)stream.abort.abort();}
