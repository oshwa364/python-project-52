from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import ProtectedError


class UserPermissionEditDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)
    

class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = 'Вы не вошли. Пожалуйста, войдите.'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class AuthorPermissionMixin:
    permission_message = 'Задачу может удалить только ее автор'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().author.id:
            messages.error(self.request, self.permission_message)
            return redirect(reverse_lazy('tasks_list'))
        return super().dispatch(request, *args, **kwargs)
    

class DeleteProtectionMixin:
    protected_message = 'Нельзя удалить пользователя, потому что ему назначена задача'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
        return redirect(reverse_lazy('users_list'))