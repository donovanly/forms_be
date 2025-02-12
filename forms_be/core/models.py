from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from forms_be.base_models import CreateUpdateDeleteModel


class Form(CreateUpdateDeleteModel):
    form = JSONField()
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
