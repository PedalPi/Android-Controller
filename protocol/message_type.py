from enum import Enum


class MessageType(Enum):
    CONNECTED = "connected"

    BANK = "bank"
    PEDALBOARD = "patch"
    EFFECT = "effect"
    PARAM = "param"

    ACK = "ack"
    ERROR = "error"

    def __str__(self):
        return self.value
