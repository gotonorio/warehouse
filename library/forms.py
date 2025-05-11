import os

from django import forms

from library.models import BigCategory, Category, File


class FileForm(forms.ModelForm):
    """Fileモデルのフォーム
    ModelForm限定の方法としてclass Metaでwidgetを設定する。class以外も変更できる。
    https://narito.ninja/blog/detail/52/
    """

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in [".pdf", ".zip"]:
            raise forms.ValidationError("PDFまたはZIPファイルのみアップロード可能です。")
        return uploaded_file

    class Meta:
        model = File
        fields = (
            "title",
            "category",
            "summary",
            "key_word",
            "src",
            "rank",
            "created_at",
            "alive",
            "download",
        )
        # field毎に異なるclassを設定する場合には、この方法を取る。
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "select-css",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "textarea",
                }
            ),
            "key_word": forms.Textarea(
                attrs={
                    "class": "textarea",
                }
            ),
            # 'src': forms.ClearableFileInput(attrs={
            "src": forms.FileInput(
                attrs={
                    # 'class': "file",
                    "class": "input",
                }
            ),
            "rank": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "created_at": forms.DateInput(
                attrs={
                    "class": "input",
                }
            ),
            "alive": forms.NullBooleanSelect(
                attrs={
                    "class": "select-css",
                }
            ),
            "download": forms.NullBooleanSelect(
                attrs={
                    "class": "select-css",
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    """Categoryモデルのフォーム"""

    class Meta:
        model = Category
        fields = (
            "name",
            "path_name",
            "parent",
            "rank",
            "created_at",
            "restrict",
            "alive",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "path_name": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "parent": forms.Select(
                attrs={
                    "class": "select-css",
                }
            ),
            "rank": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "created_at": forms.DateInput(
                attrs={
                    "class": "input",
                }
            ),
            "restrict": forms.CheckboxInput(
                attrs={
                    "class": "checkboxinput",
                }
            ),
            "alive": forms.CheckboxInput(
                attrs={
                    "class": "checkboxinput",
                }
            ),
        }


class BigCategoryForm(forms.ModelForm):
    """親Categoryモデルのフォーム"""

    class Meta:
        model = BigCategory
        fields = ("name", "rank", "created_at", "alive", "is_admin")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "rank": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),
            "created_at": forms.DateInput(
                attrs={
                    "class": "input",
                }
            ),
            "alive": forms.CheckboxInput(
                attrs={
                    "class": "checkboxinput",
                }
            ),
            "is_admin": forms.CheckboxInput(
                attrs={
                    "class": "checkboxinput",
                }
            ),
        }
