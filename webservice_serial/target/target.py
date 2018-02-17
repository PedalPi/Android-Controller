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


class Target(object):
    def __init__(self):
        self.application = None
        self.port = None

    def init(self, application, port):
        """
        Target initialization
        :param Application application:
        :param number port:
        """
        self.application = application
        self.port = port

    def close(self):
        """
        Target close
        """
        pass

    def process(self, request, response):
        """
        Handles the message, formatting for the best receipt of
        the client. It generally decreases the amount of bits
        transmitted by removing message information.

        :param RequestMessage request: Server request
        :param ResponseMessage response: This response
        :return ResponseMessage:
        """
        return response
