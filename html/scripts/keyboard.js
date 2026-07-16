import { server } from "./index.js";
import { PressedKeyMsg, ReleasedKeyMsg } from "./message.js";

const keysound = new Audio("midia/sounds/dragon-studio-single-key-press-393908.mp3")
const keyboard = document.getElementById("keyboard");
const chars = "123C456D789EA0BF";

keysound.volume = 0.25;

function sendKey(key) {
    const msg = new PressedKeyMsg(key);
    console.log("sending key: "+key);
    server.ws.send(JSON.stringify(msg));
}

function releaseKey(key) {
    const msg = new ReleasedKeyMsg(key);
    console.log("releasing key: "+key);
    server.ws.send(JSON.stringify(msg));
}


for (let i=0,j=0;i<chars.length;i++) {
    const currChar = chars[i];
    const key = document.createElement("button");
    
    key.id = currChar;
    key.dataset.key = currChar;
    key.textContent = currChar;
    
    if (i%4===0) j++;
    
    key.style.gridRow = j;
    key.style.gridColumn = i%4+1;
    
    key.addEventListener("pointerdown", () => {
        console.log("pressed key: "+currChar);
        keysound.currentTime = 0;
        keysound.play();
        sendKey(chars[i]);
    });
    
    
    key.addEventListener("pointerup", () => {
        console.log("clicked key: "+currChar);
        keysound.currentTime = 0;
        keysound.play();
        releaseKey(chars[i])
    });
    
    keyboard.append(key)
}