from rest_framework import serializers


class DateInlineSerializer(serializers.Serializer):
    date = serializers.DateField()
    actives = serializers.IntegerField()


class ReportSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_memberships = serializers.IntegerField()
    new_memberships = serializers.IntegerField()
    one_time_visits = serializers.IntegerField()


class DatesSerializer(serializers.Serializer):
    date = serializers.DateField()
    actives = serializers.IntegerField()


class SalesSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    amount = serializers.IntegerField()
    percentage = serializers.FloatField(required=False)
    dates = DateInlineSerializer(many=True, required=False)
