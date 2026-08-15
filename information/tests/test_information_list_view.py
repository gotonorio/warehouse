from common.test_utils import LoginRequiredViewTestMixin
from django.test import TestCase


class InformationListViewTests(LoginRequiredViewTestMixin, TestCase):
    """InformationListViewのパーミッションテスト"""

    # RepairPlanPandasView呼び出しurl
    url_name = "information:information"
    # アプリケーション名
    permission_app_label = "information"
