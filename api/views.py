from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from acronyms.models import Acronym

from .serializers import AcronymSerializer


class AcronymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AcronymSerializer
    queryset = Acronym.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.kwargs["acronym"])
        acronym = self.kwargs["acronym"]
        obj = get_object_or_404(queryset, acronym__iexact=acronym)

        return obj
