from django import forms

from overview.models import OverView, PublicInformation, RoomType


class OverviewForm(forms.ModelForm):
    """法規制、設備概要データ編集用フォーム"""

    class Meta:
        model = OverView
        fields = (
            "flat_parking",
            "machine_parking",
            "bicycle_parking",
            "bike_parking",
            "youto_chiiki",
            "specified_floor_area_ratio",
            "bouka_chiiki",
            "specified_building_coverage_ratio",
            "height_limit",
            "required_parking",
            "private_water_equipment",
            "public_water_equipment",
            "trunk_room",
            "delivery_box",
            "network",
            "management",
            "entrance",
            "security",
        )
        widgets = {
            "flat_parking": forms.NumberInput(attrs={"class": "input"}),
            "machine_parking": forms.NumberInput(attrs={"class": "input"}),
            "bicycle_parking": forms.NumberInput(attrs={"class": "input"}),
            "bike_parking": forms.NumberInput(attrs={"class": "input"}),
            "youto_chiiki": forms.TextInput(attrs={"class": "input"}),
            "specified_floor_area_ratio": forms.NumberInput(attrs={"class": "input"}),
            "bouka_chiiki": forms.TextInput(attrs={"class": "input"}),
            "specified_building_coverage_ratio": forms.NumberInput(attrs={"class": "input"}),
            "height_limit": forms.TextInput(attrs={"class": "input"}),
            "required_parking": forms.TextInput(attrs={"class": "input"}),
            "private_water_equipment": forms.TextInput(attrs={"class": "input"}),
            "public_water_equipment": forms.TextInput(attrs={"class": "input"}),
            "trunk_room": forms.TextInput(attrs={"class": "input"}),
            "delivery_box": forms.TextInput(attrs={"class": "input"}),
            "network": forms.TextInput(attrs={"class": "input"}),
            "management": forms.TextInput(attrs={"class": "input"}),
            "entrance": forms.TextInput(attrs={"class": "input"}),
            "security": forms.TextInput(attrs={"class": "input"}),
        }


class RoomTypeForm(forms.ModelForm):
    """住居タイプデータ編集用フォーム"""

    class Meta:
        model = RoomType
        fields = ("type_name", "area", "kanrihi", "shuuzenhi", "ryokuchi", "niwa", "number_unit")
        widgets = {
            "type_name": forms.TextInput(attrs={"class": "input"}),
            "area": forms.NumberInput(attrs={"class": "input"}),
            "kanrihi": forms.NumberInput(attrs={"class": "input"}),
            "shuuzenhi": forms.NumberInput(attrs={"class": "input"}),
            "ryokuchi": forms.NumberInput(attrs={"class": "input"}),
            "niwa": forms.NumberInput(attrs={"class": "input"}),
            "number_unit": forms.NumberInput(attrs={"class": "input"}),
        }


class PublicInformationForm(forms.ModelForm):
    """公開情報データ編集用フォーム"""

    class Meta:
        model = PublicInformation
        fields = ("year", "pub_information", "is_published")
        widgets = {
            "year": forms.TextInput(attrs={"class": "input"}),
            "pub_information": forms.Textarea(attrs={"class": "textarea", "rows": 18}),
            "is_published": forms.CheckboxInput(attrs={"class": "checkbox"}),  # チェックボックス
        }
