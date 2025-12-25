let ipt = document.querySelector("#ipt");
let spn = document.querySelector("#spn");
let bk = document.querySelector(".bk");
let cr = document.querySelector(".cr");

chrome.action.setBadgeBackgroundColor({
    color: "#fff000"
});

let tab_id;
let max = 300, min = 0, wi = 200;

ipt.max = max;
ipt.min = min;
ipt.value = 100;
document.querySelector(':root').style.cssText += `--wi: ${wi}px;`;

chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    if (tabs.length > 0) {
        tab_id = tabs[0].id;
        chrome.storage.local.get(['data'], (result) => {
            if (result.data && result.data[tab_id] !== undefined) {
                ipt.value = result.data[tab_id];
            }
            spn.innerText = ipt.value + "%";
            pt();
            if (ipt.value != 100) {
                chrome.runtime.sendMessage({
                    type: 'startCapture',
                    tab_id
                });

                chrome.runtime.sendMessage({
                    type: 'changeVolume',
                    tab_id,
                    volume: ipt.value
                });
            }
        });
    }
});

function pt() {
    cr.style.left = (wi - 16) * ipt.value / max + 8 + "px";
    bk.style["background-size"] = `${ipt.value / max * 100}% 100%`;
}

ipt.addEventListener("input", () => {
    pt();
    updateVolume();
});
document.querySelector(".d2").addEventListener("dblclick", () => {
    ipt.value = 100;
    pt();
    updateVolume();
});

function updateVolume() {
    spn.innerText = ipt.value + "%";
    chrome.action.setBadgeText({ text: ipt.value, tabId: tab_id });

    chrome.storage.local.get(['data'], (result) => {
        let data = result.data || {};
        data[tab_id] = ipt.value;

        chrome.storage.local.set({ data }, () => {
            if (ipt.value == 100) {
                chrome.runtime.sendMessage({
                    type: 'stopCapture',
                    tab_id
                });
                return;
            }
            chrome.runtime.sendMessage({
                type: 'startCapture',
                tab_id
            });

            chrome.runtime.sendMessage({
                type: 'changeVolume',
                tab_id,
                volume: ipt.value
            });
        });
    });
}