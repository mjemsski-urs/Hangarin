from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView
from .models import Task, Category, Priority, SubTask, Note

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_priorities"] = Priority.objects.count()
        context["tasks_due_today"] = Task.objects.filter(deadline=timezone.now().date()).count()
        return context

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = "__all__"

class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['content']

class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["title", "deadline", "status"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "deadline"

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        context["subtasks"] = SubTask.objects.filter(parent_task=task)
        context["notes"] = Note.objects.filter(task=task)
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("category-list")

class PriorityListView(ListView):
    model = Priority
    context_object_name = "priorities"
    template_name = "priority_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = "priority_confirm_delete.html"
    success_url = reverse_lazy("priority-list")

# SubTasks
class SubTaskListView(ListView):
    model = SubTask
    template_name = "subtask_list.html"
    context_object_name = "subtasks"
    paginate_by = 10

class SubTaskDetailView(DetailView):
    model = SubTask
    template_name = "subtask_detail.html"
    context_object_name = "subtask"

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object.parent_task 
        return context

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.parent_task.id})

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtask_confirm_delete.html"
    success_url = reverse_lazy("subtask-list")

# Notes
class NoteListView(ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"
    paginate_by = 10

class NoteDetailView(DetailView):
    model = Note
    template_name = "note_detail.html"
    context_object_name = "note"

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object.task 
        return context

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.id})

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("note-list")

def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.parent_task = task
            subtask.save()
            return redirect('task-detail', pk=task.id)
    else:
        form = SubTaskForm()
    return render(request, 'subtask_form.html', {'form': form, 'task': task})

def add_note(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.task = task
            note.save()
            return redirect('task-detail', pk=task.id)
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form, 'task': task})