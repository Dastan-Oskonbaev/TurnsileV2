from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _

from .models import Key
from .constants import GenderChoices


class KeyFilterSet(filters.FilterSet):
    key_type = filters.ChoiceFilter(
        field_name='key_type',
        choices=GenderChoices.choices,
        label=_('Key type')
    )

    class Meta:
        model = Key
        fields = ('key_type', )
