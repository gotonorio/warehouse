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
        )
        widgets = {
            'room_no': forms.NumberInput(attrs={'class': 'input'}),
            'room_type': forms.Select(attrs={'class': 'select-css'}),
            'owner': forms.TextInput(attrs={'class': 'input'}),
            'tenant': forms.TextInput(attrs={'class': 'input'}),
            'parking_fee': forms.NumberInput(attrs={'class': 'input'}),
            'bicycle_fee': forms.NumberInput(attrs={'class': 'input'}),
            'bike_fee': forms.NumberInput(attrs={'class': 'input'}),
            'chounaika': forms.CheckboxInput(attrs={'class': 'checkbox'})
        }
