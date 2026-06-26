# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime as dd
from datetime import timezone
from datetime import timedelta
import re

def timestamp_to_datetime(timestamp, timezonehour=0):
    tzUTC = timezone(timedelta(hours=timezonehour))
    try:
        return [dd.fromtimestamp(tstamp).astimezone(tzUTC) for tstamp in timestamp]
    except:
        return dd.fromtimestamp(timestamp).astimezone(tzUTC)
def str_to_datetime_UTC(string):
    return dd.strptime(string + "+0000", "%Y%m%d%H%M%S%z")

def datetime_to_str(datetime):
    return datetime.strftime("%Y%m%d%H%M%S%z")

def midtime(timelist, returntype = "timestamp"):
    timestamp = (timelist[0].timestamp() + timelist[1].timestamp()) / 2
    if returntype == "timestamp":
        return timestamp
    if returntype == "datetime":
        return timestamp_to_datetime([timestamp])[0]
    
def index_of_nearesttime(datetimelist, time):
    temptd = np.inf
    result = None
    for i_t, t in enumerate(datetimelist):
        if abs(t.timestamp() - time.timestamp()) < temptd:
            result = i_t
            temptd = abs(t.timestamp() - time.timestamp())
    return result

def indexlist_in_timerange(datetimelist, starttime, endtime):
    result = []
    for i_t, t in enumerate(datetimelist):
        if t >= starttime and t <= endtime:
            result.append(i_t)

    return result

def indexlist_of_specific_times(datetimelist, specific_times, timefmt):
    """pick specific time (for example: 06:00, 12:00, 18:00, 00:00)
    Args:
        datetimelist (list): list of datetime
        specific_times (list): list of str (["0600", "1200", "1800", "0000"])
        timefmt (str): format of time to compare with specific_times ("%H%M")
    """
    result = []
    for i_t, t in enumerate(datetimelist):
        if t.strftime(timefmt) in specific_times:
            result.append(i_t)
    return result

def era5time_to_datetime(time):
    return timestamp_to_datetime(time.astype(float)*3600 - (dd(1970, 1, 1) - dd(1900, 1, 1)).total_seconds())