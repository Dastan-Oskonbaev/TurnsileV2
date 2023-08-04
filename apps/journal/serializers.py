from datetime import datetime, date, timedelta

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from utils.time import get_current_time
from .models import Journal


class JournalSerializer(serializers.ModelSerializer):
    key_name = serializers.CharField(source='key.name', read_only=True)
    membership_name = serializers.CharField(source='membership.get_full_name', read_only=True)
    membership_number = serializers.CharField(source='membership.membership_number', read_only=True)
    membership_type_name = serializers.CharField(source='membership_type.name', read_only=True)

    def validate(self, data):
        _membership = data.get('membership')
        _key = data.get('key')

        _payment = _membership.get_actual_payment()

        if not _payment:
            raise serializers.ValidationError({
                'membership': _('Membership has no active payments')
            })

        if _membership.remaining_visits <= 0:
            raise serializers.ValidationError({
                'membership': _('Membership has no remaining visits')
            })

        if _key.membership and not data.get('actual_exit_time'):
            raise serializers.ValidationError({
                'key': _('Key is already in use')
            })

        data['membership_type'] = _payment.type
        data['payment'] = _payment

        if _membership.assigned_trainer:
            data['trainer'] = _membership.assigned_trainer

        pool_duration = _payment.pool_duration

        if not data.get('id'):
            data['entry_time'] = get_current_time()
            data['exit_time'] = (datetime.combine(date.today(), data.get('entry_time')) +
                                 timedelta(hours=pool_duration.hour, minutes=pool_duration.minute)).time()

        return data

    class Meta:
        model = Journal
        fields = (
            'id',
            'key',
            'key_name',
            'membership',
            'membership_type',
            'membership_type_name',
            'membership_name',
            'membership_number',
            'entry_time',
            'create_date',
            'actual_exit_time',
            'exit_time',
        )
