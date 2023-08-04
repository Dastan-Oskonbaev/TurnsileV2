from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.time import get_current_date
from .models import Journal


@receiver(post_save, sender=Journal)
def update_membership(sender, instance, created, **kwargs):
    if instance.actual_exit_time:
        instance.membership.remaining_visits -= 1

        if instance.membership.remaining_visits == 0:
            instance.membership.assigned_trainer = None

            instance.payment.is_active = False
            instance.payment.end_date = get_current_date()
            instance.payment.save()

        instance.membership.save()


@receiver(post_save, sender=Journal)
def update_key(sender, instance, created, **kwargs):
    if not instance.actual_exit_time:
        instance.key.membership = instance.membership
    else:
        instance.key.membership = None

    instance.key.save()
