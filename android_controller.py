import os

from pluginsmanager.observer.update_type import UpdateType

from application.component.component import Component
from application.controller.current_controller import CurrentController

from android_controller.android_controller_client import AndroidControllerClient
from android_controller.android_updates_observer import AndroidUpdatesObserver
from android_controller.protocol.message import Message
from android_controller.protocol.message_type import MessageType


class AndroidController(Component):
    port = 8888
    activity = 'io.github.pedalpi.pedalpi_display/io.github.pedalpi.pedalpi_display.MainActivity'

    def __init__(self, application, adb_command="adb"):
        super(AndroidController, self).__init__(application)

        self.client = AndroidControllerClient('localhost', AndroidController.port)
        self.observer = AndroidUpdatesObserver(self.client)
        self.adb_command = adb_command

    def init(self):
        self.start_android_application(AndroidController.port, AndroidController.activity)
        self.client.message_listener = self.process_message
        self.register_observer(self.observer)
        self.client.run()

        self.client.connected_listener = lambda: self._on_connected()

    def _on_connected(self):
        data = {
            'pedalboard': self.current_pedalboard.json,
            'update_type': str(UpdateType.UPDATED),
            'index': self.current_pedalboard.index,
            'origin': None
        }

        self.client.send(Message(MessageType.PEDALBOARD_UPDATED, data))

    def start_android_application(self, port, activity):
        os.system(self.adb_command + ' shell am start -n ' + activity)
        os.system(self.adb_command + ' forward --remove-all')
        os.system(self.adb_command + ' forward tcp:' + str(port) + ' tcp:' + str(port))

    def process_message(self, message):
        print("Message received:", message)

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

