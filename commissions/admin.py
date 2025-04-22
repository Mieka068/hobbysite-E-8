from django.contrib import admin
from .models import Commission, Job


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_on", "updated_on")
    list_filter = ("status",)
    search_fields = ("title",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("commission", "role", "manpower_required", "status")
    list_filter = ("status",)
    search_fields = ("role",)