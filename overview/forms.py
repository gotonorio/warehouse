from django import forms

from overview.models import OverView
from overview.models import Room


class OverviewForm(forms.ModelForm):
    """ 法規制、設備概要データ編集用フォーム """
    class Meta:
        model = OverView
        fields = (
            'flat_parking',
            'machine_parking',
            'bicycle_parking',
            'bike_parking',
            'youto_chiiki',
            'specified_floor_area_ratio',
            'bouka_chiiki',
            'specified_building_coverage_ratio',
            'height_limit',
            'required_parking',
            'private_water_equipment',
            'public_water_equipment',
            'trunk_room',
            'delivery_box',
            )
        widgets = {
            'flat_parking': forms.NumberInput(attrs={'class': 'input'}),
            'machine_parking': forms.NumberInput(attrs={'class': 'input'}),
            'bicycle_parking': forms.NumberInput(attrs={'class': 'input'}),
            'bike_parking': forms.NumberInput(attrs={'class': 'input'}),
            'youto_chiiki': forms.TextInput(attrs={'class': 'input'}),
            'specified_floor_area_ratio': forms.NumberInput(attrs={'class': 'input'}),
            'bouka_chiiki': forms.TextInput(attrs={'class': 'input'}),
            'specified_building_coverage_ratio': forms.NumberInput(attrs={'class': 'input'}),
            'height_limit': forms.TextInput(attrs={'class': 'input'}),
            'required_parking': forms.TextInput(attrs={'class': 'input'}),
            'private_water_equipment': forms.TextInput(attrs={'class': 'input'}),
            'public_water_equipment': forms.TextInput(attrs={'class': 'input'}),
            'trunk_room': forms.TextInput(attrs={'class': 'input'}),
            'delivery_box': forms.TextInput(attrs={'class': 'input'}),
        }


class RoomForm(forms.ModelForm):
    """ 区分所有者データの作成sakusei """
    class Meta:
        model = Room
        fields = (
            'room_no',
            'room_type',
            'owner',
            'tenant',
            'parking_fee',
            'bicycle_fee',
            'bike_fee',
            'chounaikai',
            'mishuu_fee',
            'comment',
            'zip_code',
            'prefecture',
            'municipality',
            'house_number',
            'building',
            'tel_number',
        )
        widgets = {
            'room_no': forms.NumberInput(attrs={'class': 'input', 'readonly': 'readonly'}),
            # 'room_type': forms.Select(attrs={'class': 'select-css', 'disabled': 'disable'}),
            'room_type': forms.Select(attrs={'class': 'input', 'readonly': 'readonly'}),
            'owner': forms.TextInput(attrs={'class': 'input'}),
            'tenant': forms.TextInput(attrs={'class': 'input'}),
            'parking_fee': forms.NumberInput(attrs={'class': 'input'}),
            'bicycle_fee': forms.NumberInput(attrs={'class': 'input'}),
            'bike_fee': forms.NumberInput(attrs={'class': 'input'}),
            'chounaika': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'mishuu_fee': forms.NumberInput(attrs={'class': 'input'}),
            'comment': forms.TextInput(attrs={'class': 'input'}),
            'zip_code': forms.TextInput(attrs={'class': 'input'}),
            'prefecture': forms.TextInput(attrs={'class': 'input'}),
            'municipality': forms.TextInput(attrs={'class': 'input'}),
            'house_number': forms.TextInput(attrs={'class': 'input'}),
            'building': forms.TextInput(attrs={'class': 'input'}),
            'tel_number': forms.TextInput(attrs={'class': 'input'}),
        }
        help_texts = {
            'zip_code': '※ 郵便番号はハイフン(-)無しです。',
            'tel_number': '※ 電話番号はハイフン(-)無しです。',
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code:
            if '-' in zip_code:
                self.add_error('zip_code', '郵便番号にハイフン(-)を含めないでください。')
        return zip_code

    def clean_tel_number(self):
        tel_number = self.cleaned_data.get('tel_number')
        if tel_number:
            if '-' in tel_number:
                self.add_error('tel_number', '電話番号にハイフン(-)を含めないでください。')
        return tel_number


class CSVImportForm(forms.Form):
    """ 部屋番号, 駐車場使用料 """
    file = forms.FileField(
        label='CSVファイル',
        help_text='※ CSVファイルはヘッダー無しです。'
        )
