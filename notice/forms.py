from django import forms

from notice.models import News


class NewsForm(forms.ModelForm):
    """ Newsモデルのフォーム.
    ModelFormでclassを指定する場合、Metaクラスで行う。"""

    class Meta:
        model = News
        fields = '__all__'
        """ checkboxが綺麗に表示できない。 """
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "input is-size-6",
            }),
            'comment': forms.Textarea(attrs={
                'class': "textarea is-size-6 ",
            }),
            'display_news': forms.CheckboxInput(attrs={
                'class': "is-size-6",
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'is-size-6',
            }),
        }
