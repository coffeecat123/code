var root=document.querySelector(':root');
var hrt=document.querySelector("#hrt");
var cvs=document.querySelector("#cvs");
var ctx=cvs.getContext("2d");
let btsr;
let dcl=Math.round(innerHeight*(outerWidth/innerWidth));
chrome.storage.local.get(['btsr'], function(result) {
  btsr=result.btsr;
  start();
});
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
function start(){
  let evl=[];
  let bkcr="#181818";
  let ra=100;
  let tma=5;
  let pa={
    x:-ra*2,
    y:-ra*2
  };
  drbk();
  fltxt("click to start",300,900,["#f900ff","#0000ff","#ff0000"]);
  fltxt(`total time: ${tma}`,200,2000,["#ffff00","#00ff00"]);
  fltxt(`bestscore: ${btsr}`,200,1400,["#ff0000","#ffff00"]);
  cvs.addEventListener('click',evl[0]=(e)=>{
    cvs.removeEventListener("click",evl[0]);
    cvs.removeEventListener('mousemove',evl[1]);
    play();
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
  function drbk(){
    ctx.clearRect(0,0,cvs.width,cvs.height);
    ctx.fillStyle=bkcr;
    ctx.fillRect(0,0,cvs.width,cvs.height);
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
  function cltxt(text,fms,h,clr){
    ctx.font=`${fms}px Comic Sans MS,標楷體`;
    ctx.fillStyle=clr;
    ctx.fillRect((cvs.width-ctx.measureText(text).width)/2,h-fms,ctx.measureText(text).width,fms+50);
  }
  function gmor(scr){//game over
    ctx.fillStyle=bkcr;
    ctx.fillRect(0,800,1024,20);
    let me=new Path2D();
    //Time's up
    //score
    //best
    //button(try again)
    drbk();
    fltxt("Time's up",300,900,["#f900ff","#0000ff","#ff0000"]);
    fltxt(`score: ${scr}`,200,1400,["#ffff00","#00ff00"]);
    fltxt(`bestscore: ${btsr}`,200,2000,["#ff0000","#ffff00"]);
    let cr = new Path2D();
    ctx.fillStyle="#ff0000";
    cr.rect (800,2500,200,200);
    ctx.fill(cr);
    cvs.addEventListener('click',function ai(e){
      if (ctx.isPointInPath(cr, e.offsetX, e.offsetY)) {
        cvs.removeEventListener('click',ai);
        setTimeout(play,0);
      }
    });
  }
  function play(){//play
    drbk();
    let tm=tma*1000;
    let tm1=Date.now();
    let lv=-1;
    tidr();
    function tidr(){
      let _q=50,_s=cvs.width-50*2;
      let _z=Date.now()-tm1;
      ctx.fillStyle=bkcr;
      ctx.fillRect(_q,800,_s,20);
      ctx.fillStyle="#fff";
      ctx.fillRect(_q,800,_s*((tm-_z)/tm),20);
      if(_z>=tm){
        if(lv>btsr){
          btsr=lv;
          chrome.storage.local.set({btsr});
        }
        setTimeout(()=>{
          gmor(lv);
        },0);
        return;
      }
      setTimeout(tidr,10);
    }
    nxlv();
    function nxlv(){
      lv++;
      cltxt(` score:${lv} `,300,500,bkcr);
      fltxt(`score:${lv}`,300,500,["#ff0000","#f900ff"]);
      dbox(parseInt(lv/3+2));
    }
    function dbox(a){//draw box
      let sp=50-a/2;//spacing
      let bxw=(3072-(a+1)*sp)/a;//box width
      let wq=parseInt(50-lv*2);//clr sp
      if(wq<=0)wq=1;
      let _b=256-wq*2;
      let _a=[parseInt(Math.random()*_b%_b)+wq,
              parseInt(Math.random()*_b%_b)+wq,
              parseInt(Math.random()*_b%_b)+wq];
      let clr=`#${_a[0].toString(16).padStart(2,"0")}${_a[1].toString(16).padStart(2,"0")}${_a[2].toString(16).padStart(2,"0")}`;
      ctx.fillStyle="#000000";
      ctx.fillRect(0,1024,3072,3072);
      let add=parseInt(Math.random()*2%2);
      for(let i=0;i<3;i++){
        if(add){
          _a[i]+=wq;
        }
        else{
          _a[i]-=wq;
        }
      }
      let clr2=`#${_a[0].toString(16).padStart(2,"0")}${_a[1].toString(16).padStart(2,"0")}${_a[2].toString(16).padStart(2,"0")}`;
      let bb={
        x:parseInt(Math.random()*a%a),
        y:parseInt(Math.random()*a%a)
      }
      ctx.fillStyle=clr;
      for(let i=0;i<a;i++){
        for(let j=0;j<a;j++){
          ctx.fillRect ((i+1)*sp+i*bxw,1024+(j+1)*sp+j*bxw,bxw,bxw);
        }
      }
      let cr = new Path2D();
      ctx.fillStyle=clr2;
      cr.rect ((bb.x+1)*sp+bb.x*bxw,1024+(bb.y+1)*sp+bb.y*bxw,bxw,bxw);
      ctx.fill(cr);
      cvs.addEventListener('click',function qi(e){
        if(Date.now()-tm1>=tm){
          cvs.removeEventListener('click',qi);
          return;
        }
        if (ctx.isPointInPath(cr, e.offsetX, e.offsetY)) {
          cvs.removeEventListener('click',qi);
          tm1+=0.25*1000;
          nxlv();
        }
      });
    }
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