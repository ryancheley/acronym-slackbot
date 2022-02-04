from django.urls import include, path

from .views import AcronymViewSet

app_name = "api"

user_list = AcronymViewSet.as_view({"get": "list"})
user_detail = AcronymViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", AcronymViewSet.as_view({"get": "list"}), name="acronym-list"),
    path("<acronym>/", AcronymViewSet.as_view({"get": "retrieve"}), name="acronym-detail"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
