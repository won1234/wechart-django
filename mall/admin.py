from django.contrib import admin
from .models import Category, Product, ProductPrice, ProductPriceGroup


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'price', 'stock',
                    'available', 'created', 'updated', 'category')
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ('number', 'price', 'stock', 'available')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price2', 'price_group')
    list_filter = ['product', 'price_group']
    list_editable = ('price2', 'price_group')


admin.site.register(ProductPrice, ProductPriceAdmin)

class ProductPriceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductPriceGroup, ProductPriceGroupAdmin)