from django.db import models

class CreateUpdateDeleteModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True