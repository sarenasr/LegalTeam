# scraper/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.case_search, name='case_search'),
]
