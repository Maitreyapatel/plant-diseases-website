from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class posts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    description = models.CharField(max_length=700)
