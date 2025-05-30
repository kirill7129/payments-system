from django.contrib import admin

from organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'inn',
        'balance',
    )
