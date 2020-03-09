from file_storage.models import BigCategory


def menu(request):
    """ テンプレートに毎回渡すデータ。
    この関数をsetting.pyのTEMPLATESに登録する。
    """
    context = {
        'menu_list': BigCategory.objects.all().order_by('order'),
    }
    return context
