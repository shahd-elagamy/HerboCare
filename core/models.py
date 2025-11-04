from django.db import models
from django.contrib.auth.models import User


class Herb(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.TextField(help_text="Comma-separated symptoms")
    usage = models.TextField()
    warning = models.TextField(blank=True)
    image_url = models.CharField(max_length=500,blank=True,null=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_herbs', blank=True)


    def _str_(self):
      return self.name
    
