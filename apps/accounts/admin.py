from django.contrib import admin

from apps.payments.models import MembershipPayment
from .models import CustomUser, Membership, Trainer, TrainerSchedule


class TrainerScheduleInline(admin.TabularInline):
    model = TrainerSchedule
    extra = 1


class MembershipPaymentInline(admin.TabularInline):
    model = MembershipPayment
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'scan_id',
        'username',
        'phone_number',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
        'updated_at',
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
         {'fields': (
             'id',
             'scan_id',
             'membership_number',
             'first_name',
             'last_name',
             'address',
             'phone_number',
             'email',
             'note',
             'assigned_trainer',
             'is_active',
         )}),
        (None,
         {
                'fields': (
                    'remaining_visits',
                    'username',
                ),
         })
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'remaining_visits',
        'username',
    )
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'address',
        'membership_number',
        'remaining_visits',
        'assigned_trainer',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    inlines = [
        MembershipPaymentInline,
    ]


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'scan_id',
        'username',
        'phone_number',
        'email',
        'is_active',
        'salary',
        'about_me',
    )

    inlines = [
        TrainerScheduleInline,
    ]
