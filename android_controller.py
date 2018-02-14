from application.component.component import Component

from android_controller.adb import Adb
from android_controller.android_controller_client import AndroidControllerClient
from android_controller.request_message_processor import RequestMessageProcessor


class AndroidController(Component):
    port = 8888
    activity = 'io.github.pedalpi.pedalpi_display/io.github.pedalpi.pedalpi_display.MainActivity'

    def __init__(self, application, ws_port, adb_command="adb"):
        """
        :param Application application: that AndroidController will be executed
        :param int ws_port:
        :param string adb_command: Command that call the Android Debug Bridge
                                   In Raspberry maybe be a `./adb` executable file
        """
        super(AndroidController, self).__init__(application)

        self._client = AndroidControllerClient('localhost', AndroidController.port)
        self.adb = Adb(adb_command, application.log)
        self.request_message_processor = RequestMessageProcessor(ws_port)

    def init(self):
        self._client.connected_listener = self._on_connected
        self._client.message_listener = self._process_message

        self.request_message_processor.processed_listener = self._on_processed

        self.adb.start(AndroidController.port, AndroidController.activity)
        self._client.connect()

    def close(self):
        self.request_message_processor.close()
        self.adb.close(AndroidController.port)

    def _on_connected(self):
        self.application.log('AndroidController - DisplayView connected')

    def _process_message(self, message):
        self.application.log('AndroidController - Message received: {}', message)

        self.request_message_processor.process(message)

    def _on_processed(self, request_message, response_message):
        self._client.send(response_message)
