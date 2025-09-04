from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from products.models import Product
from core.models import Category, Store


class HomeView(TemplateView):
    template_name = 'store/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get store configuration
        try:
            store = Store.objects.filter(is_active=True).first()
        except Store.DoesNotExist:
            store = None
        context['store'] = store
        
        # Get featured products
        featured_products = Product.objects.filter(
            status='active',
            is_featured=True
        ).select_related('category').prefetch_related('images')[:8]
        context['featured_products'] = featured_products
        
        # Get categories
        categories = Category.objects.filter(
            is_active=True,
            parent__isnull=True  # Only top-level categories
        ).order_by('sort_order', 'name')[:8]
        context['categories'] = categories
        
        # Demo categories for when none exist
        context['demo_categories'] = ['Electronics', 'Fashion', 'Home', 'Sports']
        
        return context


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)
