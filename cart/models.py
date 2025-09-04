from django.db import models
from django.core.validators import MinValueValidator
import uuid
from core.models import TimeStampedModel
from customers.models import Customer
from products.models import Product, ProductVariant


class Cart(TimeStampedModel):
    """
    Shopping cart for customers and anonymous users
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    
    # Cart metadata
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        if self.customer:
            return f"Cart for {self.customer.email}"
        return f"Anonymous cart ({self.session_key[:8]}...)"
    
    @property
    def total_items(self):
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    @property
    def subtotal(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total
    
    @property
    def is_empty(self):
        return self.items.count() == 0
    
    def add_item(self, product, variant=None, quantity=1):
        """Add or update item in cart"""
        item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            item.quantity += quantity
            item.save()
        
        return item
    
    def remove_item(self, product, variant=None):
        """Remove item from cart"""
        try:
            item = self.items.get(product=product, variant=variant)
            item.delete()
            return True
        except CartItem.DoesNotExist:
            return False
    
    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()
    
    class Meta:
        db_table = 'cart_cart'


class CartItem(TimeStampedModel):
    """
    Individual items in shopping cart
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def __str__(self):
        product_name = self.product.name
        if self.variant:
            product_name += f" - {self.variant.name}"
        return f"{product_name} x {self.quantity}"
    
    @property
    def unit_price(self):
        """Get the effective unit price"""
        if self.variant and self.variant.price:
            return self.variant.price
        return self.product.price
    
    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.unit_price * self.quantity
    
    @property
    def is_available(self):
        """Check if item is still available"""
        if not self.product.status == 'active':
            return False
        
        if self.variant:
            return self.variant.is_active and self.variant.is_in_stock
        
        return self.product.is_in_stock
    
    class Meta:
        db_table = 'cart_cart_item'
        unique_together = ['cart', 'product', 'variant']


class WishList(TimeStampedModel):
    """
    Customer wishlist/favorites
    """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='My Wishlist')
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.customer.email}'s {self.name}"
    
    @property
    def item_count(self):
        return self.items.count()
    
    def add_item(self, product):
        """Add product to wishlist"""
        item, created = WishListItem.objects.get_or_create(
            wishlist=self,
            product=product
        )
        return item, created
    
    def remove_item(self, product):
        """Remove product from wishlist"""
        try:
            item = self.items.get(product=product)
            item.delete()
            return True
        except WishListItem.DoesNotExist:
            return False
    
    def has_product(self, product):
        """Check if product is in wishlist"""
        return self.items.filter(product=product).exists()
    
    class Meta:
        db_table = 'cart_wishlist'


class WishListItem(TimeStampedModel):
    """
    Items in customer wishlist
    """
    wishlist = models.ForeignKey(WishList, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.wishlist.customer.email} - {self.product.name}"
    
    class Meta:
        db_table = 'cart_wishlist_item'
        unique_together = ['wishlist', 'product']
