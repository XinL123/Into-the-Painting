// Local-only production-build QA server. /slow delays artwork delivery;
// /fail fails the first overview/tile request, then permits explicit retries.
import http from 'node:http';
import { readFile,appendFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(dir,'../../../dist');
const attempts=new Map();
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.m4a':'audio/mp4','.ogg':'audio/ogg','.wav':'audio/wav'};
http.createServer(async(req,res)=>{
 const u=new URL(req.url,'http://localhost');const mode=u.pathname.split('/')[1];
 const rel=u.pathname.replace(/^\/(slow|fail)\/?/,'/');
 const name=path.basename(rel);const key=u.pathname;const n=(attempts.get(key)||0)+1;attempts.set(key,n);
 const isScene=/^(\d{5}|gusu-preview)-/.test(name);
 if(mode==='slow'&&isScene)await new Promise(r=>setTimeout(r,1800));
 const status=mode==='fail'&&isScene&&n===1?503:200;
 await appendFile(path.join(dir,'delivery-log.jsonl'),JSON.stringify({mode,url:u.pathname,attempt:n,status,time:Date.now()})+'\n');
 if(status!==200){res.writeHead(status,{'content-type':'text/plain','cache-control':'no-store'});res.end('Temporary QA image failure');return;}
 const target=path.resolve(root,'.'+(rel==='/'?'/index.html':rel));
 if(!target.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
 try{const bytes=await readFile(target);res.writeHead(200,{'content-type':mime[path.extname(target)]??'application/octet-stream','cache-control':'no-store'});res.end(bytes);}
 catch{res.writeHead(404);res.end('Not found');}
}).listen(4182,'127.0.0.1',()=>console.log('QA delivery server http://localhost:4182/{slow,fail}/'));
