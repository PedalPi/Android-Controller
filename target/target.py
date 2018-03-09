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
