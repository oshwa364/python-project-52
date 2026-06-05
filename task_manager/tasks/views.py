from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.mixins import AuthorPermissionMixin, AuthRequiredMixin

from .forms import TaskForm
from .models import Task


class TaskListView(AuthRequiredMixin, ListView):
    template_name = 'tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'
    extra_context = {
        'title': 'Задачи',
    }


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно создана'
    extra_context = {
        'title': 'Создать задачу',
        'button_text': 'Создать',
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(AuthRequiredMixin, DetailView):
    template_name = 'tasks/detail.html'
    model = Task
    context_object_name = 'task'
    extra_context = {
        'title': 'Просмотр задачи',
    }


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно изменена'
    extra_context = {
        'title': 'Изменение задачи',
        'button_text': 'Изменить',
    }


class TaskDeleteView(AuthRequiredMixin, AuthorPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'
    extra_context = {
        'title': 'Удаление задачи',
        'button_text': 'Да, удалить',
    }
