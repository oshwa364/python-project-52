from task_manager.users.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    DeleteProtectionMixin,
    UserPermissionEditDeleteMixin,
)
from task_manager.users.forms import UserForm


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'
    extra_context = {
        'title': 'Регистрация',
        'button_text': 'Зарегистрировать',
    }


class UserUpdateView(UserPermissionEditDeleteMixin,
                    SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('users_list')
    permission_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'
    permission_message = 'У вас нет прав для изменения'
    extra_context = {
        'title': 'Редактирование пользователя',
        'button_text': 'Изменить',
    }


class UserDeleteView(UserPermissionEditDeleteMixin, DeleteProtectionMixin,
                     SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    permission_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'
    permission_message = 'У вас нет прав для изменения'
    protection_message = 'Нельзя удалить пользователя, ' \
                         'потому что ему назначена задача'
    protection_url = reverse_lazy('users_list')
    extra_context = {
        'title': 'Удаление пользователя',
        'button_text': 'Да, удалить',
    }
