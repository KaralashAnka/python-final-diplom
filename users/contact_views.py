from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Address
from .contact_serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet для управления контактными данными"""
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Если это первый адрес или указан как основной, делаем его основным
        user_addresses = Address.objects.filter(user=self.request.user)
        is_default = serializer.validated_data.get('is_default', False)
        
        if not user_addresses.exists() or is_default:
            # Сбрасываем флаг основного у всех адресов пользователя
            Address.objects.filter(user=self.request.user).update(is_default=False)
            serializer.validated_data['is_default'] = True
        
        serializer.save(user=self.request.user)


class ContactCreateView(APIView):
    """API для создания контакта согласно спецификации"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """API запрос добавления контакта"""
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Если это первый адрес или указан как основной, делаем его основным
            user_addresses = Address.objects.filter(user=request.user)
            is_default = serializer.validated_data.get('is_default', False)
            
            if not user_addresses.exists() or is_default:
                # Сбрасываем флаг основного у всех адресов пользователя
                Address.objects.filter(user=request.user).update(is_default=False)
                serializer.validated_data['is_default'] = True
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
