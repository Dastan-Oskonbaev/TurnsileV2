from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentTypeChoices(models.TextChoices):
    ONE_TIME = 'ONE_TIME', _('One-time entry')
    MEMBERSHIP = 'MEMBERSHIP', _('Membership')
