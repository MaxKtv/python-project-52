from django.views.generic.base import TemplateView
from django.http import HttpResponseServerError
import rollbar


class HomeView(TemplateView):
    template_name = 'index.html'


def test_rollbar_error(request):
    rollbar.report_message('Test error from task manager', 'error')
    return HttpResponseServerError('Test error page')
