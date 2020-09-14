from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.main.models import GeneralSettings


CONF = GeneralSettings.load()


class HomePageViews(TemplateView):
    template_name = 'pages/main/home.html'


class SettingsViews(TemplateView):
    template_name = 'pages/settings/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['setting'] = CONF
        return self.render_to_response(context)

    def post(self, request):
        uzs = request.POST.get('uzs')
        CONF.course_usd_to_uzs = int(uzs)
        CONF.save()
        return redirect(reverse('settings'))
