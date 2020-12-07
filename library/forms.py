from django import forms

from library.models import BigCategory, Category, File


class FileForm(forms.ModelForm):
    """ Fileモデルのフォーム
    ModelForm限定の方法としてclass Metaでwidgetを設定する。class以外も変更できる。
    https://narito.ninja/blog/detail/52/
    """
    class Meta:
        model = File
        fields = ("title", "category", "summary", "key_word",
                  "src", "rank", "created_at", "alive", "download")
        # field毎に異なるclassを設定する場合には、この方法を取る。
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'category': forms.Select(attrs={
                'class': "select is-size-6",
            }),
            'summary': forms.Textarea(attrs={
                'class': "textarea is-size-6",
            }),
            'key_word': forms.Textarea(attrs={
                'class': "textarea is-size-6",
            }),
            'src': forms.ClearableFileInput(attrs={
                'class': "file is-size-6",
            }),
            'rank': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'datetimeinput is-size-6',
            }),
            'alive': forms.CheckboxInput(attrs={
                'class': "checkboxinput is-size-4",
            }),
            'download': forms.CheckboxInput(attrs={
                'class': "checkboxinput is-size-4",
            }),
        }


class CategoryForm(forms.ModelForm):
    """ Categoryモデルのフォーム """
    class Meta:
        model = Category
        fields = ('name', 'path_name', 'parent',
                  'rank', 'created_at', 'restrict', 'alive')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'path_name': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'parent': forms.Select(attrs={
                'class': "select is-size-6",
            }),
            'rank': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': "datetimeinput is-size-6",
            }),
            'restrict': forms.CheckboxInput(attrs={
                'class': "checkboxinput is-size-4",
            }),
            'alive': forms.CheckboxInput(attrs={
                'class': "checkboxinput is-size-4",
            }),
        }


class BigCategoryForm(forms.ModelForm):
    """ 親Categoryモデルのフォーム """
    class Meta:
        model = BigCategory
        fields = ('name', 'rank', 'created_at', 'alive')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'rank': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': "datetimeinput is-size-6",
            }),
            'alive': forms.CheckboxInput(attrs={
                'class': "checkboxinput is-size-4",
            }),
        }
