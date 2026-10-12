#!/usr/bin/env node
import {open} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const LIMIT=4096;
export function checkJson(bytes){
 if(bytes.length>LIMIT)return {status:'TOO_LARGE',maxBytes:LIMIT};
 let text;
 try{text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{return {status:'INVALID',reason:'INVALID_UTF8'};}
 try{const v=JSON.parse(text);return {status:'VALID',bytes:bytes.length,topLevelType:v===null?'null':Array.isArray(v)?'array':typeof v,scope:'syntax_only',duplicateKeysChecked:false,networkUsed:false};}
 catch{return {status:'INVALID',reason:'JSON_SYNTAX',bytes:bytes.length,networkUsed:false};}
}
async function readBounded(path){
 if(path==='-'){
  const chunks=[];let size=0;
  for await(const chunk of process.stdin){size+=chunk.length;if(size>LIMIT){process.stdin.destroy();return Buffer.alloc(LIMIT+1);}chunks.push(chunk);}
  return Buffer.concat(chunks);
 }
 const f=await open(path,'r');
 try{const buf=Buffer.alloc(LIMIT+1);let size=0;while(size<buf.length){const {bytesRead}=await f.read(buf,size,buf.length-size,null);if(!bytesRead)break;size+=bytesRead;}return buf.subarray(0,size);}finally{await f.close();}
}
export async function main(args){
 if(args.length!==1){console.log(JSON.stringify({status:'INPUT_ERROR',usage:'node check-json.mjs <file|->'}));return 2;}
 let out;try{out=checkJson(await readBounded(args[0]));}catch{out={status:'INPUT_ERROR',reason:'READ_FAILED'};}
 console.log(JSON.stringify(out));return out.status==='VALID'?0:out.status==='INVALID'?1:2;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)process.exitCode=await main(process.argv.slice(2));
