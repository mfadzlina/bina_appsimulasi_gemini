import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'child_process';
const FPS=30, FF=process.env.FF;
const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1920,height:1080}});
import fs from 'fs'; await pg.addInitScript(tl=>{window.TL=tl}, JSON.parse(fs.readFileSync('timeline.json','utf8')));
await pg.goto('file://'+process.cwd()+'/index.html');
await pg.evaluate(async()=>{await Promise.all(['400 20px Poppins','500 20px Poppins','600 20px Poppins','700 20px Poppins','800 20px Poppins','700 20px Caveat'].map(f=>document.fonts.load(f)));await document.fonts.ready});
await pg.waitForTimeout(800);
const T=await pg.evaluate(()=>TOTAL); const n=Math.round(T*FPS);
const ff=spawn(FF,['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','music.wav',
 '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',process.env.OUT||'LO_to_Screen.mp4'],{stdio:['pipe','inherit','inherit']});
const t0=Date.now();
for(let i=0;i<n;i++){ await pg.evaluate(t=>seek(t),i/FPS);
 const buf=await pg.screenshot({type:'jpeg',quality:92});
 if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
 if(i%300===0) console.log(i,'/',n, ((Date.now()-t0)/1000).toFixed(0)+'s'); }
ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('done');
