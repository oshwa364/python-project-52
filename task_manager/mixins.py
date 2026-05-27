from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


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
