from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserPermissionEditDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)