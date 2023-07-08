from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from common.view_mixins import RedirectToDashboardMixin
from app.models import PetPhoto

"""
If using TemplateView, you need to use the 
get_context_data method
to provide any context data variables to your template.
"""


# *************************************************************
# TEMPLATE_VIEW  Renders a given template, with the context
# containing parameters captured in the URL
# RedirectToDashboardMixin -> check in dispatch if user is logged in


class HomeView(RedirectToDashboardMixin, TemplateView):
    template_name = 'app/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # used for navbar items in base.html
        # hide Add photo ,Add pet from navigation when show 'home'
        context['hide_additional_nav_items'] = True  # use in template as {{variable}}
        return context


class DashboardView(ListView):
    model = PetPhoto
    template_name = 'app/dashboard.html'
    context_object_name = 'pet_photos'
#   paginate_by = 10


def error_401(request, exception):
    data = {}
    return render(request, 'app/401.html', data)

