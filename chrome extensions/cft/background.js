let clr = '#330000';

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({color: clr,bk:"#000000"}, function() {
    console.log('Default background color set to %c   ', `background-color: ${clr}`);
  });
});