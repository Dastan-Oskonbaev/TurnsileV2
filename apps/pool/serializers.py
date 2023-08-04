from rest_framework import serializers

from .models import Key, ServiceCard


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class ServiceCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCard
        fields = '__all__'
