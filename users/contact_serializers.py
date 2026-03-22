from rest_framework import serializers
from .models import Address


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для контактных данных согласно спецификации API"""
    
    class Meta:
        model = Address
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'email', 'phone',
            'city', 'street', 'house', 'building', 'structure', 'apartment',
            'is_default'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'city': {'required': True},
            'street': {'required': True},
            'house': {'required': True},
        }
