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

import subprocess

from webservice_serial.target.android.adb import Adb
from webservice_serial.target.target import Target


class AndroidDisplayView(Target):
    activity = 'io.github.pedalpi.displayview/io.github.pedalpi.displayview.activity.resume.ResumeActivity'

    def __init__(self):
        super(AndroidDisplayView, self).__init__()
        self.adb = None

    def init(self, application, port):
        super(AndroidDisplayView, self).init(application, port)

        adb_command = self._discover_adb_command()
        self.application.log('AndroidDisplayView - Android Debug Bridge command "{}"', adb_command)

        self.adb = Adb(adb_command, application.log)
        self.adb.start(port, AndroidDisplayView.activity)

    def close(self):
        if self.adb is not None:
            self.adb.close(self.port)

    def _discover_adb_command(self):
        if Adb.has_installed():
            return "adb"

        path = self.application.path_data / "adb"

        if not path.is_file():
            self.application.log("AndroidDisplayView - Downloading adb pre-compiled")
            self._download_adb(path)

        return path

    def _download_adb(self, path):
        if self._version() == 'Raspberry 3':
            command = "wget -O {} https://github.com/PedalPi/adb-arm/raw/master/adb-rpi3".format(path)
        else:
            command = "wget -O {} https://github.com/PedalPi/adb-arm/raw/master/adb-arm-binary".format(path)

        subprocess.call(command.split())
        subprocess.call("chmod +x {}".format(path).split())

    def _version(self):
        command = 'cat /sys/firmware/devicetree/base/model'

        if 'Raspberry Pi 3' in subprocess.check_output(command).decode('UTF-8').split('\n')[0]:
            return 'Raspberry Pi 3'

        return ""
