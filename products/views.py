from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CreateCategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CategoryByIdSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CategoryByIdSerializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductByIdSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductByIdSerializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        """Custom action to handle inventory restocking."""
        inventory = self.get_object()
        quantity = request.data.get('quantity', 0)
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inventory.quantity += quantity
        inventory.last_restock_date = timezone.now().date()
        inventory.save()
        
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """List inventory items that need restocking."""
        low_stock_items = self.get_queryset().filter(
            quantity__lte=models.F('reorder_level')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

