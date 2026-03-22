from rest_framework import serializers
from .models import Supplier, PriceList


class SupplierSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = ['id', 'user', 'user_email', 'company_name', 'inn', 'contact_person',
                 'phone', 'email', 'is_active', 'rating', 'created_at', 'updated_at',
                 'products_count']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_products_count(self, obj):
        return obj.products.count()


class PriceListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    file_name = serializers.CharField(source='file.name', read_only=True)
    
    class Meta:
        model = PriceList
        fields = ['id', 'supplier', 'supplier_name', 'name', 'file', 'file_name',
                 'uploaded_at', 'is_active']
        read_only_fields = ['supplier', 'uploaded_at']
