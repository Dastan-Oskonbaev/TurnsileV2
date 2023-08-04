from django.contrib import admin

from apps.journal.models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'key',
        'membership',
        'membership_type',
        'entry_time',
        'create_date',
        'actual_exit_time',
        'exit_time',
    )
    list_display_links = (
        'id',
        'key',
        'membership'
    )
    readonly_fields = (
        'entry_time',
        'exit_time',
        'trainer',
        'membership_type',
        'payment',
    )
    list_filter = (
        'create_date',
    )
    search_fields = (
        'membership__user__first_name',
        'membership__user__last_name',
    )
