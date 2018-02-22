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

from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError

from webservice_serial.protocol.request_verb import RequestVerb
from webservice_serial.protocol.response_message import ResponseMessage
from webservice_serial.protocol.response_verb import ResponseVerb


class RequestMessageProcessor(object):
    """
    :param port: Port that WebService are executing
    """

    def __init__(self, port, token=None):
        self.http_client = AsyncHTTPClient()
        self.url = 'http://localhost:{}'.format(port)
        self.processed_listener = lambda message, response: ...
        self.token = token

    def process(self, message):
        """
        :param RequestMessage message:
        """
        if message.verb is RequestVerb.SYSTEM:
            return

        request = HTTPRequest(self.url + message.path, method=message.verb.value, headers=self.headers)
        self.http_client.fetch(
            request,
            lambda http_response: self.response(message, http_response)
        )

    @property
    def headers(self):
        if self.token is not None:
            return {'x-xsrf-token': self.token}
        else:
            return None

    def response(self, request, http_response):
        """
        :param RequestMessage request: Request message
        :param HTTPResponse http_response: WebService response message
        :return:
        """
        try:
            response = ResponseMessage(ResponseVerb.RESPONSE, http_response.body.decode('utf8'), identifier=request.identifier)

        except HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
            #FIXME
            return

        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
            return

        self.processed_listener(request, response)

    def close(self):
        self.http_client.close()

    def process_event(self, message):
        """
        :param dict message:
        :return ResponseMessage:
        """
        return ResponseMessage(ResponseVerb.EVENT, message)
