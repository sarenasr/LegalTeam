from django.urls import path
from . import views
# DocAnalysis/urls.py
urlpatterns = [
    path('', views.index, name='analysis'), 
    path('analyze/', views.analyze_document, name='analyze_document'),
    path('ask/', views.ask_question, name='ask_question'),
]
