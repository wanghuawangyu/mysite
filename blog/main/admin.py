from django.contrib import admin
import database.models as models

# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.Account)
admin.site.register(models.Category)