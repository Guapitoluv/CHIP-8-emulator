console.log("JS iniciou");

import { RestartMsg } from "./message.js";

export class Server {
    constructor(url, startConn=false) {
        this.url = url;
        this.ws = null;
        this.connection = false;
        this.waiting_key = false;
        
        this.onDisplay = null;
        this.onSound = null;
        this.onWaitingKey = null;
        
        if (startConn) this.startConnection();
    }
    
    startConnection() {
        this.ws = new WebSocket(this.url);
        this.connection = true;
        
        this.ws.onopen = () => console.log("WebSocket conectado");
        this.ws.onerror = e => console.log("Erro websocket "+e);
        this.ws.onmessage = e => this.onmessage(e);
    }
    
    onmessage(event) {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
            case "display": this.onDisplay?.(data.pixels); break;
            case "sound": this.onSound?.(data.playing); break;
            case "waiting_key": this.onWaitingKey?.(); break;
        }
    }
}


const startServerConnectionBtn = document.getElementById("init-connection");
const restartBtn = document.getElementById("restart");
const canvas = document.getElementById("screen");
const ctx = canvas.getContext("2d");
export const server = new Server("ws://localhost:8765", false);

function sendRestart() {
    const msg = new RestartMsg();
    console.log("sending restart");
    server.ws.send(JSON.stringify(msg));
}

restartBtn.addEventListener("click", () => {
    if (server.ws) sendRestart()
});

startServerConnectionBtn.addEventListener("click", () => {
    server.startConnection()
    
    server.onDisplay = drawPixels;
    
    server.onWaitingKey = () => {
        console.log("received waiting_key")
        server.waiting_key = true;
    }
    server.onSound = (playing) => console.log("received sound");
    
    function drawPixels(pixels) {
        const width = 64;
        const height = 32;
        
        const image = ctx.createImageData(width, height);
        
        for (let i=0;i<pixels.length;i++) {
            const color = pixels[i] ? 255 : 0;
    
            image.data[i * 4 + 0] = 0; // R
            image.data[i * 4 + 1] = color; // G
            image.data[i * 4 + 2] = 0; // B
            image.data[i * 4 + 3] = 255;   // Alpha
        }
        
        ctx.putImageData(image, 0, 0);
    }
});