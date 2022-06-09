console.log('Hello world!vlm-3');
let gainNode;
//
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('request',request);
  try{
  if(request.cha){
    navigator.mediaDevices.getUserMedia({
      video: false,
      audio: true,
      audio: {
        mandatory: {
          chromeMediaSource: 'tab',
          chromeMediaSourceId: request.streamId
        }
      }
    }).then((stream) => {
      console.log(stream);
      var audioCtx = new AudioContext();
      var source = audioCtx.createMediaStreamSource(stream);
      gainNode = audioCtx.createGain();
      gainNode.gain.value = 1;
      source.connect(gainNode);
      gainNode.connect(audioCtx.destination);
    });
  }
  gainNode.gain.value = Number(request.vlm) / 100;
  console.log(gainNode.gain.value);
  }catch(e){
    console.log(e);
  }
});