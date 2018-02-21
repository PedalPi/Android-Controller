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

from application.component.component import Component
from webservice_serial.protocol.response_verb import ResponseVerb

from webservice_serial.request_message_processor import RequestMessageProcessor
from webservice_serial.webservice_serial_client import WebServiceSerialClient
from webservice_serial.websocket_client import WebSocketClient

from time import sleep


class WebServiceSerial(Component):
    port = 8888

    def __init__(self, application, target, ws_port=3000):
        """
        :param Application application: that AndroidController will be executed
        :param Target target: Device protocol expected to communication
        :param int ws_port: WebService port
        """
        super(WebServiceSerial, self).__init__(application)

        self.target = target
        self._client = WebServiceSerialClient('localhost', WebServiceSerial.port)
        self.request_message_processor = RequestMessageProcessor(ws_port)
        self._websocket_client = WebSocketClient(ws_port)

    def init(self):
        self._client.connected_listener = self._on_connected
        self._client.message_listener = self._process_message
        self._client.disconnected_listener = lambda: self._try_connect(5)

        self.request_message_processor.processed_listener = self._on_processed

        self._websocket_client.token_defined_listener = self._on_token_defined
        self._websocket_client.message_listener = self._on_event

        self._websocket_client.connect()

        self._try_connect()

    def _try_connect(self, delay=0):
        self._log('Trying to connect with {}', self.target.name)
        self.target.init(self.application, WebServiceSerial.port)
        sleep(delay)
        self._client.connect()

    def _on_token_defined(self, token):
        self.request_message_processor.token = token

    def close(self):
        self.request_message_processor.close()
        self.target.close()
        self._websocket_client.close()
        self._client.close()

    def _on_connected(self):
        self._log('{} connected', self.target.name)

        from webservice_serial.protocol.keyboard.keyboard import KeyEvent, KeyNumber, KeyCode
        from webservice_serial.protocol.response_message import ResponseMessage
        from webservice_serial.protocol.response_verb import ResponseVerb

        from time import sleep
        while True:
        #    sleep(1)
        #    self.target.adb.execute('shell input keyevent 19')
        #    sleep(1)
        #    self.target.adb.execute('shell input keyevent 20')
            message = KeyEvent(KeyCode.DOWN, KeyNumber.DPAD_DOWN)
            msg = ResponseMessage(ResponseVerb.KEYBOARD_EVENT, message)
            self._log('Message sent: {}', msg)
            self._client.send(msg)

            message = KeyEvent(KeyCode.DOWN, KeyNumber.DPAD_DOWN)
            msg = ResponseMessage(ResponseVerb.KEYBOARD_EVENT, message)
            self._log('Message sent: {}', msg)
            self._client.send(msg)

            sleep(1)

            message = KeyEvent(KeyCode.DOWN, KeyNumber.DPAD_UP)
            msg = ResponseMessage(ResponseVerb.KEYBOARD_EVENT, message)
            self._log('Message sent: {}', msg)
            self._client.send(msg)

            '''
            sleep(1)

            message = KeyEvent(KeyCode.DOWN, KeyNumber.DPAD_CENTER)
            msg = ResponseMessage(ResponseVerb.KEYBOARD_EVENT, message)
            self._log('Message sent: {}', msg)
            self._client.send(msg)
            '''
            break

    def _process_message(self, message):
        """
        :param RequestMessage message:
        """
        self._log('Message received: {}', message)

        self.request_message_processor.process(message)

    def _on_processed(self, request_message, response_message):
        response_message = self.target.process(request_message, response_message)

        self._log('Message sent: {}', response_message)
        self._client.send(response_message)

    def _on_event(self, message):
        response_message = self.request_message_processor.process_event(message)
        response_message = self.target.process(None, response_message)

        self._log('Message sent: {}', response_message)
        self._client.send(response_message)

    def _log(self, message, *args, **kwargs):
        self.application.log('{} - {}'.format(self.__class__.__name__, message), *args, **kwargs)
