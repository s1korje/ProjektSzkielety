from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html', {'tytul': 'Strona główna', 'items': ['a', 'b', 'c']})