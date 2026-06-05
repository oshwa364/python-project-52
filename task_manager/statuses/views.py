from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin

from .forms import StatusForm
from .models import Status


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно создан'
    extra_context = {
        'title': 'Создать статус',
        'button_text': 'Создать'
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно изменен'
    extra_context = {
        'title': 'Редактирование статуса',
        'button_text': 'Изменить'
    }


class StatusDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно удален'
    extra_context = {
        'title': 'Удаление статуса',
        'button_text': 'Да, удалить'
    }
