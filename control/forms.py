from django import forms
from control.models import ControlRecord


class UpdateControlForm(forms.ModelForm):
    """ 仮登録メニューの表示/非表示を設定 """
    class Meta:
        model = ControlRecord
        fields = ('tmp_user_flg',)
        labels = {
            'tmp_user_flg': '仮登録表示',
        }
        widgets = {
            'tmp_user_flg': forms.NullBooleanSelect(attrs={
                'class': 'select-css',
            }),
        }
