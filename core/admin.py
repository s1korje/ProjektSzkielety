from django.contrib import admin
from .models import Profile, Team, Event
from .forms import EventForm
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

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "game", "country")
    list_filter = ("game", "country")
    search_fields = ("name", "tag", "country")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm

    list_display = (
        "title",
        "game",
        "organizer",
        "start_date",
        "status"
    )

    list_filter = ("game", "status", "event_type")
    search_fields = ("title",)
    filter_horizontal = ("teams",)