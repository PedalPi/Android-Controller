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

from webservice_serial.request_message_processor import RequestMessageProcessor
from webservice_serial.webservice_serial_client import WebServiceSerialClient
from webservice_serial.websocket_client import WebSocketClient


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

        self.request_message_processor.processed_listener = self._on_processed

        self.target.init(self.application, WebServiceSerial.port)

        self._websocket_client.token_defined_listener = self._on_token_defined
        self._websocket_client.message_listener = self._on_event

        self._websocket_client.connect()
        self._client.connect()

    def _on_token_defined(self, token):
        self.request_message_processor.token = token

    def close(self):
        self.request_message_processor.close()
        self.target.close()
        self._websocket_client.close()
        self._client.close()

    def _on_connected(self):
        self.application.log('AndroidController - DisplayView connected')

    def _process_message(self, message):
        self.application.log('AndroidController - Message received: {}', message)

        self.request_message_processor.process(message)

    def _on_processed(self, request_message, response_message):
        response_message = self.target.process(request_message, response_message)

        self.application.log('AndroidController - Message sent: {}', response_message)
        self._client.send(response_message)

    def _on_event(self, message):
        response_message = self.request_message_processor.process_event(message)
        response_message = self.target.process(None, response_message)

        self.application.log('AndroidController - Message sent: {}', response_message)
        self._client.send(response_message)
