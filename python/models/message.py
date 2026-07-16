from dataclasses import dataclass, asdict, field
import json


@dataclass
class Message:
    type: str

    async def send(self, ws):
        await ws.send(json.dumps(asdict(self)))


@dataclass
class PressedKeyMsg(Message):
    key: str
    type: str = field(init=False, default="pressedkey")


@dataclass
class ReleasedKeyMsg(Message):
    key: str
    type: str = field(init=False, default="releasedkey")


@dataclass
class WaitingKeyMsg(Message):
    type: str = field(init=False, default="waiting_key")


@dataclass
class DisplayMsg(Message):
    pixels: list
    type: str = field(init=False, default="display")


@dataclass
class SoundMsg(Message):
    playing: bool
    type: str = field(init=False, default="sound")


@dataclass
class DelayMsg(Message):
    value: bool
    type: str = field(init=False, default="delay")


@dataclass
class ResetMsg(Message):
    type: str = field(init=False, default="reset")
