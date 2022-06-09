let rmea=[`<svg class="btn" width="20px" version="1.0" viewBox="0 0 980 982" style="position:relative;left: 0px;top: 1px;"><g transform="translate(0.000000,982.000000) scale(0.100000,-0.100000)"><path d="M1047 9794 c-115 -18 -282 -74 -385 -130 -322 -176 -544 -471 -639 -851 -16 -63 -17 -322 -20 -3878 -3 -2680 -1 -3835 7 -3893 22 -169 96 -363 191 -504 59 -86 189 -220 280 -288 132 -98 291 -171 476 -217 63 -16 321 -17 3863 -20 3320 -3 3807 -2 3890 11 344 54 661 241 861 510 79 105 162 275 196 401 l28 100 3 2608 2 2607 -305 0 -305 0 -2 -2577 -3 -2578 -26 -67 c-37 -95 -80 -157 -162 -235 -85 -80 -201 -144 -313 -173 -76 -20 -130 -20 -3819 -20 l-3743 0 -80 23 c-105 31 -182 77 -264 159 -74 73 -137 189 -157 286 -8 38 -11 1139 -11 3816 0 3721 0 3764 20 3840 26 104 81 204 157 286 104 113 220 176 364 199 43 7 868 11 2522 11 l2457 0 -2 293 -3 292 -2495 2 c-2063 1 -2510 -1 -2583 -13z"/><path d="M7952 9790 c-85 -23 -170 -66 -233 -118 -72 -59 -4794 -4637 -4822 -4674 -36 -48 -73 -125 -92 -193 -10 -33 -312 -637 -672 -1343 -360 -705 -661 -1303 -670 -1328 -22 -64 -14 -195 15 -250 54 -106 127 -155 238 -162 40 -2 93 0 117 6 24 7 322 145 663 308 945 452 1753 839 1914 916 80 39 176 79 215 90 134 38 189 73 335 214 74 72 1138 1101 2365 2288 1227 1187 2260 2189 2297 2228 174 183 217 430 113 653 -18 39 -47 89 -66 112 -19 23 -292 291 -607 596 -602 582 -630 606 -762 648 -97 31 -254 35 -348 9z m288 -720 c57 -29 72 -42 451 -412 358 -348 363 -354 363 -478 0 -124 -6 -132 -389 -504 l-336 -326 -530 522 c-291 288 -529 526 -529 530 0 3 147 148 326 322 303 294 361 343 434 367 46 15 162 4 210 -21z m-890 -1620 c294 -281 535 -515 535 -520 0 -12 -3428 -3331 -3437 -3328 -14 6 -1068 1032 -1066 1038 4 10 3422 3320 3428 3320 4 0 247 -230 540 -510z m-3864 -3752 c334 -324 422 -414 412 -423 -20 -19 -1602 -944 -1642 -960 -105 -44 -216 25 -216 134 0 37 9 61 43 117 159 264 964 1544 970 1544 5 0 199 -185 433 -412z"/></g></svg>`,`<svg class="btn" width="25px" version="1.1" x="0px" y="0px" viewBox="0 0 335.765 335.765" style="position:relative;left: 0px;top: 2px;"><polygon points="311.757,41.803 107.573,245.96 23.986,162.364 0,186.393 107.573,293.962 335.765,65.795"/></svg>`]
let url = location.href;
let id = "";
let scl=1,scm=0.05;
let dark;
let keydown=0;
let sv = 0;
let oldname,oldinn;
let wb = ["#000000", "#ffffff"];
var bgc = document.querySelector("#bgc");
var gbk = document.querySelector("#gbk");
var ipc = document.querySelector("#ipc");
var aqz = document.querySelector("#aqz");
var aqz = document.querySelector("#aqz");
var rme = document.querySelector("#rme");
var rna = document.querySelector("#rna");
var root = document.querySelector(':root');
var aqw = aqz.contentWindow.document.body;
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
rme.innerHTML=rmea[sv];
chrome.storage.local.get(['dark'], function(result) {
  dark = result.dark;
  chcr(wb[dark ^ 1]);
  id=decodeURI(location.hash.substring(1));
  if(id==""){
    error_page();
  }
  else{
    loin();
  }
});
function loin() {
  document.title=id;
  chrome.storage.local.get(['data', 'dark'], function(result) {
    rna.value = id;
    if(result.data[id]==undefined){
      error_page();
      return;
    }
    aqw.innerHTML = result.data[id][1];
    chcr(result.data[id][0]);
    scl=result.data[id][2]
    aqw.style.transform=`scale(${scl})`;
    start();
    aqw.setAttribute("contenteditable", "");
  });
}
function error_page() {
  rna.value = "error";
  rna.style.color = "var(--oln)";
  aqw.style.fontSize = "50px";
  aqw.innerHTML = "no file";
}
function chcr(c) {
  if ((parseInt(c.substring(1, 3), 16) + parseInt(c.substring(3, 5), 16) + parseInt(c.substring(5, 7), 16)) / 3 > 128) {
    c1 = 0;
  }
  else {
    c1 = 1;
  }
  dark = c1;
  if (dark) {
    root.style.cssText += `--btnh: #969696;`;
    root.style.cssText += `--scrollbar-track: #2f2f2f`;
    root.style.cssText += `--scrollbar-thumbh: #7d7d7d`;
    root.style.cssText+=`--oln: #00ff00`;
  }
  else {
    root.style.cssText += `--btnh: #e2e2e2;`;
    root.style.cssText += `--scrollbar-track: #e3e3e3`;
    root.style.cssText += `--scrollbar-thumbh: #c4c4c4`;
    root.style.cssText+=`--oln: #ff0000`;
  }
  aqw.style.color=`${wb[c1]}`;
  ipc.value = c;
  root.style.cssText += `--bg: ${c};`;
  root.style.cssText += `--clr1: ${wb[c1]};`;
}
gbk.onclick = () => {
  window.open(`fpg.html`, "_self");
};
document.body.onmousemove=(e)=>{
  if(sv==0){
    if(e.target.id=="rna"&&keydown){
      document.querySelector("#sdl").select();
    }
  }
}
document.body.onmouseup=(e)=>{
  keydown=0;
}
document.body.onmousedown=(e)=>{
  keydown=1;
}
function start() {
  aqw.style["overflow-wrap"] = "unset";
  aqw.style["overflow"] = "auto";
  aqw.style["transform-origin"] = "0px 0px";
  aqw.oninput=()=>{
    sav();
  };
  const keyCodeMap = {
    // 91: true, // command
    61: true,
    107: true, // 数字键盘 +
    109: true, // 数字键盘 -
    173: true, // 火狐 - 号
    187: true, // +
    189: true, // -
  };
  // 覆盖ctrl||command + ‘+’/‘-’
  aqw.onkeydown = function (event) {
    const e = event || window.event;
    const ctrlKey = e.ctrlKey || e.metaKey;
    if (ctrlKey && keyCodeMap[e.keyCode]) {
      e.preventDefault();
    } else if (e.detail) { // Firefox
      event.returnValue = false;
    }
  };
  // 覆盖鼠标滑动
  aqw.addEventListener('wheel', (e) => {
    if (e.ctrlKey) {
      if (e.deltaY < 0) {
        e.preventDefault();
        return false;
      }
      if (e.deltaY > 0) {
        e.preventDefault();
        return false;
      }
    }
  }, { passive: false });
  aqz.contentDocument.onwheel=(e)=>{
    if(e.ctrlKey){
      if(e.deltaY>0){
        scl-=scm;
      }
      else{
        scl+=scm;
      }
      scl=Number(scl.toFixed(2));
      if(scl<=scm)scl=scm;
      aqw.style.transform=`scale(${scl})`;
      chrome.storage.local.get(['data'],(rst)=>{
        dt = rst.data;
        dt[id][2] = scl;
        chrome.storage.local.set({data:dt});
      });
    }
  };
  ipc.oninput=()=>{
    let data, icl = ipc.value;
    chcr(icl);
    chrome.storage.local.get(['data'],(rst)=>{
      data = rst.data;
      data[id][0] = icl;
      chrome.storage.local.set({data});
    });
  };
  rme.onclick=()=>{
    if (sv == 0) {
      aqw.removeAttribute("contenteditable");
      sv=1;
      oldname=rna.value;
      gbk.style["pointer-events"]="none";
      bgc.style["pointer-events"]="none";
      rna.style.border=`2px var(--clr1) solid`;
      rna.removeAttribute("disabled");
      rna.focus();
      rna.select();
    }
    else{
      gbk.style["pointer-events"]="unset";
      bgc.style["pointer-events"]="unset";
      rna.style.border=`2px var(--bg) solid`;
      rna.setAttribute("disabled","");
      let newname=rna.value;
      if(oldname!=newname){
        chrome.storage.local.get(['data'],(rst)=>{
          let dt = rst.data;
          let olddt=dt[oldname];
          let nname;
          delete dt[oldname];
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
          chrome.storage.local.set({data:dt});
          rna.value=nname;
          id=nname;
          document.title=id;
          location.hash=id;
        });
      }
      document.querySelector("#sdl").select();
      aqw.setAttribute("contenteditable", "");
      sv = 0;
    }
    rme.innerHTML=rmea[sv];
  };
  function sav() {
    let data, icl = aqw.innerHTML;
    chrome.storage.local.get(['data'],(rst)=>{
      data = rst.data;
      data[id][1] = icl;
      chrome.storage.local.set({data});
    });
  }
}