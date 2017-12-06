from django.db import models


class semantic(models.Model):
    security = models.CharField(max_length=100)
    sentence1 = models.CharField(max_length=300)
    sentence1 = models.CharField(max_length=300)
    result = models.CharField(default = None,max_length=30)
