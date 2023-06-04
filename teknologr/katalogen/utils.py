import datetime
from django.utils.formats import date_format 


def create_duration_string(begin, end):
    if begin.month == 1 and begin.day == 1 and end.month == 12 and end.day == 31:
        return f'{begin.year}' if begin.year == end.year else f'{begin.year}-{end.year}'
    return f'{date_format(begin)} - {date_format(end)}'


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
