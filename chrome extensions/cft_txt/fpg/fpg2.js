let trash,data,dark;
let nt=Date.now();
let defi={};
let tr={};
let hl=2629743832;//2629743832
let wb=["#000000","#ffffff"];
var root=document.querySelector(':root');
var gbk=document.querySelector("#gbk");
var aqz=document.querySelector("#aqz");
var res=document.querySelector("#res");
var del=document.querySelector("#del");
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
chrome.storage.local.get(['trash','dark'],(result)=>{
  trash=result.trash;
  dark=result.dark;
  chcr();
  if(trash.length==0){
    aqz.style.color = "var(--oln)";
    aqz.style.fontSize = "50px";
    aqz.innerHTML = "no file";
    return;
  }
  for (let i=0;i<trash.length;i++){
    if(nt-trash[i][2]>hl){
      trash.splice(i,1);
      i--;
    }
    else{
      tr[trash[i][2]]=[trash[i]];
      let b=document.createElement("div");
      let b1=document.createElement("t");
      let c=trash[i][1][0],c1;
      b.className="fle";
      b.setAttribute('tme',trash[i][2]);
      b1.innerText=trash[i][0];
      b1.className="tet";
      b1.setAttribute("disabled","");
      b.aid=trash[i][0];
      b.style.background=c;
      if((parseInt(c.substring(1,3),16)+parseInt(c.substring(3,5),16)+parseInt(c.substring(5,7),16))/3>128){
        c1=0;
      }
      else{
        c1=1;
      }
      b1.style.color=wb[c1];
      b.style.border="3px var(--clr1) solid";
      b.onclick=()=>{
        let _a=`${b.getAttribute("tme")}:${b.firstChild.innerText}`;
        if(defi.hasOwnProperty(_a)){
          b.style.outline=`none`;
          delete defi[_a];
        }
        else{
          b.style.outline=`4px var(--oln) solid`;
          defi[_a]=1;
        }
        del.title=`delete(${Object.keys(defi).length})`;
        res.title=`restore(${Object.keys(defi).length})`;
      };
      b.onmousemove=()=>{
        document.querySelector("#sdl").select();
      }
      b.append(b1);
      aqz.append(b);
    }
  }
  chrome.storage.local.set({trash});
  if(aqz.childElementCount==0){
    aqz.style.color = "var(--oln)";
    aqz.style.fontSize = "50px";
    aqz.innerHTML = "no file";
  }
});
del.onclick=()=>{
  if(Object.keys(defi).length==0){
    alert('select one to delete');
    return;
  }
  if(confirm(del.title)){
    chrome.storage.local.get(['trash'],(rst)=>{
      let trh=rst.trash;
      for (let i=0;i<trh.length;i++){
        let _a=`${trh[i][2]}:${trh[i][0]}`;
        if(defi.hasOwnProperty(_a)){
          let aqq=aqz.children;
          for(let i=0;i<aqq.length;i++){
            if(aqq[i].getAttribute("tme")==_a.split(":")[0]&&aqq[i].firstChild.innerText==_a.substring(_a.indexOf(":")+1)){
              aqq[i].remove();
              break;
            }
          }
          trh.splice(i,1);
          delete defi[_a];
          i--;
        }
      }
      trash=trh;
      chrome.storage.local.set({trash:trh});
      del.title="delete(0)";
      defi={};
      if(Object.keys(trash).length==0){
        aqz.style.color = "var(--oln)";
        aqz.style.fontSize = "50px";
        aqz.innerHTML = "no file";
      }
    });
  }
};
res.onclick=()=>{
  if(Object.keys(defi).length==0){
    alert('select one to restore');
    return;
  }
  if(confirm(res.title)){
    chrome.storage.local.get(['trash','data'],(rst)=>{
      let trh=rst.trash;
      let dt=rst.data;
      for (let i=0;i<trh.length;i++){
        let _a=`${trh[i][2]}:${trh[i][0]}`;
        if(defi.hasOwnProperty(_a)){
          let aqq=aqz.children;
          for(let k=0;k<aqq.length;k++){
            if(aqq[k].getAttribute("tme")==_a.split(":")[0]&&aqq[k].firstChild.innerText==_a.substring(_a.indexOf(":")+1)){
              aqq[k].remove();
              break;
            }
          }
          let nname,newname=trh[i][0];
          let olddt=trh[i][1];
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
          trh.splice(i,1);
          delete defi[_a];
          i--;
        }
      }
      data=dt;
      trash=trh;
      chrome.storage.local.set({data:dt,trash:trh});
      del.title="restore(0)";
      defi={};
      if(Object.keys(trash).length==0){
        aqz.style.color = "var(--oln)";
        aqz.style.fontSize = "50px";
        aqz.innerHTML = "no file";
      }
    });
  }
};
gbk.onclick = () => {
    window.open(`fpg.html`, "_self");
};
function chcr(){
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