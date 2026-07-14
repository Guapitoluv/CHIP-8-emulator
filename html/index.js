console.log("JS iniciou");

export let ws;
export let waiting_key = false;

const startServerConnectionBtn = document.getElementById("init-connection");

startServerConnectionBtn.addEventListener("click", () => {
    ws = new WebSocket("ws://localhost:8765");
    
    ws.onopen = () => {
        console.log("WebSocket conectado")
    };
    
    ws.onerror = e => {
        console.log("Erro websocket "+e);
    }
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
    
        if (data.type === "display") {
            drawPixels(data.pixels);
        }
        
        if (data.type === "waiting_key") {
            console.log("received waiting_key")
            waiting_key = true;
        }
        
        if (data.type === "sound") {
            console.log("received sound")
        }
    };
    
    const canvas = document.getElementById("screen");
    const ctx = canvas.getContext("2d");
    
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