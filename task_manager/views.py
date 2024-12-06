from django.views.generic.base import TemplateView
from django.http import HttpResponseServerError
import rollbar


class HomeView(TemplateView):
    template_name = 'index.html'
