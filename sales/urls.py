# urls.py
from django.urls import path
from .views import (
    ProductListView,
    CreateSaleView,
    ReceiptDetailView,
    CustomerCreateView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('create/', CreateSaleView.as_view(), name='create-sale'),
    path('<int:sale_id>/receipt/', ReceiptDetailView.as_view(), name='sale-receipt'),
    path('customers/create/', CustomerCreateView.as_view(), name='create-customer'),
]