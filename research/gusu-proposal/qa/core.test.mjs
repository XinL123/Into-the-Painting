import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createImageCache } from '../../../src/explore/images.js';
import { sceneFrame } from '../../../src/explore/framing.js';
import { stories } from '../../../src/paintings/gusu/stories.js';
const focus=JSON.parse(await readFile(new URL('../../../src/paintings/gusu/focus.json',import.meta.url)));
const approved=JSON.parse(await readFile(new URL('../hotspots.json',import.meta.url))).hotspots;
const tick=()=>new Promise(r=>setImmediate(r));

const editorial=JSON.parse(await readFile(new URL('../../gusu-editorial-2026-10-28/approved-copy.json',import.meta.url)));
const before=JSON.parse(await readFile(new URL('../../gusu-editorial-2026-10-28/before-stories.json',import.meta.url)));
const expansion=JSON.parse(await readFile(new URL('../../gusu-expansion/final-review/final-hotspots.json',import.meta.url))).new_candidates;
test('22 approved scenes keep their coordinates and copy while the route runs left-to-right',()=>{
 assert.equal(stories.length,22);
 for(const s of stories.filter(s=>s.packageId)){const original=approved.find(a=>a.package_id===s.packageId);assert.deepEqual(s.box,original.box);}
 for(const story of stories.filter(s=>s.candidateId)){const a=expansion.find(a=>a.id===story.candidateId);assert.deepEqual(story.box,a.box);assert.deepEqual(story.anchor,focus[story.id]?.anchor??a.anchor);assert.equal(story.title,a.title);}
 for(const story of stories.filter(s=>!['school','pagoda'].includes(s.id)))assert.deepEqual(story.text,editorial[story.id]??before.find(s=>s.id===story.id).text);
 assert.equal(stories[0].id,'pagoda');assert.equal(stories.at(-1).id,'school');
 assert.equal(stories.at(-1).nextLabel,'Restart the Journey');assert.equal(stories.filter(s=>s.nextLabel).length,1);
 for(let i=1;i<stories.length;i++){const x=s=>s.anchor?.[0]??(s.box[0]+s.box[2])/2;assert.ok(x(stories[i-1])<x(stories[i]));}
});
test('all scenes fit safe image area on desktop, phone and short landscape',()=>{
 for(const [vw,vh] of [[1440,900],[805,745],[768,1024],[640,480],[390,844],[320,568],[844,390]]) {
  for(const story of stories){
   const f=sceneFrame({box:story.frameBox ?? story.box,width:35311,height:1010,vw,vh,rest:{x:-17000,y:0,s:.75},cardHeight:300,cardBottom:88,maxZoom:story.maxZoom??1.25});
   const [x0,y0,x1,y1]=story.frameBox ?? story.box;
   assert.ok(f.s<=(story.maxZoom??1.25));
   assert.ok(f.x+x0*f.s>=-.01&&f.x+x1*f.s<=vw+.01,`${vw}: ${story.id} horizontal`);
   assert.ok(f.y+y0*f.s>=f.top-.01&&f.y+y1*f.s<=f.bottom+.01,`${vw}: ${story.id} vertical`);
  }
 }
});
test('slow images cannot exceed concurrency or grow an unbounded cache',async()=>{
 const resolvers=[];let count=0,peak=0;
 const load=()=>new Promise(resolve=>{count++;peak=Math.max(peak,count);resolvers.push(()=>{count--;resolve({image:true});});});
 const cache=createImageCache({load,limit:2,concurrency:2});
 for(let i=0;i<5;i++)cache.request(String(i),'image');
 assert.equal(cache.state().pending,2);assert.equal(cache.state().queued,3);
 while(resolvers.length){resolvers.shift()();await tick();}
 assert.equal(peak,2);assert.equal(cache.state().cached,2);cache.destroy();
});
test('stale requests abort, failures retain fallback and explicit retry recovers',async()=>{
 let failed=true,aborted=false;
 const cache=createImageCache({load:(url,signal)=>url==='stale'?new Promise((_,reject)=>signal.addEventListener('abort',()=>{aborted=true;reject(new Error('abort'));})):failed?Promise.reject(new Error('404')):Promise.resolve({ok:true})});
 cache.request('old','stale');cache.retain(['new']);await tick();assert.equal(aborted,true);
 cache.request('new','broken');await tick();assert.equal(cache.get('new'),null);
 failed=false;cache.retry();cache.request('new','fixed');await tick();assert.deepEqual(cache.get('new'),{ok:true});
 cache.destroy();assert.equal(cache.state().pending,0);assert.equal(cache.state().cached,0);assert.equal(cache.state().disposed,true);
});

test('sound cancellation while bytes are pending cannot start a stale clip',async()=>{
 const events=new EventTarget();
 const saved={document:globalThis.document,window:globalThis.window,localStorage:globalThis.localStorage,fetch:globalThis.fetch};
 let release,started=0,closed=0;
 const gain=()=>({gain:{value:1,cancelScheduledValues(){},setValueAtTime(){},linearRampToValueAtTime(){}},connect(){},disconnect(){}});
 class AudioContext {state='running';currentTime=0;destination={};createGain=()=>gain();decodeAudioData=async()=>({});createBufferSource=()=>({connect(){return {connect(){}}},start(){started++},stop(){},disconnect(){}});close(){this.state='closed';closed++;return Promise.resolve();}}
 globalThis.document={createElement:()=>({canPlayType:()=> 'probably'}),addEventListener:events.addEventListener.bind(events),removeEventListener:events.removeEventListener.bind(events)};
 globalThis.window={AudioContext};globalThis.localStorage={getItem(){return null},setItem(){}};
 globalThis.fetch=()=>new Promise(resolve=>{release=()=>resolve({ok:true,arrayBuffer:async()=>new ArrayBuffer(8)});});
 try{
  const {createSound}=await import('../../../src/explore/sound.js');
  const sound=createSound({clip:{ogg:'/clip.ogg'}});const playing=sound.play({file:'clip',mode:'once'});
  sound.stop();release();await playing;assert.equal(started,0);assert.equal(sound.state().playing,null);
  sound.destroy();assert.equal(closed,1);assert.equal(sound.state().disposed,true);
 }finally{Object.assign(globalThis,saved);}
});
