from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GenderChoices(TextChoices):
    MAIL = "М", _("Мужской")
    FEMAIL = "Ж", _("Женский")


class RoleChoices(TextChoices):
    OWNER = "O", _("Владелец")
    ADMIN = "A", _("Администратор")
    TRAINER = "T", _("Тренер")
    MEMBERSHIP = "M", _("Абонемент")


class DayChoices(TextChoices):
    MON = "MON", _("Понедельник")
    TUE = "TUE", _("Вторник")
    WED = "WED", _("Среда")
    THU = "THU", _("Четверг")
    FRI = "FRI", _("Пятница")
    SAT = "SAT", _("Суббота")
    SUN = "SUN", _("Воскресенье")
