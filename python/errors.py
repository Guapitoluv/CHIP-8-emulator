class InvalidMsgTypeError(Exception):
    def __init__(self, caught_type: str) -> None:
        super().__init__(
            f"Invalid message type: {caught_type}"
        )
        self.caught_type: str = caught_type


class InvalidMsgFormatError(Exception):
    def __init__(self, caught_format: str) -> None:
        super().__init__(
            f"Invalid message format: {caught_format}"
        )
        self.caught_format: str = caught_format