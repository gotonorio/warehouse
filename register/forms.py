from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input is-size-6'
            field.widget.attrs['placeholder'] = field.label
