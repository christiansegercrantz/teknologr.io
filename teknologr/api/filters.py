import django_filters
from members.models import *
from functools import reduce
from operator import and_

class MemberFilter(django_filters.rest_framework.FilterSet):
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
    STAFF_ONLY_FILTERS = ('birth_date', 'student_id', 'dead', 'subscribed_to_modulen', 'allow_studentbladet', 'allow_publish_info', 'comment', 'username', 'bill_code', )
    birth_date = django_filters.DateFromToRangeFilter(
        label='(Admins only) Född mellan'
    )
    student_id = django_filters.CharFilter(
        label='(Admins only) Studienummer'
    )
    dead = django_filters.BooleanFilter(
        label='(Admins only) Avliden?'
    )
    subscribed_to_modulen = django_filters.BooleanFilter(
        label='(Admins only) Prenumererar på Modulen?'
    )
    allow_studentbladet = django_filters.BooleanFilter(
        label='(Admins only) Prenumererar på Studentbladet?'
    )
    allow_publish_info = django_filters.BooleanFilter(
        label='(Admins only) Tillåter publicering av kontaktinformation?'
    )
    comment = django_filters.CharFilter(
        lookup_expr='icontains',
        label='(Admins only) Kommentaren innehåller',
    )
    username = django_filters.CharFilter(
        label='(Admins only) Användarnamn'
    )
    bill_code = django_filters.CharFilter(
        label='(Admins only) BILL-konto'
    )

    class Meta:
        model = Member
        fields = ()

    def filter_queryset(self, queryset):
        '''
        Override parent method to add skipping of staff-only filters for non-staff users.
        '''
        if not self.is_staff:
            for name in self.STAFF_ONLY_FILTERS:
                self.form.cleaned_data.pop(name)

        return super().filter_queryset(queryset)

    @property
    def is_staff(self):
        ''' Helper method for checking if the user making the request is staff '''
        user = self.request.user
        return user and user.is_staff

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