
from django import forms
from .models import Event,Game,Organizer


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "game",
            "organizer",
            "event_type",
            "status",
            "start_date",
            "end_date",
            "location",
            "is_online",
            "website",
        ]
        labels = {
            "title": "Nazwa wydarzenia",
            "description": "Opis",
            "game": "Gra",
            "organizer": "Organizator",
            "event_type": "Rodzaj wydarzenia",
            "status": "Status",
            "start_date": "Data rozpoczęcia",
            "end_date": "Data zakończenia",
            "location": "Lokalizacja",
            "is_online": "Wydarzenie online",
            "website": "Strona internetowa",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "game": forms.Select(attrs={
                "class": "form-select",
            }),
            "organizer": forms.Select(attrs={
                "class": "form-select",
            }),
            "event_type": forms.Select(attrs={
                "class": "form-select",
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "start_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "location": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "is_online": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
            }),
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["name", "genre", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "genre": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
        }
        labels = {
            "name": "Nazwa gry",
            "genre": "Gatunek",
            "description": "Opis gry",
        }


class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ["name", "email", "website"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
            }),
        }
        labels = {
            "name": "Nazwa organizatora",
            "email": "Adres e-mail",
            "website": "Strona internetowa",
        }




def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    date_format = "%Y-%m-%dT%H:%M"

    self.fields["start_date"].input_formats = [date_format]
    self.fields["end_date"].input_formats = [date_format]
