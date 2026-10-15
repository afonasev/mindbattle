import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp,rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { ReleaseCatalog } from '../../desktop/releases.mjs';

test('API selection ignores draft/prerelease/incomplete releases, pins bytes and uses conditional caching',async t=>{
 const root=await mkdtemp(path.join(os.tmpdir(),'mindbattle-template-catalog-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const hash='a'.repeat(64), base='https://github.com/afonasev/mindbattle/releases/download/content-3';
 const release={tag_name:'content-3',draft:false,prerelease:false,published_at:'2026-10-15T00:00:00Z',assets:[{name:'latest.json',state:'uploaded',browser_download_url:`${base}/latest.json`},{name:hash,state:'uploaded',size:2}]};
 let calls=0;
 const fetcher=async(url,options)=>{
   if(url.includes('api.github.com')) {calls++;if(calls===2){assert.equal(options.headers['If-None-Match'],'fixture');return new Response(null,{status:304});}return Response.json([{...release,prerelease:true,tag_name:'content-9'},{...release,draft:true,tag_name:'content-8'},release],{headers:{etag:'fixture'}});}
   assert.equal(url,`${base}/latest.json`);return new Response('signed');
 };
 const catalog=new ReleaseCatalog({cache:path.join(root,'cache.json'),fetcher});
 const shell={platform:'win32-x64',state:{highWater:0}};
 const content={state:{highWater:0},candidate:raw=>({raw,manifest:{sequence:3,version:'1.0.1',objectBaseUrl:base,files:[{sha256:hash,size:2}]}})};
 const result=await catalog.candidate({shell,content});assert.equal(result.raw.toString(),'signed');assert.equal(result.kind,'content');
 assert.ok(await catalog.candidate({shell,content}));assert.equal(calls,2);
 release.assets.pop();assert.equal(await catalog.candidate({shell,content}),null);
});
