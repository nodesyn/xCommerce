from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg, Count, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import models
from .models import Product, ProductImage
from core.models import Category


class ProductCatalogView(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='active').select_related('category').prefetch_related('images')
        
        # Category filtering
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            queryset = queryset.filter(Q(category=category) | Q(categories=category))
        
        # Search filtering
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(short_description__icontains=search_query)
            )
        
        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
                
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'name')
        sort_options = {
            'name': 'name',
            'price_low': 'price',
            'price_high': '-price',
            'newest': '-created_at',
            'popular': '-sales_count',
            'rating': '-view_count',  # Placeholder for rating
        }
        
        if sort_by in sort_options:
            queryset = queryset.order_by(sort_options[sort_by])
        else:
            queryset = queryset.order_by('name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current category if filtered
        category_slug = self.request.GET.get('category')
        if category_slug:
            try:
                context['current_category'] = Category.objects.get(slug=category_slug, is_active=True)
            except Category.DoesNotExist:
                context['current_category'] = None
        else:
            context['current_category'] = None
        
        # Get all categories for filter
        context['categories'] = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
        
        # Get total products count
        context['total_products'] = self.get_queryset().count()
        
        # Current filters for display
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'sort': self.request.GET.get('sort', 'name'),
        }
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(status='active').select_related('category').prefetch_related(
            'images', 'variants', 'categories'
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        Product.objects.filter(pk=obj.pk).update(view_count=models.F('view_count') + 1)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related products
        related_products = Product.objects.filter(
            category=self.object.category,
            status='active'
        ).exclude(pk=self.object.pk).select_related('category').prefetch_related('images')[:4]
        
        context['related_products'] = related_products
        
        # Get product images
        context['product_images'] = self.object.images.all().order_by('sort_order')
        
        # Get product variants
        context['product_variants'] = self.object.variants.filter(is_active=True)
        
        return context


def search_products(request):
    """AJAX search for product suggestions"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        status='active'
    ).select_related('category').prefetch_related('images')[:10]
    
    results = []
    for product in products:
        image_url = product.images.first().image.url if product.images.first() else None
        results.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'price': str(product.price),
            'image': image_url,
            'category': product.category.name if product.category else 'Uncategorized'
        })
    
    return JsonResponse({'results': results})
