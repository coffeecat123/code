let ipt = document.querySelector("#ipt");
let spn = document.querySelector("#spn");
let bk = document.querySelector(".bk");
let cr = document.querySelector(".cr");
let cr1 = document.querySelector(".cr1");
chrome.action.setBadgeBackgroundColor({
  color: "#fff000"
});
let cha = 1,
  tab_id,
  max=1000,min=0,wi=200;
ipt.max=max;
ipt.min=min;
ipt.value=100;
document.querySelector(':root').style.cssText+=`--wi: ${wi}px;`;
chrome.tabs.query({
  currentWindow: true,
  active: true
}, function(tabs) {
  tab_id = tabs[0].id;
  chrome.storage.local.get(['data'],(result)=>{
    console.log(result.data);
    if (result.data[tab_id] != undefined) {
      console.log(result.data[tab_id]);
      ipt.value = result.data[tab_id];
      spn.innerText = ipt.value + "%";
      chrome.action.setBadgeText({text: result.data[tab_id],tabId: tab_id});
      cha = 0;
    }
    console.log(cha);
    pt();
  });
});
function pt(){
  cr.style.left=(wi-16)*ipt.value/max+8+"px";
  cr1.style.left=(wi-16)*ipt.value/max+8+"px";
  bk.style["background-size"]=`${ipt.value/max*100}% 100%`;
}
ipt.addEventListener("input",()=>{
  pt();
  _wle();
});
function _wle() {
  let a=cha;
  cha=0;
  spn.innerText = ipt.value + "%";
  chrome.action.setBadgeText({text: ipt.value,tabId: tab_id});
  chrome.storage.local.get(['data'], (result)=>{
    console.log(result.data);
    let data = result.data;
    data[tab_id] = ipt.value;
    chrome.storage.local.set({data},()=>{
      if(a){
        chrome.tabCapture.getMediaStreamId({consumerTabId: tab_id}, (streamId) => {
        send({streamId,vlm:ipt.value,cha:a});
        });
      }
      else{
        send({vlm:ipt.value,cha:a});
      }
    });
  });
};
function send(msg){
  chrome.tabs.sendMessage(tab_id, msg);
}