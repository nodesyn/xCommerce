from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

from .models import Cart, CartItem, WishList, WishListItem
from products.models import Product, ProductVariant


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            customer=request.user,
            defaults={'is_active': True}
        )
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            customer=None,
            defaults={'is_active': True}
        )
    
    return cart


class CartDetailView(TemplateView):
    template_name = 'cart/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        
        context['cart'] = cart
        context['cart_items'] = cart.items.select_related('product', 'variant').prefetch_related('product__images')
        
        # Calculate totals
        context['subtotal'] = cart.subtotal
        context['shipping_cost'] = Decimal('10.00')  # Static for now
        context['tax_rate'] = Decimal('0.08')  # 8% tax
        context['tax_amount'] = context['subtotal'] * context['tax_rate']
        context['total'] = context['subtotal'] + context['shipping_cost'] + context['tax_amount']
        
        return context


@require_POST
def add_to_cart(request):
    """Add item to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, status='active')
        variant = None
        
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        
        cart = get_or_create_cart(request)
        cart.add_item(product, variant, quantity)
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': cart.total_items,
            'cart_subtotal': str(cart.subtotal)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': cart.total_items,
            'cart_subtotal': str(cart.subtotal)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def update_cart_item(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.quantity = quantity
        item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'cart_count': cart.total_items,
            'cart_subtotal': str(cart.subtotal),
            'item_total': str(item.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = get_or_create_cart(request)
        cart.clear()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_count': 0,
            'cart_subtotal': '0.00'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


class CheckoutView(TemplateView):
    template_name = 'cart/checkout.html'
    
    def dispatch(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        if cart.is_empty:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        
        context['cart'] = cart
        context['cart_items'] = cart.items.select_related('product', 'variant').prefetch_related('product__images')
        
        # Calculate totals
        context['subtotal'] = cart.subtotal
        context['shipping_cost'] = Decimal('10.00')
        context['tax_rate'] = Decimal('0.08')
        context['tax_amount'] = context['subtotal'] * context['tax_rate']
        context['total'] = context['subtotal'] + context['shipping_cost'] + context['tax_amount']
        
        return context


def checkout_success(request):
    """Checkout success page"""
    return render(request, 'cart/checkout_success.html')


# Wishlist Views
@method_decorator(login_required, name='dispatch')
class WishListView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/wishlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        wishlist, created = WishList.objects.get_or_create(customer=self.request.user)
        context['wishlist'] = wishlist
        context['wishlist_items'] = wishlist.items.select_related('product').prefetch_related('product__images')
        
        return context


@require_POST
@login_required
def add_to_wishlist(request):
    """Add product to wishlist"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id, status='active')
        wishlist, created = WishList.objects.get_or_create(customer=request.user)
        
        item, created = wishlist.add_item(product)
        
        if created:
            message = f'{product.name} added to wishlist'
        else:
            message = f'{product.name} is already in your wishlist'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'in_wishlist': True
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
@login_required
def remove_from_wishlist(request):
    """Remove product from wishlist"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        wishlist = get_object_or_404(WishList, customer=request.user)
        
        if wishlist.remove_item(product):
            message = f'{product.name} removed from wishlist'
        else:
            message = f'{product.name} was not in your wishlist'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'in_wishlist': False
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
