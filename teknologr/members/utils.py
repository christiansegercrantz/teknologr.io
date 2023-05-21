import datetime
from .models import *

def getCurrentDate():
    return datetime.datetime.now()


def getCurrentYear():
    return getCurrentDate().year


def getFirstDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 1, 1)


def getLastDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 12, 31)
