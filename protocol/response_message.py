import json


class ResponseMessage(object):

    def __init__(self, verb, content=None):
        """
        :param ResponseVerb verb:
        :param string content:
        """
        self.verb = verb
        self.content = json.dumps({}) if content is None else content

    def __str__(self):
        return "{} {}\n".format(self.verb, self.content)
