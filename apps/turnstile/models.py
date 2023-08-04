from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.turnstile.constants import InOutChoices
from apps.accounts.models import Membership
from apps.pool.models import Key, ServiceCard


class TurnstileHistory(models.Model):
    key = models.ForeignKey(
        Key,
        on_delete=models.CASCADE,
        verbose_name=_("Key"),
        null=True, blank=True
    )
    membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        verbose_name=_("Membership"),
        null=True, blank=True
    )
    service_card = models.ForeignKey(
        ServiceCard,
        on_delete=models.CASCADE,
        verbose_name=_("Service Card"),
        null=True, blank=True
    )
    create_date = models.DateTimeField(
        _('Create date'),
        auto_now_add=True,
    )
    status = models.BooleanField(
        _('Status'),
        default=True,
        choices=InOutChoices.choices,
        db_index=True
    )

    class Meta:
        db_table = 'turnstile_history'
        verbose_name = _('Pass history')
        verbose_name_plural = _('Pass histories')

    def __str__(self):
        if self.key and self.membership:
            return f"{self.key} - {self.membership}"
        elif self.service_card:
            return f"{self.service_card}"
        elif self.key:
            return f"{self.key}"
        return _("No data")
