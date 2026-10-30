from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'first_name',
        'last_name',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'first_name',
        'last_name'
    )