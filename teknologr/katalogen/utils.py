import datetime
from operator import attrgetter
from functools import total_ordering
from django.utils.formats import date_format

@total_ordering
class Duration:
    def __init__(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date

    def __str__(self):
        return create_duration_string(self.begin_date, self.end_date)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.end_date, self.begin_date) == (other.end_date, other.begin_date)

    def __lt__(self, other):
        return (self.end_date, self.begin_date) < (other.end_date, other.begin_date)

    def to_string(self):
        return str(self)

    def to_sort_string(self):
        return f'{self.end_date.isoformat()}{self.begin_date.isoformat()}'

class DurationsHelper:
    def __init__(self, items):
        self.__dict = {}
        for key, duration in items:
            self.add(key, duration)

    def add(self, key, new_duration):
        if key not in self.__dict:
            self.__dict[key] = []
        self.__dict[key].append(new_duration)

    def simplify(self):
        for key, durations in self.__dict.items():
            self.__dict[key] = simplify_durations(durations)
        return self

    def items(self):
        return self.__dict.items()


def create_duration_string(begin, end):
    '''
    Turn a date interval into a string, where the dates are simplified as much as possible. These rules are followed:
     - A.B.YYYY - A.B.YYYY   -> 'A BB YYYY'
     - A.B.YYYY - C.B.YYYY   -> 'A-C BB YYYY'
     - A.B.YYYY - C.D.YYYY   -> 'A BB - C DD YYYY'
     - 1.1.YYYY - 31.12.YYYY -> 'YYYY'
     - 1.1.YYYY - 31.12.ZZZZ -> 'YYYY-ZZZZ'
    '''
    if begin.month == 1 and begin.day == 1 and end.month == 12 and end.day == 31:
        return f'{begin.year}' if begin.year == end.year else f'{begin.year}-{end.year}'

    b = date_format(begin)
    e = date_format(end)
    if begin.year != end.year:
        return f'{b} - {e}'
    if begin.month != end.month:
        i = b.rfind(' ')
        return f'{b[:i]} - {e}'
    if begin.day != end.day:
        return f'{begin.day}-{e}'
    return b

def simplify_durations(durations):
    '''
    The parameter is a list of durations. Overlapping durations will be simplified into a single duration.

    Returns a list of simplified durations.
    '''
    if not len(durations):
        return []

    durations.sort(key=attrgetter('begin_date'))

    simplified = [durations[0]]
    for next in durations[1:]:
        last = simplified[-1]
        if next.begin_date > last.end_date + datetime.timedelta(days=1):
            simplified.append(next)
        elif next.end_date > last.end_date:
            last.end_date = next.end_date

    return simplified

def simplify_durations_by_key(items):
    '''
    The parameter is a list of (key, duration) pairs. Durations with the same key that follows eachother will be simplified into a single duration.

    Returns a list of (key, duration) pairs.
    '''
    items = DurationsHelper(items).simplify().items()
    res = []
    for key, durations in items:
        for duration in durations:
            res.append((key, duration))
    return res

def create_duration_strings_by_key(items):
    '''
    The parameter is a list of (key, duration) pairs. All durations with the same key will be combined into one string.

    Returns a list of (key, string) pairs.
    '''
    items = DurationsHelper(items).simplify().items()
    return [(key, ', '.join([str(d) for d in durations])) for key, durations in items]
