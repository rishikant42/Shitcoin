# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.

class Home(View):
    template_name = 'home.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
