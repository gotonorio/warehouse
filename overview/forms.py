from django import forms

from overview.models import OverView


class OverviewForm(forms.ModelForm):
    """ 法規制、設備概要データ編集用フォーム """
    flat_parking = forms.IntegerField(
        label='平置き駐車場',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )
    machine_parking = forms.IntegerField(
        label='機械式駐車場',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )
    bicycle_parking = forms.IntegerField(
        label='駐輪場',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )
    bike_parking = forms.IntegerField(
        label='バイク置場',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )

    youto_chiiki = forms.CharField(
        label='用途地域',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    specified_floor_area_ratio = forms.FloatField(
        label='指定容積率',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )
    bouka_chiiki = forms.CharField(
        label='防火地域',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    specified_building_coverage_ratio = forms.FloatField(
        label='指定建ぺい率',
        widget=forms.NumberInput(attrs={'class': 'input'})
    )
    height_limit = forms.CharField(
        label='高度制限',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    required_parking = forms.CharField(
        label='必要駐車場台数',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    class Meta:
        model = OverView
        fields = (
            "flat_parking",
            "machine_parking",
            "bicycle_parking",
            "bike_parking",
            "youto_chiiki",
            "specified_floor_area_ratio",
            'bouka_chiiki',
            "specified_building_coverage_ratio",
            "height_limit",
            "required_parking",
            )
