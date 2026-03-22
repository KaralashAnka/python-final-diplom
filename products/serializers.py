from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductAttributeValue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent']


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'type', 'is_required']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'barcode', 'model', 'category', 'category_name',
                 'supplier', 'supplier_name', 'price', 'price_rrc', 'wholesale_price', 'stock_quantity',
                 'min_order_quantity', 'is_active', 'image', 'created_at', 'updated_at',
                 'attribute_values']
        read_only_fields = ['created_at', 'updated_at']
