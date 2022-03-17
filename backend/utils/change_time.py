# encoding: utf-8
"""
处理各种时间的转换
"""
import datetime
import time


def get_begin_and_time(dt=None, formats="%Y-%m-%d"):
    """
    根据日志获取当天的utc开始和结束时间戳
    """
    date_stamp = datetime.datetime.strptime(dt, formats)
    time_begin = int(time.mktime(date_stamp.timetuple()))
    time_end = int(time.mktime((date_stamp + datetime.timedelta(days=1)).timetuple()))
    return time_begin, time_end

def get_datestr_by_stmp(time_stmp, fmt="%Y-%m-%d %H:%M:%S"):
    date_obj = datetime.datetime.fromtimestamp(time_stmp)
    date_str = date_obj.strftime(fmt)
    return date_str

def stmp_by_date(date_str, fmt="%Y-%m-%d %H:%M:%S"):
    date_obj = datetime.datetime.strptime(date_str, fmt)
    date_stmp = int(time.mktime(date_obj.timetuple()))
    return date_stmp