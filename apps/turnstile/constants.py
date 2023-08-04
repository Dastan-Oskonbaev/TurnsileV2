from django.db import models
from django.utils.translation import gettext_lazy as _


class InOutChoices(models.TextChoices):
    IN = True, _('Вход')
    OUT = False, _('Выход')
