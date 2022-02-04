from rest_framework import serializers

from acronyms.models import Acronym


class AcronymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acronym
        fields = [
            "id",
            "acronym",
            "definition",
        ]
