from django.contrib import admin

# Register your models here.

from app1.models import Recipe,Review

admin.site.register(Recipe)
admin.site.register(Review)