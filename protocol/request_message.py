from android_controller.protocol.verb import Verb


class RequestMessage(object):
    """
    Message send form the app to the AndroidController

    :param Verb verb:
    :param string path:
    :param dict content:
    """

    def __init__(self, verb, path, content):
        self.verb = verb
        self.path = path
        self.content = content

    def __str__(self):
        return '{} {}\n{}\nEOF'.format(self.verb, self.path, self.content)
