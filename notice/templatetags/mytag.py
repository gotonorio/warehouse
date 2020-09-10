import markdown
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

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


@register.filter
def markdown_to_html(text):
    """ マークダウンをhtmlに変換する。
    https://python-markdown.github.io/reference/#extensions
    このfilterでhtml表示する場合、bulmaではclass='content'が必要。
    """
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)
