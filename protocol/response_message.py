import json


class ResponseMessage(object):

    def __init__(self, verb, content=None):
        """
        :param ResponseVerb verb:
        :param dict content:
        """
        self.verb = verb
        self.content = {} if content is None else content

    def __str__(self):
        return str(self.verb) + " " + json.dumps(self.content) + "\n"

    def __getitem__(self, key):
        return self.content[key]
