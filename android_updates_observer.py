from android_controller.protocol.message import Message
from android_controller.protocol.message_type import MessageType

from application.component.application_observer import ApplicationObserver


class AndroidUpdatesObserver(ApplicationObserver):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        pass

    def on_param_value_changed(self, param, **kwargs):
        effect = param.effect

        data = {
            'effect': effect.index,
            'param': param.index,
            'value': param.value
        }
        message = Message(MessageType.PARAM, data)
        self.client.send(message)

    def on_effect_status_toggled(self, effect, **kwargs):
        message = Message(MessageType.EFFECT, {'index': effect.index})
        self.client.send(message)

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        pass

    def on_current_pedalboard_changed(self, pedalboard, **kwargs):
        message = Message(MessageType.PATCH, pedalboard.json)
        self.client.send(message)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        pass

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        pass
