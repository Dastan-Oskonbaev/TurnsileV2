from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import date, timedelta, datetime

from apps.accounts.models import Membership, Trainer
from apps.payments.models import PaymentType, MembershipPayment
from apps.pool.models import Key
from utils.time import get_current_time


class Journal(models.Model):
    key = models.ForeignKey(
        Key,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name=_('Key')
    )
    membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name=_('Membership')
    )
    membership_type = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name=_('Membership type'),
        blank=True,
    )
    payment = models.ForeignKey(
        MembershipPayment,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name=_('Payment'),
        null=True,
        blank=True,
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='journals',
        verbose_name=_('Trainer'),
        null=True,
        blank=True,
    )
    entry_time = models.TimeField(
        _('Entry time'),
        auto_now_add=True
    )
    exit_time = models.TimeField(
        _('Exit time'),
        null=True,
        blank=True,
    )
    actual_exit_time = models.TimeField(
        _('Actual exit time'),
        null=True,
        blank=True,
    )
    create_date = models.DateField(
        _('Create date'),
        auto_now_add=True,
        null=True,
        blank=True,
    )

    def clean(self):
        self.payment = self.membership.get_actual_payment()

        if not self.payment:
            raise ValidationError({
                'membership': _('Membership has no active payments')
            })

        if self.membership.remaining_visits <= 0:
            raise ValidationError({
                'membership': _('Membership has no remaining visits')
            })

        if self.key.membership and not self.actual_exit_time:
            raise ValidationError({
                'key': _('Key is already in use')
            })

        self.membership_type = self.payment.type

        if self.membership.assigned_trainer:
            self.trainer = self.membership.assigned_trainer

        pool_duration = self.payment.pool_duration

        if not self.pk:
            self.entry_time = get_current_time()
            self.exit_time = (datetime.combine(date.today(), self.entry_time) +
                              timedelta(hours=pool_duration.hour, minutes=pool_duration.minute)).time()

    def __str__(self):
        return f'{self.membership}: {self.create_date}'


class Meta:
    verbose_name = _('Journal')
    verbose_name_plural = _('Journals')
