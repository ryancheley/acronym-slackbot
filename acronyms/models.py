from django.db import models


class Acronym(models.Model):
    acronym = models.CharField(max_length=8)
    definition = models.TextField()

    def save(self, *args, **kwargs):
        self.acronym = self.acronym.lower()
        super(Acronym, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("acronym", "definition")
        ordering = ["acronym"]

    def __str__(self) -> str:
        return self.acronym
