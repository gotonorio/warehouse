import logging

from user_agents import parse

logger = logging.getLogger(__name__)


class UAmiddleware(object):
    """mobile判定をrequestに追加する。
    def get_template_names(self):
        if self.request.user_agent.is_mobile:
            return mobile.html
        elif self.request.user_agent.is_tablet:
            return tablet.html
        elif self.request.user_agent.is_pc:
            return pc.html
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.user_agent = parse(request.META.get("HTTP_USER_AGENT", ""))

        response = self.get_response(request)
        return response
