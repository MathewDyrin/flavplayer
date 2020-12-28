from django.urls import path
from flavaudio import views

urlpatterns = [
    path("", views.AudioView.as_view())
]