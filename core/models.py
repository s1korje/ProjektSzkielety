from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Gra"
        verbose_name_plural = "Gry"

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"

    def __str__(self):
        return self.name


class Event(models.Model):
    class EventType(models.TextChoices):
        TOURNAMENT = "TOURNAMENT", "Turniej"
        LEAGUE = "LEAGUE", "Liga"
        OTHER = "OTHER", "Inne"

    class EventStatus(models.TextChoices):
        UPCOMING = "UPCOMING", "Nadchodzące"
        ONGOING = "ONGOING", "W trakcie"
        FINISHED = "FINISHED", "Zakończone"

    title = models.CharField(max_length=200)
    description = models.TextField()
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name="events",
    )
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.PROTECT,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.TOURNAMENT,
    )
    status = models.CharField(
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.UPCOMING,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

    def clean(self):
        super().clean()

        if (
            self.start_date
            and self.end_date
            and self.end_date <= self.start_date
        ):
            raise ValidationError({
                "end_date": "Data zakończenia musi być późniejsza niż rozpoczęcia."
            })

    def __str__(self):
        return self.title


class PlannedEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="planned_events",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="user_plans",
    )
    added_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["event__start_date"]
        verbose_name = "Zaplanowane wydarzenie"
        verbose_name_plural = "Zaplanowane wydarzenia"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"],
                name="unique_user_planned_event",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.event}"

