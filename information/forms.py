from django import forms

from information.models import Information, InformationType


class InformationForm(forms.ModelForm):
    """Information登録用のフォーム."""

    type_name = forms.ModelChoiceField(
        queryset=InformationType.objects.all(),
        empty_label="選択してください",
        widget=forms.Select(attrs={"class": "select-css is-primary"}),
    )

    class Meta:
        model = Information
        # fields = "__all__"
        fields = ("title", "comment", "information", "display_info", "created_at", "type_name", "sequense")
        widgets = {
            "title": forms.TextInput(attrs={"class": "input"}),
            "comment": forms.TextInput(attrs={"class": "input"}),
            "information": forms.Textarea(attrs={"class": "textarea"}),
            "display_info": forms.CheckboxInput(),
            "created_at": forms.DateTimeInput(attrs={"class": "input"}),
            "sequense": forms.NumberInput(attrs={"class": "input"}),
        }
