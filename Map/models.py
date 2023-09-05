from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Map(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)