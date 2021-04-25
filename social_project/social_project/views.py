from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "index.html"


class ReLoginPage(TemplateView):
    template_name = "test.html"


class ReLogoutPage(TemplateView):
    template_name = "thanks.html"
