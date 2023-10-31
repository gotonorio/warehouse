from django import forms

from information.models import Information


class InformationForm(forms.ModelForm):
    """Information登録用のフォーム."""

    class Meta:
        model = Information
        fields = "__all__"
        fields = ("title", "comment", "information", "display_info", "created_at")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input is-size-6",
                }
            ),
            "comment": forms.TextInput(
                attrs={
                    "class": "input is-size-6",
                }
            ),
            "information": forms.Textarea(
                attrs={
                    "class": "textarea is-size-6",
                }
            ),
            "display_info": forms.CheckboxInput(
                attrs={
                    "class": "checkboxinput is-size-4",
                }
            ),
            "created_at": forms.DateTimeInput(
                attrs={
                    "class": "input is-size-6",
                }
            ),
        }
