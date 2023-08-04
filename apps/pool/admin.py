from django.contrib import admin

from .models import Key, ServiceCard


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'membership',
    )


@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner_name',
        'scan_id',
    )