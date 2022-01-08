'''
    Module that gives a logger instance
'''
import logging
import sys

def logger_build():
    ''' Creates a logger instance '''
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter('[%(asctime)s] [%(funcName)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    )
    log.addHandler(stream_handler)
    log.propagate = False
    return log

class Logger(logging.getLoggerClass()):
    ''' Singleton for log management '''
    instance = None
    def __new__(cls):
        if not Logger.instance:
            Logger.instance = logger_build()
        return Logger.instance
