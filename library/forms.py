import os
import re
import unicodedata

from django import forms
from django.conf import settings

from library.models import BigCategory, Category, File


class FileForm(forms.ModelForm):
    """Fileモデルのフォーム
    ModelForm限定の方法としてclass Metaでwidgetを設定する。class以外も変更できる。
    https://narito.ninja/blog/detail/52/
    """

    def clean_src(self):
        uploaded_file = self.cleaned_data["src"]
        # (1) ファイルの拡張子をチェック
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in [".pdf", ".zip"]:
            raise forms.ValidationError("PDFまたはZIPファイルのみアップロード可能です。")
        # (2) ファイルサイズをチェック（50MB以下）
        if uploaded_file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise forms.ValidationError("ファイルサイズは50MB以下に分割してください。")
        # (3) ファイル名の正規化
        uploaded_file.name = unicodedata.normalize("NFKC", uploaded_file.name)

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
            "is_confidential",
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
            # "alive": forms.NullBooleanSelect(
            #     attrs={
            #         "class": "select-css",
            #     }
            # ),
            # "download": forms.NullBooleanSelect(
            #     attrs={
            #         "class": "select-css",
            #     }
            # ),
        }
        help_texts = {
            "src": "※ fileサイズは50MB以下にしてください。",
        }


class CategoryForm(forms.ModelForm):
    """Categoryモデルのフォーム"""

    def clean_path_name(self):
        path_name = self.cleaned_data["path_name"]
        # 英数字のみ許可（大文字・小文字・数字）
        if not re.fullmatch(r"[A-Za-z0-9]+", path_name):
            raise forms.ValidationError("パス名は英数字のみ使用できます。")

        return path_name

    def clean_name(self):
        category_name = self.cleaned_data["name"]
        # カテゴリ名の正規化
        category_name.name = unicodedata.normalize("NFKC", category_name.name)
        # 重複チェック
        if Category.objects.filter(name=category_name).exists():
            raise forms.ValidationError("このカテゴリ名は既に使用されています。別の名前を指定してください。")
        return category_name

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

    def clean_name(self):
        bigcategory_name = self.cleaned_data["name"]
        # 親カテゴリ名の正規化
        bigcategory_name.name = unicodedata.normalize("NFKC", bigcategory_name.name)
        # 重複チェック
        if BigCategory.objects.filter(name=bigcategory_name).exists():
            raise forms.ValidationError(
                "この親カテゴリ名は既に使用されています。別の名前を指定してください。"
            )
        return bigcategory_name

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
