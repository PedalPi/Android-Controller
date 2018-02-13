import os
from android_controller.android_controller_client import AndroidControllerClient
from android_controller.android_updates_observer import AndroidUpdatesObserver
from android_controller.protocol.message import Message
from android_controller.protocol.message_type import MessageType
from application.application.controller import current_controller
from application.application.controller import effect_controller
from application.application.controller import param_controller
from application.architecture.Component import Component


class AndroidController(Component):
    def __init__(self, application, adb_command="adb"):
        super(AndroidController, self).__init__(application)
        self.client = AndroidControllerClient('localhost', 8888)
        self.observer = AndroidUpdatesObserver(self.client)
        self.adb_command = adb_command

    def init(self):
        self.start_android_application()
        self.client.message_listener = self.process_message
        self.register_observer(self.observer)
        self.client.run()

        self.client.connected_listener = lambda: self.client.send(Message(MessageType.PATCH, self.current_patch.json))

    def start_android_application(self):
        activity = 'com.pedalpi.pedalpi/com.pedalpi.pedalpi.PatchActivity'
        port = 8888

        os.system(self.adb_command + ' shell am start -n ' + activity)
        os.system(self.adb_command + ' forward --remove-all')
        os.system(self.adb_command + ' forward tcp:' + str(port) + ' tcp:' + str(port))

    def process_message(self, message):
        print("Message received:", message)

        current_patch = self.current_patch

        if message.message_type == MessageType.EFFECT:
            effect_index = message['index']
            effect = current_patch.effects[effect_index]

            controller = self.controller(effect_controller)
            controller.toggleStatus(effect, self.token)

        elif message.message_type == MessageType.PARAM:
            effect_index = message['effect']
            param_index = message['param']
            value = message['value']

            effect = current_patch.effects[effect_index]
            param = effect.params[param_index]

            controller = self.controller(param_controller)
            controller.updateValue(param, value, self.token)

    @property
    def current_patch(self):
        controller = self.controller(current_controller)
        return controller.current_patch
