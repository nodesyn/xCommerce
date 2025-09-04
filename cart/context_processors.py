from .models import Cart


def cart_context(request):
    """Add cart information to all templates"""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(customer=request.user, is_active=True)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        # Handle anonymous users
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key, customer=None, is_active=True)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0
    
    return {
        'cart_count': cart_count,
    }