import test from 'node:test';import assert from 'node:assert/strict';import {readFile}from'node:fs/promises';
import {stories}from'../../src/paintings/gusu/stories.js';
const before=JSON.parse(await readFile(new URL('./before-stories.json',import.meta.url)));
const focus=JSON.parse(await readFile(new URL('../../src/paintings/gusu/focus.json',import.meta.url)));
const json=x=>JSON.parse(JSON.stringify(x));
test('every one of 22 scene identities retains artwork, focus and its approved balanced sound',async()=>{
 const balanced=JSON.parse(await readFile(new URL('../gusu-smooth-audio-2026-11-01/after-levels.json',import.meta.url)));
 for(const s of stories){const b=balanced.find(x=>x.id===s.id);assert.deepEqual(s.sound,{file:b.file,mode:'once',gain:b.gain});}
 assert.equal(stories.length,22);assert.equal(new Set(stories.map(s=>s.id)).size,22);
 const fields=['box','anchor','frameBox','spot','packageId','candidateId','sources'];
 for(const s of stories){const original=before.find(a=>a.id===s.id);assert.ok(original);const old={...original,...focus[s.id]};for(const f of fields)assert.deepEqual(json({[f]:s[f]}),json({[f]:old[f]}),`${s.id} ${f}`);}
});
test('all 22 positions and numbers follow increasing approved master x',()=>{
 const x=s=>s.anchor?.[0]??(s.box[0]+s.box[2])/2;
 for(let i=1;i<stories.length;i++)assert.ok(x(stories[i])>x(stories[i-1]));
 assert.equal(stories[0].id,'pagoda');assert.equal(stories[21].id,'school');
 assert.ok(!stories[0].nextLabel);assert.equal(stories[21].nextLabel,'Restart the Journey');
});
test('only two passages with obsolete route directions change; other 20 texts are exact',()=>{
 for(const s of stories){const old=before.find(a=>a.id===s.id);if(!['school','pagoda'].includes(s.id)){assert.deepEqual(s.text,old.text);assert.equal(s.title,old.title);}}
 const school=stories.at(-1);assert.deepEqual(school.text.slice(1),before.find(s=>s.id==='school').text.slice(1));assert.ok(!school.text[0].includes('before we'));
 assert.ok(!stories[0].title.includes('Finish'));assert.ok(stories[0].text.join(' ').includes('Tiger Hill'));
});
