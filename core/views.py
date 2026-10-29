from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Event
from .forms import EventForm

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
