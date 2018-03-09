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
        self.token_defined_listener = lambda token: ...
        self.message_listener = lambda message: ...

    @property
    def url(self):
        return 'ws://localhost:{}/ws/'.format(self.port)

    @gen.coroutine
    def connect(self):
        IOLoop.current().spawn_callback(lambda: self._connect())

    @gen.coroutine
    def _connect(self):
        self.connection = yield websocket_connect(self.url)
        self._await_messages(self.connection)

    @gen.coroutine
    def _await_messages(self, connection):
        while True:
            msg = yield connection.read_message()
            if msg is None:
                break

            message = json.loads(msg)

            if message['type'] == 'TOKEN':
                self.token_defined_listener(message['value'])
            else:
                self.message_listener(message)

    def close(self):
        if self.connection is not None:
            self.connection.close()
