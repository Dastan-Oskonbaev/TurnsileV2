from celery import shared_task
from apps.payments.models import MembershipPayment
from utils.time import get_current_date


@shared_task
def clear_subscriptions():
    today = get_current_date()
    expired_payments = MembershipPayment.objects.filter(end_date__lt=today, is_active=True)

    for payment in expired_payments:
        membership = payment.membership

        if membership.get_actual_payment():
            continue

        membership.remaining_visits = 0
        membership.assigned_trainer = None
        membership.save()

        payment.is_active = False
        payment.end_date = today
        payment.save()


@shared_task
def activate_payment():
    today = get_current_date()
    payments = MembershipPayment.objects.filter(start_date=today, is_active=False)

    for payment in payments:
        payment.is_active = True
        payment.save()
