# Copyright 2018 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from webservice_serial.protocol.request_message import RequestMessage
from webservice_serial.protocol.request_verb import RequestVerb


class MessageBuilder(object):
    buffer = []

    @staticmethod
    def generate(message):
        """
        :param string message: Message part
        :return RequestMessage: Message received
        """
        if message != "EOF":
            MessageBuilder.buffer.append(message)
            return None

        buffer = MessageBuilder.clean_buffer()

        identifier, verb, path = buffer[0].split(" ")
        data = buffer[1]

        verb = MessageBuilder.discover_verb(verb)

        return MessageBuilder.generate_request_message(identifier, verb, path, data)

    @staticmethod
    def clean_buffer():
        buffer = MessageBuilder.buffer
        MessageBuilder.buffer = []
        return buffer

    @staticmethod
    def discover_verb(word):
        for verb in RequestVerb:
            if verb.value == word:
                return verb

        return RequestVerb.SYSTEM

    @staticmethod
    def generate_request_message(identifier, verb, path, data):
        """
        :param int identifier: Sequence number
        :param RequestVerb verb: Verb
        :param string path: Path
        :param string data: Data
        :return RequestMessage: message generated
        """
        data = json.loads(data)
        if verb == RequestVerb.GET:
            data = None

        return RequestMessage(identifier, verb, path, data)
