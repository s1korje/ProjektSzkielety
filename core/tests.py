from django.test import TestCase
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Game, Organizer, Event, PlannedEvent


User = get_user_model()


class EventModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestoweHaslo123!"
        )

        self.game = Game.objects.create(
            name="Counter-Strike 2",
            genre="FPS",
            description="Gra e-sportowa"
        )

        self.organizer = Organizer.objects.create(
            name="Test Esports",
            email="test@example.com",
            website="https://example.com"
        )


        self.event = Event.objects.create(
            title="Testowy turniej CS2",
            description="Opis turnieju",
            game=self.game,
            organizer=self.organizer,
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=8),
            location="Warszawa",
            is_online=False,
            website="https://example.com"
        )

    def test_game_is_saved(self):
        """Sprawdza zapis gry w bazie."""
        game = Game.objects.get(name="Counter-Strike 2")

        self.assertEqual(game.genre, "FPS")
        self.assertEqual(str(game), "Counter-Strike 2")

    def test_event_relations(self):
        """Sprawdza relacje wydarzenia z grą i organizatorem."""
        self.assertEqual(self.event.game, self.game)
        self.assertEqual(self.event.organizer, self.organizer)

        # Sprawdza relację odwrotną
        self.assertIn(self.event, self.game.events.all())
        self.assertIn(self.event, self.organizer.events.all())

    def test_user_can_plan_event(self):
        """Sprawdza zapis wydarzenia w planerze użytkownika."""
        planned = PlannedEvent.objects.create(
            user=self.user,
            event=self.event,
            notes="Chcę obejrzeć finał"
        )

        self.assertEqual(planned.user, self.user)
        self.assertEqual(planned.event, self.event)
        self.assertEqual(
            self.user.planned_events.count(),
            1
        )

    def test_event_dates_validation(self):
        """Sprawdza, czy data zakończenia jest późniejsza."""
        self.event.end_date = (
            self.event.start_date - timedelta(days=1)
        )

        with self.assertRaises(ValidationError):
            self.event.full_clean()

    def test_user_cannot_plan_same_event_twice(self):
        """Sprawdza unikalność wpisów planera."""
        PlannedEvent.objects.create(
            user=self.user,
            event=self.event
        )

        duplicate = PlannedEvent(
            user=self.user,
            event=self.event
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

