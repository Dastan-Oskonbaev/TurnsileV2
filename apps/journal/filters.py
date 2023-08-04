from django.db.models import Q
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _

from .models import Journal
from ..payments.constants import PaymentTypeChoices
from ..pool.constants import GenderChoices


class JournalFilterSet(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    payment_type = filters.ChoiceFilter(
        field_name='membership_type__type',
        choices=PaymentTypeChoices.choices,
        label=_('Membership type')
    )
    sort_by_time = filters.OrderingFilter(
        fields=('entry_time',)
    )
    key_type = filters.ChoiceFilter(
        field_name='key__key_type',
        choices=GenderChoices.choices,
        label=_('Key type')
    )
    date = filters.DateFilter(
        field_name='create_date',
        label=_('Date'),
        help_text=_('Format: YYYY-MM-DD')
    )

    def filter_search(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(membership__first_name__icontains=value) |
                Q(membership__last_name__icontains=value) |
                Q(membership__membership_number__icontains=value)
            )

        return queryset

    class Meta:
        model = Journal
        fields = (
            'payment_type',
            'sort_by_time',
            'key_type',
            'date',
            'search',
        )
