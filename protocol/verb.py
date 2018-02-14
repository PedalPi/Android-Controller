from enum import Enum


class Verb(Enum):
    SYSTEM = "SYSTEM"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __str__(self):
        return self.value
