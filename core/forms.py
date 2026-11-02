
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Event, Game, Organizer

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Adres e-mail"
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Imię"
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Nazwisko"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ten adres e-mail jest już zajęty."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )

        return user


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        label="Adres e-mail"
    )

    class Meta:
        model = Profile

        fields = [
            'first_name',
            'last_name',
            'bio',
            'avatar'
        ]

        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'bio': 'O mnie',
            'avatar': 'Zdjęcie profilowe'
        }

        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Napisz coś o sobie...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data['email']

        users = User.objects.filter(email__iexact=email)
        users = users.exclude(pk=self.instance.user.pk)

        if users.exists():
            raise forms.ValidationError(
                "Ten adres e-mail jest już zajęty."
            )

        return email

    def save(self, commit=True):
        profile = super().save(commit=False)

        if commit:
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()

        return profile


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

    for field in self.fields.values():
        field.widget.attrs.update({
            'class': 'form-control'
        })
