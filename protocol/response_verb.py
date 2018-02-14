from enum import Enum


class ResponseVerb(Enum):
    RESPONSE = "RESPONSE"
    EVENT = "EVENT"

    def __str__(self):
        return self.value
