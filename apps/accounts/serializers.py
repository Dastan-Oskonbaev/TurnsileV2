from rest_framework import serializers

from apps.payments.serializers import PaymentInlineSerializer

from .models import CustomUser, Trainer, TrainerSchedule, Membership


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'password',
            'role'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'scan_id'
        )


class MembershipSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField(read_only=True)

    def get_payment(self, obj: Membership) -> dict:
        payment = obj.get_actual_payment()

        if not payment:
            return {}

        return PaymentInlineSerializer(payment).data

    class Meta:
        model = Membership
        fields = (
            'id',
            'membership_number',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'trainer',
            'gender',
            'note',
            'remaining_visits',
            'payment',
            'scan_id',
            'created_at'
        )


class TrainerScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerSchedule
        fields = '__all__'


class TrainerScheduleInlineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = TrainerSchedule
        fields = (
            'id',
            'day',
            'start_time',
            'end_time'
        )


class TrainerSerializer(serializers.ModelSerializer):
    schedules = TrainerScheduleInlineSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Trainer
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'address',
            'about_me',
            'salary',
            'email',
            'password',
            'username',
            'schedules',
            'scan_id',
            'created_at'
        )


class TrainerUpdateSerializer(serializers.ModelSerializer):
    schedules = TrainerScheduleInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Trainer
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'address',
            'about_me',
            'salary',
            'email',
            'username',
            'schedules',
            'created_at',
        )


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = (
            'password',
            'new_password',
        )
