# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime as dd
from datetime import timezone
from datetime import timedelta
import re

def timestamp_to_datetime(timestamp, timezonehour=0):
    tzUTC = timezone(timedelta(hours=timezonehour))
    if isinstance(timestamp, float) or isinstance(timestamp, int):
        return dd.fromtimestamp(timestamp).astimezone(tzUTC)
    return [dd.fromtimestamp(tstamp).astimezone(tzUTC) for tstamp in timestamp]

def str_to_datetime_UTC(string):
    return dd.strptime(string + "+0000", "%Y%m%d%H%M%S%z")

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