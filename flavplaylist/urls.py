from django.urls import path
from flavplaylist import views

urlpatterns = [
    path('', views.PlayListView.as_view())
]