var root=document.querySelector(':root');
var hrt=document.querySelector("#hrt");
var cvs=document.querySelector("#cvs");
var ctx=cvs.getContext("2d");
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