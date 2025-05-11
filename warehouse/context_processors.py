from django.conf import settings
from library.models import BigCategory


def menu(request):
    """テンプレートに毎回渡すデータ。
    この関数をsetting.pyのTEMPLATESに登録する。
    ユーザが「データ管理者」以上の権限を持っている場合は、全てのカテゴリを表示する。
    """
    has_permission = request.user.has_perm("library.add_file")
    if has_permission:
        qs_menu = BigCategory.objects.all().filter(alive=True).order_by("rank")
    else:
        qs_menu = BigCategory.objects.all().filter(alive=True, is_admin=False).order_by("rank")

    context = {
        "menu_list": qs_menu,
    }
    return context


def version_no(request):
    """プロジェクト共通のTextをtemplatesファイルで使えるように"""
    return {"VERSION_NO": settings.VERSION_NO}


def is_debug(request):
    """DEBUGモードを判定する"""
    return {"DEBUG": settings.DEBUG}
