from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductCatalogView.as_view(), name='catalog'),
    path('search/', views.search_products, name='search'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]