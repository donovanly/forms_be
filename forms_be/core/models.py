from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from forms_be.base_models import CreateUpdateDeleteModel


class Form(CreateUpdateDeleteModel):
    description = models.CharField(max_length=200)
    form = JSONField()
    name = models.CharField(max_length=200)
