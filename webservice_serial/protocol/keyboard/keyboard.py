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

from enum import Enum


class KeyCode(Enum):
    DOWN = "DOWN"
    UP = "EVENT"


class KeyNumber(Enum):
    DPAD_UP = 0x00000013
    DPAD_DOWN = 0x00000014
    DPAD_LEFT = 0x00000015
    DPAD_RIGHT = 0x00000016

    DPAD_CENTER = 0x00000017

    PLUS = 0x00000051
    MINUS = 0x00000045


class KeyEvent(object):
    """
    :param KeyCode code:
    :param KeyNumber number:
    """

    def __init__(self, code, number):
        self.code = code
        self.number = number

    def __dict__(self):
        return {
            'code': self.code.value,
            'number': self.number.value
        }

    def __str__(self):
        return str(self.__dict__())
