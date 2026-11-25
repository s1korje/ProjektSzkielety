
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .forms import (
    RegisterForm,
    ProfileForm,
    EventForm,
    GameForm,
    OrganizerForm,
    TeamForm,
)
from .models import Profile, Event, PlannedEvent, Team, Organizer


class CustomLoginView(LoginView):
    template_name = 'core/user/login.html'
    redirect_authenticated_user = True


def home(request):
    return render(request, 'core/home.html', {
        'tytul': 'Strona główna',
        'items': ['a', 'b', 'c'],
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, 'Konto zostało utworzone!')
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'core/user/register.html', {
        'form': form,
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'core/user/login.html', {
        'form': form,
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(request, 'core/user/profile.html', {
        'profile': user_profile,
    })


@login_required
def edit_profile(request):
    user_profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile,
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profil został zaktualizowany!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'core/user/edit_profile.html', {
        'form': form,
    })


@login_required
def event_list(request):
    events = Event.objects.select_related(
        "game", "organizer"
    ).annotate(
        planned_count=Count("user_plans")
    )

    query = request.GET.get("q", "").strip()

    if query:
        events = events.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(game__name__icontains=query)
            | Q(organizer__name__icontains=query)
        )

    return render(request, "events/event_list.html", {
        "events": events,
        "query": query,
    })


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related(
            "game", "organizer"
        ).annotate(
            planned_count=Count("user_plans")
        ),
        pk=event_id,
    )

    return render(request, "events/event_detail.html", {
        "event": event,
    })


@staff_member_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save()
            messages.success(request, "Wydarzenie zostało dodane.")
            return redirect("event_detail", event_id=event.pk)
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {
        "form": form,
    })


@staff_member_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(
            request.POST,
            request.FILES,
            instance=event,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Wydarzenie zostało zaktualizowane!"
            )
            return redirect("event_detail", event_id=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_form.html", {
        "form": form,
        "page_title": "Edytuj wydarzenie",
        "event": event,
    })


@staff_member_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event_title = event.title
        event.delete()

        messages.success(
            request,
            f'Wydarzenie "{event_title}" zostało usunięte.'
        )
        return redirect("event_list")

    return render(request, "core/confirm_delete.html", {
        "object": event,
        "object_name": "wydarzenie",
        "cancel_url": reverse(
            "event_detail",
            kwargs={"event_id": event.pk},
        ),
        "warning": (
            "Usunięte zostaną również zapisy użytkowników "
            "na to wydarzenie."
        ),
    })


@staff_member_required
def game_create(request):
    form = GameForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Gra została dodana.")
        return redirect("game_create")

    return render(request, "events/game_form.html", {
        "form": form,
        "page_title": "Dodaj grę",
    })


@staff_member_required
def organizer_create(request):
    form = OrganizerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Organizator został dodany.")
        return redirect("organizer_list")

    return render(request, "events/organizer_form.html", {
        "form": form,
        "page_title": "Dodaj organizatora",
    })


@login_required
def organizer_list(request):
    organizers = Organizer.objects.all().order_by("name")

    return render(request, "core/organizer_list.html", {
        "organizers": organizers,
    })


@staff_member_required
def organizer_delete(request, organizer_id):
    organizer = get_object_or_404(Organizer, pk=organizer_id)

    if request.method == "POST":
        organizer_name = organizer.name

        try:
            organizer.delete()
            messages.success(
                request,
                f'Organizator "{organizer_name}" został usunięty.'
            )
        except ProtectedError:
            messages.error(
                request,
                "Nie można usunąć tego organizatora, ponieważ "
                "jest przypisany do istniejących wydarzeń. "
                "Najpierw zmień organizatora tych wydarzeń lub je usuń."
            )

        return redirect("organizer_list")

    return render(request, "core/confirm_delete.html", {
        "object": organizer,
        "object_name": "organizatora",
        "cancel_url": reverse("organizer_list"),
        "warning": (
            "Organizator przypisany do wydarzeń nie może zostać "
            "usunięty. Najpierw trzeba zmienić organizatora "
            "tych wydarzeń lub usunąć same wydarzenia."
        ),
    })


@login_required
@require_POST
def add_to_plan(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    planned_event, created = PlannedEvent.objects.get_or_create(
        user=request.user,
        event=event,
    )

    if created:
        messages.success(
            request,
            "Wydarzenie dodano do Twojego planu!"
        )
    else:
        messages.info(
            request,
            "To wydarzenie jest już w Twoim planie."
        )

    return redirect("event_detail", event_id=event.id)


@login_required
def my_plan(request):
    planned_events = PlannedEvent.objects.filter(
        user=request.user
    ).select_related(
        "event",
        "event__game",
        "event__organizer",
    )

    return render(request, "events/my_plan.html", {
        "planned_events": planned_events,
    })


@login_required
@require_POST
def remove_from_plan(request, event_id):
    planned_event = get_object_or_404(
        PlannedEvent,
        user=request.user,
        event_id=event_id,
    )

    planned_event.delete()
    messages.success(
        request,
        "Wydarzenie usunięto z Twojego planu."
    )

    return redirect("my_plan")


@staff_member_required
def team_create(request):
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Drużyna została dodana.")
            return redirect("team_list")
    else:
        form = TeamForm()

    return render(request, "core/team_create.html", {
        "form": form,
    })


@require_GET
def teams_by_game(request):
    game_id = request.GET.get("game_id")

    if not game_id:
        return JsonResponse({"teams": []})

    teams = Team.objects.filter(
        game_id=game_id
    ).order_by("name")

    data = {
        "teams": [
            {
                "id": team.id,
                "name": str(team),
            }
            for team in teams
        ]
    }

    return JsonResponse(data)


@login_required
def team_list(request):
    teams = Team.objects.select_related("game").order_by("name")

    return render(request, "core/team_list.html", {
        "teams": teams,
    })


@staff_member_required
def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.method == "POST":
        team_name = team.name
        team.delete()

        messages.success(
            request,
            f'Drużyna "{team_name}" została usunięta.'
        )
        return redirect("team_list")

    return render(request, "core/confirm_delete.html", {
        "object": team,
        "object_name": "drużynę",
        "cancel_url": reverse("team_list"),
        "warning": (
            "Drużyna zostanie odłączona od wydarzeń, "
            "do których była przypisana. Same wydarzenia pozostaną."
        ),
    })
