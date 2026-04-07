"""
URL configuration for hangarin_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    HomePageView,
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView, 
    SubTaskListView, SubTaskDetailView, SubTaskUpdateView, SubTaskDeleteView,
    NoteListView, NoteDetailView, NoteUpdateView, NoteDeleteView, add_subtask, add_note
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('pwa.urls')),
    path("accounts/", include("allauth.urls")),
    path("", HomePageView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/add/", TaskCreateView.as_view(), name="task-add"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/add/", CategoryCreateView.as_view(), name="category-add"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-edit"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
    path("priorities/", PriorityListView.as_view(), name="priority-list"),
    path("priorities/add/", PriorityCreateView.as_view(), name="priority-add"),
    path("priorities/<int:pk>/edit/", PriorityUpdateView.as_view(), name="priority-edit"),
    path("priorities/<int:pk>/delete/", PriorityDeleteView.as_view(), name="priority-delete"),
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail'),
    path('subtasks/<int:pk>/edit/', SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('tasks/<int:task_id>/subtask/add/', add_subtask, name='subtask-add'),
    path('tasks/<int:task_id>/note/add/', add_note, name='note-add'),
]
