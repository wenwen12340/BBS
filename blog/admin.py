from django.contrib import admin

# Register your models here.

from blog import models

admin.site.register(models.Userinfo)
admin.site.register(models.Blog)
admin.site.register(models.Artical)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.Artical2Tag)
admin.site.register(models.Aritalupdown)