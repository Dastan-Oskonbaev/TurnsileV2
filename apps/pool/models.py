from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Membership
from .constants import GenderChoices


class Key(models.Model):
    name = models.CharField(
        _('Key name'),
        max_length=255
    )
    scan_id = models.CharField(
        _('Scan ID'),
        max_length=255,
        unique=True
    )
    key_type = models.CharField(
        _('Key type'),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        related_name='keys',
        verbose_name=_('Membership'),
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Key {self.name}"

    class Meta:
        verbose_name = _("Key")
        verbose_name_plural = _("Keys")


class ServiceCard(models.Model):
    owner_name = models.CharField(
        _("Owner's name"),
        max_length=255,
    )
    scan_id = models.CharField(
        _('Scan ID'),
        max_length=50,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.owner_name} - {self.scan_id}"

    class Meta:
        verbose_name = _("Service card")
        verbose_name_plural = _("Service cards")
