chrome.runtime.onInstalled.addListener(() => {
  console.log('Hello!');
});
chrome.storage.local.set({data:{}},() => {
  console.log('ok!');
});
