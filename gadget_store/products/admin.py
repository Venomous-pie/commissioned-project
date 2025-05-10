# products/admin.py

from django.contrib import admin
from .models import Category, Product, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'is_featured', 'created', 'updated']
    list_filter = ['is_featured', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_date']
    list_filter = ['added_date']