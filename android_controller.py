import os

from application.component.component import Component
from application.controller.current_controller import CurrentController
from pluginsmanager.observer.update_type import UpdateType

from android_controller.adb import Adb
from android_controller.android_controller_client import AndroidControllerClient
from android_controller.android_updates_observer import AndroidUpdatesObserver
from android_controller.message_processor import MessageProcessor
from android_controller.protocol.message import Message
from android_controller.protocol.message_type import MessageType


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
        self._observer = AndroidUpdatesObserver(self._client)
        self.adb = Adb(adb_command, application.log)
        self.message_processor = MessageProcessor(ws_port)

    def init(self):
        self.register_observer(self._observer)

        self.adb.start(AndroidController.port, AndroidController.activity)

        self._client.message_listener = self._process_message
        self._client.connected_listener = self._on_connected

        self._client.connect()

    def close(self):
        self.message_processor.close()
        self.adb.close(AndroidController.port)

    def _on_connected(self):
        self.application.log('AndroidController - DisplayView connected')

        data = {
            'pedalboard': self.current_pedalboard.json,
            'update_type': str(UpdateType.UPDATED),
            'index': self.current_pedalboard.index,
            'origin': None
        }

        self._client.send(Message(MessageType.PEDALBOARD_UPDATED, data))

    def _process_message(self, message):
        self.application.log('AndroidController - Message received: {}', message)

        current_pedalboard = self.current_pedalboard

        if message.message_type == MessageType.EFFECT_UPDATED:
            effect_index = message['index']
            effect = current_pedalboard.effects[effect_index]

            controller = self.controller(effect_controller)
            controller.toggleStatus(effect, self.token)

        elif message.message_type == MessageType.PARAM_VALUE_CHANGE:
            effect_index = message['effect']
            param_index = message['param']
            value = message['value']

            effect = current_pedalboard.effects[effect_index]
            param = effect.params[param_index]

            controller = self.controller(current_pedalboard)
            controller.updateValue(param, value, self.token)

    @property
    def current_pedalboard(self):
        return self.controller(CurrentController).pedalboard

