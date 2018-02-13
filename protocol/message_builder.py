import json

from android_controller.protocol.message import Message
from android_controller.protocol.message_type import Verb


class MessageBuilder(object):
    buffer = []

    @staticmethod
    def generate(message):
        if message != "EOF":
            MessageBuilder.buffer.append(message)
            return None

        buffer = MessageBuilder.clean_buffer()

        verb, path = buffer[0].split(" ")
        data = buffer[1]

        verb = MessageBuilder.discover_verb(verb)

        return MessageBuilder.generate_message(verb, path, data)

    @staticmethod
    def clean_buffer():
        buffer = MessageBuilder.buffer
        MessageBuilder.buffer = []
        return buffer

    @staticmethod
    def discover_verb(word):
        for verb in Verb:
            if verb.value == word:
                return verb

        return Verb.SYSTEM

    @staticmethod
    def generate_message(verb, path, data):
        # FIXME - Use path
        return Message(verb, json.loads(data))
