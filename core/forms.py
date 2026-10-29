
from django import forms
from .models import Event


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        date_format = "%Y-%m-%dT%H:%M"

        self.fields["start_date"].input_formats = [date_format]
        self.fields["end_date"].input_formats = [date_format]
