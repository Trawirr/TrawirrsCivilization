from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Map(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

class FavouriteMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.image.name}"