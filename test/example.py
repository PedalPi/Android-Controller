# Copyright 2017 SrMouraSilva
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

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.observer.mod_host.mod_host import ModHost

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.connection import Connection

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder

from pluginsmanager.model.system.system_effect import SystemEffect


#if __name__ == '__main__':
if True:
    # Imports application
    from application.application import Application

    address = 'localhost'
    application = Application(path_data="data/", address=address, test=True)

    # Register WebService before WebServiceSerial
    from webservice.webservice import WebService

    application.register(WebService(application))

    # Register WebServiceSerial after WebService
    from webservice_serial.webservice_serial import WebServiceSerial
    from webservice_serial.target.android.android_display_view import AndroidDisplayView

    target = AndroidDisplayView()
    application.register(WebServiceSerial(application, target))

    # Start Application
    application.start()

    #import tornado

    #try:
    #    tornado.ioloop.IOLoop.current().start()
    #except KeyboardInterrupt:
    #    application.stop()

    import time
    time.sleep(5)
