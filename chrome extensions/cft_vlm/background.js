chrome.runtime.onInstalled.addListener(() => {
  console.log('Hello!');
});
let gd={};
let data={};
chrome.storage.local.set({data}, function() {
  console.log(data);
});
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
  console.log("rqt:",request);
  chrome.storage.local.get(['data'], (result)=>{
    data=result.data;
    if(request.cha){
      chrome.tabCapture.capture({audio: !0,video: !1}, (audio) => {
        console.log('cft',chrome.runtime.lastError);
        var audioCtx = new AudioContext();
        var source = audioCtx.createMediaStreamSource(audio);
        let gainNode = audioCtx.createGain();
        gainNode.gain.value=Number(data[request.tab_id])/100;
        source.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        gd[request.tab_id]=gainNode;
      });
    }
    else{
      try{
        gd[request.tab_id].gain.value=Number(data[request.tab_id])/100;
      }catch(e){
        console.log(e);
      }
    }
    //sendResponse('我收到你的消息了：'+JSON.stringify("request"));
  });
})