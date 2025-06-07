from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ProductImgTabularAdmin(admin.TabularInline):
    extra = 1
    model = models.ProductImage

@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImgTabularAdmin]
    list_display = ['id', 'title']