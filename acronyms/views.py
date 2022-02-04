from django.views.generic import TemplateView


class HomePageTemplateView(TemplateView):
    template_name = "acronyms/index.html"
    http_method_names = ["get", "post"]
