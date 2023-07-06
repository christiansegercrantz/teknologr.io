import datetime
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

def durations_to_strings(dict_of_date_pairs):
    a = []
    for key, pairs in dict_of_date_pairs.items():
        a.append((key, ', '.join([create_duration_string(*pair) for pair in pairs])))
    return a


def add_to_durations(durations, key, begin, end):
    if key not in durations:
        durations[key] = [[begin, end]]
        return durations

    pairs = durations[key]
    last = pairs[-1]
    if begin <= last[1] + datetime.timedelta(days=1):
        last[1] = end
    else:
        pairs.append([begin, end])
    durations[key] = pairs


def create_functionary_duration_strings(functionaries):
    durations = {}
    for f in functionaries:
        add_to_durations(durations, f.functionarytype, f.begin_date, f.end_date)

    return durations_to_strings(durations)


def create_group_type_duration_strings(group_memberships):
    durations = {}
    for gm in group_memberships:
        g = gm.group
        add_to_durations(durations, g.grouptype, g.begin_date, g.end_date)

    return durations_to_strings(durations)
