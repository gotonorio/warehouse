from django import forms

from information.models import Information, InformationType


class InformationForm(forms.ModelForm):
    """Information登録用のフォーム."""

    class Meta:
        model = Information
        fields = "__all__"
        fields = ("title", "comment", "information", "display_info", "created_at", "type_name")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "comment": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "information": forms.Textarea(
                attrs={
                    "class": "textarea",
                }
            ),
            "display_info": forms.CheckboxInput(
                attrs={
                    "class": "checkbox",
                }
            ),
            "created_at": forms.DateTimeInput(
                attrs={
                    "class": "input",
                }
            ),
            "type_name": forms.Select(
                attrs={
                    "class": "select-css",
                }
            ),
        }

    def get_initial_for_field(self, field, field_name):
        initial_id = InformationType.objects.get(type_name="情報")
        if field_name == "type_name":
            return initial_id
        return super().get_initial_for_field(field, field_name)
