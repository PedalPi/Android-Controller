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

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError

from webservice_serial.protocol.message_builder import MessageBuilder


class WebServiceSerialClient(object):

    def __init__(self, address, port, encoding="utf-8"):
        self.address = address
        self.port = port
        self.encoding = encoding

        self.stream = None
        self.message_listener = lambda message: ...
        self.connected_listener = lambda: ...

        self.disconnected_listener = lambda: print('Disconnected :(')

    def connect(self):
        IOLoop.current().spawn_callback(self._connect)

    @gen.coroutine
    def _connect(self):
        self.stream = yield self._try_connect()
        if self.stream is None:
            return

        self.connected_listener()
        yield self._start_read_data()

    @gen.coroutine
    def _try_connect(self):
        try:
            stream = yield TCPClient().connect(self.address, self.port)
            return stream
        except StreamClosedError as e:
            self.disconnected_listener()
            return None

    @gen.coroutine
    def _start_read_data(self):
        while True:
            data = yield self._read_data()
            if data is None:
                break
            data = data.decode(self.encoding).strip()

            generated = MessageBuilder.generate(data)
            if generated is not None:
                self.message_listener(generated)

    @gen.coroutine
    def _read_data(self):
        try:
            data = yield self.stream.read_until('\n'.encode(self.encoding))
        except StreamClosedError as e:
            self.disconnected_listener()
            return None

        return data

    def send(self, message):
        if self.stream is None:
            return

        try:
            text = str(message).encode(self.encoding)
            self.stream.write(text)
        except StreamClosedError:
            self.disconnected_listener()

    def close(self):
        if self.stream is not None and not self.stream.closed():
            self.stream.close()
