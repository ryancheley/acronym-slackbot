from django.db import models


class Acronym(models.Model):
    acronym = models.CharField(max_length=8)
    definition = models.TextField()
    create_by = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    update_by = models.CharField(max_length=32)
    update_date = models.DateTimeField(auto_now=True)
    delete_by = models.CharField(max_length=32, blank=True, default="")
    delete_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField()

    class Meta:
        unique_together = ("acronym", "definition")
        ordering = ["acronym"]

    def __str__(self) -> str:
        return self.acronym

    def save(self, *args, **kwargs):
        self.acronym = self.acronym.lower()
        super().save(*args, **kwargs)
