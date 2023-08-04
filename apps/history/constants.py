from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class HistoryTypeChoices(TextChoices):
    FREEZE = 'freeze', _("Freeze")
    UNFREEZE = 'unfreeze', _("Unfreeze")
    REFUND = 'refund', _("Refund")
    PAYMENT = 'payment', _("Payment")
