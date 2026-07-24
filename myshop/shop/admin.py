from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    search_fields = ['translations__name']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = [
        'name',
        'category',
        'slug',
        'price',
        'available',
        'stock',
        'created',
        'updated'
    ]

    list_filter = [
        'available',
        'created',
        'updated'
    ]

    list_editable = [
        'price',
        'available',
        'stock'
    ]

    search_fields = [
        'translations__name',
        'translations__description',
    ]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
