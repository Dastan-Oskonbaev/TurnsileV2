from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.time import get_current_date
from .models import MembershipPayment


@receiver(post_save, sender=MembershipPayment)
def add_remaining_visits(sender, instance, created, **kwargs):
    today = get_current_date()

    old_is_active = instance.is_active
    instance.is_active = instance.start_date <= today < instance.end_date

    if old_is_active != instance.is_active:
        instance.save()

    membership = instance.membership

    payment = membership.get_actual_payment()

    if payment == instance:
        if not old_is_active:
            membership.remaining_visits = instance.visits_count

        if instance.trainer:
            membership.assigned_trainer = instance.trainer

        membership.save()
