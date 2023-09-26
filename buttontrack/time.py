"""
Unix timestamp library
"""
import datetime
import time


def current_ts():
    """return current seconds since unix epoch"""
    dt = datetime.datetime.now(datetime.timezone.utc)
    return time.mktime(dt.timetuple())
