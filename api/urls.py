from django.urls import include, path

from .views import AcronymViewSet, AddAcronym, CountAcronyms, Events, UpdateAcronym, DeleteAcronym

app_name = "api"

user_list = AcronymViewSet.as_view({"get": "list"})
user_detail = AcronymViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", AcronymViewSet.as_view({"get": "list"}), name="acronym-list"),
    path("<acronym>/", AcronymViewSet.as_view({"get": "retrieve"}), name="acronym-detail"),
    path("slack/events/", Events.as_view(), name="events"),
    path("slack/count/", CountAcronyms.as_view(), name="count-acronyms"),
    path("slack/add/", AddAcronym.as_view(), name="add-acronym"),
    path("slack/update/", UpdateAcronym.as_view(), name="update-acronym"),
    path("slack/delete/", DeleteAcronym.as_view(), name="delete-acronym"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
