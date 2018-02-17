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

from webservice_serial.target.target import Target
from webservice_serial.target.android.adb import Adb


class AndroidDisplayView(Target):
    """
    :param string adb_command: Command that call the Android Debug Bridge
                               In Raspberry maybe be a `./adb` executable file
    """
    activity = 'io.github.pedalpi.pedalpi_display/io.github.pedalpi.pedalpi_display.MainActivity'

    def __init__(self, adb_command="adb"):
        super(AndroidDisplayView, self).__init__()
        self.adb = None
        self.adb_command = adb_command

    def init(self, application, port):
        super(AndroidDisplayView, self).init(application, port)

        self.adb = Adb(self.adb_command, application.log)
        self.adb.start(port, AndroidDisplayView.activity)

    def close(self):
        self.adb.close(self.port)
