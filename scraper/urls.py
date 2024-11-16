
from django.urls import path
from . import views
# scraper/urls.py
urlpatterns = [
    path('search/', views.case_search, name='case_search'),
]
