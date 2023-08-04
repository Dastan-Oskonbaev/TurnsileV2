from django.contrib import admin

from apps.payments.models import PaymentType, MembershipPayment


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'type',
        'price',
        'period',
        'visits_count',
        'with_trainer',
        'pool_duration',
    )
    list_display_links = ('name',)
    list_filter = ('type',)
    search_fields = (
        'name',
        'price'
    )


@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'membership',
        'type',
        'amount',
        'period',
        'visits_count',
        'trainer',
        'pool_duration',
        'created_at',
        'start_date',
        'end_date',
        'is_active',
    )
    search_fields = (
        'membership_user__first_name',
        'membership_user__last_name',
    )
    readonly_fields = (
        'end_date',
    )
    list_filter = (
        'type',
        'is_active',
        # 'created_at',
        'end_date',
    )
