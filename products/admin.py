from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductAttributeValue


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'description']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    ordering = ['name']


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'supplier', 'price', 'stock_quantity', 'is_active']
    list_filter = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'sku', 'description']
    ordering = ['name']
    inlines = [ProductAttributeValueInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'sku', 'barcode', 'category', 'supplier')
        }),
        ('Pricing', {
            'fields': ('price', 'wholesale_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'min_order_quantity', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_required']
    list_filter = ['type', 'is_required']
    search_fields = ['name']
    ordering = ['name']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['product__name', 'attribute__name', 'value']
    ordering = ['product', 'attribute']
