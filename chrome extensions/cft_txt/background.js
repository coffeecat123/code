let data={},//[name,[bgcolor,content]]
    dark=0,//0:light 1:dark
    durl={},//
    htcr="#ff0000",
    trash=[];//[name,[bgcolor,content,time]]

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['durl','htcr','trash','data','dark'], function(result) {
    if(result.data!=undefined)data=result.data;
    if(result.dark!=undefined)dark=result.dark;
    if(result.htcr!=undefined)htcr=result.htcr;
    if(result.durl!=undefined)durl=result.durl;
    if(result.trash!=undefined)trash=result.trash;
    chrome.storage.local.set({htcr,trash,durl,data,dark});
  });
});
chrome.storage.onChanged.addListener(function(changes, namespace) {
  if(changes.data!=undefined)data=changes.data.newValue;
  if(changes.dark!=undefined)dark=changes.dark.newValue;
  if(changes.durl!=undefined)durl=changes.durl.newValue;
  if(changes.htcr!=undefined)htcr=changes.htcr.newValue;
  if(changes.trash!=undefined)trash=changes.trash.newValue;
});