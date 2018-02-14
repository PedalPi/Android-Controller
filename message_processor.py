from tornado.httpclient import HTTPRequest, HTTPClient, HTTPError


class MessageProcessor(object):
    """
    :param port: Port that WebService are executing
    """

    def __init__(self, port):
        self.http_client = HTTPClient()
        self.url = 'http://localhost:{}/'.format(port)

    def process(self, message):
        request = HTTPRequest(self.url, method='GET')

        try:
            response = self.http_client.fetch(request)
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
