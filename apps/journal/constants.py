from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.TextChoices):
    MAIL = "M", _("Male")
    FEMAIL = "F", _("Female")


class EnterExitStatusChoices(models.IntegerChoices):
    ENTERED = True, _("Entered")
    EXITED = False, _("Exited")
