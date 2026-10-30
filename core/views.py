from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Event
from .forms import EventForm,GameForm, OrganizerForm

def home(request):
    return render(request, 'core/home.html', {'tytul': 'Strona główna', 'items': ['a', 'b', 'c']})


def event_list(request):
    events = Event.objects.select_related(
        "game", "organizer"
    ).all()

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


def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related("game", "organizer"),
        pk=event_id,
    )

    return render(request, "events/event_detail.html", {
        "event": event,
    })

@staff_member_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save()
            return redirect("event_detail", event_id=event.pk)
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {
        "form": form,
    })



@staff_member_required
def game_create(request):
    form = GameForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
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
        return redirect("organizer_create")

    return render(request, "events/organizer_form.html", {
        "form": form,
        "page_title": "Dodaj organizatora",
    })