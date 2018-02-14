from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from android_controller.protocol.verb import Verb


class RequestMessageProcessor(object):
    """
    :param port: Port that WebService are executing
    """

    def __init__(self, port):
        self.http_client = AsyncHTTPClient()
        self.url = 'http://localhost:{}'.format(port)

    def process(self, message):
        """
        :param RequestMessage message:
        """
        if message.verb is Verb.SYSTEM:
            return

        request = HTTPRequest(self.url + message.path, method=message.verb.value)
        self.http_client.fetch(request, lambda response: self.response(message, response=response))

    def response(self, message, response):
        """
        :param RequestMessage message: Request message
        :param HTTPResponse response: Response message
        :return:
        """
        try:
            print('RESPONSE ...')
            print(response.body)

        except HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))

        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))

    def close(self):
        self.http_client.close()
