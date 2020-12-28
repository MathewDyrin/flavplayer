from django.urls import path
from flavsearch import views

urlpatterns = [
    path('', views.SearchView.as_view())
]
