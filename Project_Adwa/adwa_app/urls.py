from django.urls import path
from . import views

urlpatterns = [
    path('response/', views.answer, name='answer'),
    path('feedback/', views.feedback, name='feedback'),
]
