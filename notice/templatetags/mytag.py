from django import template

register = template.Library()

"""
paginate処理とgetパラメータの同時使用を許すためのページ処理用templateタグ。
"""
@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える."""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()
