class Message {
    constructor(type) {
        this.type = type;
    }
}

export class WaitingKeyMsg extends Message {
    constructor(key) {
        super("waiting_key");
    }
}

export class PressedKeyMsg extends Message {
    constructor(key) {
        super("pressedkey");
        this.key = key;
    }
}

export class SoundMsg extends Message {
    constructor(key) {
        super("sound");
        this.key = key;
    }
}