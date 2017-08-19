from kivy.logger import Logger


class Loggable(object):
    def prefix(self):
        return self.__class__.__name__ + ': '

    def trace(self, msg, *args, **kwargs):
        Logger.trace(self.prefix() + msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        Logger.debug(self.prefix() + msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        Logger.info(self.prefix() + msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        Logger.warning(self.prefix() + msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        Logger.error(self.prefix() + msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        Logger.critical(self.prefix() + msg, *args, **kwargs)
