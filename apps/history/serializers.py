from rest_framework import serializers
from .models import HistoryType, MembershipHistory


class HistoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryType
        fields = '__all__'


class MembershipHistorySerializer(serializers.ModelSerializer):
    type = HistoryTypeSerializer(read_only=True)

    class Meta:
        model = MembershipHistory
        fields = '__all__'
