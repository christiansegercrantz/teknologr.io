from datetime import date, datetime
from .models import *

def getCurrentDate():
    return datetime.now()


def getCurrentYear():
    return getCurrentDate().year


def getFirstDayOfCurrentYear():
    return date(getCurrentYear(), 1, 1)


def getLastDayOfCurrentYear():
    return date(getCurrentYear(), 12, 31)
