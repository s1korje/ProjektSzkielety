from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("my-plan/", views.my_plan, name="my_plan"),
    path("events/<int:event_id>/add-to-plan/", views.add_to_plan, name="add_to_plan"),
    path("events/<int:event_id>/remove-from-plan/", views.remove_from_plan, name="remove_from_plan"),
]