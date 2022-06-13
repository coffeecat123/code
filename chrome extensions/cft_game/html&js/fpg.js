var root=document.querySelector(':root');
var hrt=document.querySelector("#hrt");
var cvs=document.querySelector("#cvs");
var ctx=cvs.getContext("2d");
let dcl=Math.round(innerHeight*(outerWidth/innerWidth));
window.onresize=res;
res();
function res(){
  if(Math.round(1000*(outerWidth/innerWidth))/1000<1){
    document.querySelector("html").style.height="100vh";
  }
  else{
    document.querySelector("html").style.height="";
  }
  let a=dcl*Math.round(1000*(outerWidth/innerWidth))/1000;
  document.body.style.height=`${a}px`;
  document.body.style.width=`${a*0.75}px`;
  cvs.style.transform=`scale(${a/4096})`;
}
function fltxt(text,fms,h,clr){
  ctx.font=`${fms}px Comic Sans MS,標楷體`;
  var gdt=ctx.createLinearGradient((cvs.width-ctx.measureText(text).width)/2,0,(cvs.width+ctx.measureText(text).width)/2,0);
  for(let i in clr){
    
    gdt.addColorStop(i/(clr.length-1),clr[i]);
  }
  ctx.fillStyle=gdt;
  ctx.fillText(text,(cvs.width-ctx.measureText(text).width)/2,h);
}
start();
function start(){
  let evl=[];
  let ctt = new Path2D();
  ctt.rect(0,0,cvs.width,cvs.height);
  ctx.fillStyle="#181818";
  ctx.fill(ctt);
  let ra=100;
  let pa={
    x:-ra*2,
    y:-ra*2
  };
  fltxt("click to start","300",900,["#f900ff","#0000ff","#ff0000"]);
  fltxt("time: 30","200",2000,["#ffff00","#00ff00"]);
  chrome.storage.local.get(['btsr'], function(result) {
    fltxt(`bestscore: ${result.btsr}`,"200",1400,["#ff0000","#ffff00"]);
  });
  cvs.addEventListener('mousedown',evl[0]=(e)=>{
    if (ctx.isPointInPath(ctt, e.offsetX, e.offsetY)) {
      cvs.removeEventListener("mousedown",evl[0]);
      play();
    }
  });
  cvs.addEventListener('mousemove',evl[1]=(e)=>{
    let x=e.offsetX,y=e.offsetY;
    if(((pa.x-x)**2+(pa.y-y)**2)<=(ra)**2*0.5)return;
    pa.x=x;
    pa.y=y;
    ctx.beginPath();
    var gradient=ctx.createLinearGradient(0,0,cvs.width,0);
    gradient.addColorStop("0.0","#f900ff80");
    gradient.addColorStop("0.5","#0000ff80");
    gradient.addColorStop("1.0","#ff000080");
    ctx.fillStyle=gradient;
    ctx.arc(x,y, ra,0,Math.PI*2);
    ctx.fill();
  });
  function play(){
    console.log("play");
    cvs.removeEventListener('mousemove',evl[1]);
    ctx.beginPath();
    ctx.clearRect(0,0,cvs.width,cvs.height);
    ctx.fillStyle="#ffffff";
    ctx.rect(0,0,cvs.width,cvs.height);
    ctx.fill();
    ctx.beginPath();
    ctx.fillStyle="#f900ff";
    ctx.rect(0,1024,3072,3072);
    ctx.fill();
    fltxt("level:1","300",900,["#0000ff","#ff0000"]);
  }
}
hrt.onclick=()=>{
    let _a=parseInt(Math.random()*1000%256).toString(16).padStart(2,"0");
    let _b=parseInt(Math.random()*1000%256).toString(16).padStart(2,"0");
    let _c=parseInt(Math.random()*1000%256).toString(16).padStart(2,"0");
    let _d=`#${_a}${_b}${_c}`;
    root.style.cssText+=`--hrt: ${_d};`;
    chrome.storage.local.set({htcr:_d});
};
chrome.storage.local.get(['htcr'], function(result) {
  root.style.cssText+=`--hrt: ${result.htcr};`;
});