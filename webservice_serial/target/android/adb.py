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

import os


class Adb(object):
    """
    :param string command: Command that call the Android Debug Bridge
                           In Raspberry maybe be a `./adb` executable file
    :param callable log: Log function to show the command called
                         If None, not call
    """

    def __init__(self, command="adb", log=None):
        self.command = command
        self.log = log

    def start(self, port, activity):
        self.execute('shell am start -n {}'.format(activity))
        #FIXME delay?
        #self.execute('forward --remove-all')
        self.execute('forward tcp:{} tcp:{}'.format(port, port))

    def execute(self, command):
        command = '{} {}'.format(self.command, command)
        if self.log is not None:
            self.log('ADB - {}'.format(command))

        os.system(command)

    def close(self, port):
        self.execute('forward --remove tcp:{}'.format(port))
