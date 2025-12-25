const audioContextMap = {};

chrome.runtime.sendMessage({ type: 'offscreenReady' });

chrome.runtime.onMessage.addListener(async (message) => {
    if (message.type === 'processAudio') {
        const { mediaStreamId, tab_id } = message;
        await setupAudioProcessing(mediaStreamId, tab_id);
    }
    if (message.type === 'changeVolume') {
        const { tab_id, volume } = message;
        const ctx = audioContextMap[tab_id];
        if (!ctx) return;

        ctx.gainNode.gain.value = volume / 100;
    }


    if (message.type === 'stopCapture') {
        const { tab_id } = message;
        stopAudioProcessing(tab_id);
    }
});

const setupAudioProcessing = async (mediaStreamId, tab_id) => {
    if (audioContextMap[tab_id]) {
        stopAudioProcessing(tab_id);
    }

    const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
            mandatory: {
                chromeMediaSource: "tab",
                chromeMediaSourceId: mediaStreamId
            }
        }
    });

    const audioContext = new AudioContext();
    await audioContext.resume();

    const source = audioContext.createMediaStreamSource(stream);
    const gainNode = audioContext.createGain();

    gainNode.gain.value = 1;

    source.connect(gainNode);
    gainNode.connect(audioContext.destination);

    audioContextMap[tab_id] = {
        audioContext,
        gainNode,
        stream
    };

    console.log('Audio started:', tab_id);
};

const stopAudioProcessing = async (tab_id) => {
    const ctx = audioContextMap[tab_id];
    if (!ctx) return;

    ctx.stream.getTracks().forEach(track => track.stop());
    await ctx.audioContext.close();

    delete audioContextMap[tab_id];
    console.log('Audio stopped:', tab_id);
};
