from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    """権限不足時に指定した403画面を表示するMixin"""

    permission_denied_template = "403.html"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(
                self.request,
                self.permission_denied_template,
                status=403,
            )

        return super().handle_no_permission()
