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

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect


class WebSocketClient(object):
    """
    :param int port: WebService port
    """

    def __init__(self, port):
        self.port = port
        self.connection = None
        self.message_listener = lambda message: ...
        self.on_connected_listener = lambda: ...

    @property
    def url(self):
        return 'ws://localhost:{}/ws/'.format(self.port)

    @gen.coroutine
    def connect(self):
        IOLoop.current().spawn_callback(lambda: self._connect())

    @gen.coroutine
    def _connect(self):
        self.connection = yield websocket_connect(self.url)
        self.on_connected_listener()
        self._await_messages(self.connection)

    @gen.coroutine
    def _await_messages(self, connection):
        while True:
            msg = yield connection.read_message()
            if msg is None:
                break

            message = json.loads(msg)
            self.message_listener(message)

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def register(self, token):
        data = json.dumps({'register': token})
        self.connection.write_message(data)
