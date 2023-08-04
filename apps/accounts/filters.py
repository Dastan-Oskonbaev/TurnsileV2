import django_filters as filters
from django.db.models import Q

from apps.accounts.models import Membership
from apps.payments.constants import PaymentTypeChoices


class MembershipFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    assigned_trainer = filters.NumberFilter(field_name='assigned_trainer__id')
    payment_type = filters.CharFilter(method='filter_type')

    def filter_search(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(membership_number__icontains=value)
            )

        return queryset

    def filter_type(self, queryset, name, value):
        if value == PaymentTypeChoices.ONE_TIME:
            queryset = self.queryset.filter(
                payments__type__type=PaymentTypeChoices.ONE_TIME,
                payments__is_active=True
            )
        elif value == PaymentTypeChoices.MEMBERSHIP:
            queryset = self.queryset.filter(
                payments__type__type=PaymentTypeChoices.MEMBERSHIP,
                payments__is_active=True
            )

        return queryset

    class Meta:
        model = Membership
        fields = [
            'search',
            'assigned_trainer',
            'payment_type'
        ]
