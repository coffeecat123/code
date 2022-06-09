let mode=[`<svg width="24px" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sun"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`,`<svg width="30px" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`];
let data,dark;
let defi={};
let tab_id;
let wb=["#000000","#ffffff"];
var root=document.querySelector(':root');
var aqz=document.querySelector("#aqz");
var mde=document.querySelector("#mde");
var fpg=document.querySelector("#fpg");
var nee=document.querySelector("#nee");
var del=document.querySelector("#del");
chrome.tabs.query({
  active: true,
  currentWindow: true
},(tabs)=>{
  tab_id=tabs[0].id;
  if(tabs[0].url.indexOf("chrome-extension://")==0){
    window.open("q.html",'_self');
  }
  chrome.storage.local.get(['durl'], function(result) {
    let du=result.durl;
    if(du.hasOwnProperty(tab_id)){
      if(du[tab_id]!=location.href){
        window.open(du[tab_id],'_self');
      }
    }
    else{
      du[tab_id]=location.href;
      chrome.storage.local.set({durl:du});
    }
  });
});
chrome.storage.local.get(['data','dark'], function(result) {
    data=result.data;
    dark=result.dark;
    chcr();
    if(Object.keys(data).length==0){
      aqz.style.color = "var(--oln)";
      aqz.style.fontSize = "50px";
      aqz.innerHTML = "no file";
      return;
    }
    for (const a of Object.entries(data)) {
      let b=document.createElement("button");
      let b1=document.createElement("textarea");
      let c=a[1][0],c1;
      b.className="fle";
      b1.value=a[0];
      b1.className="tet";
      b1.setAttribute("disabled","");
      b.aid=a[0];
      b.style.background=c;
      if((parseInt(c.substring(1,3),16)+parseInt(c.substring(3,5),16)+parseInt(c.substring(5,7),16))/3>128){
        c1=0;
      }
      else{
        c1=1;
      }
      b1.style.color=wb[c1];
      b.style.border="3px var(--clr1) solid";
      b.ondblclick=()=>{
        window.open(`popup1.html#${encodeURI(b.aid)}`,"_self").focus();
      };
      b.onclick=()=>{
        if(defi.hasOwnProperty(b.firstChild.value)){
          b.style.outline=`none`;
          delete defi[b.firstChild.value];
        }
        else{
          b.style.outline=`4px var(--oln) solid`;
          defi[b.firstChild.value]=1;
        }
        if(Object.keys(defi).length==0){
          del.title=`goto recycle bin`;
        }
        else{
          del.title=`delete(${Object.keys(defi).length})`;
        }
      };
      b.onmousemove=()=>{
        document.querySelector("#sdl").select();
      }
      b.append(b1);
      aqz.append(b);
    }
});
fpg.onclick=()=>{
  window.open("../fpg/fpg.html",'_blank').focus();
};
del.onclick=()=>{
  if(Object.keys(defi).length==0){
    window.open("popup2.html",'_self').focus();
    return;
  }
  if(confirm(del.title)){
    chrome.storage.local.get(['data','trash'],(rst)=>{
      let dt = rst.data;
      let trh=rst.trash;
      for (let a of Object.entries(defi)) {
        trh.push([a[0],dt[a[0]],Date.now()]);
        let aqq=aqz.children;
        for(let i=0;i<aqq.length;i++){
          if(aqq[i].firstChild.value==a[0]){
            aqq[i].remove();
            break;
          }
        }
        delete dt[a[0]];
      }
      data=dt;
      chrome.storage.local.set({data:dt,trash:trh});
      del.title="goto recycle bin";
      defi={};
      if(Object.keys(data).length==0){
        aqz.style.color = "var(--oln)";
        aqz.style.fontSize = "50px";
        aqz.innerHTML = "no file";
      }
    });
  }
};
mde.onclick=()=>{
  dark^=1;
  chcr();
  chrome.storage.local.set({dark});
};
nee.onclick=()=>{
  let newname=prompt('new file name').replaceAll("\r\n","\n");
  if(newname==null)return;
  if(newname=='')return;
  chrome.storage.local.get(['data'],(rst)=>{
    let dt = rst.data;
    let olddt=[wb[dark^1],"",1];
    let nname;
    if(dt.hasOwnProperty(`${newname}`)){
      let cnt=1;
      while(dt.hasOwnProperty(`${newname} (${cnt})`)){
        cnt++;
      }
      nname=`${newname} (${cnt})`;
      alert(`change:\n${newname}\nto:\n${nname}`);
    }
    else{
      nname=newname;
    }
    dt[nname]=[];
    dt[nname][0]=olddt[0];
    dt[nname][1]=olddt[1];
    dt[nname][2]=olddt[2];
    chrome.storage.local.set({data:dt});
    let a=[nname,dt[nname]];
    let b=document.createElement("button");
    let b1=document.createElement("textarea");
    let c=a[1][0],c1;
    b.className="fle";
    b1.value=a[0];
    b1.className="tet";
    b1.setAttribute("disabled","");
    b.aid=a[0];
    b.style.background=c;
    if((parseInt(c.substring(1,3),16)+parseInt(c.substring(3,5),16)+parseInt(c.substring(5,7),16))/3>128){
      c1=0;
    }
    else{
      c1=1;
    }
    b1.style.color=wb[c1];
    b.style.border="3px var(--clr1) solid";
    b.ondblclick=()=>{
      window.open(`popup1.html#${encodeURI(b.aid)}`,"_self").focus();
    };
    b.onclick=()=>{
      if(defi.hasOwnProperty(b.firstChild.value)){
        b.style.outline=`none`;
        delete defi[b.firstChild.value];
      }
      else{
        b.style.outline=`4px var(--oln) solid`;
        defi[b.firstChild.value]=1;
      }
      if(Object.keys(defi).length==0){
        del.title=`goto recycle bin`;
      }
      else{
        del.title=`delete(${Object.keys(defi).length})`;
      }
    };
    if(aqz.innerHTML=="no file"){
      aqz.innerHTML='';
    }
    b.onmousemove=()=>{
      document.querySelector("#sdl").select();
    }
    b.append(b1);
    aqz.append(b);
  });
};
function chcr(){
  mde.innerHTML=mode[dark];
  root.style.cssText+=`--bg: ${wb[dark^1]};`;
  root.style.cssText+=`--clr1: ${wb[dark]};`;
  if(dark){
    root.style.cssText+=`--btnh: #969696;`;
    root.style.cssText+=`--scrollbar-track: #2f2f2f`;
    root.style.cssText+=`--scrollbar-thumbh: #7d7d7d`;
    root.style.cssText+=`--oln: #00ff00`;
  }
  else{
    root.style.cssText+=`--btnh: #e2e2e2;`;
    root.style.cssText+=`--scrollbar-track: #e3e3e3`;
    root.style.cssText+=`--scrollbar-thumbh: #c4c4c4`;
    root.style.cssText+=`--oln: #ff0000`;
  }
}