# encoding: utf-8
import datetime
import json
import logging
import time


class CeFormat(logging.Formatter):
    """
    日志输出格式
    """
    def format(self, record):
        currentDateAndTime = datetime.datetime.now()
        asctime = currentDateAndTime.strftime('%Y-%m-%d %H:%M:%S')
        mymessage = "{asctime} - {message}".format(
            asctime=asctime, message=json.dumps(record.msg)
        )
        return mymessage

