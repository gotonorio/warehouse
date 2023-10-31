from django.conf import settings

from library.models import BigCategory


def menu(request):
    """テンプレートに毎回渡すデータ。
    この関数をsetting.pyのTEMPLATESに登録する。
    """
    context = {
        "menu_list": BigCategory.objects.all().filter(alive=True).order_by("rank"),
    }
    return context


def version_no(request):
    """プロジェクト共通のTextをtemplatesファイルで使えるように"""
    return {"VERSION_NO": settings.VERSION_NO}
