from application.component.component import Component

from webservice_serial.webservice_serial_client import WebServiceSerialClient
from webservice_serial.request_message_processor import RequestMessageProcessor


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

    def init(self):
        self._client.connected_listener = self._on_connected
        self._client.message_listener = self._process_message

        self.request_message_processor.processed_listener = self._on_processed

        self.target.init(self.application, WebServiceSerial.port)
        self._client.connect()

    def close(self):
        self.request_message_processor.close()
        self.target.close()

    def _on_connected(self):
        self.application.log('AndroidController - DisplayView connected')

    def _process_message(self, message):
        self.application.log('AndroidController - Message received: {}', message)

        self.request_message_processor.process(message)

    def _on_processed(self, request_message, response_message):
        self.application.log('AndroidController - Message sent: {}', response_message)

        response_message = self.target.process(request_message, response_message)
        self._client.send(response_message)
