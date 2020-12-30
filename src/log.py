'''
    Module that gives a logger instance
'''
import logging
import sys
import json
from datetime import datetime

def data_log(publicIp, user_name, user_email, type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({
        "user_name": f"{user_name}",
        "email": f"{user_email}",
        "type": f"{type}",
        "publicIp": publicIp,
        "timestamp": f"{timestamp}"
    })

def _build():
    ''' Creates a logger instance '''
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)-5.5s] [%(funcName)s] %(message)s')
    )
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
    return log

class Logger(logging.getLoggerClass()):
    ''' Singleton for log management '''
    instance = None
    def __new__(cls):
        if not Logger.instance:
            Logger.instance = _build()
        return Logger.instance
