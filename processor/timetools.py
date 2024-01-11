# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime as dd
from datetime import timezone
from datetime import timedelta
import re

def timestamp_to_datetime(timestamparray):
    tzUTC = timezone(timedelta(0))
    return [dd.fromtimestamp(tstamp).astimezone(tzUTC) for tstamp in timestamparray]

def str_to_datetime_UTC(string):
    return dd.strptime(string + "+0000", "%Y%m%d%H%M%S%z")

def midtime(timelist, returntype = "timestamp"):
    timestamp = (timelist[0].timestamp() + timelist[1].timestamp()) / 2
    if returntype == "timestamp":
        return timestamp
    if returntype == "datetime":
        return timestamp_to_datetime([timestamp])[0]