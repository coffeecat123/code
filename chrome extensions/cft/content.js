console.log('Hello world!');
chrome.storage.sync.get(["color"], (e) => {
    //document.body.style.backgroundColor = e.color;
    console.log(e.color);
});