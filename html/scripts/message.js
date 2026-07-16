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

export class RestartMsg extends Message {
    constructor(key) {
        super("reset");
    }
}

export class PressedKeyMsg extends Message {
    constructor(key) {
        super("pressedkey");
        this.key = key;
    }
}

export class ReleasedKeyMsg extends Message {
    constructor(key) {
        super("releasedkey");
        this.key = key;
    }
}

export class SoundMsg extends Message {
    constructor(key) {
        super("sound");
        this.key = key;
    }
}