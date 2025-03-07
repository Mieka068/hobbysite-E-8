from django.contrib import admin
from .models import Commission, Comment


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ("title", "people_required", "created_on", "updated_on")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("commission", "entry", "created_on", "updated_on")
