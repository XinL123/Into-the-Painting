import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';
const text=await readFile(new URL('../../src/transitions/enter.js',import.meta.url),'utf8');
const timelines=[];
const gsap={set(el,{clearProps}){for(const k of clearProps.split(','))el.style[k]='';},timeline(){const t={queue:[],alive:true,to(obj,props){this.queue.push(()=>{for(const [k,v] of Object.entries(props))if(!['duration','ease','onUpdate'].includes(k))obj[k]=v;props.onUpdate?.();});return this;},add(fn){this.queue.push(fn);return this;},pause(){this.paused=true;},resume(){this.resumes=(this.resumes??0)+1;},isActive(){return this.alive;},kill(){this.alive=false;},next(){if(this.alive)this.queue.shift()?.();}};timelines.push(t);return t;}};
globalThis.__transitionQA=gsap;globalThis.innerWidth=1000;globalThis.innerHeight=700;globalThis.addEventListener=()=>{};globalThis.removeEventListener=()=>{};
const source=text.replace("import { reducedMotion } from '../motion.js';","const reducedMotion=false;").replace("import gsap from 'gsap';","const gsap=globalThis.__transitionQA;");
const {createTransition}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
function classes(){const s=new Set();return{add(...a){a.forEach(x=>s.add(x));},remove(...a){a.forEach(x=>s.delete(x));},contains(x){return s.has(x);}};}
function setup(){let resolve;const ready=new Promise(r=>resolve=r);let starts=0,done=0;const el=()=>({style:{},classList:classes(),getBoundingClientRect:()=>({left:100,top:100,width:150,height:350})});const opening=el(),ink=el(),img=el(),view=el();const root={classList:classes(),querySelector:()=>view};const stage={ready,measure(){},restRect:()=>({left:-100,top:20,width:1500,height:600}),start(){starts++;},wake(){},sleep(){},stop(){}};const transition=createTransition({root,live:{opening,ink,img,painting:{place:{x:20,y:20,w:10,h:50}}},stage,onLayout(){},onLeaveDone(){done++;}});return{transition,root,opening,resolve,get starts(){return starts},get done(){return done}};}
test('late image readiness cannot revive a painting after an interrupted entry',async()=>{
 const x=setup();x.transition.enter();const entry=timelines.at(-1);entry.next();entry.next();assert.equal(entry.paused,true);
 x.transition.leave();const leave=timelines.at(-1);leave.next();leave.next();x.transition.destroy();x.resolve();await Promise.resolve();
 assert.equal(x.starts,0);assert.equal(entry.resumes,undefined);assert.equal(x.done,1);assert.ok(!x.root.classList.contains('is-on'));assert.equal(x.opening.style.opacity,'');assert.ok(!x.opening.classList.contains('is-travelling'));
});
test('successful handoff starts once and exit restores CSS ownership without replaying ink',async()=>{
 const x=setup();x.transition.enter();const entry=timelines.at(-1);entry.next();entry.next();x.resolve();await Promise.resolve();entry.next();entry.next();assert.equal(x.starts,1);assert.ok(x.root.classList.contains('is-inside'));
 x.transition.leave();const leave=timelines.at(-1);leave.next();leave.next();assert.equal(x.opening.style.opacity,'');assert.ok(x.opening.classList.contains('is-visited'));assert.equal(x.done,1);assert.ok(!x.root.classList.contains('is-on'));x.transition.destroy();
});
