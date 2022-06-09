var root=document.querySelector(':root');
let trash,dark,data,htcr;
let wb=["#000000","#ffffff"];
let tet=document.querySelector(".tet");
chrome.storage.local.get(['trash','dark','htcr','data'], function(result) {
  trash=result.trash;
  dark=result.dark;
  htcr=result.htcr;
  data=result.data;
  root.style.cssText+=`--hrt: ${htcr};`;
  chcr(result.htcr);
  tet.value=`\
color: ${htcr}
files: ${Object.keys(data).length}
deleted: ${Object.keys(trash).length}
theme: ${dark?"dark":"light"}
${navigator.platform}
${navigator.language}
${navigator.appName}
${navigator.appCodeName}
`;
});
function chcr(c){
  if((parseInt(c.substring(1,3),16)+parseInt(c.substring(3,5),16)+parseInt(c.substring(5,7),16))/3>128){
    c1=0;
  }
  else{
    c1=1;
  }
  if(c1){
    root.style.cssText+=`--scrollbar-track: #2f2f2f`;
    root.style.cssText+=`--scrollbar-thumbh: #7d7d7d`;
  }
  else{
    root.style.cssText+=`--scrollbar-track: #e3e3e3`;
    root.style.cssText+=`--scrollbar-thumbh: #c4c4c4`;
  }
  root.style.cssText+=`--bg: ${c};`;
  root.style.cssText+=`--clr1: ${wb[c1]};`;
}