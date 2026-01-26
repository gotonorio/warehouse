from django.contrib.auth.decorators import login_required


@login_required
def weasyprint(request, pk):
    """Generate pdf. warehoouseでは未使用
    https://docs.djangoproject.com/ja/4.0/topics/auth/default/
    https://qiita.com/mag-chang/items/c01ccb21a05c51cb1b45
    https://thr3a.hatenablog.com/entry/20200816/1597541884
    https://weasyprint.readthedocs.io/en/stable/tutorial.html
    https://doc.courtbouillon.org/weasyprint/latest/first_steps.html#linux
    """
    from django.http import HttpResponse
    from django.template.loader import get_template
    from weasyprint import HTML

    # Model data
    target_qs = Information.objects.get(id=pk)

    # pdf化するtemplatesを読み込む
    html_template = get_template("information/weasyprint.html")

    html_str = html_template.render({"target": target_qs}, request)
    pdf_file = HTML(
        string=html_str,
        # 現在アクセスしているページのURLを設定
        base_url=request.build_absolute_uri(),
    ).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    file_name = "information.pdf"
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response
