from pprintpp import pformat

class Response(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return pformat(self.__dict__).encode('utf-8')