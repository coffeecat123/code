const audioContextMap = {};

chrome.runtime.sendMessage({ type: 'offscreenReady' });

chrome.runtime.onMessage.addListener(async (message) => {
    if (message.type === 'processAudio') {
        const { mediaStreamId, tab_id } = message;
        await setupAudioProcessing(mediaStreamId, tab_id);
    }
    if (message.type === 'changeVolume') {
        const { tab_id, volume } = message;
        audioContextMap[tab_id].gainNode.gain.value = volume / 100;
    }
    if(message.type === 'stopCapture'){
        const { tab_id } = message;
        if (audioContextMap.hasOwnProperty(tab_id)) {
            delete audioContextMap[tab_id];
        }
    }
});

const setupAudioProcessing = async (mediaStreamId, tab_id) => {

    const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
            mandatory: {
                chromeMediaSource: "tab",
                chromeMediaSourceId: mediaStreamId
            }
        }
    });

    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const gainNode = audioContext.createGain();

    gainNode.gain.value = 1;
    source.connect(gainNode);
    gainNode.connect(audioContext.destination);

    audioContextMap[tab_id] = {
        audioContext: audioContext,
        gainNode: gainNode
    };
    console.log(audioContextMap);
};
