import django_filters
from members.models import *
from functools import reduce
from operator import and_

class BaseFilter(django_filters.rest_framework.FilterSet):
    '''
    Base filter class that takes care of normal users from using staff-only filters.
    '''
    STAFF_ONLY = []
    created = django_filters.DateFromToRangeFilter(label='Skapad mellan')
    modified = django_filters.DateFromToRangeFilter(label='Modifierad mellan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        always_last = ['created', 'modified']
        if self.STAFF_ONLY == '__all__':
            self.STAFF_ONLY = [k for k in list(self.filters.keys()) if k not in always_last]
        self.STAFF_ONLY = self.STAFF_ONLY + always_last

        # If normal user, remove all staff-only filters, otherwise move them last and add a prefix to their labels
        is_staff = self.is_staff
        for key in self.STAFF_ONLY:
            f = self.filters.pop(key)
            if is_staff:
                f.label = f'[Staff only] {f.label}'
                self.filters[key] = f

    @property
    def is_staff(self):
        ''' Helper method for checking if the user making the request is staff '''
        user = self.request.user
        return user and user.is_staff


class MemberFilter(BaseFilter):
    '''
    A custom FilterSet class that set up filters for Members. Some filters are ignored if the requesting user is not staff.
    '''

    # Public filters
    name = django_filters.CharFilter(
        # NOTE: 'given_names' is a semi-public field
        method='filter_name',
        label='Namnet innehåller',
    )
    address = django_filters.CharFilter(
        # NOTE: Semi-public field
        method='filter_address',
        label='Adressen innehåller',
    )
    email = django_filters.CharFilter(
        # NOTE: Semi-public field
        method='filter_email',
        label='E-postadressen innehåller',
    )
    degree_programme = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Studieprogrammet innehåller',
    )
    enrolment_year = django_filters.RangeFilter(
        label='Inskrivingsåret är mellan',
    )
    graduated = django_filters.BooleanFilter(
        method='filter_graduated',
        label='Utexaminerad?',
    )
    graduated_year = django_filters.RangeFilter(
        label='Utexamineringsåret är mellan',
    )

    # Staff only filters
    STAFF_ONLY = ['birth_date', 'student_id', 'dead', 'subscribed_to_modulen', 'allow_studentbladet', 'allow_publish_info', 'comment', 'username', 'bill_code']
    birth_date = django_filters.DateFromToRangeFilter(
        label='Född mellan',
    )
    student_id = django_filters.CharFilter(
        label='Studienummer',
    )
    dead = django_filters.BooleanFilter(
        label='Avliden?',
    )
    subscribed_to_modulen = django_filters.BooleanFilter(
        label='Prenumererar på Modulen?',
    )
    allow_studentbladet = django_filters.BooleanFilter(
        label='Prenumererar på Studentbladet?',
    )
    allow_publish_info = django_filters.BooleanFilter(
        label='Tillåter publicering av kontaktinformation?',
    )
    comment = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Kommentaren innehåller',
    )
    username = django_filters.CharFilter(
        label='Användarnamn',
    )
    bill_code = django_filters.CharFilter(
        label='BILL-konto',
    )

    def filter_non_public_memebers(self, queryset):
        ''' Helper method for filtering members that have not allowed their info to be published '''
        if self.is_staff:
            return queryset
        return queryset.filter(Member.get_show_info_Q())

    def filter_name(self, queryset, name, value):
        is_staff = self.is_staff

        # Split the filter value and compare all individual values against all address columns
        queries = []
        for v in value.split():
            q = Q(preferred_name__icontains=v) | Q(surname__icontains=v)
            # Non-staff users only get to filter on 'given_names' if the Member has allowed publishing of info
            if is_staff:
                q |= Q(given_names__icontains=v)
            else:
                q |= (Q(given_names__icontains=v) & Member.get_show_info_Q())
            queries.append(q)
        return queryset.filter(reduce(and_, queries))

    def filter_address(self, queryset, name, value):
        # Remove hidden Members if not staff
        if not self.is_staff:
            queryset = self.filter_non_public_memebers(queryset)

        # Split the filter value and compare all individual values against all address columns
        queries = []
        for v in value.split():
            queries.append(
                Q(street_address__icontains=v) |
                Q(postal_code__icontains=v) |
                Q(city__icontains=v) |
                Q(country__icontains=v)
            )
        return queryset.filter(reduce(and_, queries))

    def filter_email(self, queryset, name, value):
        # Remove hidden Members if not staff
        if not self.is_staff:
            queryset = self.filter_non_public_memebers(queryset)

        return queryset.filter(email__icontains=value)

    def filter_graduated(self, queryset, name, value):
        '''
        Modifying the graduated flag whan adding a graduated year can sometimes be forgotten, so taking that into consideration for this filter query.
        '''
        if value:
            # Graduated or graduated year is set
            return queryset.filter(Q(graduated=True) | Q(graduated_year__isnull=False))
        # Not graduated and graduated year is not set
        return queryset.filter(Q(graduated=False) & Q(graduated_year__isnull=True))


class DecorationFilter(BaseFilter):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Betygelsens namn innehåller',
    )

class DecorationOwnershipFilter(BaseFilter):
    decoration__id = django_filters.NumberFilter(label='Betygelsens nam')
    decoration__name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Betygelsens namn innehåller',
    )
    member__id = django_filters.NumberFilter(label='Medlemmens id')
    acquired = django_filters.DateFromToRangeFilter(label='Tilldelat mellan')


class FunctionaryTypeFilter(BaseFilter):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Postens namn innehåller',
    )

class FunctionaryFilter(BaseFilter):
    functionarytype__id = django_filters.NumberFilter(label='Postens id')
    functionarytype__name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Postens namn innehåller',
    )
    member__id = django_filters.NumberFilter(label='Medlemmens id')
    begin_date = django_filters.DateFromToRangeFilter(label='Startdatum mellan')
    end_date = django_filters.DateFromToRangeFilter(label='Slutdatum mellan')


class GroupTypeFilter(BaseFilter):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Gruppens namn innehåller',
    )

class GroupFilter(BaseFilter):
    begin_date = django_filters.DateFromToRangeFilter(label='Startdatum mellan')
    end_date = django_filters.DateFromToRangeFilter(label='Slutdatum mellan')
    grouptype__id = django_filters.NumberFilter(label='Gruppens id')
    grouptype__name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Gruppens namn innehåller',
    )

class GroupMembershipFilter(BaseFilter):
    group__id = django_filters.NumberFilter(label='Undergruppens id')
    group__begin_date = django_filters.DateFromToRangeFilter(label='Undergruppens startdatum mellan')
    group__end_date = django_filters.DateFromToRangeFilter(label='Undergruppens slutdatum mellan')
    group__grouptype__id = django_filters.NumberFilter(label='Gruppens id')
    group__grouptype__name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Gruppens namn innehåller',
    )
    member__id = django_filters.NumberFilter(label='Medlemmens id')


class MemberTypeFilter(BaseFilter):
    STAFF_ONLY = '__all__'
    begin_date = django_filters.DateFromToRangeFilter(label='Startdatum mellan')
    end_date = django_filters.DateFromToRangeFilter(label='Slutdatum mellan')
    type = django_filters.ChoiceFilter(choices=MemberType.TYPES, label='Medlemstyp')
    member__id = django_filters.NumberFilter(label='Medlemmens id')
