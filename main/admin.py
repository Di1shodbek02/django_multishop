from django.contrib import admin

from .models import Product, Picture

admin.site.register((Product, Picture))
