let htcr="#ff0000",
    btsr=0;

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['htcr','btsr'], function(result) {
    if(result.htcr!=undefined)htcr=result.htcr;
    if(result.btsr!=undefined)btsr=result.btsr;
    chrome.storage.local.set({htcr,btsr});
  });
});
chrome.storage.onChanged.addListener(function(changes, namespace) {
  if(changes.htcr!=undefined)htcr=changes.htcr.newValue;
  if(changes.btsr!=undefined)btsr=changes.btsr.newValue;
});