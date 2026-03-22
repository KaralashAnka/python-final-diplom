from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier, PriceList
from .serializers import SupplierSerializer, PriceListSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    search_fields = ['company_name', 'contact_person']
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        supplier = self.get_object()
        supplier.is_active = not supplier.is_active
        supplier.save()
        return Response({
            'message': f'Supplier {"activated" if supplier.is_active else "deactivated"}',
            'is_active': supplier.is_active
        })
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        supplier = self.get_object()
        # Get orders that contain products from this supplier
        from orders.models import OrderItem
        order_items = OrderItem.objects.filter(supplier=supplier)
        orders = list(set(item.order for item in order_items))
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status,
                'total_amount': order.total_amount,
                'created_at': order.created_at,
                'items_count': order_items.filter(order=order).count()
            })
        
        return Response(orders_data)


class PriceListViewSet(viewsets.ModelViewSet):
    serializer_class = PriceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'supplier':
            try:
                supplier = self.request.user.supplier_profile
                return PriceList.objects.filter(supplier=supplier)
            except Supplier.DoesNotExist:
                return PriceList.objects.none()
        return PriceList.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.user_type == 'supplier':
            supplier = self.request.user.supplier_profile
            serializer.save(supplier=supplier)
