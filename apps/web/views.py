from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def home(request):
    if request.user.is_authenticated:
        return render(request, 'frontend/react_app.html')
    else:
        return render(request, 'web/landing_page.html')


def simulate_error(request):
    raise Exception('This is a simulated error.')
