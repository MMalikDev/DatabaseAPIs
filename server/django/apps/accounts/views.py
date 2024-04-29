from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


# Create your views here.
class Index(TemplateView):
    template_name = "common/index.html"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
