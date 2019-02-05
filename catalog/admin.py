from django.contrib import admin
from .models import Category, Vendor, Product


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'category', 'vendor', 'id')
    list_filter = ('vendor', 'category')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'id')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'alias', 'url', 'id')