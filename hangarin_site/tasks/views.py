from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task  # Tandaan: Dapat may Task model ka na sa models.py

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"