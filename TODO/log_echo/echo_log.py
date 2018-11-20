import logging
import colorlog


class Echo_Log:
    def __init__(self, filename=None, level=logging.DEBUG):
        LOG_LEVEL = level
        LOGFORMAT = "[%(log_color)s%(levelname)s] [%(log_color)s%(asctime)s] %(log_color)s%(filename)s [line:%(log_color)s%(lineno)d] : %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        if filename:
            colorlog.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                 filename=filename,
                                 filemode='w', datefmt='%a, %d %b %Y %H:%M:%S', )
        formatter = colorlog.ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger()
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)

    def debug(self, msg=""):
        self.log.debug(msg)

    def warn(self, msg=""):
        self.log.warn(msg)

    def info(self, msg=""):
        self.log.info(msg)

    def error(self, msg=""):
        self.log.error(msg)

    def critical(self, msg=""):
        self.log.critical(msg)

