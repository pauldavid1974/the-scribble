#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');
const file = path.resolve(process.argv[2] || path.join(__dirname, '..', 'hardware', 'case_model_viewer.html'));
const src = fs.readFileSync(file, 'utf8');
const match = src.match(/window\.SCRIBBLE_V6_DATA=(\{[^\n]+\});/);
assert.ok(match, 'v6 OpenSCAD mesh data is embedded in viewer');
const payload = JSON.parse(match[1]);
const expected = {rear:[46,82],bezel:[46,82],caps:null};
for (const [id,extent] of Object.entries(expected)) {
  const d=zlib.inflateSync(Buffer.from(payload[id],'base64'));
  const n=d.readUInt16LE(0), faces=d.readUInt16LE(2);
  assert.equal(d.length,4+n*6+faces*6, 'packed bytes match geometry header');
  assert.ok(n>15 && faces>20, id+' mesh is populated');
  const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<n;i++) for(let j=0;j<3;j++){
    const v=d.readInt16LE(4+i*6+j*2)/100;
    min[j]=Math.min(min[j],v);max[j]=Math.max(max[j],v);
  }
  for(let i=0;i<faces*3;i++) assert.ok(d.readUInt16LE(4+n*6+i*2)<n,'valid triangle index');
  if(extent){assert.ok(Math.abs(max[0]-min[0]-extent[0])<.08,id+' case width');assert.ok(Math.abs(max[1]-min[1]-extent[1])<.08,id+' case length');}
  console.log('  OK',id,n,'vertices',faces,'faces',max.map((v,i)=>(v-min[i]).toFixed(2)).join(' x '),'mm');
}
for(const phrase of ['V6 FIT PROTOTYPE','Simulate Talk','Cutaway fit','Exploded assembly','USB side']) {
  assert.ok(src.toLowerCase().includes(phrase.toLowerCase()), 'missing viewer feature '+phrase);
}
assert.ok(!src.includes('STEP-Matched .STL'),'obsolete fake-export button is gone');
console.log('Scribble v6 viewer mesh integrity and controls: PASS');
