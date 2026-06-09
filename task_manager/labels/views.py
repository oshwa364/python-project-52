from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin

from .forms import LabelForm
from .models import Label


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    extra_context = {
        'title': 'Метки'
    }


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно создана'
    extra_context = {
        'title': 'Создать метку',
        'button_text': 'Создать',
    }


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно изменена'
    extra_context = {
        'title': 'Редактирование метки',
        'button_text': 'Изменить',
    }


class LabelDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно удалена'
    protection_message = 'Невозможно удалить метку'
    protection_url = reverse_lazy('labels_list')
    extra_context = {
        'title': 'Удаление метки',
        'button_text': 'Да, удалить'
    }