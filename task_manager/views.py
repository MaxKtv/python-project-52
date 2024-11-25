from django.views.generic.base import TemplateView
from django.http import HttpResponseServerError
import rollbar

class HomeView(TemplateView):
    template_name = 'index.html'


def test_rollbar_error(request):
    try:
        1 / 0
    except ZeroDivisionError:
        rollbar.report_exc_info()
        return HttpResponseServerError("This is a test error sent to Rollbar.")

