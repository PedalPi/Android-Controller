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
import subprocess


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
        #self.execute('forward --remove-all')
        self.execute('forward tcp:{} tcp:{}'.format(port, port))

    def execute(self, command):
        command = '{} {}'.format(self.command, command)
        if self.log is not None:
            self.log('ADB - {}'.format(command))

        os.system(command)

    def close(self, port):
        self.execute('forward --remove tcp:{}'.format(port))

    def usb_support(self):
        """
        Check if has USB Accessory Api support (AOA)

        Based on http://jjmilburn.github.io/2017/05/08/Android-AOA-Support/
        """
        usb_permissions = subprocess.check_output("adb shell ls /system/etc/permissions | grep 'usb'", shell=True).split()
        return len(usb_permissions) > 0

    @staticmethod
    def has_installed():
        """
        Check if the current system have the ``adb`` installed
        :return:
        """
        try:
            subprocess.call(["adb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            return False

        return True
