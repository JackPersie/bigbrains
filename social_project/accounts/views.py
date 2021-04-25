from django.shortcuts import render
from . import models, forms
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/


class SignupView(CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
