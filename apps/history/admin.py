from django.contrib import admin

from .models import MembershipHistory, HistoryType


@admin.register(MembershipHistory)
class MembershipHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'membership',
        'type',
        'description',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'type',
    )
    search_fields = (
        'membership',
    )
    list_display_links = (
        'membership',
    )


@admin.register(HistoryType)
class HistoryTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'icon',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_display_links = (
        'name',
    )
