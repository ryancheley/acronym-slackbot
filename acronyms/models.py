from pyexpat import model
from django.db import models


class Acronym(models.Model):
    acronym = models.CharField(max_length=8)
    definition = models.TextField()

    def __str__(self) -> str:
        return self.acronym
