from django.contrib import admin
from .models import Herb
# Register your models here.
admin.site.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display=['name','symptoms','usage','warning','image_url']