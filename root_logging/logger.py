import logging


class Logger(object):

    def __init__(self, name, level, handler, str_format=None):
        self.logger = logging.getLogger(name)
        self.handler = handler
        self.level = level
        self.str_format = '%(asctime)s :: %(name)s:%(lineno)s :: %(levelname)s :: %(message)s' if str_format is None else str_format

        self.__init_logger()

    def get_logger(self):
        return logging.getLogger(self.logger.name)

    @property
    def log(self):
        return self.get_logger()

    def set_logger(self, logger=None):
        self.logger = self.logger if logger is None else logger
        self.set_level()

    def set_level(self, level=None):
        self.level = self.level if level is None else level
        self.logger.setLevel(self.level)

    def set_handler(self, handler=None):
        self.handler = self.handler if handler is None else handler

        self.set_handler_format()
        self.set_handler_level()

        self.logger.addHandler(self.handler)

    def set_handler_level(self, level=None):
        level = self.level if level is None else level
        self.handler.setLevel(level)

    def set_handler_format(self, str_format=None):
        str_format = self.str_format if str_format is None else str_format
        self.str_format = str_format

        self.handler.setFormatter(logging.Formatter(self.str_format))

    def __init_logger(self):
        self.set_logger()
        self.set_handler()
        self.logger.debug('Logger `{}` was initialized'.format(self.logger.name))
