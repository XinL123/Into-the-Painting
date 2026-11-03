import test from 'node:test';
import assert from 'node:assert/strict';
import {createMusic} from '../../src/gallery/music.js';
const tick=()=>new Promise(r=>setImmediate(r));
function fixture(saved=null){
 const storage=new Map(saved==null?[]:[['painting.music',saved]]);
 const root=new EventTarget(),toggle=new EventTarget(),attrs={};let allowed=false,plays=0,release;
 toggle.classList={toggle(){}};toggle.setAttribute=(k,v)=>attrs[k]=v;
 class Audio extends EventTarget{paused=true;volume=1;src='';play(){plays++;if(!allowed)return Promise.reject(new Error('NotAllowedError'));this.paused=false;return release?new Promise(r=>{release.resolve=r;}):Promise.resolve();}pause(){this.paused=true;}}
 globalThis.Audio=Audio;globalThis.localStorage={getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)};
 const music=createMusic(root,['/one.m4a','/two.m4a'],{toggle});
 return {root,toggle,attrs,storage,music,allow:()=>{allowed=true;},defer:()=>{release={};},resolve:()=>release.resolve(),plays:()=>plays};
}
test('default remains enabled if autoplay is blocked; first gesture retries',async()=>{
 const f=fixture();await tick();assert.equal(f.music.on,true);assert.equal(f.attrs['aria-label'],'Play music');assert.equal(f.music.audio.paused,true);assert.equal(f.storage.has('painting.music'),false);
 f.allow();f.root.dispatchEvent(new Event('pointerdown'));await tick();assert.equal(f.music.audio.paused,false);
 f.music.suspend();
});
test('manual mute stays during this visit; stale saved off cannot mute a new load',async()=>{
 const f=fixture();await tick();f.allow();f.root.dispatchEvent(new Event('click'));await tick();f.toggle.dispatchEvent(new Event('click'));await tick();assert.equal(f.music.on,false);assert.equal(f.attrs['aria-label'],'Music off');assert.equal(f.storage.has('painting.music'),false);
 const count=f.plays();f.allow();f.root.dispatchEvent(new Event('pointerdown'));await tick();assert.equal(f.plays(),count);
 const returning=fixture('off');await tick();assert.equal(returning.music.on,true);assert.equal(returning.attrs['aria-label'],'Play music');
});
test('pending playback cannot escape mute or painting suspension',async()=>{
 const f=fixture();await tick();f.allow();f.defer();f.root.dispatchEvent(new Event('keydown'));f.music.suspend();f.resolve();await tick();assert.equal(f.music.audio.paused,true);assert.equal(f.music.on,true);
});

test('scene mute survives controller switches, but ignores stale storage after reload',async()=>{
 const previous=globalThis.document,events=new EventTarget();
 globalThis.document={createElement:()=>({canPlayType:()=> 'probably'}),addEventListener:events.addEventListener.bind(events),removeEventListener:events.removeEventListener.bind(events)};
 globalThis.localStorage={getItem:()=> 'off',setItem:()=>{throw Error('No persistent mute should be written');}};
 try{
  const {createSound}=await import('../../src/explore/sound.js?visit-one');
  const a=createSound({});assert.equal(a.muted,false);a.setMuted(true);a.destroy();
  const b=createSound({});assert.equal(b.muted,true);b.destroy();
  const fresh=await import('../../src/explore/sound.js?visit-two');
  const c=fresh.createSound({});assert.equal(c.muted,false);c.destroy();
 }finally{globalThis.document=previous;}
});

test('quieter exploration level continues the stream without restarting; mute remains authoritative',async()=>{
 const f=fixture();await tick();f.allow();f.root.dispatchEvent(new Event('pointerdown'));await tick();
 f.music.audio.currentTime=37;f.music.setLevel(.28);await tick();
 assert.equal(f.music.audio.paused,false);assert.equal(f.music.audio.currentTime,37);
 f.music.setEnabled(false);assert.equal(f.music.on,false);f.music.setLevel(1);assert.equal(f.music.on,false);
 f.music.setEnabled(true);await tick();assert.equal(f.music.audio.paused,false);assert.equal(f.music.audio.currentTime,37);f.music.suspend();
});

test('first speaker click after refused autoplay starts music rather than muting it',async()=>{
 const f=fixture();await tick();assert.equal(f.music.state().blocked,true);f.allow();f.toggle.dispatchEvent(new Event('click'));await tick();assert.equal(f.music.on,true);assert.equal(f.music.audio.paused,false);assert.equal(f.music.state().blocked,false);assert.equal(f.attrs['aria-label'],'Music on');f.music.suspend();
});
test('click and touch-end both unlock playback without visiting a project',async()=>{
 for(const name of ['click','touchend']){const f=fixture();await tick();f.allow();f.root.dispatchEvent(new Event(name));await tick();assert.equal(f.music.audio.paused,false);f.music.suspend();}
});
