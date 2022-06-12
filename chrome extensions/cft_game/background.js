let htcr="#ff0000";

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['htcr'], function(result) {
    if(result.htcr!=undefined)htcr=result.htcr;
    chrome.storage.local.set({htcr});
  });
});
chrome.storage.onChanged.addListener(function(changes, namespace) {
  if(changes.htcr!=undefined)htcr=changes.htcr.newValue;
});