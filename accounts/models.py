from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Herb(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'herb')# يمنع التكرار

