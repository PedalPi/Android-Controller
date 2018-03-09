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


class RequestMessage(object):
    """
    Message send form the app to the AndroidController

    :param RequestVerb verb:
    :param string path:
    :param dict content:
    """

    def __init__(self, verb, path, content):
        self.verb = verb
        self.path = path
        self.content = content

    def __str__(self):
        return '{} {}\n{}\nEOF'.format(self.verb, self.path, self.content)
