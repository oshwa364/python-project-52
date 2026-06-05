from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, AuthorPermissionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView
from django.contrib.auth.models import User


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


class TaskDeleteView(AuthRequiredMixin, AuthorPermissionMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'
    permission_message = 'Нельзя удалить пользователя, потому что ему назначена задача'
    extra_context = {
        'title': 'Удаление задачи',
        'button_text': 'Да, удалить',
    }
