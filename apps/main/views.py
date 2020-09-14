from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.main.models import *


class HomePageViews(TemplateView):
    template_name = 'pages/main/home.html'


class SettingsViews(TemplateView):
    template_name = 'pages/settings/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['setting'] = GeneralSettings.load()
        return self.render_to_response(context)

    def post(self, request):
        conf = GeneralSettings.load()
        uzs = request.POST.get('uzs')
        conf.course_usd_to_uzs = int(uzs)
        conf.save()
        return redirect(reverse('settings'))
