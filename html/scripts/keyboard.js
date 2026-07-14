import { ws, waiting_key } from "./index.js";
import { PressedKeyMsg } from "./message.js";

const keysound = new Audio("midia/sounds/dragon-studio-single-key-press-393908.mp3")
const keyboard = document.getElementById("keyboard");
const chars = "123C456D789EA0BF";

keysound.volume = 0.25;


function sendKey(key) {
    const msg = new PressedKeyMsg(key);
    console.log("sending key: "+key);
    ws.send(JSON.stringify(msg));
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
    
    key.addEventListener("click", () => {
        console.log("clicked key: "+currChar);
        keysound.currentTime = 0;
        keysound.play();
        if (waiting_key) sendKey(chars[i]);
    });
    
    keyboard.append(key)
}