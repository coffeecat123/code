// 改進：使用物件管理狀態，避免全域變數污染
const captureState = {
    mediaStreamId: null,
    tab_id: null,
    capturingTabs: new Set()
};

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    chrome.offscreen.hasDocument().then(hasDocument => {
        if (hasDocument) {
            chrome.runtime.sendMessage({ type: 'stopCapture', tab_id: tabId });
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    chrome.storage.local.get(['data'], (result) => {
        let data = result.data || {};
        if (data.hasOwnProperty(tabId)) {
            chrome.action.setBadgeText({ text: data[tabId], tabId });
        }
    });
});

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.type === 'startCapture') {
        await handleStartCapture(message.tab_id, sendResponse);
    } else if (message.type === 'offscreenReady') {
        await handleOffscreenReady(sendResponse);
    } else if (message.type === 'stopCapture') {
        handleStopCapture(message.tab_id);
    }
});

async function handleStartCapture(tabId, sendResponse) {
    if (captureState.capturingTabs.has(tabId)) {
        return;
    }

    try {
        const mediaStreamId = await chrome.tabCapture.getMediaStreamId({
            targetTabId: tabId
        });

        captureState.mediaStreamId = mediaStreamId;
        captureState.tab_id = tabId;
        captureState.capturingTabs.add(tabId);

        const hasDocument = await chrome.offscreen.hasDocument();
        
        if (!hasDocument) {
            await createOffscreen();
        } else {
            chrome.runtime.sendMessage({
                type: 'processAudio',
                mediaStreamId,
                tab_id: tabId
            });
        }
    } catch (error) {
        //console.error('Error starting capture:', error);
    }
}

async function handleOffscreenReady(sendResponse) {
    console.log('Offscreen document ready, sending processAudio');
    chrome.runtime.sendMessage({
        type: 'processAudio',
        mediaStreamId: captureState.mediaStreamId,
        tab_id: captureState.tab_id
    });
}

function handleStopCapture(tabId) {
    captureState.capturingTabs.delete(tabId);
    chrome.runtime.sendMessage({
        type: 'stopCapture',
        tab_id: tabId
    });
}

async function createOffscreen() {
    try {
        await chrome.offscreen.createDocument({
            url: 'offscreen.html',
            reasons: ['AUDIO_PLAYBACK'],
            justification: 'Processing audio from captured tab'
        });
        console.log('Offscreen document created successfully');
    } catch (error) {
        console.error('Error creating offscreen document:', error);
    }
}