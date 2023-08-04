from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.history.constants import HistoryTypeChoices
from apps.pool.models import Membership


class HistoryType(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=255,
        choices=HistoryTypeChoices.choices
    )
    icon = models.URLField(
        _('Icon'),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('History type')
        verbose_name_plural = _('History types')


class MembershipHistory(models.Model):
    membership = models.ForeignKey(
        Membership,
        verbose_name=_('Membership'),
        on_delete=models.CASCADE,
        related_name='history'
    )
    type = models.ForeignKey(
        HistoryType,
        verbose_name=_('Type'),
        on_delete=models.CASCADE,
        related_name='history'
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )

    def __str__(self):
        return f"{self.membership} - {self.type}"

    class Meta:
        verbose_name = _('Membership history')
        verbose_name_plural = _('Membership histories')
