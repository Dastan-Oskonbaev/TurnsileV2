from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.accounts.constants import GenderChoices, RoleChoices, DayChoices
from utils.time import generate_dates


class CustomUser(AbstractUser):
    scan_id = models.CharField(
        _('Scan ID'),
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    address = models.CharField(
        _('Address'),
        max_length=200,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        _("Phone number"),
        max_length=100,
        unique=True
    )
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.MAIL
    )
    role = models.CharField(
        _('Role'),
        choices=RoleChoices.choices,
        max_length=1,
        default=RoleChoices.OWNER
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )
    delete_date = models.DateTimeField(
        _('Delete date'),
        null=True, blank=True
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [
        'username',
        'role',
    ]

    def __str__(self):
        return f"{self.last_name} {self.first_name}" if self.last_name and self.first_name else self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True

            if not self.password.startswith("pbkdf2_sha256"):
                self.password = make_password(self.password)

            if not self.username:
                self.username = self.phone_number

            if self.role in [RoleChoices.OWNER, RoleChoices.ADMIN, RoleChoices.TRAINER]:
                self.is_staff = True

            if self.role == RoleChoices.OWNER:
                self.is_superuser = True
        else:
            existing_user = CustomUser.objects.get(pk=self.pk)

            if self.password != existing_user.password:
                self.password = make_password(self.password)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Membership(CustomUser):
    """ Абонемент """
    membership_number = models.PositiveIntegerField(
        _('Membership number'),
        unique=True,
        db_index=True
    )
    assigned_trainer = models.ForeignKey(
        'Trainer',
        on_delete=models.SET_NULL,
        related_name='memberships',
        verbose_name=_('Trainer'),
        null=True,
        blank=True
    )
    remaining_visits = models.PositiveIntegerField(
        _('Visit left'),
        default=0
    )
    note = models.TextField(
        _('Note'),
        null=True,
        blank=True,
        help_text=_('Note about membership')
    )

    username = ['email']

    @property
    def full_name(self):
        return self.get_full_name() or self.phone_number

    def get_actual_payment(self):
        payments = self.payments.filter(
            start_date__lte=date.today(),
            end_date__gte=date.today(),
            is_active=True
        )

        return payments.first()

    def get_payment_by_date(self, start_date: date, end_date: date, exclude: int = None):
        date_range = generate_dates(start_date, end_date)

        payments = self.payments.filter(
            Q(start_date__in=date_range) | Q(end_date__in=date_range)
        ).exclude(pk=exclude)

        return payments.first()

    def get_freeze_payment(self):
        payments = self.payments.filter(
            start_date__lte=date.today(),
            end_date__gt=date.today(),
            is_active=False
        )

        if payments.exists():
            return payments.first()

        return None

    def __str__(self):
        return self.full_name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.role = RoleChoices.MEMBERSHIP
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")


class Trainer(CustomUser):
    middle_name = models.CharField(
        _('Middle name'),
        max_length=100,
        null=True,
        blank=True
    )
    salary = models.PositiveIntegerField(
        _('Salary'),
        null=True,
        blank=True
    )
    about_me = models.TextField(
        _('About me'),
        null=True,
        blank=True
    )

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.role = RoleChoices.TRAINER
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("Trainer")
        verbose_name_plural = _("Trainers")


class TrainerSchedule(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Trainer')
    )
    day = models.CharField(
        _('Day'),
        max_length=3,
        choices=DayChoices.choices,
        default=DayChoices.MON
    )
    start_time = models.TimeField(
        _('Start time')
    )
    end_time = models.TimeField(
        _('End time')
    )

    class Meta:
        verbose_name = _("Trainer schedule")
        verbose_name_plural = _("Trainer schedules")
