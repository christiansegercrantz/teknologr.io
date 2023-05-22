import datetime
from django.utils.formats import date_format 


def create_duration_string(begin, end):
    if begin.month == 1 and begin.day == 1 and end.month == 12 and end.day == 31:
        return f'{begin.year}' if begin.year == end.year else f'{begin.year}-{end.year}'
    return f'{date_format(begin)} - {date_format(end)}'


def date_pairs_to_duration_strings(dict_of_pairs):
    for key, pairs in dict_of_pairs.items():
        dict_of_pairs[key] = ', '.join([create_duration_string(*pair) for pair in pairs])
    return dict_of_pairs


def add_to_durations(durations_dict, key, begin, end):
    if key not in durations_dict:
        durations_dict[key] = [[begin, end]]
        return durations_dict

    durations = durations_dict[key]
    last = durations[-1]
    if begin <= last[1] + datetime.timedelta(days=1):
        last[1] = end
    else:
        durations.append([begin, end])
    durations_dict[key] = durations
    return durations_dict


def create_functionary_duration_strings(functionaries):
    d = {}
    for f in functionaries:
        d = add_to_durations(d, f.functionarytype, f.begin_date, f.end_date)

    d = date_pairs_to_duration_strings(d)
    return [(key, value) for key, value in d.items()]


def create_group_type_duration_strings(group_memberships):
    d = {}
    for gm in group_memberships:
        g = gm.group
        d = add_to_durations(d, g.grouptype, g.begin_date, g.end_date)

    d = date_pairs_to_duration_strings(d)
    return [(key, value) for key, value in d.items()]
