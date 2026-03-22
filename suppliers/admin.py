from django.contrib import admin
from .models import Supplier, PriceList


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'email', 'phone', 'is_active', 'rating', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email']
    ordering = ['company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Company Info', {
            'fields': ('user', 'company_name', 'inn', 'contact_person', 'email', 'phone')
        }),
        ('Status', {
            'fields': ('is_active', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'uploaded_at', 'is_active']
    list_filter = ['is_active', 'uploaded_at', 'supplier']
    search_fields = ['name', 'supplier__company_name']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at']
