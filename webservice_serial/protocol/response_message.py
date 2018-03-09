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

import json
from webservice_serial.protocol.response_verb import ResponseVerb


class ResponseMessage(object):
    """
    :param ResponseVerb verb:
    :param object content:
    :param int identifier:
    """

    @staticmethod
    def error(message, identifier=0):
        return ResponseMessage(ResponseVerb.ERROR, '{"message": "'+message+'"}', identifier=identifier)

    def __init__(self, verb, content=None, identifier=0):
        self.identifier = identifier
        self.verb = verb
        self.content = json.dumps({}) if content is None else content

    def __str__(self):
        return "{} {} {}\n".format(self.identifier, self.verb, str(self.content))
