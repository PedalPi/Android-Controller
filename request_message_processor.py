import json

from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from android_controller.protocol.request_verb import RequestVerb
from android_controller.protocol.response_message import ResponseMessage
from android_controller.protocol.response_verb import ResponseVerb
from android_controller.protocol.response_verb import ResponseVerb


class RequestMessageProcessor(object):
    """
    :param port: Port that WebService are executing
    """

    def __init__(self, port):
        self.http_client = AsyncHTTPClient()
        self.url = 'http://localhost:{}'.format(port)
        self.processed_listener = lambda message, response: ...

    def process(self, message):
        """
        :param RequestMessage message:
        """
        if message.verb is RequestVerb.SYSTEM:
            return

        request = HTTPRequest(self.url + message.path, method=message.verb.value)
        self.http_client.fetch(
            request,
            lambda response: self.response(message, response=response)
        )

    def response(self, message, response):
        """
        :param RequestMessage message: Request message
        :param HTTPResponse response: Response message
        :return:
        """
        try:
            response_message = ResponseMessage(ResponseVerb.RESPONSE, response.body.decode('utf8'))

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

        self.processed_listener(message, response_message)

    def close(self):
        self.http_client.close()
