from datetime import timedelta, time

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from apps.accounts.models import Membership, Trainer
from apps.payments.constants import PaymentTypeChoices
from utils.time import get_current_date


class PaymentType(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    type = models.CharField(
        _('Memreship Type'),
        max_length=100,
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.MEMBERSHIP
    )
    price = models.PositiveIntegerField(
        _('Price'),
        default=0
    )
    period = models.PositiveIntegerField(
        _('Period'),
        default=1
    )
    visits_count = models.PositiveIntegerField(
        _('Visits Count'),
        default=1
    )
    with_trainer = models.BooleanField(
        _('With Trainer'),
        default=False
    )
    pool_duration = models.TimeField(
        _('Pool Duration'),
        default=time(hour=1)
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Membership Type")
        verbose_name_plural = _("Membership Types")


class MembershipPayment(models.Model):
    membership = models.ForeignKey(
        Membership,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('Membership')
    )
    type = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Membership Type')
    )
    amount = models.PositiveIntegerField(
        _('Payment amount'),
        null=True, blank=True
    )
    period = models.PositiveIntegerField(
        _('Period'),
        null=True, blank=True
    )
    visits_count = models.PositiveIntegerField(
        _('Visits count'),
        null=True, blank=True
    )
    start_date = models.DateField(
        _('Start date of the payment period'),
        default=get_current_date
    )
    end_date = models.DateField(
        _('End date of payment period'),
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        _('Date of creation'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Update date'),
        auto_now=True
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='trainer',
        verbose_name=_('Trainer'),
        null=True,
        blank=True,
    )
    pool_duration = models.TimeField(
        _('Pool duration'),
        default=time(1, 0)
    )
    is_active = models.BooleanField(
        _('Is active'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.membership} - {self.type}"

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def clean(self):
        if not self.type:
            raise ValidationError({
                'type': _('Membership type is required.')
            })

        if self.type.with_trainer and not self.trainer:
            raise ValidationError({
                'trainer': _('Trainer is required.')
            })
        else:
            self.trainer = None

        if not self.period:
            self.period = self.type.period

        self.end_date = self.start_date + timedelta(days=self.period)

        payment = self.membership.get_payment_by_date(
            self.start_date,
            self.end_date,
            exclude=self.pk if self.pk else None
        )

        if payment:
            raise ValidationError({
                'start_date': _('The specified payment period overlaps with an existing payment for this '
                                'membership.')})

        if not self.amount:
            self.amount = self.type.price

        if not self.visits_count:
            self.visits_count = self.type.visits_count

        if not self.pool_duration:
            self.pool_duration = self.type.pool_duration
