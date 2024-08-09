let mediaStreamId,tab_id;

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    chrome.offscreen.hasDocument().then(hasDocument => {
        if (hasDocument) {
            chrome.runtime.sendMessage({ type: 'stopCapture',tab_id: tabId});
        }
    });
});
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    chrome.storage.local.get(['data'], (result) => {
        let data = result.data || {};
        if(data.hasOwnProperty(tabId)) {
            chrome.action.setBadgeText({ text: data[tabId], tabId });
        }
    });
});
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.type === 'startCapture') {
        mediaStreamId = await chrome.tabCapture.getMediaStreamId({
            targetTabId: message.tab_id
        });
        tab_id = message.tab_id;
        console.log(tab_id);
        chrome.offscreen.hasDocument().then(hasDocument => {
            if (!hasDocument) {
                createoffscreen();
            }else{
                console.log('send');
                chrome.runtime.sendMessage({
                    type: 'processAudio',
                    mediaStreamId: mediaStreamId,
                    tab_id: tab_id
                });
            }
        });
    }
    if (message.type === 'offscreenReady') {
        console.log('send');
        chrome.runtime.sendMessage({
            type: 'processAudio',
            mediaStreamId: mediaStreamId,
            tab_id: tab_id
        });
    }
});
async function createoffscreen() {
    await chrome.offscreen.createDocument({
        url: 'offscreen.html',
        reasons: ['CLIPBOARD'],
        justification: 'Reason for needing the document',
    });
    console.log("created");
}